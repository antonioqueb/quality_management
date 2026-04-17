from odoo import models, fields, api, _


class ResPartnerQuality(models.Model):
    _inherit = 'res.partner'

    quality_certificate_ids = fields.One2many(
        'quality.certificate', 'partner_id', string='Certificados de Calidad'
    )
    quality_certificate_count = fields.Integer(
        compute='_compute_quality_certificate_count', string='Certificados'
    )
    quality_return_ids = fields.One2many(
        'quality.customer.return', 'partner_id', string='Devoluciones de Calidad'
    )
    quality_return_count = fields.Integer(
        compute='_compute_quality_return_count', string='Devoluciones'
    )
    quality_document_ids = fields.One2many(
        'quality.customer.document', 'partner_id', string='Documentos de Calidad'
    )
    quality_document_count = fields.Integer(
        compute='_compute_quality_document_count', string='Docs. Calidad'
    )
    quality_inspection_ids = fields.One2many(
        'quality.inspection', 'partner_id', string='Inspecciones de Calidad'
    )
    quality_inspection_count = fields.Integer(
        compute='_compute_quality_inspection_count', string='Inspecciones'
    )

    @api.depends('quality_certificate_ids')
    def _compute_quality_certificate_count(self):
        data = self.env['quality.certificate']._read_group(
            [('partner_id', 'in', self.ids)],
            ['partner_id'], ['__count'],
        )
        mapped = {partner.id: count for partner, count in data}
        for rec in self:
            rec.quality_certificate_count = mapped.get(rec.id, 0)

    @api.depends('quality_return_ids')
    def _compute_quality_return_count(self):
        data = self.env['quality.customer.return']._read_group(
            [('partner_id', 'in', self.ids)],
            ['partner_id'], ['__count'],
        )
        mapped = {partner.id: count for partner, count in data}
        for rec in self:
            rec.quality_return_count = mapped.get(rec.id, 0)

    @api.depends('quality_document_ids')
    def _compute_quality_document_count(self):
        data = self.env['quality.customer.document']._read_group(
            [('partner_id', 'in', self.ids)],
            ['partner_id'], ['__count'],
        )
        mapped = {partner.id: count for partner, count in data}
        for rec in self:
            rec.quality_document_count = mapped.get(rec.id, 0)

    @api.depends('quality_inspection_ids')
    def _compute_quality_inspection_count(self):
        data = self.env['quality.inspection']._read_group(
            [('partner_id', 'in', self.ids)],
            ['partner_id'], ['__count'],
        )
        mapped = {partner.id: count for partner, count in data}
        for rec in self:
            rec.quality_inspection_count = mapped.get(rec.id, 0)

    @api.depends('name', 'vat', 'email', 'city', 'ref', 'parent_id')
    @api.depends_context('show_vat', 'show_email')
    def _compute_display_name(self):
        """Diferenciar clientes con mismo nombre en el dropdown de calidad."""
        show_vat = self.env.context.get('show_vat')
        show_email = self.env.context.get('show_email')
        if not (show_vat or show_email):
            return super()._compute_display_name()
        # Detectar duplicados por nombre
        names = [p.name for p in self if p.name]
        duplicates = set()
        if names:
            groups = self.env['res.partner']._read_group(
                [('name', 'in', names)],
                ['name'], ['__count'],
            )
            duplicates = {name for name, count in groups if count > 1}
        for partner in self:
            base = partner.name or ''
            if partner.parent_id:
                base = f"{partner.parent_id.name}, {base}"
            # Solo agrega identificador si hay homónimos
            if partner.name in duplicates:
                extras = []
                if show_vat and partner.vat:
                    extras.append(partner.vat)
                elif partner.ref:
                    extras.append(partner.ref)
                elif partner.city:
                    extras.append(partner.city)
                elif show_email and partner.email:
                    extras.append(partner.email)
                if extras:
                    base = f"{base} ({' · '.join(extras)})"
            partner.display_name = base or _('Sin nombre')

    def action_view_quality_certificates(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Certificados de Calidad'),
            'res_model': 'quality.certificate',
            'view_mode': 'list,form',
            'domain': [('partner_id', '=', self.id)],
            'context': {'default_partner_id': self.id},
        }

    def action_view_quality_returns(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Devoluciones'),
            'res_model': 'quality.customer.return',
            'view_mode': 'list,form',
            'domain': [('partner_id', '=', self.id)],
            'context': {'default_partner_id': self.id},
        }

    def action_view_quality_documents(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Documentos de Calidad'),
            'res_model': 'quality.customer.document',
            'view_mode': 'list,form',
            'domain': [('partner_id', '=', self.id)],
            'context': {'default_partner_id': self.id},
        }

    def action_view_quality_inspections(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Inspecciones de Calidad'),
            'res_model': 'quality.inspection',
            'view_mode': 'list,form',
            'domain': [('partner_id', '=', self.id)],
            'context': {'default_partner_id': self.id},
        }


class SaleOrderQuality(models.Model):
    _inherit = 'sale.order'

    quality_drawing_ids = fields.One2many(
        'quality.drawing.release', 'sale_order_id',
        string='Liberaciones de Plano'
    )
    quality_drawing_count = fields.Integer(
        compute='_compute_quality_drawing_count', string='Planos'
    )
    quality_return_ids = fields.One2many(
        'quality.customer.return', 'sale_order_id',
        string='Devoluciones'
    )
    quality_return_count = fields.Integer(
        compute='_compute_quality_return_count', string='Devoluciones'
    )

    @api.depends('quality_drawing_ids')
    def _compute_quality_drawing_count(self):
        data = self.env['quality.drawing.release']._read_group(
            [('sale_order_id', 'in', self.ids)],
            ['sale_order_id'], ['__count'],
        )
        mapped = {so.id: count for so, count in data}
        for rec in self:
            rec.quality_drawing_count = mapped.get(rec.id, 0)

    @api.depends('quality_return_ids')
    def _compute_quality_return_count(self):
        data = self.env['quality.customer.return']._read_group(
            [('sale_order_id', 'in', self.ids)],
            ['sale_order_id'], ['__count'],
        )
        mapped = {so.id: count for so, count in data}
        for rec in self:
            rec.quality_return_count = mapped.get(rec.id, 0)

    def action_view_quality_drawings(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Planos de Calidad'),
            'res_model': 'quality.drawing.release',
            'view_mode': 'list,form',
            'domain': [('sale_order_id', '=', self.id)],
            'context': {
                'default_sale_order_id': self.id,
                'default_partner_id': self.partner_id.id,
            },
        }

    def action_view_quality_returns(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Devoluciones'),
            'res_model': 'quality.customer.return',
            'view_mode': 'list,form',
            'domain': [('sale_order_id', '=', self.id)],
            'context': {
                'default_sale_order_id': self.id,
                'default_partner_id': self.partner_id.id,
            },
        }


class MrpProductionQuality(models.Model):
    _inherit = 'mrp.production'

    quality_inspection_ids = fields.One2many(
        'quality.inspection', 'production_order_id',
        string='Inspecciones de Calidad'
    )
    quality_inspection_count = fields.Integer(
        compute='_compute_quality_inspection_count', string='Inspecciones'
    )

    @api.depends('quality_inspection_ids')
    def _compute_quality_inspection_count(self):
        data = self.env['quality.inspection']._read_group(
            [('production_order_id', 'in', self.ids)],
            ['production_order_id'], ['__count'],
        )
        mapped = {mo.id: count for mo, count in data}
        for rec in self:
            rec.quality_inspection_count = mapped.get(rec.id, 0)

    def action_view_quality_inspections(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Inspecciones de Calidad'),
            'res_model': 'quality.inspection',
            'view_mode': 'list,form',
            'domain': [('production_order_id', '=', self.id)],
            'context': {'default_production_order_id': self.id},
        }