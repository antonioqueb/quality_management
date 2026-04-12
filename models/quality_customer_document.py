from odoo import models, fields, api, _
from datetime import timedelta


class QualityCustomerDocument(models.Model):
    _name = 'quality.customer.document'
    _description = 'Documento Solicitado por Cliente'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_requested desc, id desc'

    name = fields.Char(
        'Referencia', required=True, readonly=True,
        default='Nuevo', copy=False
    )
    partner_id = fields.Many2one(
        'res.partner', 'Cliente Solicitante',
        required=True, tracking=True
    )
    document_type = fields.Selection([
        ('rohs', 'RoHS'),
        ('psw', 'PSW'),
        ('ppap', 'PPAP'),
        ('apariencia', 'Apariencia'),
        ('pfmea', 'PFMEA'),
        ('diagrama_flujo', 'Diagrama de Flujo'),
        ('especificacion_empaque', 'Especificación de Empaque'),
        ('carta_garantia', 'Carta Garantía'),
        ('otro', 'Otro'),
    ], string='Tipo de Documento', required=True, tracking=True)
    description = fields.Text('Descripción Adicional')
    requires_dimensions = fields.Boolean(
        'Implica Mediciones Dimensionales', required=True,
        tracking=True
    )
    client_format_ids = fields.Many2many(
        'ir.attachment', 'quality_doc_client_format_rel',
        'document_id', 'attachment_id',
        string='Formatos del Cliente'
    )
    result_document_ids = fields.Many2many(
        'ir.attachment', 'quality_doc_result_rel',
        'document_id', 'attachment_id',
        string='Documentos Generados'
    )
    requested_by = fields.Many2one(
        'res.users', 'Solicitante (Ventas)',
        required=True, default=lambda self: self.env.user,
        tracking=True
    )
    responsible_id = fields.Many2one(
        'res.users', 'Responsable en Calidad',
        required=True, tracking=True
    )
    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
        ('enviado', 'Enviado'),
    ], string='Estado', default='borrador', required=True,
        tracking=True, copy=False)
    date_requested = fields.Date(
        'Fecha de Solicitud', required=True,
        default=fields.Date.context_today
    )
    date_due = fields.Date(
        'Fecha Límite', compute='_compute_date_due',
        store=True, readonly=False
    )
    date_completed = fields.Date('Fecha de Entrega Real')
    company_id = fields.Many2one(
        'res.company', 'Compañía',
        default=lambda self: self.env.company
    )

    @api.depends('date_requested', 'requires_dimensions')
    def _compute_date_due(self):
        for rec in self:
            if rec.date_requested:
                days = 7 if rec.requires_dimensions else 5
                rec.date_due = rec.date_requested + timedelta(days=days)
            else:
                rec.date_due = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'quality.customer.document') or 'Nuevo'
        return super().create(vals_list)

    def action_start(self):
        for rec in self:
            rec.state = 'en_proceso'
            rec.activity_schedule(
                'mail.mail_activity_data_todo',
                date_deadline=rec.date_due,
                summary=_('Generar documento de calidad: %s - %s') % (
                    rec.name,
                    dict(rec._fields['document_type'].selection).get(
                        rec.document_type, ''
                    ),
                ),
                user_id=rec.responsible_id.id,
            )

    def action_complete(self):
        for rec in self:
            rec.state = 'completado'
            rec.date_completed = fields.Date.today()
            rec.activity_feedback(
                ['mail.mail_activity_data_todo'],
                feedback=_('Documento completado')
            )
            # Notificar a Ventas
            rec.message_post(
                body=_(
                    '✅ Documento completado por Calidad. '
                    'Ventas: proceder a enviar al cliente %s.'
                ) % rec.partner_id.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_send(self):
        for rec in self:
            rec.state = 'enviado'
            rec.message_post(
                body=_('Documento enviado al cliente %s') % rec.partner_id.name,
                subtype_xmlid='mail.mt_comment',
            )
