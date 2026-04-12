from odoo import models, fields, api, _
from datetime import timedelta


class QualityDrawingRelease(models.Model):
    _name = 'quality.drawing.release'
    _description = 'Liberación de Planos'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_requested desc, id desc'

    name = fields.Char(
        'Referencia', required=True, readonly=True,
        default='Nuevo', copy=False
    )
    partner_id = fields.Many2one(
        'res.partner', 'Cliente', required=True, tracking=True
    )
    sale_order_id = fields.Many2one(
        'sale.order', 'Orden de Venta', tracking=True
    )
    drawing_attachment_ids = fields.Many2many(
        'ir.attachment', 'quality_drawing_attachment_rel',
        'drawing_id', 'attachment_id',
        string='Plano y Cotización/Dibujo', required=True
    )
    # PDF principal para preview embebido
    drawing_pdf = fields.Binary('Plano Principal (PDF)', attachment=True)
    drawing_pdf_name = fields.Char('Nombre del Plano')
    requested_by = fields.Many2one(
        'res.users', 'Solicitante (Ventas)',
        required=True, default=lambda self: self.env.user,
        tracking=True
    )
    inspector_id = fields.Many2one(
        'res.users', 'Inspector de Calidad', tracking=True
    )
    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('en_revision', 'En Revisión'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
    ], string='Estado', default='borrador', required=True,
        tracking=True, copy=False)
    rejection_reason = fields.Text('Motivo de Rechazo')
    date_requested = fields.Date(
        'Fecha de Solicitud', required=True,
        default=fields.Date.context_today
    )
    date_released = fields.Date('Fecha de Liberación')
    company_id = fields.Many2one(
        'res.company', 'Compañía',
        default=lambda self: self.env.company
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'quality.drawing.release') or 'Nuevo'
        return super().create(vals_list)

    def action_submit_review(self):
        for rec in self:
            rec.state = 'en_revision'
            quality_users = self.env.ref(
                'quality_management.group_quality_inspector'
            ).users
            if rec.inspector_id:
                quality_users = rec.inspector_id
            for user in quality_users:
                rec.activity_schedule(
                    'mail.mail_activity_data_todo',
                    date_deadline=fields.Date.today() + timedelta(days=3),
                    summary=_('Revisión de plano: %s') % rec.name,
                    user_id=user.id,
                )
            rec.message_post(
                body=_('Solicitud de revisión de plano enviada por %s') % rec.requested_by.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_accept(self):
        for rec in self:
            rec.state = 'aceptado'
            rec.date_released = fields.Date.today()
            rec.activity_feedback(
                ['mail.mail_activity_data_todo'],
                feedback=_('Plano liberado')
            )
            rec.message_post(
                body=_('✅ Plano LIBERADO por %s') % self.env.user.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_reject(self):
        for rec in self:
            if not rec.rejection_reason:
                raise models.ValidationError(
                    _('Debe capturar el motivo de rechazo.')
                )
            rec.state = 'rechazado'
            rec.activity_feedback(
                ['mail.mail_activity_data_todo'],
                feedback=_('Plano rechazado: %s') % rec.rejection_reason
            )
            rec.message_post(
                body=_('❌ Plano RECHAZADO por %s.\nMotivo: %s') % (
                    self.env.user.name, rec.rejection_reason),
                subtype_xmlid='mail.mt_comment',
            )

    def action_reset_draft(self):
        for rec in self:
            rec.state = 'borrador'
            rec.rejection_reason = False

    def action_print_drawing_release(self):
        return self.env.ref(
            'quality_management.action_report_drawing_release'
        ).report_action(self)
