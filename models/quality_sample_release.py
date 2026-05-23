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
        result_mode = getattr(template, "result_mode", False) or "cumple"

        return {
            "attribute_template_id": template.id,
            "name": template.name,
            "attribute_type": template.attribute_type,
            "capture_zone": getattr(template, "capture_zone", False) or "additional",
            "result_mode": result_mode,
            "value_float": 0.0,
            "value_char": False,
            "value_cumple": (
                "na"
                if template.attribute_type == "boolean" and result_mode == "cumple"
                else False
            ),
            "value_ok": (
                "na"
                if template.attribute_type == "boolean" and result_mode == "ok"
                else False
            ),
            "min_value": template.min_value,
            "max_value": template.max_value,
            "unit": template.unit,
            "allow_zero": getattr(template, "allow_zero", False),
            "result": "na",
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

    def _check_attributes_valid(self):
        for rec in self:
            if not rec.inspection_line_ids:
                raise UserError(
                    _("Debe capturar al menos un atributo de inspección antes de avanzar.")
                )

            zero_lines = rec.inspection_line_ids.filtered(
                lambda line: (
                    line.attribute_type == "float"
                    and not getattr(line, "allow_zero", False)
                    and not line.value_float
                    and line.result != "na"
                )
            )
            if zero_lines:
                raise UserError(
                    _("Hay atributos con valor 0 que deben capturarse: %s")
                    % ", ".join(zero_lines.mapped("name"))
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
            rec._check_spec_pdf()
            rec._check_pt_workflow()
            rec._check_attributes_valid()
            rec.state = "en_inspeccion"

            users = rec.inspector_id
            if not users:
                group = self.env.ref(
                    "quality_management.group_quality_inspector",
                    raise_if_not_found=False,
                )
                users = group.users if group else self.env["res.users"]

            for user in users:
                rec.activity_schedule(
                    "mail.mail_activity_data_todo",
                    date_deadline=fields.Date.today() + timedelta(days=2),
                    summary=_("Inspección de muestra: %s") % rec.name,
                    user_id=user.id,
                )

    def action_accept(self):
        for rec in self:
            rec._check_attributes_valid()
            failing = rec.inspection_line_ids.filtered(
                lambda line: line.result in ("no_cumple", "no_ok")
            )
            if failing:
                raise UserError(
                    _("No se puede liberar: hay %d atributo(s) que no cumplen.")
                    % len(failing)
                )

            rec.state = "aceptado"
            rec.date_inspected = fields.Datetime.now()
            rec.activity_feedback(
                ["mail.mail_activity_data_todo"],
                feedback=_("Muestra aceptada"),
            )
            rec.message_post(
                body=_("Muestra ACEPTADA y liberada por %s") % self.env.user.name,
                subtype_xmlid="mail.mt_comment",
            )

    def action_reject(self):
        for rec in self:
            rec.state = "rechazado"
            rec.date_inspected = fields.Datetime.now()
            rec.activity_feedback(
                ["mail.mail_activity_data_todo"],
                feedback=_("Muestra rechazada"),
            )

            partner_ids = []
            if rec.requested_by.partner_id:
                partner_ids.append(rec.requested_by.partner_id.id)
                rec.message_subscribe(partner_ids=partner_ids)

            rec.message_post(
                body=_("Muestra RECHAZADA por %s. Notificando a la solicitante: %s")
                % (self.env.user.name, rec.requested_by.name),
                partner_ids=partner_ids,
                subtype_xmlid="mail.mt_comment",
            )

    def action_reset_draft(self):
        for rec in self:
            rec.state = "borrador"

    def action_print_sample_release(self):
        return self.env.ref(
            "quality_management.action_report_sample_release"
        ).report_action(self)
