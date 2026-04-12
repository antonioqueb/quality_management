from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import timedelta


class QualitySampleRelease(models.Model):
    _name = 'quality.sample.release'
    _description = 'Liberación de Muestras'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_requested desc, id desc'

    name = fields.Char(
        'Referencia', required=True, readonly=True,
        default='Nuevo', copy=False
    )
    project_task_id = fields.Many2one(
        'project.task', 'Tarea de Proyecto',
        required=True, tracking=True,
        help='Tarea del proyecto Muestras & Prototipos'
    )
    product_id = fields.Many2one(
        'product.product', 'Producto/Muestra',
        required=True, tracking=True
    )
    requested_by = fields.Many2one(
        'res.users', 'Solicitante (Diseño)',
        required=True, default=lambda self: self.env.user,
        tracking=True
    )
    inspector_id = fields.Many2one(
        'res.users', 'Inspector de Calidad',
        tracking=True
    )
    date_requested = fields.Date(
        'Fecha de Solicitud', required=True,
        default=fields.Date.context_today
    )
    date_inspected = fields.Date('Fecha de Inspección', tracking=True)
    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('en_inspeccion', 'En Inspección'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
    ], string='Estado', default='borrador', required=True,
        tracking=True, copy=False)
    inspection_line_ids = fields.One2many(
        'quality.inspection.line', 'sample_release_id',
        string='Atributos Inspeccionados'
    )
    notes = fields.Html('Observaciones')
    company_id = fields.Many2one(
        'res.company', 'Compañía',
        default=lambda self: self.env.company
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'quality.sample.release') or 'Nuevo'
        return super().create(vals_list)

    def action_submit_inspection(self):
        """Enviar a inspección - genera actividad para Calidad."""
        for rec in self:
            rec.state = 'en_inspeccion'
            # Crear actividad programada para inspectores de calidad
            quality_users = self.env.ref(
                'quality_management.group_quality_inspector'
            ).users
            if rec.inspector_id:
                quality_users = rec.inspector_id
            for user in quality_users:
                rec.activity_schedule(
                    'mail.mail_activity_data_todo',
                    date_deadline=fields.Date.today() + timedelta(days=2),
                    summary=_('Inspección de muestra: %s') % rec.name,
                    user_id=user.id,
                )
            rec.message_post(
                body=_('Solicitud de inspección enviada por %s') % rec.requested_by.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_accept(self):
        """Liberar muestra - ACEPTADO."""
        for rec in self:
            # Validar que todos los atributos cumplen
            if rec.inspection_line_ids:
                failing = rec.inspection_line_ids.filtered(
                    lambda l: l.result == 'no_cumple'
                )
                if failing:
                    raise UserError(_(
                        'No se puede liberar: hay %d atributo(s) que no cumplen.'
                    ) % len(failing))
            rec.state = 'aceptado'
            rec.date_inspected = fields.Date.today()
            rec.activity_feedback(
                ['mail.mail_activity_data_todo'],
                feedback=_('Muestra aceptada')
            )
            rec.message_post(
                body=_('✅ Muestra ACEPTADA y liberada por %s') % self.env.user.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_reject(self):
        """Rechazar muestra."""
        for rec in self:
            rec.state = 'rechazado'
            rec.date_inspected = fields.Date.today()
            rec.activity_feedback(
                ['mail.mail_activity_data_todo'],
                feedback=_('Muestra rechazada')
            )
            rec.message_post(
                body=_('❌ Muestra RECHAZADA por %s. Se notifica a Diseño para corrección.') % self.env.user.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_reset_draft(self):
        """Regresar a borrador."""
        for rec in self:
            rec.state = 'borrador'
