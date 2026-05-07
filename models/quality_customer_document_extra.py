# -*- coding: utf-8 -*-
"""
Bloqueos adicionales para Documentos de Cliente:
- write() bloqueado si no hay descripción ni documento cargado y se intenta
  avanzar de borrador.
- Fecha de entrega real al pasar a 'enviado'.
- Actividades automáticas para Calidad al crear.
- Notificación a Ventas al completar.
"""
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import timedelta


class QualityCustomerDocumentExtra(models.Model):
    _inherit = "quality.customer.document"

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            if rec.responsible_id:
                rec.activity_schedule(
                    "mail.mail_activity_data_todo",
                    date_deadline=rec.date_due or (
                        fields.Date.today() + timedelta(days=5)),
                    summary=_("Atender solicitud de documento: %s") % rec.name,
                    user_id=rec.responsible_id.id)
        return records

    def write(self, vals):
        """Bloquea avance sin descripción ni documento."""
        for rec in self:
            target_state = vals.get("state", rec.state)
            if target_state in ("en_proceso", "completado", "enviado"):
                desc = vals.get("description", rec.description)
                if not desc or not (desc or "").strip():
                    raise UserError(_(
                        "No se puede avanzar el documento '%s' sin descripción."
                    ) % (rec.name or "Nuevo"))
                has_doc = (
                    vals.get("main_pdf", rec.main_pdf)
                    or vals.get("main_image", rec.main_image)
                    or rec.result_document_ids
                    or rec.client_format_ids)
                if not has_doc:
                    raise UserError(_(
                        "No se puede avanzar '%s' sin al menos un documento "
                        "cargado (PDF, imagen o adjunto)."
                    ) % (rec.name or "Nuevo"))
        return super().write(vals)

    def action_complete(self):
        res = super().action_complete()
        for rec in self:
            # Notificar a Ventas (solicitante)
            if rec.requested_by and rec.requested_by.partner_id:
                rec.message_post(
                    body=_("📄 Documento listo para envío al cliente."),
                    partner_ids=[rec.requested_by.partner_id.id],
                    subtype_xmlid="mail.mt_comment")
        return res

    def action_send(self):
        res = super().action_send()
        for rec in self:
            # Fecha de entrega real
            if not rec.date_completed:
                rec.date_completed = fields.Date.today()
        return res
