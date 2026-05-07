# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta


class QualitySampleRelease(models.Model):
    _name = "quality.sample.release"
    _description = "Liberación de Muestras"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_requested desc, id desc"

    name = fields.Char("Referencia", required=True, readonly=True,
                       default="Nuevo", copy=False)

    # Tipo de muestra (req. 3)
    sample_type = fields.Selection([
        ("mp", "Opción 1: MP - Sale de Laminadora"),
        ("pt", "Opción 2: PT - Pasa por Taller CNC / Transformación"),
    ], string="Tipo de Muestra", required=True, default="mp", tracking=True)

    project_task_id = fields.Many2one("project.task", "Tarea de Proyecto",
                                      required=True, tracking=True)
    product_id = fields.Many2one("product.product", "Producto/Muestra",
                                 required=True, tracking=True)
    requested_by = fields.Many2one("res.users", "Solicitante (Diseño)",
                                   required=True,
                                   default=lambda s: s.env.user, tracking=True)
    inspector_id = fields.Many2one("res.users", "Inspector de Calidad",
                                   tracking=True)

    # Fechas: automáticas y bloqueadas (req. 3.2)
    date_requested = fields.Datetime("Fecha de Solicitud", required=True,
                                     readonly=True, copy=False,
                                     default=fields.Datetime.now)
    date_limit = fields.Datetime("Fecha Límite de Inspección",
                                 compute="_compute_date_limit", store=True,
                                 readonly=True, copy=False,
                                 help="Solicitud + 48 horas")
    date_inspected = fields.Datetime("Fecha de Inspección",
                                     readonly=True, copy=False, tracking=True)

    state = fields.Selection([
        ("borrador", "Borrador"),
        ("en_inspeccion", "En Inspección"),
        ("aceptado", "Aceptado"),
        ("rechazado", "Rechazado"),
    ], default="borrador", required=True, tracking=True, copy=False)

    inspection_line_ids = fields.One2many("quality.inspection.line",
                                          "sample_release_id",
                                          string="Atributos Inspeccionados")

    # Especificación PDF obligatoria (req. 3.1)
    spec_pdf = fields.Binary("Especificación (PDF)", attachment=True)
    spec_pdf_name = fields.Char("Nombre Especificación")

    # Pestaña Evidencia (req. 3.1)
    evidence_ids = fields.Many2many(
        "ir.attachment", "quality_sample_evidence_rel",
        "sample_id", "attachment_id", string="Evidencia",
    )

    # Captura para Opción 2 - Transformación CNC (req. 3.3)
    cnc_design_user_id = fields.Many2one("res.users", "Personal de Diseño")
    cnc_date_realized = fields.Datetime("Fecha de Realización CNC",
                                        readonly=True)
    cnc_observations = fields.Html("Observaciones CNC")

    notes = fields.Html("Observaciones")
    company_id = fields.Many2one("res.company", "Compañía",
                                 default=lambda s: s.env.company)

    # ------------------------------------------------------------------ compute
    @api.depends("date_requested")
    def _compute_date_limit(self):
        for rec in self:
            rec.date_limit = (rec.date_requested + timedelta(hours=48)
                              if rec.date_requested else False)

    # ------------------------------------------------------------------- create
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Nuevo") == "Nuevo":
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "quality.sample.release") or "Nuevo"
        return super().create(vals_list)

    # ---------------------------------------------------------------- guardrails
    def _check_attributes_valid(self):
        """Bloqueo: no permitir atributos en 0 ni faltantes (req. 3.1)."""
        for rec in self:
            if not rec.inspection_line_ids:
                raise UserError(_("Debe capturar al menos un atributo "
                                  "de inspección antes de avanzar."))
            zero_lines = rec.inspection_line_ids.filtered(
                lambda l: l.attribute_type == "float" and not l.value_float
            )
            if zero_lines:
                names = ", ".join(zero_lines.mapped("name"))
                raise UserError(_(
                    "Hay atributos con valor 0 que deben capturarse: %s"
                ) % names)

    def _check_spec_pdf(self):
        for rec in self:
            if not rec.spec_pdf:
                raise UserError(_(
                    "La Especificación PDF es obligatoria. "
                    "Sin plano o dibujo no se puede inspeccionar."
                ))

    def _check_pt_workflow(self):
        """Para PT bloquea avance si Diseño no capturó atributos en CNC."""
        for rec in self:
            if rec.sample_type == "pt" and not rec.cnc_date_realized:
                raise UserError(_(
                    "Esta muestra PT requiere captura previa en "
                    "Transformación (Taller CNC) antes de mover a "
                    "Inspección de Calidad."
                ))

    # -------------------------------------------------------------- transitions
    def action_register_cnc(self):
        """Diseño marca terminada la transformación en CNC."""
        for rec in self:
            if rec.sample_type != "pt":
                raise UserError(_("Solo aplica a muestras PT."))
            self._check_attributes_valid()
            rec.cnc_date_realized = fields.Datetime.now()
            rec.cnc_design_user_id = self.env.user
            rec.message_post(
                body=_("✓ CNC: transformación registrada por %s") % self.env.user.name,
                subtype_xmlid="mail.mt_comment",
            )

    def action_submit_inspection(self):
        for rec in self:
            rec._check_spec_pdf()
            rec._check_pt_workflow()
            rec._check_attributes_valid()
            rec.state = "en_inspeccion"
            users = self.env.ref(
                "quality_management.group_quality_inspector").users
            if rec.inspector_id:
                users = rec.inspector_id
            for u in users:
                rec.activity_schedule(
                    "mail.mail_activity_data_todo",
                    date_deadline=fields.Date.today() + timedelta(days=2),
                    summary=_("Inspección de muestra: %s") % rec.name,
                    user_id=u.id,
                )

    def action_accept(self):
        for rec in self:
            rec._check_attributes_valid()
            failing = rec.inspection_line_ids.filtered(
                lambda l: l.result == "no_cumple")
            if failing:
                raise UserError(
                    _("No se puede liberar: hay %d atributo(s) que no cumplen.")
                    % len(failing))
            rec.state = "aceptado"
            rec.date_inspected = fields.Datetime.now()
            rec.activity_feedback(["mail.mail_activity_data_todo"],
                                  feedback=_("Muestra aceptada"))
            rec.message_post(
                body=_("✅ Muestra ACEPTADA y liberada por %s")
                % self.env.user.name,
                subtype_xmlid="mail.mt_comment")

    def action_reject(self):
        """Notificar SOLO a la solicitante en rechazo (req. 3.4)."""
        for rec in self:
            rec.state = "rechazado"
            rec.date_inspected = fields.Datetime.now()
            rec.activity_feedback(["mail.mail_activity_data_todo"],
                                  feedback=_("Muestra rechazada"))
            if rec.requested_by.partner_id:
                rec.message_subscribe([rec.requested_by.partner_id.id])
            rec.message_post(
                body=_("❌ Muestra RECHAZADA por %s. Notificando a la solicitante: %s")
                % (self.env.user.name, rec.requested_by.name),
                partner_ids=[rec.requested_by.partner_id.id]
                if rec.requested_by.partner_id else [],
                subtype_xmlid="mail.mt_comment")

    def action_reset_draft(self):
        for rec in self:
            rec.state = "borrador"

    def action_print_sample_release(self):
        return self.env.ref(
            "quality_management.action_report_sample_release"
        ).report_action(self)
