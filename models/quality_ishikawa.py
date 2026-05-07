# -*- coding: utf-8 -*-
from odoo import models, fields


class QualityIshikawa(models.Model):
    _name = "quality.ishikawa"
    _description = "Diagrama de Ishikawa (Causa-Efecto)"
    _order = "category, sequence, id"

    corrective_id = fields.Many2one("quality.corrective.action", required=True,
                                    ondelete="cascade", index=True)
    category = fields.Selection([
        ("metodo", "Método"), ("maquina", "Máquina"),
        ("mano_obra", "Mano de Obra"), ("material", "Material"),
        ("medicion", "Medición"), ("medio_ambiente", "Medio Ambiente"),
    ], required=True)
    sequence = fields.Integer(default=10)
    cause = fields.Text("Causa Identificada", required=True)
    is_root_cause = fields.Boolean("Causa Raíz")
