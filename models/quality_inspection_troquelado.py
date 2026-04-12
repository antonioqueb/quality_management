from odoo import models, fields


class QualityInspectionTroquelado(models.Model):
    _name = 'quality.inspection.troquelado'
    _description = 'Captura de Troquelado'
    _order = 'sequence, id'

    inspection_id = fields.Many2one(
        'quality.inspection', 'Inspección',
        required=True, ondelete='cascade'
    )
    sequence = fields.Integer('N°', default=1)
    medida = fields.Float('Medida (mm)', required=True)
    resultado = fields.Selection([
        ('cumple', 'Cumple'),
        ('no_cumple', 'No Cumple'),
    ], string='Resultado', default='cumple')
    notas = fields.Char('Notas')
