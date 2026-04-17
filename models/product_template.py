from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    quality_attribute_template_ids = fields.One2many(
        'quality.attribute.template', 'product_tmpl_id',
        string='Plantillas de Atributos de Calidad'
    )
    quality_attribute_count = fields.Integer(
        compute='_compute_quality_attribute_count',
        string='Atributos de Calidad'
    )

    @api.depends('quality_attribute_template_ids')
    def _compute_quality_attribute_count(self):
        for rec in self:
            rec.quality_attribute_count = len(rec.quality_attribute_template_ids)

    def action_view_quality_attributes(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Plantillas de Atributos'),
            'res_model': 'quality.attribute.template',
            'view_mode': 'list,form',
            'domain': [('product_tmpl_id', '=', self.id)],
            'context': {'default_product_tmpl_id': self.id},
        }