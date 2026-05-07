# -*- coding: utf-8 -*-
"""
Ciclo completo: Retenido → Corrección por Producción → Hecho → Reinspección.
Se monta sobre el state existente sin modificarlo, usando un sub-estado.
"""
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import timedelta


class QualityInspectionRetention(models.Model):
    _inherit = "quality.inspection"

    retention_state = fields.Selection([
        ("none", "Sin retención"),
        ("retenido", "Retenido — esperando corrección"),
        ("en_correccion", "En corrección por Producción"),
        ("correccion_hecha", "Corrección hecha — pendiente reinspección"),
        ("reinspeccion", "Reinspección en curso"),
        ("liberado_post_retencion", "Liberado tras reinspección"),
        ("rechazado_post_retencion", "Rechazado tras reinspección"),
    ], default="none", required=True, tracking=True, copy=False,
       string="Sub-estado de Retención")

    retention_log_ids = fields.One2many(
        "quality.inspection.retention.log", "inspection_id",
        string="Bitácora de Retención")
    retention_correction_notes = fields.Html(
        "Notas de Corrección (Producción)")
    retention_correction_done_by = fields.Many2one(
        "res.users", "Producción marcó hecho", readonly=True)
    retention_correction_done_date = fields.Datetime(
        "Fecha Hecho", readonly=True)

    def _log_retention(self, msg):
        for rec in self:
            self.env["quality.inspection.retention.log"].create({
                "inspection_id": rec.id,
                "user_id": self.env.user.id,
                "description": msg,
                "retention_state_after": rec.retention_state,
            })

    # ---- Override: cuando se retiene, marcar sub-estado --------------------
    def action_retain(self):
        res = super().action_retain()
        for rec in self:
            rec.retention_state = "retenido"
            rec._log_retention(_("Producto retenido por Calidad."))
        return res

    # ---- Producción acepta corregir ----------------------------------------
    def action_accept_correction(self):
        for rec in self:
            if rec.state != "retenido" or rec.retention_state not in (
                    "retenido", "en_correccion"):
                raise UserError(_(
                    "Solo se puede aceptar corrección desde una inspección retenida."))
            rec.retention_state = "en_correccion"
            rec._log_retention(_("Producción acepta corregir el producto."))

    # ---- Producción / Supervisor marca corrección como hecha ---------------
    def action_correction_done(self):
        for rec in self:
            if rec.retention_state not in ("retenido", "en_correccion"):
                raise UserError(_(
                    "La inspección no está en estado de corrección."))
            rec.retention_state = "correccion_hecha"
            rec.retention_correction_done_by = self.env.user
            rec.retention_correction_done_date = fields.Datetime.now()
            rec._log_retention(
                _("Supervisor/Producción marca corrección como HECHA."))

            # Avisar a Calidad
            inspector = rec.inspector_id
            if inspector:
                rec.activity_schedule(
                    "mail.mail_activity_data_todo",
                    date_deadline=fields.Date.today() + timedelta(days=1),
                    summary=_("Reinspeccionar producto: %s") % rec.name,
                    user_id=inspector.id)
            partners = []
            if inspector and inspector.partner_id:
                partners.append(inspector.partner_id.id)
            rec.message_post(
                body=_("✋ Producción marcó corrección hecha. Calidad debe REINSPECCIONAR."),
                partner_ids=partners,
                subtype_xmlid="mail.mt_comment")

    # ---- Calidad inicia reinspección ---------------------------------------
    def action_start_reinspection(self):
        for rec in self:
            if rec.retention_state != "correccion_hecha":
                raise UserError(_(
                    "No hay corrección pendiente de reinspección."))
            rec.retention_state = "reinspeccion"
            rec.state = "en_proceso"  # reabrir captura
            rec._log_retention(_("Calidad inicia reinspección."))

    # ---- Calidad acepta tras reinspección ----------------------------------
    def action_accept_after_retention(self):
        for rec in self:
            if rec.retention_state != "reinspeccion":
                raise UserError(_(
                    "Debe iniciar la reinspección primero."))
            rec._full_quality_validation_hardening()
            rec.state = "aceptado"
            rec.retention_state = "liberado_post_retencion"
            rec._log_retention(_("Aceptado tras reinspección."))

    # ---- Calidad rechaza tras reinspección ---------------------------------
    def action_reject_after_retention(self):
        for rec in self:
            if rec.retention_state != "reinspeccion":
                raise UserError(_(
                    "Debe iniciar la reinspección primero."))
            rec.state = "rechazado"
            rec.retention_state = "rechazado_post_retencion"
            rec._log_retention(_("Rechazado tras reinspección."))


class QualityInspectionRetentionLog(models.Model):
    _name = "quality.inspection.retention.log"
    _description = "Bitácora de Retención"
    _order = "date desc, id desc"

    inspection_id = fields.Many2one(
        "quality.inspection", required=True, ondelete="cascade", index=True)
    date = fields.Datetime(default=fields.Datetime.now, readonly=True)
    user_id = fields.Many2one("res.users", "Usuario")
    description = fields.Text("Descripción", required=True)
    retention_state_after = fields.Char("Sub-estado tras evento")
