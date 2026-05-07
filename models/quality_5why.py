# -*- coding: utf-8 -*-
from odoo import models, fields


class Quality5Why(models.Model):
    _name = "quality.5why"
    _description = "5 Por qué (8D)"
    _order = "sequence asc, id asc"

    corrective_id = fields.Many2one("quality.corrective.action", required=True,
                                    ondelete="cascade", index=True)
    sequence = fields.Selection([
        ("1", "Por qué 1"), ("2", "Por qué 2"), ("3", "Por qué 3"),
        ("4", "Por qué 4"), ("5", "Por qué 5"),
    ], required=True)
    question = fields.Char("Pregunta", required=True)
    answer = fields.Text("Respuesta", required=True)
