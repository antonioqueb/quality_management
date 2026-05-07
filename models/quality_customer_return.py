# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import timedelta


class QualityCustomerReturn(models.Model):
    _name = "quality.customer.return"
    _description = "Devolución de Cliente"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_received desc, id desc"

    name = fields.Char("Referencia", required=True, readonly=True,
                       default="Nuevo", copy=False)
    partner_id = fields.Many2one("res.partner", "Cliente",
                                 required=True, tracking=True)
    sale_order_id = fields.Many2one("sale.order", "Orden de Venta Original",
                                    tracking=True)
    defect_type = fields.Selection([
        ("dimensional", "Dimensional"),
        ("apariencia", "Apariencia"),
        ("funcional", "Funcional"),
        ("empaque", "Empaque"),
        ("otro", "Otro"),
    ], required=True, tracking=True)
    defect_other_desc = fields.Char("Descripción Defecto Otro")
    defect_pieces = fields.Integer("Piezas con Defecto", required=True)
    return_reason = fields.Text("Motivo de la Devolución", required=True)
    production_date = fields.Date("Fecha de Producción", required=True)
    delivery_date = fields.Date("Fecha de Entrega Producción/Fabricación")

    evidence_ids = fields.Many2many(
        "ir.attachment", "quality_return_evidence_rel",
        "return_id", "attachment_id",
        string="Evidencia Fotográfica", required=True)

    evidence_pdf = fields.Binary("Reporte de Evidencia (PDF)", attachment=True)
    evidence_pdf_name = fields.Char()
    pallets_returned = fields.Boolean("Se Regresan Tarimas")
    pallet_return_date = fields.Date("Fecha Retorno de Tarimas")

    # Formato de reclamación obligatorio (req. 7.5 / 8)
    claim_format_pdf = fields.Binary("Formato de Reclamación (PDF)",
                                     attachment=True, required=False)
    claim_format_pdf_name = fields.Char()

    affects_functionality = fields.Boolean("Afecta Funcionalidad",
                                           tracking=True)
    corrective_action_id = fields.Many2one("quality.corrective.action",
                                           "8D Generado", readonly=True,
                                           tracking=True)

    # Justificación comercial cuando excede 30 días (req. 7.4 / 8)
    sales_manager_justification = fields.Text(
        "Motivo Comercial - Gerente de Ventas",
        help="Cuando comercialmente se decide proceder con devolución/"
             "reposición pese al bloqueo (>30 días).",
    )
    sales_manager_id = fields.Many2one("res.users",
                                       "Gerente de Ventas Autorizó")

    state = fields.Selection([
        ("borrador", "Borrador"),
        ("evaluacion_ventas", "Evaluación Ventas"),
        ("evaluacion_calidad", "Evaluación Calidad"),
        ("en_8d", "En 8D"),
        ("cerrada", "Cerrada"),
        ("no_procede", "No Procede"),
    ], default="borrador", required=True, tracking=True, copy=False)

    date_received = fields.Date("Fecha de Recepción", required=True,
                                default=fields.Date.context_today)
    days_since_production = fields.Integer(
        compute="_compute_days_since_production")
    is_within_period = fields.Boolean(
        compute="_compute_days_since_production")
    pallet_alert_15 = fields.Boolean(
        "Alerta: Retorno >15 días",
        compute="_compute_pallet_alert_15", store=True)
    company_id = fields.Many2one("res.company", "Compañía",
                                 default=lambda s: s.env.company)

    @api.depends("production_date", "date_received")
    def _compute_days_since_production(self):
        for rec in self:
            if rec.production_date and rec.date_received:
                delta = (rec.date_received - rec.production_date).days
                rec.days_since_production = delta
                rec.is_within_period = delta < 30
            else:
                rec.days_since_production = 0
                rec.is_within_period = True

    @api.depends("pallet_return_date", "date_received", "pallets_returned")
    def _compute_pallet_alert_15(self):
        for rec in self:
            if (rec.pallets_returned and rec.pallet_return_date
                    and rec.date_received):
                delta = (rec.pallet_return_date - rec.date_received).days
                rec.pallet_alert_15 = delta > 15
            else:
                rec.pallet_alert_15 = False

    @api.constrains("defect_type", "defect_other_desc")
    def _check_other(self):
        for rec in self:
            if rec.defect_type == "otro" and not rec.defect_other_desc:
                raise UserError(_(
                    "Tipo de defecto OTRO requiere descripción."))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Nuevo") == "Nuevo":
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "quality.customer.return") or "Nuevo"
        return super().create(vals_list)

    def _check_required_attachments(self):
        for rec in self:
            if not rec.evidence_ids:
                raise UserError(_("Debe adjuntar evidencia fotográfica."))
            if not rec.claim_format_pdf:
                raise UserError(_(
                    "Debe adjuntar el Formato de Reclamación (PDF)."
                ))

    def action_submit_sales(self):
        for rec in self:
            rec._check_required_attachments()
            if not rec.is_within_period and not rec.sales_manager_justification:
                rec.state = "no_procede"
                rec.message_post(
                    body=_(
                        "🚫 Devolución NO PROCEDE: %d días desde producción "
                        "(>30). Capture el motivo comercial del Gerente "
                        "de Ventas si desea proceder."
                    ) % rec.days_since_production,
                    subtype_xmlid="mail.mt_comment")
                continue
            rec.state = "evaluacion_ventas"

    def action_authorize_commercial(self):
        """Permite continuar pese a >30 días si Gerente de Ventas lo justifica."""
        for rec in self:
            if not rec.sales_manager_justification:
                raise UserError(_(
                    "Capture el motivo comercial del Gerente de Ventas."
                ))
            rec.sales_manager_id = self.env.user
            rec.state = "evaluacion_ventas"
            rec.message_post(
                body=_(
                    "✓ Autorización comercial por %s. Motivo: %s"
                ) % (self.env.user.name, rec.sales_manager_justification),
                subtype_xmlid="mail.mt_comment")

    def action_submit_quality(self):
        for rec in self:
            rec.state = "evaluacion_calidad"
            users = self.env.ref(
                "quality_management.group_quality_manager").users
            for u in users:
                rec.activity_schedule(
                    "mail.mail_activity_data_todo",
                    date_deadline=fields.Date.today() + timedelta(days=3),
                    summary=_("Evaluar devolución: %s") % rec.name,
                    user_id=u.id)
            if rec.pallets_returned:
                rec.message_post(
                    body=_(
                        "📦 Tarimas retornadas. Logística/Producción: "
                        "evaluar físicamente de inmediato."),
                    subtype_xmlid="mail.mt_comment")
            if rec.pallet_alert_15:
                rec.message_post(
                    body=_(
                        "⚠️ Alerta: el retorno de tarimas se programó a "
                        "más de 15 días hábiles desde recepción."),
                    subtype_xmlid="mail.mt_comment")

    def action_generate_8d(self):
        for rec in self:
            ca = self.env["quality.corrective.action"].create({
                "origin_type": "devolucion",
                "defect_type": rec.defect_type,
                "defect_other_desc": rec.defect_other_desc,
                "origin_description": _(
                    "Devolución de cliente: %s\nTipo de defecto: %s\n"
                    "Piezas: %d\nMotivo: %s"
                ) % (rec.partner_id.name,
                     dict(rec._fields["defect_type"].selection).get(
                         rec.defect_type, ""),
                     rec.defect_pieces, rec.return_reason),
                "origin_return_id": rec.id,
                "responsible_id": self.env.user.id,
            })
            rec.corrective_action_id = ca.id
            rec.state = "en_8d"

    def action_close(self):
        for rec in self:
            rec.state = "cerrada"

    def action_no_proceed(self):
        for rec in self:
            rec.state = "no_procede"

    def action_print_customer_return(self):
        return self.env.ref(
            "quality_management.action_report_customer_return"
        ).report_action(self)
