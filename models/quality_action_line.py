# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class QualityActionLine(models.Model):
    _name = "quality.action.line"
    _description = "Línea de Acción Correctiva"
    _order = "date_due, id"

    corrective_id = fields.Many2one(
        "quality.corrective.action",
        required=True,
        ondelete="cascade",
    )
    description = fields.Text("Descripción de la Acción", required=True)
    responsible_id = fields.Many2one("res.users", "Responsable", required=True)
    date_due = fields.Date("Fecha de Cumplimiento", required=True)
    date_completed = fields.Date("Fecha de Cumplimiento Real")
    evidence_ids = fields.Many2many(
        "ir.attachment",
        "quality_action_evidence_rel",
        "action_line_id",
        "attachment_id",
        string="Evidencia",
    )

    # FOLIO-QM-ODOO18-005: se elimina el compute de state porque no asignaba valor
    # en todas las rutas y podía romper la carga del registro; el avance por evidencia
    # se controla ahora en create/write y en las acciones explícitas.
    state = fields.Selection(
        [
            ("pendiente", "Pendiente"),
            ("en_proceso", "En Proceso"),
            ("completada", "Completada"),
            ("vencida", "Vencida"),
        ],
        default="pendiente",
        required=True,
        readonly=False,
    )

    delay_days = fields.Integer(compute="_compute_delay_days", store=True)
    notes = fields.Text()

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec, vals in zip(records, vals_list):
            # FOLIO-QM-ODOO18-006: si la acción nace con evidencia, debe iniciar en proceso.
            if vals.get("evidence_ids") and rec.state == "pendiente":
                rec.state = "en_proceso"
        return records

    def write(self, vals):
        res = super().write(vals)
        if "evidence_ids" in vals:
            for rec in self.filtered(lambda line: line.evidence_ids and line.state == "pendiente"):
                # FOLIO-QM-ODOO18-006: al adjuntar evidencia se refleja avance sin depender de compute.
                rec.state = "en_proceso"
        return res

    @api.depends("date_due", "state")
    def _compute_delay_days(self):
        today = fields.Date.today()
        for line in self:
            if line.date_due and line.state in ("pendiente", "en_proceso", "vencida"):
                line.delay_days = max(0, (today - line.date_due).days)
            else:
                line.delay_days = 0

    def action_complete(self):
        for rec in self:
            if not rec.evidence_ids:
                raise UserError(_("No se puede completar la acción sin adjuntar evidencia."))
            rec.state = "completada"
            rec.date_completed = fields.Date.today()

    def action_reopen(self):
        for rec in self:
            rec.state = "en_proceso"
            rec.date_completed = False