# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression


SAMPLE_RELEASE_PROJECT_ID = 12
SAMPLE_RELEASE_PROJECT_NAME = "Muestras & Prototipos"
SAMPLE_RELEASE_PROJECT_TASK_DOMAIN = [
    "|",
    ("project_id", "=", SAMPLE_RELEASE_PROJECT_ID),
    ("project_id.name", "=", SAMPLE_RELEASE_PROJECT_NAME),
]


class QualitySampleRelease(models.Model):
    _name = "quality.sample.release"
    _description = "Liberación de Muestras"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_requested desc, id desc"

    name = fields.Char(
        "Referencia",
        required=True,
        readonly=True,
        default="Nuevo",
        copy=False,
    )

    sample_type = fields.Selection(
        [
            ("mp", "Opción 1: MP - Sale de Laminadora"),
            ("pt", "Opción 2: PT - Pasa por Taller CNC / Transformación"),
        ],
        string="Tipo de Muestra",
        required=True,
        default="mp",
        tracking=True,
    )

    project_task_id = fields.Many2one(
        "project.task",
        "Tarea de Proyecto",
        required=True,
        tracking=True,
        domain=SAMPLE_RELEASE_PROJECT_TASK_DOMAIN,
        help=(
            "Solo se permiten tareas del proyecto ID 12 o del proyecto "
            "'Muestras & Prototipos'."
        ),
    )

    product_id = fields.Many2one(
        "product.product",
        "Producto/Muestra",
        required=True,
        tracking=True,
    )

    requested_by = fields.Many2one(
        "res.users",
        "Solicitante (Diseño)",
        required=True,
        default=lambda s: s.env.user,
        tracking=True,
    )

    inspector_id = fields.Many2one(
        "res.users",
        "Inspector de Calidad",
        tracking=True,
    )

    date_requested = fields.Datetime(
        "Fecha de Solicitud",
        required=True,
        readonly=True,
        copy=False,
        default=fields.Datetime.now,
    )

    date_limit = fields.Datetime(
        "Fecha Límite de Inspección",
        compute="_compute_date_limit",
        store=True,
        readonly=True,
        copy=False,
        help="Solicitud + 48 horas",
    )

    date_inspected = fields.Datetime(
        "Fecha de Inspección",
        readonly=True,
        copy=False,
        tracking=True,
    )

    state = fields.Selection(
        [
            ("borrador", "Borrador"),
            ("en_inspeccion", "En Inspección"),
            ("aceptado", "Aceptado"),
            ("rechazado", "Rechazado"),
        ],
        default="borrador",
        required=True,
        tracking=True,
        copy=False,
    )

    inspection_line_ids = fields.One2many(
        "quality.inspection.line",
        "sample_release_id",
        string="Atributos Inspeccionados",
    )

    spec_pdf = fields.Binary("Especificación (PDF)", attachment=True)
    spec_pdf_name = fields.Char("Nombre Especificación")

    evidence_ids = fields.Many2many(
        "ir.attachment",
        "quality_sample_evidence_rel",
        "sample_id",
        "attachment_id",
        string="Evidencia",
    )

    cnc_design_user_id = fields.Many2one("res.users", "Personal de Diseño")
    cnc_date_realized = fields.Datetime("Fecha de Realización CNC", readonly=True)
    cnc_observations = fields.Html("Observaciones CNC")

    notes = fields.Html("Observaciones")

    company_id = fields.Many2one(
        "res.company",
        "Compañía",
        default=lambda s: s.env.company,
    )

    @api.model
    def _get_sample_release_project_task_domain(self):
        return list(SAMPLE_RELEASE_PROJECT_TASK_DOMAIN)

    @api.constrains("project_task_id")
    def _check_project_task_id_allowed(self):
        Task = self.env["project.task"].sudo()

        for rec in self:
            if not rec.project_task_id:
                continue

            domain = expression.AND(
                [
                    [("id", "=", rec.project_task_id.id)],
                    rec._get_sample_release_project_task_domain(),
                ]
            )

            if not Task.search_count(domain):
                raise ValidationError(_(
                    "La Tarea de Proyecto debe pertenecer al proyecto ID %(project_id)s "
                    "o al proyecto '%(project_name)s'."
                ) % {
                    "project_id": SAMPLE_RELEASE_PROJECT_ID,
                    "project_name": SAMPLE_RELEASE_PROJECT_NAME,
                })

    @api.depends("date_requested")
    def _compute_date_limit(self):
        for rec in self:
            rec.date_limit = (
                rec.date_requested + timedelta(hours=48)
                if rec.date_requested
                else False
            )

    def _prepare_sample_attribute_line_vals(self, template):
        """
        En Liberación de Muestras los atributos booleanos se capturan siempre como
        Cumple / No Cumple. OK / NO OK queda reservado para inspecciones donde el
        proceso lo configure explícitamente, pero no para esta pantalla operativa.

        N/A tampoco se usa como valor por defecto: solo queda disponible cuando la
        plantilla permita No aplica y el usuario lo marque de forma explícita.
        """
        attribute_type = template.attribute_type
        is_boolean = attribute_type == "boolean"
        is_float = attribute_type == "float"
        is_selection = attribute_type == "selection"
        result_mode = "cumple" if is_boolean else (getattr(template, "result_mode", False) or "cumple")

        return {
            "attribute_template_id": template.id,
            "name": template.name,
            "attribute_type": attribute_type,
            "capture_zone": getattr(template, "capture_zone", False) or "additional",
            "result_mode": result_mode,
            "value_float": 0.0,
            "value_char": False,
            "value_selection": False,
            "value_cumple": False,
            "value_cumple_required": False,
            "value_ok": False,
            "value_ok_required": False,
            "min_value": template.min_value if is_float else 0.0,
            "max_value": template.max_value if is_float else 0.0,
            "unit": template.unit if is_float else False,
            "allow_zero": getattr(template, "allow_zero", False) if is_float else False,
            "allow_not_applicable": getattr(template, "allow_not_applicable", False),
            "is_not_applicable": False,
            "selection_options": template.selection_options if is_selection else False,
            "result": False,
            "result_required": False,
            "sequence": template.sequence,
        }

    def _reload_sample_attribute_templates(self, clear_existing=True):
        for rec in self:
            if not rec.product_id:
                if clear_existing:
                    rec.inspection_line_ids = [(5, 0, 0)]
                continue

            templates = rec.env["quality.attribute.template"]._get_applicable_templates_for_capture(
                product=rec.product_id,
                process=False,
                include_general=False,
                strict_binary=False,
            )

            commands = [(5, 0, 0)] if clear_existing else []

            for template in templates:
                commands.append((0, 0, rec._prepare_sample_attribute_line_vals(template)))

            if clear_existing:
                rec.inspection_line_ids = commands or [(5, 0, 0)]
            elif commands:
                rec.inspection_line_ids = commands

    @api.onchange("product_id")
    def _onchange_product_load_sample_attribute_templates(self):
        for rec in self:
            rec._reload_sample_attribute_templates(clear_existing=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Nuevo") == "Nuevo":
                vals["name"] = (
                    self.env["ir.sequence"].next_by_code("quality.sample.release")
                    or "Nuevo"
                )

        records = super().create(vals_list)

        for rec, vals in zip(records, vals_list):
            if (
                not vals.get("inspection_line_ids")
                and not rec.inspection_line_ids
                and rec.product_id
            ):
                rec.with_context(skip_quality_template_autoload=True)._reload_sample_attribute_templates(
                    clear_existing=False,
                )

        return records

    def write(self, vals):
        reload_templates = (
            not self.env.context.get("skip_quality_template_autoload")
            and "inspection_line_ids" not in vals
            and "product_id" in vals
        )

        res = super().write(vals)

        if reload_templates:
            draft_records = self.filtered(lambda rec: rec.state == "borrador")
            draft_records.with_context(skip_quality_template_autoload=True)._reload_sample_attribute_templates(
                clear_existing=True,
            )

        return res

    def _check_attributes_valid(self, block_failing=False):
        for rec in self:
            if not rec.inspection_line_ids:
                raise UserError(
                    _("Debe capturar al menos un atributo de inspección antes de avanzar.")
                )

            rec.inspection_line_ids._sync_line_result_hardening()

            missing_lines = rec.inspection_line_ids.filtered(
                lambda line: (
                    line.attribute_template_id.is_required
                    if line.attribute_template_id
                    else True
                )
                and line._quality_line_is_missing_hardening()
            )
            if missing_lines:
                raise UserError(
                    _("Hay atributos obligatorios sin captura válida: %s")
                    % "; ".join(
                        missing_lines.mapped(lambda line: line._quality_line_missing_reason_hardening())
                    )
                )

            not_allowed_na = rec.inspection_line_ids.filtered(
                lambda line: (
                    (line.result == "na" or line.is_not_applicable)
                    and not line.allow_not_applicable
                )
            )
            if not_allowed_na:
                raise UserError(
                    _("Estos atributos no permiten N/A: %s")
                    % ", ".join(not_allowed_na.mapped("name"))
                )

            if block_failing:
                failing = rec.inspection_line_ids.filtered(
                    lambda line: line.result in ("no_cumple", "no_ok")
                )
                if failing:
                    raise UserError(
                        _("No se puede liberar: hay atributo(s) que no cumplen: %s.")
                        % ", ".join(failing.mapped("name"))
                    )

    def _check_spec_pdf(self):
        for rec in self:
            if not rec.spec_pdf:
                raise UserError(
                    _(
                        "La Especificación PDF es obligatoria. "
                        "Sin plano o dibujo no se puede inspeccionar."
                    )
                )

    def _check_pt_workflow(self):
        for rec in self:
            if rec.sample_type == "pt" and not rec.cnc_date_realized:
                raise UserError(
                    _(
                        "Esta muestra PT requiere captura previa en Transformación "
                        "(Taller CNC) antes de mover a Inspección de Calidad."
                    )
                )


    def _get_sample_release_notification_partners(self):
        """
        Devuelve únicamente los contactos que deben recibir avisos de Liberación de Muestras:
        - Solicitante (Diseño)
        - Inspector de Calidad

        No se usa el grupo completo de inspectores ni fallback a todos los usuarios.
        """
        self.ensure_one()
        partners = self.env["res.partner"].browse()

        for user in (self.requested_by, self.inspector_id):
            if user and user.partner_id:
                partners |= user.partner_id

        return partners

    def _notify_sample_release_participants(self, body, subject=False, log_note=True):
        """
        Registra una nota interna en el chatter y manda notificación directa solo a:
        Solicitante (Diseño) e Inspector de Calidad.

        Se evita message_post con subtype 'mail.mt_comment' para no notificar a
        seguidores/grupos completos de la liberación.
        """
        for rec in self:
            partners = rec._get_sample_release_notification_partners()

            if log_note:
                rec.message_post(
                    body=body,
                    subtype_xmlid="mail.mt_note",
                )

            if not partners:
                continue

            notify_vals = {
                "partner_ids": partners.ids,
                "subject": subject or _("Liberación de muestra %s") % (rec.name or ""),
                "body": body,
                "record_name": rec.display_name,
            }

            try:
                rec.message_notify(**notify_vals)
            except TypeError:
                # Compatibilidad con variantes de firma entre versiones.
                notify_vals.pop("record_name", None)
                rec.message_notify(**notify_vals)


    def action_register_cnc(self):
        for rec in self:
            if rec.sample_type != "pt":
                raise UserError(_("Solo aplica a muestras PT."))

            rec._check_attributes_valid()
            rec.cnc_date_realized = fields.Datetime.now()
            rec.cnc_design_user_id = self.env.user
            rec.message_post(
                body=_("CNC: transformación registrada por %s") % self.env.user.name,
                subtype_xmlid="mail.mt_comment",
            )

    def action_submit_inspection(self):
        for rec in self:
            if not rec.inspector_id:
                raise UserError(_(
                    "Seleccione un Inspector de Calidad antes de enviar la muestra a inspección."
                ))

            rec._check_spec_pdf()
            rec._check_pt_workflow()
            rec._check_attributes_valid()
            rec.state = "en_inspeccion"

            rec.activity_schedule(
                "mail.mail_activity_data_todo",
                date_deadline=fields.Date.today() + timedelta(days=2),
                summary=_("Inspección de muestra: %s") % rec.name,
                user_id=rec.inspector_id.id,
            )

            rec._notify_sample_release_participants(
                body=_(
                    "Muestra enviada a inspección.<br/>"
                    "<b>Solicitante (Diseño):</b> %(requester)s<br/>"
                    "<b>Inspector de Calidad:</b> %(inspector)s"
                ) % {
                    "requester": rec.requested_by.name or "—",
                    "inspector": rec.inspector_id.name or "—",
                },
                subject=_("Muestra enviada a inspección: %s") % rec.name,
            )

    def action_accept(self):
        for rec in self:
            rec._check_attributes_valid(block_failing=True)

            rec.state = "aceptado"
            rec.date_inspected = fields.Datetime.now()
            rec.activity_feedback(
                ["mail.mail_activity_data_todo"],
                feedback=_("Muestra aceptada"),
            )

            rec._notify_sample_release_participants(
                body=_("Muestra ACEPTADA y liberada por %s") % self.env.user.name,
                subject=_("Muestra aceptada: %s") % rec.name,
            )


    def action_reject(self):
        for rec in self:
            rec.state = "rechazado"
            rec.date_inspected = fields.Datetime.now()
            rec.activity_feedback(
                ["mail.mail_activity_data_todo"],
                feedback=_("Muestra rechazada"),
            )

            rec._notify_sample_release_participants(
                body=_("Muestra RECHAZADA por %s.") % self.env.user.name,
                subject=_("Muestra rechazada: %s") % rec.name,
            )


    def action_reset_draft(self):
        for rec in self:
            rec.state = "borrador"

    def action_print_sample_release(self):
        return self.env.ref(
            "quality_management.action_report_sample_release"
        ).report_action(self)
