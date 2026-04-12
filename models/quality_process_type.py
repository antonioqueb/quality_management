from odoo import models, fields


class QualityProcessType(models.Model):
    _name = 'quality.process.type'
    _description = 'Tipo de Proceso de Calidad'
    _order = 'sequence, id'

    name = fields.Char('Nombre del Proceso', required=True)
    code = fields.Char(
        'Código Interno', required=True,
        help='Código único. Ej: laminadora_remanejo, octagono, corte_laser'
    )
    sequence = fields.Integer('Secuencia', default=10)
    active = fields.Boolean('Activo', default=True)
    description = fields.Text('Descripción')
    # Configuración de campos visibles
    show_largo = fields.Boolean('Mostrar Largo')
    show_ancho = fields.Boolean('Mostrar Ancho')
    show_espesor = fields.Boolean('Mostrar Espesor')
    show_hexagono = fields.Boolean('Mostrar Hexágono')
    show_resistencia = fields.Boolean('Mostrar Resistencia')
    show_apariencia = fields.Boolean('Mostrar Apariencia')
    show_humedad = fields.Boolean('Mostrar % Humedad')
    show_pegado = fields.Boolean('Mostrar Pegado')
    show_retiramiento = fields.Boolean('Mostrar Retiramiento')
    show_calibracion = fields.Boolean('Mostrar Calibración')
    show_engomado = fields.Boolean('Mostrar Engomado')
    show_ranurado = fields.Boolean('Mostrar Ranurado')
    show_troquelado = fields.Boolean('Mostrar Troquelado')
    show_papel = fields.Boolean('Mostrar Datos de Papel')
    show_adhesivo = fields.Boolean('Mostrar Datos de Adhesivo')
    show_tipo_hexagono = fields.Boolean('Mostrar Tipo de Hexágono')
    show_corte_guillotina = fields.Boolean('Mostrar Corte en Guillotina')
    show_numero_corrida = fields.Boolean('Mostrar Número de Corrida')
    # Plantillas de atributos
    attribute_template_ids = fields.One2many(
        'quality.attribute.template', 'process_type_id',
        string='Plantillas de Atributos'
    )
    company_id = fields.Many2one(
        'res.company', 'Compañía',
        default=lambda self: self.env.company
    )

    _sql_constraints = [
        ('code_company_unique', 'unique(code, company_id)',
         'El código del proceso debe ser único por compañía.'),
    ]
