# -*- coding: utf-8 -*-
from odoo import models, fields


class QualityWorkTeam(models.Model):
    _name = "quality.work.team"
    _description = "Equipo de Trabajo (8D)"

    corrective_id = fields.Many2one("quality.corrective.action", required=True,
                                    ondelete="cascade", index=True)
    user_id = fields.Many2one("res.users", "Miembro", required=True)
    role = fields.Char("Rol en el Equipo")
    notify_progress = fields.Boolean("Notificar Avances", default=True)
