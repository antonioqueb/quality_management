from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
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
    # ── Tipo de proceso dinámico ──
    process_type_id = fields.Many2one(
        'quality.process.type', 'Tipo de Proceso',
        required=True, tracking=True
    )
    inspection_type = fields.Selection([
        ('laminadora_remanejo', 'Laminadora y Remanejo'),
        ('octagono', 'Octágono'),
        ('guillotina_pegado', 'Guillotina y Pegado'),
    ], string='Tipo (Legacy)',
        compute='_compute_inspection_type', store=True)
    # ── Visibilidad dinámica ──
    show_largo = fields.Boolean(related='process_type_id.show_largo')
    show_ancho = fields.Boolean(related='process_type_id.show_ancho')
    show_espesor = fields.Boolean(related='process_type_id.show_espesor')
    show_hexagono = fields.Boolean(related='process_type_id.show_hexagono')
    show_resistencia = fields.Boolean(related='process_type_id.show_resistencia')
    show_apariencia = fields.Boolean(related='process_type_id.show_apariencia')
    show_humedad = fields.Boolean(related='process_type_id.show_humedad')
    show_pegado = fields.Boolean(related='process_type_id.show_pegado')
    show_retiramiento = fields.Boolean(related='process_type_id.show_retiramiento')
    show_calibracion = fields.Boolean(related='process_type_id.show_calibracion')
    show_engomado = fields.Boolean(related='process_type_id.show_engomado')
    show_ranurado = fields.Boolean(related='process_type_id.show_ranurado')
    show_troquelado = fields.Boolean(related='process_type_id.show_troquelado')
    show_papel = fields.Boolean(related='process_type_id.show_papel')
    show_adhesivo = fields.Boolean(related='process_type_id.show_adhesivo')
    show_tipo_hexagono = fields.Boolean(related='process_type_id.show_tipo_hexagono')
    show_corte_guillotina = fields.Boolean(related='process_type_id.show_corte_guillotina')
    show_numero_corrida = fields.Boolean(related='process_type_id.show_numero_corrida')
    # ── Datos generales ──
    production_order_id = fields.Many2one(
        'mrp.production', 'Orden de Producción', tracking=True
    )
    lot_id = fields.Many2one('stock.lot', 'Lote de Fabricación', tracking=True)
    product_id = fields.Many2one(
        'product.product', 'Producto', required=True, tracking=True
    )
    operator_id = fields.Many2one('hr.employee', 'Operador', required=True)
    supervisor_id = fields.Many2one('hr.employee', 'Supervisor', required=True)
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
        ('planta_3', 'Planta 3'),
        ('planta_6', 'Planta 6'),
        ('planta_7', 'Planta 7'),
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
    # ── Campos de medición ──
    largo = fields.Float('Largo (mm)')
    ancho = fields.Float('Ancho (mm)')
    espesor = fields.Float('Espesor')
    espesor_unit = fields.Selection([
        ('in', 'Pulgadas (in)'),
        ('mm', 'Milímetros (mm)'),
    ], string='Unidad Espesor', default='in')
    espesor_label = fields.Char(
        'Etiqueta Espesor', compute='_compute_espesor_label', store=False
    )
    hexagono = fields.Selection([
        ('tipo_1', 'Tipo 1'),
        ('tipo_2', 'Tipo 2'),
        ('tipo_3', 'Tipo 3'),
        ('tipo_4', 'Tipo 4'),
    ], string='Hexágono')
    resistencia = fields.Float('Resistencia (Lbf)')
    resistencia_na = fields.Boolean('Resistencia No Aplica')
    apariencia = fields.Selection([
        ('cumple', 'Cumple'),
        ('no_cumple', 'No Cumple'),
    ], string='Apariencia')
    humedad_pct = fields.Float('% Humedad')
    ranurado_unit = fields.Selection([
        ('mm', 'Milímetros (mm)'),
        ('in', 'Pulgadas (in)'),
    ], string='Unidad Ranurado', default='mm')
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
    oct_ancho = fields.Float('Ancho Octágono (mm)')
    oct_espesor = fields.Float('Espesor Octágono (mm)')
    oct_hexagono = fields.Float('Hexágono Octágono')
    oct_retiramiento = fields.Float('Retiramiento')
    oct_pegado = fields.Selection([
        ('cumple', 'Cumple'),
        ('no_cumple', 'No Cumple'),
    ], string='Pegado Octágono')
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
    # ── Evidencia con preview ──
    evidence_pdf = fields.Binary('Documento de Evidencia (PDF)', attachment=True)
    evidence_pdf_name = fields.Char('Nombre del Documento')
    # ── General ──
    notes = fields.Html('Observaciones')
    certificate_ids = fields.One2many(
        'quality.certificate', 'inspection_id', string='Certificados'
    )
    certificate_count = fields.Integer(compute='_compute_certificate_count')
    company_id = fields.Many2one(
        'res.company', 'Compañía',
        default=lambda self: self.env.company
    )

    @api.depends('process_type_id', 'process_type_id.code')
    def _compute_inspection_type(self):
        legacy_codes = ('laminadora_remanejo', 'octagono', 'guillotina_pegado')
        for rec in self:
            code = rec.process_type_id.code if rec.process_type_id else False
            rec.inspection_type = code if code in legacy_codes else False

    @api.depends('certificate_ids')
    def _compute_certificate_count(self):
        for rec in self:
            rec.certificate_count = len(rec.certificate_ids)

    @api.depends('espesor_unit')
    def _compute_espesor_label(self):
        for rec in self:
            if rec.espesor_unit == 'mm':
                rec.espesor_label = 'Espesor (mm)'
            else:
                rec.espesor_label = 'Espesor (in)'

    @api.onchange('resistencia_na')
    def _onchange_resistencia_na(self):
        if self.resistencia_na:
            self.resistencia = 0.0

    @api.constrains('resistencia', 'resistencia_na', 'show_resistencia')
    def _check_resistencia(self):
        # Si resistencia_na=True se permite dejar resistencia en 0 sin error.
        # No se necesita validación adicional; se deja explícito como doc.
        pass

    @api.onchange('process_type_id', 'product_id')
    def _onchange_load_attribute_templates(self):
        """Carga plantillas del tipo de proceso (sin producto específico) +
        plantillas específicas del producto seleccionado."""
        if not self.process_type_id and not self.product_id:
            return
        templates = self.env['quality.attribute.template']
        # Plantillas del tipo de proceso (que no estén atadas a un producto)
        if self.process_type_id:
            templates |= self.process_type_id.attribute_template_ids.filtered(
                lambda t: not t.product_tmpl_id and t.active
            )
        # Plantillas específicas del producto
        if self.product_id and self.product_id.product_tmpl_id:
            templates |= self.env['quality.attribute.template'].search([
                ('product_tmpl_id', '=', self.product_id.product_tmpl_id.id),
                ('active', '=', True),
            ])
        if templates:
            lines = [(5, 0, 0)]  # limpia las líneas existentes
            for tmpl in templates:
                lines.append((0, 0, {
                    'attribute_template_id': tmpl.id,
                    'name': tmpl.name,
                    'attribute_type': tmpl.attribute_type,
                    'min_value': tmpl.min_value,
                    'max_value': tmpl.max_value,
                    'unit': tmpl.unit,
                    'sequence': tmpl.sequence,
                }))
            self.line_ids = lines

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
        for rec in self:
            rec.state = 'retenido'
            rec.message_post(
                body=_(
                    '⚠️ Producto RETENIDO por %s. '
                    'Lote: %s - Se notifica a Programación/Producción.'
                ) % (self.env.user.name, rec.lot_id.name or 'N/A'),
                subtype_xmlid='mail.mt_comment',
            )
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

    def action_print_inspection(self):
        return self.env.ref(
            'quality_management.action_report_inspection_summary'
        ).report_action(self)