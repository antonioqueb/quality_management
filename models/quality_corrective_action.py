# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class QualityCorrectiveAction(models.Model):
    _name = "quality.corrective.action"
    _description = "Acción Correctiva/Preventiva (8D)"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_opened desc, id desc"

    name = fields.Char(
        "Referencia",
        required=True,
        readonly=True,
        default="Nuevo",
        copy=False,
    )

    origin_type = fields.Selection(
        [
            ("inspeccion", "Inspección"),
            ("auditoria_interna", "Auditoría Interna"),
            ("auditoria_externa", "Auditoría Externa"),
            ("devolucion", "Devolución"),
            ("reclamacion", "Reclamación"),
            ("otro", "Otro"),
        ],
        required=True,
        tracking=True,
    )

    defect_type = fields.Selection(
        [
            ("dimensional", "Dimensional"),
            ("apariencia", "Apariencia"),
            ("funcional", "Funcional"),
            ("afecta_funcionalidad", "Afecta Funcionalidad"),
            ("empaque", "Empaque"),
            ("otro", "Otro"),
        ],
        string="Tipo de Defecto",
    )
    defect_other_desc = fields.Char(
        "Descripción de Defecto (Otro)",
        help="Aplica cuando Tipo de Defecto = OTRO",
    )

    origin_description = fields.Text("Descripción del Incumplimiento", required=True)
    origin_inspection_id = fields.Many2one("quality.inspection", "Inspección Origen")
    origin_return_id = fields.Many2one("quality.customer.return", "Devolución Origen")

    responsible_id = fields.Many2one(
        "res.users",
        "Responsable General",
        required=True,
        tracking=True,
    )

    work_team_ids = fields.One2many(
        "quality.work.team",
        "corrective_id",
        string="Equipo de Trabajo",
    )
    action_line_ids = fields.One2many(
        "quality.action.line",
        "corrective_id",
        string="Acciones Específicas",
    )

    containment_actions = fields.Text(
        "D3 - Acciones de Contención",
        help="Acciones inmediatas para contener el problema y proteger al cliente.",
    )
    containment_date = fields.Date("Fecha de Contención")
    containment_responsible_id = fields.Many2one("res.users", "Responsable Contención")

    prevention_actions = fields.Text(
        "D7 - Acciones Preventivas Sistémicas",
        help="Cambios al sistema para evitar recurrencia.",
    )
    prevention_implemented_date = fields.Date("Fecha de Implementación de Prevención")
    prevention_responsible_id = fields.Many2one("res.users", "Responsable Prevención")

    team_recognition = fields.Text("D8 - Reconocimiento al Equipo")
    d8_closing_date = fields.Date("Fecha de Cierre D8")

    why_ids = fields.One2many("quality.5why", "corrective_id", string="5 Por qué")
    ishikawa_ids = fields.One2many(
        "quality.ishikawa",
        "corrective_id",
        string="Diagrama de Ishikawa",
    )

    state = fields.Selection(
        [
            ("borrador", "Borrador"),
            ("evaluacion_calidad", "Evaluación Calidad"),
            ("abierta", "Abierta"),
            ("en_proceso", "En Proceso"),
            ("cerrada", "Cerrada"),
            ("no_procede", "No Procede"),
        ],
        default="borrador",
        required=True,
        tracking=True,
        copy=False,
    )

    no_procede_reason = fields.Text("Motivo No Procede")
    quality_evaluated_by = fields.Many2one("res.users", "Calidad Evaluó", readonly=True)
    quality_evaluated_date = fields.Datetime("Fecha Evaluación Calidad", readonly=True)

    date_opened = fields.Date(
        "Fecha de Apertura",
        required=True,
        default=fields.Date.context_today,
    )
    date_closed = fields.Date(
        "Fecha de Cierre",
        tracking=True,
        compute="_compute_date_closed",
        store=True,
        readonly=False,
    )

    action_count = fields.Integer("Acciones", compute="_compute_action_stats")
    action_completed_count = fields.Integer("Completadas", compute="_compute_action_stats")
    action_overdue_count = fields.Integer("Vencidas", compute="_compute_action_stats")
    progress = fields.Float("Avance", compute="_compute_action_stats")

    company_id = fields.Many2one(
        "res.company",
        "Compañía",
        default=lambda s: s.env.company,
    )

    @api.depends("action_line_ids", "action_line_ids.state", "action_line_ids.evidence_ids")
    def _compute_action_stats(self):
        for rec in self:
            lines = rec.action_line_ids
            rec.action_count = len(lines)
            rec.action_completed_count = len(lines.filtered(lambda l: l.state == "completada"))
            rec.action_overdue_count = len(lines.filtered(lambda l: l.state == "vencida"))
            rec.progress = (
                rec.action_completed_count / rec.action_count * 100
                if rec.action_count
                else 0.0
            )

    @api.depends("state", "action_line_ids.date_due", "action_line_ids.state")
    def _compute_date_closed(self):
        """Fecha cierre = fecha más lejana de las acciones."""
        for rec in self:
            # FOLIO-QM-ODOO18-007: todo compute debe asignar valor a cada registro.
            if rec.state == "cerrada":
                dates = [d for d in rec.action_line_ids.mapped("date_due") if d]
                rec.date_closed = max(dates) if dates else (rec.date_closed or fields.Date.today())
            elif rec.state == "no_procede":
                rec.date_closed = rec.date_closed or fields.Date.today()
            else:
                rec.date_closed = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Nuevo") == "Nuevo":
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "quality.corrective.action"
                ) or "Nuevo"
        return super().create(vals_list)

    @api.constrains("defect_type", "defect_other_desc")
    def _check_other_desc(self):
        for rec in self:
            if rec.defect_type == "otro" and not rec.defect_other_desc:
                raise UserError(_("Cuando el tipo de defecto es OTRO, debe describir el defecto."))

    def _check_pestañas_completas(self):
        for rec in self:
            faltantes = []
            if not rec.work_team_ids:
                faltantes.append("D2 Equipo de Trabajo")
            if not rec.containment_actions:
                faltantes.append("D3 Contención")
            if len(rec.why_ids) < 5:
                faltantes.append("D4 5 Por qué (mínimo 5)")
            if not rec.ishikawa_ids:
                faltantes.append("D5 Ishikawa")
            if not rec.action_line_ids:
                faltantes.append("D6 Acciones")
            if not rec.prevention_actions:
                faltantes.append("D7 Prevención")
            if not rec.team_recognition:
                faltantes.append("D8 Reconocimiento")
            if faltantes:
                raise UserError(_("No se puede cerrar. Complete: %s") % ", ".join(faltantes))

    def action_evaluate_quality(self):
        for rec in self:
            rec.state = "evaluacion_calidad"
            rec.message_post(
                body=_("Enviado a Evaluación de Calidad."),
                subtype_xmlid="mail.mt_comment",
            )

    def action_quality_evaluated(self):
        for rec in self:
            if rec.state != "evaluacion_calidad":
                raise UserError(
                    _("Solo se puede marcar como evaluada cuando está en estado 'Evaluación Calidad'.")
                )
            rec.quality_evaluated_by = self.env.user
            rec.quality_evaluated_date = fields.Datetime.now()
            rec.state = "abierta"
            rec.activity_schedule(
                "mail.mail_activity_data_todo",
                date_deadline=fields.Date.today() + timedelta(days=1),
                summary=_("8D abierto: %s") % rec.name,
                user_id=rec.responsible_id.id,
            )

    def action_open(self):
        for rec in self:
            if not rec.quality_evaluated_by:
                raise UserError(_("Debe completar primero la 'Evaluación Calidad' antes de continuar al 8D."))
            rec.state = "abierta"

    def action_in_progress(self):
        for rec in self:
            rec.state = "en_proceso"

    def action_close(self):
        for rec in self:
            rec._check_pestañas_completas()
            pending = rec.action_line_ids.filtered(lambda l: l.state != "completada")
            if pending:
                raise UserError(_("No se puede cerrar: %d acción(es) sin completar.") % len(pending))
            rec.state = "cerrada"

    def action_no_proceed(self):
        for rec in self:
            if not rec.no_procede_reason:
                raise UserError(_("Capture el motivo por el que no procede la acción."))
            rec.state = "no_procede"

    def action_reopen(self):
        for rec in self:
            rec.state = "en_proceso"
            rec.date_closed = False

    def action_print_8d(self):
        return self.env.ref("quality_management.action_report_8d").report_action(self)

    @api.model
    def _cron_check_overdue_actions(self):
        today = fields.Date.today()
        overdue = self.env["quality.action.line"].search(
            [
                ("state", "in", ("pendiente", "en_proceso")),
                ("date_due", "<", today),
            ]
        )
        for line in overdue:
            line.state = "vencida"
            line.delay_days = (today - line.date_due).days
            partners = []
            for member in line.corrective_id.work_team_ids.filtered("notify_progress"):
                if member.user_id.partner_id:
                    partners.append(member.user_id.partner_id.id)
            line.corrective_id.message_post(
                body=_("Acción vencida (%d días): %s — Responsable: %s")
                % (line.delay_days, line.description[:80], line.responsible_id.name),
                partner_ids=list(set(partners)),
                subtype_xmlid="mail.mt_comment",
            )