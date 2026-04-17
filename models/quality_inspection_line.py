from odoo import models, fields, api


class QualityInspectionLine(models.Model):
    _name = 'quality.inspection.line'
    _description = 'Línea de Inspección'
    _order = 'sequence, id'

    inspection_id = fields.Many2one(
        'quality.inspection', 'Inspección', ondelete='cascade'
    )
    sample_release_id = fields.Many2one(
        'quality.sample.release', 'Liberación de Muestra', ondelete='cascade'
    )
    attribute_template_id = fields.Many2one(
        'quality.attribute.template', 'Atributo'
    )
    sequence = fields.Integer('Secuencia', default=10)
    name = fields.Char('Nombre del Atributo', required=True)
    attribute_type = fields.Selection([
        ('float', 'Numérico'),
        ('selection', 'Selección'),
        ('boolean', 'Cumple/No Cumple'),
        ('char', 'Texto'),
    ], string='Tipo de Dato', default='float')
    value_float = fields.Float('Valor Numérico')
    value_char = fields.Char('Valor Texto')
    value_boolean = fields.Boolean('Valor Sí/No')  # legacy
    value_cumple = fields.Selection([
        ('cumple', 'Cumple'),
        ('no_cumple', 'No Cumple'),
    ], string='Valor Cumple/No Cumple')
    value_selection = fields.Char('Valor Selección')
    min_value = fields.Float('Mínimo')
    max_value = fields.Float('Máximo')
    unit = fields.Char('Unidad')
    result = fields.Selection([
        ('cumple', 'Cumple'),
        ('no_cumple', 'No Cumple'),
        ('na', 'N/A'),
    ], string='Resultado', default='na')
    notes = fields.Char('Notas')

    @api.onchange('value_float', 'min_value', 'max_value', 'attribute_type')
    def _onchange_evaluate_result(self):
        for line in self:
            if line.attribute_type == 'float' and (line.min_value or line.max_value):
                if line.min_value and line.value_float < line.min_value:
                    line.result = 'no_cumple'
                elif line.max_value and line.value_float > line.max_value:
                    line.result = 'no_cumple'
                elif line.value_float:
                    line.result = 'cumple'

    @api.onchange('value_cumple', 'attribute_type')
    def _onchange_value_cumple(self):
        for line in self:
            if line.attribute_type == 'boolean' and line.value_cumple:
                line.result = line.value_cumple