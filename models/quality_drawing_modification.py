# -*- coding: utf-8 -*-
from odoo import models, fields, api


class QualityDrawingModification(models.Model):
    _name = "quality.drawing.modification"
    _description = "Modificación de Plano"
    _order = "sequence asc, id asc"

    drawing_id = fields.Many2one("quality.drawing.release", required=True,
                                 ondelete="cascade", index=True)
    sequence = fields.Integer("N°", required=True, default=1)
    date = fields.Datetime("Fecha", default=fields.Datetime.now,
                           readonly=True, required=True)
    description = fields.Text("Descripción del Cambio Solicitado",
                              required=True)
    requested_by = fields.Many2one("res.users", "Solicitado por",
                                   default=lambda s: s.env.user)
