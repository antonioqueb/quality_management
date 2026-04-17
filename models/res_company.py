from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    quality_stamp = fields.Binary(
        'Sello de Calidad',
        help='Imagen del sello de la empresa que aparece en los certificados de calidad.'
    )