from odoo import models, fields, api, _


class QualityCertificate(models.Model):
    _name = 'quality.certificate'
    _description = 'Certificado de Calidad'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_generated desc, id desc'

    name = fields.Char(
        'Referencia', required=True, readonly=True,
        default='Nuevo', copy=False
    )
    inspection_id = fields.Many2one(
        'quality.inspection', 'Inspección Fuente',
        required=True, tracking=True,
        domain=[('state', '=', 'aceptado')]
    )
    partner_id = fields.Many2one(
        'res.partner', 'Cliente', required=True, tracking=True
    )
    product_id = fields.Many2one(
        related='inspection_id.product_id',
        string='Producto', store=True
    )
    inspection_type = fields.Selection(
        related='inspection_id.inspection_type',
        string='Tipo de Proceso', store=True
    )
    # Atributos seleccionados para el certificado
    attribute_ids = fields.Many2many(
        'quality.inspection.line',
        'quality_certificate_attribute_rel',
        'certificate_id', 'line_id',
        string='Atributos del Certificado'
    )
    # Campos de valores certificados (snapshot)
    certified_largo = fields.Float('Largo (mm)')
    certified_ancho = fields.Float('Ancho (mm)')
    certified_espesor = fields.Float('Espesor (mm)')
    certified_hexagono = fields.Float('Hexágono')
    certified_resistencia = fields.Float('Resistencia')
    certified_apariencia = fields.Char('Apariencia')
    certified_humedad = fields.Float('% Humedad')
    certified_pegado = fields.Char('Pegado')
    certified_retiramiento = fields.Float('Retiramiento')
    certified_calibracion = fields.Float('Calibración')
    certified_engomado = fields.Char('Engomado')
    # ──
    date_generated = fields.Date(
        'Fecha de Generación', required=True,
        default=fields.Date.context_today
    )
    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('generado', 'Generado'),
        ('enviado', 'Enviado'),
    ], string='Estado', default='borrador', required=True,
        tracking=True, copy=False)
    report_pdf = fields.Binary('PDF del Certificado', attachment=True)
    report_pdf_name = fields.Char('Nombre del PDF')
    certified_by = fields.Many2one(
        'res.users', 'Certificado por',
        required=True, default=lambda self: self.env.user,
        tracking=True
    )
    company_id = fields.Many2one(
        'res.company', 'Compañía',
        default=lambda self: self.env.company
    )
    folio = fields.Char(related='inspection_id.folio', string='Folio', store=True)
    lot_id = fields.Many2one(related='inspection_id.lot_id', string='Lote', store=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'quality.certificate') or 'Nuevo'
        return super().create(vals_list)

    def action_generate(self):
        """Generar el certificado PDF."""
        for rec in self:
            rec.state = 'generado'
            rec.message_post(
                body=_('Certificado generado por %s') % self.env.user.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_send_email(self):
        """Enviar certificado por correo al cliente."""
        self.ensure_one()
        template = self.env.ref(
            'quality_management.email_template_quality_certificate',
            raise_if_not_found=False
        )
        compose_form = self.env.ref('mail.email_compose_message_wizard_form')
        ctx = {
            'default_model': 'quality.certificate',
            'default_res_ids': self.ids,
            'default_template_id': template.id if template else False,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }

    def action_mark_sent(self):
        for rec in self:
            rec.state = 'enviado'
            rec.message_post(
                body=_('Certificado enviado al cliente %s') % rec.partner_id.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_print_certificate(self):
        return self.env.ref(
            'quality_management.action_report_quality_certificate'
        ).report_action(self)
