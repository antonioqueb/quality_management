from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import timedelta


class QualityCustomerReturn(models.Model):
    _name = 'quality.customer.return'
    _description = 'Devolución de Cliente'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_received desc, id desc'

    name = fields.Char(
        'Referencia', required=True, readonly=True,
        default='Nuevo', copy=False
    )
    partner_id = fields.Many2one(
        'res.partner', 'Cliente', required=True, tracking=True
    )
    sale_order_id = fields.Many2one(
        'sale.order', 'Orden de Venta Original', tracking=True
    )
    defect_type = fields.Selection([
        ('dimensional', 'Dimensional'),
        ('apariencia', 'Apariencia'),
        ('funcional', 'Funcional'),
        ('empaque', 'Empaque'),
        ('otro', 'Otro'),
    ], string='Tipo de Defecto', required=True, tracking=True)
    defect_pieces = fields.Integer('Piezas con Defecto', required=True)
    return_reason = fields.Text('Motivo de la Devolución', required=True)
    production_date = fields.Date('Fecha de Producción', required=True)
    evidence_ids = fields.Many2many(
        'ir.attachment', 'quality_return_evidence_rel',
        'return_id', 'attachment_id',
        string='Evidencia Fotográfica', required=True
    )
    # PDF de evidencia con preview
    evidence_pdf = fields.Binary('Reporte de Evidencia (PDF)', attachment=True)
    evidence_pdf_name = fields.Char('Nombre del Reporte')
    pallets_returned = fields.Boolean('Se Regresan Tarimas')
    pallet_return_date = fields.Date('Fecha Retorno de Tarimas')
    claim_format_id = fields.Many2one(
        'ir.attachment', 'Formato de Reclamación'
    )
    affects_functionality = fields.Boolean(
        'Afecta Funcionalidad', tracking=True
    )
    corrective_action_id = fields.Many2one(
        'quality.corrective.action', '8D Generado',
        readonly=True, tracking=True
    )
    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('evaluacion_ventas', 'Evaluación Ventas'),
        ('evaluacion_calidad', 'Evaluación Calidad'),
        ('en_8d', 'En 8D'),
        ('cerrada', 'Cerrada'),
        ('no_procede', 'No Procede'),
    ], string='Estado', default='borrador', required=True,
        tracking=True, copy=False)
    date_received = fields.Date(
        'Fecha de Recepción', required=True,
        default=fields.Date.context_today
    )
    days_since_production = fields.Integer(
        'Días desde Producción',
        compute='_compute_days_since_production'
    )
    is_within_period = fields.Boolean(
        'Dentro de Periodo',
        compute='_compute_days_since_production'
    )
    company_id = fields.Many2one(
        'res.company', 'Compañía',
        default=lambda self: self.env.company
    )

    @api.depends('production_date', 'date_received')
    def _compute_days_since_production(self):
        for rec in self:
            if rec.production_date and rec.date_received:
                delta = (rec.date_received - rec.production_date).days
                rec.days_since_production = delta
                rec.is_within_period = delta < 30
            else:
                rec.days_since_production = 0
                rec.is_within_period = True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'quality.customer.return') or 'Nuevo'
        return super().create(vals_list)

    def action_submit_sales(self):
        for rec in self:
            if not rec.is_within_period:
                rec.state = 'no_procede'
                rec.message_post(
                    body=_(
                        'Devolución NO PROCEDE: fecha de producción mayor a '
                        '30 días (%d días).'
                    ) % rec.days_since_production,
                    subtype_xmlid='mail.mt_comment',
                )
                return
            rec.state = 'evaluacion_ventas'
            rec.message_post(
                body=_('Devolución registrada, en evaluación por Ventas.'),
                subtype_xmlid='mail.mt_comment',
            )

    def action_submit_quality(self):
        for rec in self:
            rec.state = 'evaluacion_calidad'
            quality_users = self.env.ref(
                'quality_management.group_quality_manager'
            ).users
            for user in quality_users:
                rec.activity_schedule(
                    'mail.mail_activity_data_todo',
                    date_deadline=fields.Date.today() + timedelta(days=3),
                    summary=_('Evaluar devolución: %s') % rec.name,
                    user_id=user.id,
                )
            rec.message_post(
                body=_('Devolución enviada a evaluación de Calidad.'),
                subtype_xmlid='mail.mt_comment',
            )
            if rec.pallets_returned:
                rec.message_post(
                    body=_(
                        '📦 Se retornaron tarimas a planta. '
                        'Logística/Producción: evaluar físicamente.'
                    ),
                    subtype_xmlid='mail.mt_comment',
                )

    def action_generate_8d(self):
        for rec in self:
            ca = self.env['quality.corrective.action'].create({
                'origin_type': 'devolucion',
                'origin_description': _(
                    'Devolución de cliente: %s\n'
                    'Tipo de defecto: %s\n'
                    'Piezas: %d\n'
                    'Motivo: %s'
                ) % (
                    rec.partner_id.name,
                    dict(rec._fields['defect_type'].selection).get(rec.defect_type, ''),
                    rec.defect_pieces,
                    rec.return_reason,
                ),
                'origin_return_id': rec.id,
                'responsible_id': self.env.user.id,
            })
            rec.corrective_action_id = ca.id
            rec.state = 'en_8d'
            rec.message_post(
                body=_('8D generado: %s') % ca.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_close(self):
        for rec in self:
            rec.state = 'cerrada'
            rec.message_post(
                body=_('Devolución cerrada por %s') % self.env.user.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_no_proceed(self):
        for rec in self:
            rec.state = 'no_procede'
            rec.message_post(
                body=_('Devolución marcada como NO PROCEDE.'),
                subtype_xmlid='mail.mt_comment',
            )

    def action_print_customer_return(self):
        return self.env.ref(
            'quality_management.action_report_customer_return'
        ).report_action(self)
