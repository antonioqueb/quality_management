from odoo import models, fields, api


class QualityAttributeTemplate(models.Model):
    _name = 'quality.attribute.template'
    _description = 'Plantilla de Atributos de Calidad'
    _order = 'sequence, id'

    name = fields.Char('Nombre del Atributo', required=True)
    sequence = fields.Integer('Secuencia', default=10)
    inspection_type = fields.Selection([
        ('laminadora_remanejo', 'Laminadora y Remanejo'),
        ('octagono', 'Octágono'),
        ('guillotina_pegado', 'Guillotina y Pegado'),
        ('muestra', 'Muestra'),
        ('general', 'General'),
    ], string='Tipo de Proceso', required=True)
    attribute_type = fields.Selection([
        ('float', 'Numérico'),
        ('selection', 'Selección'),
        ('boolean', 'Sí/No'),
        ('char', 'Texto'),
    ], string='Tipo de Dato', required=True, default='float')
    selection_options = fields.Char(
        'Opciones de Selección',
        help='Valores separados por coma. Ej: buena,regular,mala'
    )
    min_value = fields.Float('Valor Mínimo')
    max_value = fields.Float('Valor Máximo')
    unit = fields.Char('Unidad de Medida', help='Ej: mm, %, kg')
    is_required = fields.Boolean('Obligatorio', default=True)
    active = fields.Boolean('Activo', default=True)
    company_id = fields.Many2one(
        'res.company', 'Compañía',
        default=lambda self: self.env.company
    )
