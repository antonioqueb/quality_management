from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import timedelta


class QualityInspection(models.Model):
    _name = 'quality.inspection'
    _description = 'Inspección de PP/PT'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_inspection desc, id desc'

    name = fields.Char(
        'Referencia', required=True, readonly=True,
        default='Nuevo', copy=False
    )
    inspection_type = fields.Selection([
        ('laminadora_remanejo', 'Laminadora y Remanejo'),
        ('octagono', 'Octágono'),
        ('guillotina_pegado', 'Guillotina y Pegado'),
    ], string='Tipo de Proceso', required=True, tracking=True)
    production_order_id = fields.Many2one(
        'mrp.production', 'Orden de Producción', tracking=True
    )
    lot_id = fields.Many2one('stock.lot', 'Lote de Fabricación', tracking=True)
    product_id = fields.Many2one(
        'product.product', 'Producto', required=True, tracking=True
    )
    operator_id = fields.Many2one(
        'hr.employee', 'Operador', required=True
    )
    supervisor_id = fields.Many2one(
        'hr.employee', 'Supervisor', required=True
    )
    partner_id = fields.Many2one(
        'res.partner', 'Cliente', required=True, tracking=True
    )
    folio = fields.Char('Folio de Producción', required=True)
    code = fields.Char('Código de Producto', required=True)
    shift = fields.Selection([
        ('turno_1', 'Turno 1'),
        ('turno_2', 'Turno 2'),
        ('turno_3', 'Turno 3'),
    ], string='Turno', required=True)
    plant = fields.Selection([
        ('planta_1', 'Planta 1'),
        ('planta_2', 'Planta 2'),
    ], string='Planta', required=True)
    inspector_id = fields.Many2one(
        'res.users', 'Inspector de Calidad',
        required=True, default=lambda self: self.env.user,
        tracking=True
    )
    date_inspection = fields.Datetime(
        'Fecha y Hora de Inspección', required=True,
        default=fields.Datetime.now
    )
    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('en_proceso', 'En Proceso'),
        ('aceptado', 'Aceptado'),
        ('retenido', 'Retenido'),
        ('rechazado', 'Rechazado'),
    ], string='Estado', default='borrador', required=True,
        tracking=True, copy=False)
    is_pp = fields.Boolean('Producto en Proceso')
    is_pt = fields.Boolean('Producto Terminado')
    line_ids = fields.One2many(
        'quality.inspection.line', 'inspection_id',
        string='Atributos Capturados'
    )
    # ── Laminadora y Remanejo ──
    largo = fields.Float('Largo (mm)')
    ancho = fields.Float('Ancho (mm)')
    espesor = fields.Float('Espesor (mm)')
    hexagono = fields.Float('Hexágono')
    resistencia = fields.Float('Resistencia')
    apariencia = fields.Selection([
        ('buena', 'Buena'),
        ('regular', 'Regular'),
        ('mala', 'Mala'),
    ], string='Apariencia')
    humedad_pct = fields.Float('% Humedad')
    ranurado_ids = fields.One2many(
        'quality.inspection.ranurado', 'inspection_id',
        string='Capturas de Ranurado'
    )
    troquelado_ids = fields.One2many(
        'quality.inspection.troquelado', 'inspection_id',
        string='Capturas de Troquelado'
    )
    pegado_result = fields.Selection([
        ('cumple', 'Cumple'),
        ('no_cumple', 'No Cumple'),
    ], string='Resultado de Pegado')
    # ── Octágono ──
    oct_ancho = fields.Float('Ancho Octágono (mm)')
    oct_espesor = fields.Float('Espesor Octágono (mm)')
    oct_hexagono = fields.Float('Hexágono Octágono')
    oct_retiramiento = fields.Float('Retiramiento')
    oct_pegado = fields.Selection([
        ('cumple', 'Cumple'),
        ('no_cumple', 'No Cumple'),
    ], string='Pegado Octágono')
    # ── Guillotina y Pegado ──
    numero_corrida = fields.Char('Número de Corrida')
    papel_ancho = fields.Float('Ancho del Papel')
    papel_gramaje = fields.Float('Gramaje del Papel')
    papel_proveedor_id = fields.Many2one(
        'res.partner', 'Proveedor del Papel',
        domain=[('supplier_rank', '>', 0)]
    )
    adhesivo_lote1 = fields.Char('Lote 1 Adhesivo')
    adhesivo_lote2 = fields.Char('Lote 2 Adhesivo')
    tipo_hexagono = fields.Selection([
        ('tipo_a', 'Tipo A'),
        ('tipo_b', 'Tipo B'),
        ('tipo_c', 'Tipo C'),
    ], string='Tipo de Hexágono')
    calibracion = fields.Float('Calibración')
    engomado = fields.Selection([
        ('cumple', 'Cumple'),
        ('no_cumple', 'No Cumple'),
    ], string='Engomado')
    corte_guillotina = fields.Boolean('Corte en Guillotina')
    # ── General ──
    notes = fields.Html('Observaciones')
    certificate_ids = fields.One2many(
        'quality.certificate', 'inspection_id',
        string='Certificados'
    )
    certificate_count = fields.Integer(
        compute='_compute_certificate_count'
    )
    company_id = fields.Many2one(
        'res.company', 'Compañía',
        default=lambda self: self.env.company
    )

    @api.depends('certificate_ids')
    def _compute_certificate_count(self):
        for rec in self:
            rec.certificate_count = len(rec.certificate_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'quality.inspection') or 'Nuevo'
        return super().create(vals_list)

    def action_start(self):
        for rec in self:
            rec.state = 'en_proceso'

    def action_accept(self):
        for rec in self:
            rec.state = 'aceptado'
            rec.message_post(
                body=_('✅ Inspección ACEPTADA por %s') % self.env.user.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_retain(self):
        """Retener lote/producto en inventario."""
        for rec in self:
            rec.state = 'retenido'
            rec.message_post(
                body=_(
                    '⚠️ Producto RETENIDO por %s. '
                    'Lote: %s - Se notifica a Programación/Producción.'
                ) % (self.env.user.name, rec.lot_id.name or 'N/A'),
                subtype_xmlid='mail.mt_comment',
            )
            # Crear actividad para responsable de producción
            if rec.production_order_id and rec.production_order_id.user_id:
                rec.activity_schedule(
                    'mail.mail_activity_data_todo',
                    date_deadline=fields.Date.today() + timedelta(days=1),
                    summary=_('Producto retenido en calidad: %s') % rec.name,
                    user_id=rec.production_order_id.user_id.id,
                )

    def action_reject(self):
        for rec in self:
            rec.state = 'rechazado'
            rec.message_post(
                body=_('❌ Inspección RECHAZADA por %s') % self.env.user.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_reset_draft(self):
        for rec in self:
            rec.state = 'borrador'

    def action_create_certificate(self):
        """Abrir wizard para crear certificado."""
        self.ensure_one()
        if self.state != 'aceptado':
            raise UserError(_(
                'Solo se pueden crear certificados de inspecciones aceptadas.'
            ))
        return {
            'type': 'ir.actions.act_window',
            'name': _('Crear Certificado'),
            'res_model': 'quality.certificate.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_inspection_id': self.id,
                'default_partner_id': self.partner_id.id,
            },
        }

    def action_view_certificates(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Certificados'),
            'res_model': 'quality.certificate',
            'view_mode': 'list,form',
            'domain': [('inspection_id', '=', self.id)],
            'context': {'default_inspection_id': self.id},
        }
