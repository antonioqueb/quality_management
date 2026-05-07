# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import timedelta


class QualityCustomerDocument(models.Model):
    _name = "quality.customer.document"
    _description = "Documento Solicitado por Cliente"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_requested desc, id desc"

    name = fields.Char("Referencia", required=True, readonly=True,
                       default="Nuevo", copy=False)
    partner_id = fields.Many2one("res.partner", "Cliente Solicitante",
                                 required=True, tracking=True)

    # Tipos limpios (req. 9.1) — sin APARIENCIA ni ESPECIFICACION_EMPAQUE
    document_type = fields.Selection([
        ("rohs", "RoHS"),
        ("psw", "PSW"),
        ("ppap", "PPAP"),
        ("pfmea", "PFMEA"),
        ("diagrama_flujo", "Diagrama de Flujo"),
        ("carta_garantia", "Carta Garantía"),
        ("otro", "Otro"),
    ], string="Tipo de Documento", required=True, tracking=True)

    # OTRO con descripción libre (req. 9.4)
    document_type_other = fields.Char(
        "Especifique Tipo (Otro)",
        help="Cuando el tipo de documento solicitado no está en el listado.",
    )

    description = fields.Text(
        "Descripción de la Solicitud", required=True,
        help="Bloqueo: no se puede avanzar sin descripción.",
    )

    requires_dimensions = fields.Boolean(
        "Implica Mediciones Dimensionales", required=True, tracking=True)

    # Formato del cliente (Sí/No + carga) — req. 9.2
    has_client_format = fields.Selection([
        ("si", "Sí"), ("no", "No"),
    ], string="¿Cliente Solicita Llenado en su Formato?", default="no")
    client_format_ids = fields.Many2many(
        "ir.attachment", "quality_doc_client_format_rel",
        "document_id", "attachment_id", string="Formatos del Cliente")

    result_document_ids = fields.Many2many(
        "ir.attachment", "quality_doc_result_rel",
        "document_id", "attachment_id",
        string="Documentos Generados / Cargados")

    # Documento principal — soporta PDF o imagen (req. 9.2)
    main_pdf = fields.Binary("Documento Principal (PDF)", attachment=True)
    main_pdf_name = fields.Char()
    main_image = fields.Binary("Imagen Principal (PNG/JPG)", attachment=True)
    main_image_name = fields.Char()

    requested_by = fields.Many2one("res.users", "Solicitante (Ventas)",
                                   required=True,
                                   default=lambda s: s.env.user, tracking=True)
    responsible_id = fields.Many2one("res.users", "Responsable en Calidad",
                                     required=True, tracking=True)

    state = fields.Selection([
        ("borrador", "Borrador"),
        ("en_proceso", "En Proceso"),
        ("completado", "Completado"),
        ("enviado", "Enviado"),
    ], default="borrador", required=True, tracking=True, copy=False)

    # Fechas bloqueadas (req. 9.1)
    date_requested = fields.Date("Fecha de Solicitud", required=True,
                                 readonly=True, copy=False,
                                 default=fields.Date.context_today)
    date_due = fields.Date("Fecha Límite", compute="_compute_date_due",
                           store=True, readonly=True)
    date_completed = fields.Date("Fecha de Entrega Real", readonly=True)

    company_id = fields.Many2one("res.company", "Compañía",
                                 default=lambda s: s.env.company)

    @api.depends("date_requested", "requires_dimensions")
    def _compute_date_due(self):
        for rec in self:
            if rec.date_requested:
                days = 7 if rec.requires_dimensions else 5
                rec.date_due = rec.date_requested + timedelta(days=days)
            else:
                rec.date_due = False

    @api.constrains("document_type", "document_type_other")
    def _check_other(self):
        for rec in self:
            if rec.document_type == "otro" and not rec.document_type_other:
                raise UserError(_(
                    "Tipo de documento OTRO requiere especificación."))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Nuevo") == "Nuevo":
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "quality.customer.document") or "Nuevo"
        return super().create(vals_list)

    def _check_can_save(self):
        """Bloqueos req. 9.3: descripción y al menos un documento cargado."""
        for rec in self:
            if not rec.description or not rec.description.strip():
                raise UserError(_(
                    "Capture la descripción de la solicitud antes de avanzar."
                ))
            tiene_doc = (rec.main_pdf or rec.main_image
                         or rec.result_document_ids
                         or rec.client_format_ids)
            if not tiene_doc:
                raise UserError(_(
                    "Debe cargar al menos un documento (PDF, imagen o adjunto) "
                    "antes de avanzar."
                ))

    def action_start(self):
        for rec in self:
            rec._check_can_save()
            rec.state = "en_proceso"

    def action_complete(self):
        for rec in self:
            rec._check_can_save()
            rec.state = "completado"
            rec.date_completed = fields.Date.today()

    def action_send(self):
        for rec in self:
            rec.state = "enviado"

    def action_print_customer_document(self):
        return self.env.ref(
            "quality_management.action_report_customer_document"
        ).report_action(self)
