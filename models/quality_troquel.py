# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class QualityTroquel(models.Model):
    _name = "quality.troquel"
    _description = "Troquel"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name asc"

    name = fields.Char("Identificación del Troquel", required=True,
                       tracking=True, copy=False)
    partner_id = fields.Many2one("res.partner", "Cliente",
                                 required=True, tracking=True)
    part_number = fields.Char("Número de Parte", required=True, tracking=True)
    visible_label = fields.Char("Etiqueta Visible (Cliente + No. Parte)",
                                compute="_compute_visible_label", store=True)
    state = fields.Selection([
        ("recepcion", "En Recepción"),
        ("validacion", "En Validación (Calidad/Producción)"),
        ("activo", "Activo / En Producción"),
        ("danado", "Con Daño - Fuera de Uso"),
        ("reparacion_interna", "En Reparación Interna"),
        ("reparacion_proveedor", "En Reparación con Proveedor"),
        ("obsoleto", "Obsoleto"),
    ], default="recepcion", required=True, tracking=True)
    workflow_event_ids = fields.One2many(
        "quality.troquel.event", "troquel_id", string="Bitácora")

    # Recepción / nuevos troqueles (req. 10.1)
    plano_herramental = fields.Binary("Plano de Herramental (PDF)",
                                      attachment=True)
    plano_herramental_name = fields.Char()
    proveedor_id = fields.Many2one("res.partner", "Proveedor",
                                   domain=[("supplier_rank", ">", 0)])

    # Revisión (req. 10.2)
    pieces_per_review = fields.Integer(
        "Piezas para Revisión",
        help="Cantidad de piezas troqueladas tras las cuales se hace revisión.")
    last_review_date = fields.Date("Última Revisión")
    next_review_date = fields.Date("Siguiente Revisión",
                                   compute="_compute_next_review", store=True)

    # Reparación (req. 10.3)
    days_at_supplier = fields.Integer("Días Estimados Fuera de Planta")
    repair_description = fields.Text("Desglose de Reparación")
    rack_location = fields.Char("Ubicación en Rack")

    company_id = fields.Many2one("res.company", "Compañía",
                                 default=lambda s: s.env.company)

    @api.depends("partner_id", "part_number")
    def _compute_visible_label(self):
        for rec in self:
            rec.visible_label = (
                f"{rec.partner_id.name or ''} - {rec.part_number or ''}"
            ).strip(" -")

    @api.depends("last_review_date")
    def _compute_next_review(self):
        from datetime import timedelta
        for rec in self:
            rec.next_review_date = (rec.last_review_date + timedelta(days=30)
                                    if rec.last_review_date else False)

    # ---------------------------------------------------------- workflow ALTA
    def action_validate(self):
        for rec in self:
            if not rec.plano_herramental:
                raise UserError(_(
                    "Cargue el plano de herramental antes de convocar a "
                    "validación."))
            rec.state = "validacion"
            rec._log_event("Convocatoria a validación de dimensiones y "
                           "prueba funcional (Calidad y Producción).")

    def action_activate(self):
        for rec in self:
            rec.state = "activo"
            rec._log_event(
                "Troquel registrado como ACTIVO y FUNCIONAL. "
                "Etiqueta visible: %s." % rec.visible_label)

    # ---------------------------------------------------------- workflow DAÑO
    def action_report_damage(self):
        for rec in self:
            rec.state = "danado"
            rec._log_event(
                "Producción notifica daño en troquel — Diseño debe validar.")

    def action_send_to_internal_repair(self):
        for rec in self:
            rec.state = "reparacion_interna"
            rec._log_event("Reparación interna iniciada.")

    def action_send_to_supplier(self):
        for rec in self:
            if not rec.days_at_supplier:
                raise UserError(_(
                    "Indique los días estimados fuera de planta."
                ))
            rec.state = "reparacion_proveedor"
            rec._log_event(
                "Enviado a proveedor (%s) — Días fuera: %d."
                % (rec.proveedor_id.name or "—", rec.days_at_supplier))

    def action_finish_repair(self):
        for rec in self:
            rec._log_event(
                "Reparación finalizada: %s" % (rec.repair_description or "—"))
            rec.state = "validacion"

    def action_reject_repair(self):
        for rec in self:
            rec._log_event(
                "Reparación NO cumple — se retorna al proveedor / re-trabajo.")
            rec.state = "danado"

    def action_set_obsolete(self):
        for rec in self:
            rec.state = "obsoleto"
            rec._log_event("Troquel marcado como OBSOLETO.")

    # ----- helpers -----------------------------------------------------------
    def _log_event(self, msg):
        self.ensure_one()
        self.env["quality.troquel.event"].create({
            "troquel_id": self.id,
            "user_id": self.env.user.id,
            "description": msg,
            "state_after": self.state,
        })
        self.message_post(body=msg, subtype_xmlid="mail.mt_comment")


class QualityTroquelEvent(models.Model):
    _name = "quality.troquel.event"
    _description = "Evento de Troquel"
    _order = "date desc, id desc"

    troquel_id = fields.Many2one("quality.troquel", required=True,
                                 ondelete="cascade", index=True)
    date = fields.Datetime(default=fields.Datetime.now, readonly=True)
    user_id = fields.Many2one("res.users", "Registrado por")
    description = fields.Text("Descripción", required=True)
    state_after = fields.Char("Estado Resultante")
