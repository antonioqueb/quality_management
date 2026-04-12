from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import timedelta


class QualityCorrectiveAction(models.Model):
    _name = 'quality.corrective.action'
    _description = 'Acción Correctiva/Preventiva'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_opened desc, id desc'

    name = fields.Char(
        'Referencia', required=True, readonly=True,
        default='Nuevo', copy=False
    )
    origin_type = fields.Selection([
        ('inspeccion', 'Inspección'),
        ('auditoria_interna', 'Auditoría Interna'),
        ('auditoria_externa', 'Auditoría Externa'),
        ('devolucion', 'Devolución'),
        ('otro', 'Otro'),
    ], string='Tipo de Origen', required=True, tracking=True)
    origin_description = fields.Text(
        'Descripción del Incumplimiento', required=True
    )
    origin_inspection_id = fields.Many2one(
        'quality.inspection', 'Inspección Origen'
    )
    origin_return_id = fields.Many2one(
        'quality.customer.return', 'Devolución Origen'
    )
    responsible_id = fields.Many2one(
        'res.users', 'Responsable General',
        required=True, tracking=True
    )
    action_line_ids = fields.One2many(
        'quality.action.line', 'corrective_id',
        string='Acciones Específicas'
    )
    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('abierta', 'Abierta'),
        ('en_proceso', 'En Proceso'),
        ('cerrada', 'Cerrada'),
        ('no_procede', 'No Procede'),
    ], string='Estado', default='borrador', required=True,
        tracking=True, copy=False)
    date_opened = fields.Date(
        'Fecha de Apertura', required=True,
        default=fields.Date.context_today
    )
    date_closed = fields.Date('Fecha de Cierre', tracking=True)
    action_count = fields.Integer(
        'Total de Acciones', compute='_compute_action_stats'
    )
    action_completed_count = fields.Integer(
        'Acciones Completadas', compute='_compute_action_stats'
    )
    action_overdue_count = fields.Integer(
        'Acciones Vencidas', compute='_compute_action_stats'
    )
    progress = fields.Float(
        'Progreso (%)', compute='_compute_action_stats'
    )
    company_id = fields.Many2one(
        'res.company', 'Compañía',
        default=lambda self: self.env.company
    )

    @api.depends('action_line_ids', 'action_line_ids.state')
    def _compute_action_stats(self):
        for rec in self:
            lines = rec.action_line_ids
            rec.action_count = len(lines)
            rec.action_completed_count = len(
                lines.filtered(lambda l: l.state == 'completada')
            )
            rec.action_overdue_count = len(
                lines.filtered(lambda l: l.state == 'vencida')
            )
            rec.progress = (
                (rec.action_completed_count / rec.action_count * 100)
                if rec.action_count else 0.0
            )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'quality.corrective.action') or 'Nuevo'
        return super().create(vals_list)

    def action_open(self):
        for rec in self:
            rec.state = 'abierta'
            rec.message_post(
                body=_('Acción correctiva abierta por %s') % self.env.user.name,
                subtype_xmlid='mail.mt_comment',
            )
            # Notificar al responsable
            rec.activity_schedule(
                'mail.mail_activity_data_todo',
                date_deadline=fields.Date.today() + timedelta(days=1),
                summary=_('Acción correctiva asignada: %s') % rec.name,
                user_id=rec.responsible_id.id,
            )

    def action_in_progress(self):
        for rec in self:
            rec.state = 'en_proceso'

    def action_close(self):
        for rec in self:
            pending = rec.action_line_ids.filtered(
                lambda l: l.state not in ('completada',)
            )
            if pending:
                raise UserError(_(
                    'No se puede cerrar: hay %d acción(es) sin completar.'
                ) % len(pending))
            rec.state = 'cerrada'
            rec.date_closed = fields.Date.today()
            rec.activity_feedback(
                ['mail.mail_activity_data_todo'],
                feedback=_('Acción correctiva cerrada')
            )
            rec.message_post(
                body=_('✅ Acción correctiva CERRADA por %s') % self.env.user.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_no_proceed(self):
        for rec in self:
            rec.state = 'no_procede'
            rec.date_closed = fields.Date.today()
            rec.message_post(
                body=_('Acción correctiva marcada como NO PROCEDE por %s') % self.env.user.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_reopen(self):
        for rec in self:
            rec.state = 'en_proceso'
            rec.date_closed = False

    @api.model
    def _cron_check_overdue_actions(self):
        """Cron: detectar acciones vencidas y notificar."""
        today = fields.Date.today()
        overdue_lines = self.env['quality.action.line'].search([
            ('state', 'in', ('pendiente', 'en_proceso')),
            ('date_due', '<', today),
        ])
        for line in overdue_lines:
            line.state = 'vencida'
            days = (today - line.date_due).days
            line.delay_days = days
            line.corrective_id.message_post(
                body=_(
                    '⚠️ Acción vencida: "%s" - Responsable: %s - '
                    'Días de atraso: %d'
                ) % (line.description[:80], line.responsible_id.name, days),
                subtype_xmlid='mail.mt_comment',
            )
            # Actividad para el responsable
            line.corrective_id.activity_schedule(
                'mail.mail_activity_data_todo',
                date_deadline=today,
                summary=_(
                    'Acción vencida (%d días): %s'
                ) % (days, line.description[:50]),
                user_id=line.responsible_id.id,
            )
