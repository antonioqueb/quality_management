# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class QualityActionLine(models.Model):
    _name = "quality.action.line"
    _description = "Línea de Acción Correctiva"
    _order = "date_due, id"

    corrective_id = fields.Many2one("quality.corrective.action",
                                    required=True, ondelete="cascade")
    description = fields.Text("Descripción de la Acción", required=True)
    responsible_id = fields.Many2one("res.users", "Responsable", required=True)
    date_due = fields.Date("Fecha de Cumplimiento", required=True)
    date_completed = fields.Date("Fecha de Cumplimiento Real")
    evidence_ids = fields.Many2many(
        "ir.attachment", "quality_action_evidence_rel",
        "action_line_id", "attachment_id", string="Evidencia")

    state = fields.Selection([
        ("pendiente", "Pendiente"),
        ("en_proceso", "En Proceso"),
        ("completada", "Completada"),
        ("vencida", "Vencida"),
    ], default="pendiente", required=True, compute="_compute_state",
       store=True, readonly=False)

    delay_days = fields.Integer(compute="_compute_delay_days", store=True)
    notes = fields.Text()

    @api.depends("evidence_ids", "date_completed")
    def _compute_state(self):
        """Reflejar avance en cuanto haya evidencia (req. 7.3)."""
        for line in self:
            if line.state == "completada":
                continue
            if line.evidence_ids and line.state == "pendiente":
                line.state = "en_proceso"

    @api.depends("date_due", "state")
    def _compute_delay_days(self):
        today = fields.Date.today()
        for l in self:
            if l.date_due and l.state in ("pendiente", "en_proceso", "vencida"):
                l.delay_days = max(0, (today - l.date_due).days)
            else:
                l.delay_days = 0

    def action_complete(self):
        for rec in self:
            if not rec.evidence_ids:
                raise UserError(_(
                    "No se puede completar la acción sin adjuntar evidencia."
                ))
            rec.state = "completada"
            rec.date_completed = fields.Date.today()

    def action_reopen(self):
        for rec in self:
            rec.state = "en_proceso"
            rec.date_completed = False
