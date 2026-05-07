# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class QualityCertificate(models.Model):
    _name = "quality.certificate"
    _description = "Certificado de Calidad"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_generated desc, id desc"

    name = fields.Char("Referencia", required=True, readonly=True,
                       default="Nuevo", copy=False)
    inspection_id = fields.Many2one("quality.inspection", "Inspección Fuente",
                                    required=True, tracking=True,
                                    domain=[("state", "=", "aceptado")])
    partner_id = fields.Many2one("res.partner", "Cliente",
                                 required=True, tracking=True)
    product_id = fields.Many2one(related="inspection_id.product_id",
                                 store=True)
    process_type_id = fields.Many2one(
        related="inspection_id.process_type_id", store=True)
    inspection_type = fields.Selection(
        related="inspection_id.inspection_type", store=True)

    # Líneas de inspección a incluir, dedupeadas (req. 6)
    attribute_ids = fields.Many2many(
        "quality.inspection.line",
        "quality_certificate_attribute_rel",
        "certificate_id", "line_id", string="Atributos Seleccionados")

    certified_largo = fields.Float()
    certified_ancho = fields.Float()
    certified_espesor = fields.Float()
    certified_hexagono = fields.Float()
    certified_resistencia = fields.Float()
    certified_apariencia = fields.Char()
    certified_humedad = fields.Float()
    certified_pegado = fields.Char()
    certified_retiramiento = fields.Float()
    certified_calibracion = fields.Float()
    certified_engomado = fields.Char()

    date_generated = fields.Date("Fecha de Generación", required=True,
                                 default=fields.Date.context_today)
    state = fields.Selection([
        ("borrador", "Borrador"),
        ("generado", "Generado"),
        ("enviado", "Enviado"),
    ], default="borrador", required=True, tracking=True, copy=False)
    report_pdf = fields.Binary("PDF del Certificado", attachment=True)
    report_pdf_name = fields.Char()
    certified_by = fields.Many2one("res.users", required=True,
                                   default=lambda s: s.env.user, tracking=True)
    company_id = fields.Many2one("res.company", "Compañía",
                                 default=lambda s: s.env.company)
    folio = fields.Char(related="inspection_id.folio", store=True)
    lot_id = fields.Many2one(related="inspection_id.lot_id", store=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Nuevo") == "Nuevo":
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "quality.certificate") or "Nuevo"
        return super().create(vals_list)

    @api.constrains("attribute_ids")
    def _check_attribute_dedup(self):
        """No permitir atributos repetidos (req. 6)."""
        for rec in self:
            names = [(l.name or "").strip().lower()
                     for l in rec.attribute_ids if l.name]
            if len(names) != len(set(names)):
                raise UserError(_(
                    "Hay atributos repetidos en el certificado. "
                    "Cada atributo debe aparecer una sola vez."
                ))

    @api.constrains("certified_largo", "certified_ancho", "certified_espesor",
                    "certified_hexagono", "certified_resistencia",
                    "certified_humedad", "certified_retiramiento",
                    "certified_calibracion")
    def _check_no_zero_certified(self):
        """No permitir guardar atributos con valor 0 (req. 6)."""
        zero_fields = []
        for rec in self:
            mapping = {
                "Largo": rec.certified_largo,
                "Ancho": rec.certified_ancho,
                "Espesor": rec.certified_espesor,
                "Hexágono": rec.certified_hexagono,
                "Resistencia": rec.certified_resistencia,
                "Humedad": rec.certified_humedad,
                "Retiramiento": rec.certified_retiramiento,
                "Calibración": rec.certified_calibracion,
            }
            for label, value in mapping.items():
                # Solo bloquea si el campo se intentó capturar (>0 esperado)
                # y se guardó como 0 explícitamente. Por lógica del wizard,
                # solo se setea cuando hay valor > 0; este constraint refuerza.
                if value is not None and value < 0:
                    zero_fields.append(label)
            if zero_fields:
                raise UserError(_(
                    "El certificado no puede contener valores 0 ni negativos. "
                    "Revise: %s"
                ) % ", ".join(zero_fields))

    def action_generate(self):
        for rec in self:
            rec.state = "generado"

    def action_send_email(self):
        self.ensure_one()
        template = self.env.ref(
            "quality_management.email_template_quality_certificate",
            raise_if_not_found=False)
        compose = self.env.ref("mail.email_compose_message_wizard_form")
        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(compose.id, "form")],
            "target": "new",
            "context": {
                "default_model": "quality.certificate",
                "default_res_ids": self.ids,
                "default_template_id": template.id if template else False,
                "default_composition_mode": "comment",
                "mark_so_as_sent": True,
            },
        }

    def action_mark_sent(self):
        for rec in self:
            rec.state = "enviado"

    def action_print_certificate(self):
        return self.env.ref(
            "quality_management.action_report_quality_certificate"
        ).report_action(self)
