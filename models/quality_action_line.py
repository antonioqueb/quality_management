from odoo import models, fields, api


class QualityActionLine(models.Model):
    _name = 'quality.action.line'
    _description = 'Línea de Acción Correctiva'
    _order = 'date_due, id'

    corrective_id = fields.Many2one(
        'quality.corrective.action', 'Acción Correctiva',
        required=True, ondelete='cascade'
    )
    description = fields.Text('Descripción de la Acción', required=True)
    responsible_id = fields.Many2one(
        'res.users', 'Responsable', required=True
    )
    date_due = fields.Date('Fecha de Cumplimiento', required=True)
    date_completed = fields.Date('Fecha de Cumplimiento Real')
    evidence_ids = fields.Many2many(
        'ir.attachment', 'quality_action_evidence_rel',
        'action_line_id', 'attachment_id',
        string='Evidencia'
    )
    state = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completada', 'Completada'),
        ('vencida', 'Vencida'),
    ], string='Estado', default='pendiente', required=True)
    delay_days = fields.Integer(
        'Días de Atraso', compute='_compute_delay_days', store=True
    )
    notes = fields.Text('Notas')

    @api.depends('date_due', 'state')
    def _compute_delay_days(self):
        today = fields.Date.today()
        for line in self:
            if line.date_due and line.state in ('pendiente', 'en_proceso', 'vencida'):
                delta = (today - line.date_due).days
                line.delay_days = max(0, delta)
            else:
                line.delay_days = 0

    def action_start(self):
        for rec in self:
            rec.state = 'en_proceso'

    def action_complete(self):
        for rec in self:
            rec.state = 'completada'
            rec.date_completed = fields.Date.today()

    def action_reopen(self):
        for rec in self:
            rec.state = 'en_proceso'
            rec.date_completed = False
