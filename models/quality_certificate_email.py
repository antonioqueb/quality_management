# -*- coding: utf-8 -*-
"""
Certificados:
- Adjuntar PDF generado al correo automáticamente.
- Registrar bitácora de envíos.
- Marcar fecha de envío real.
"""
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64


class QualityCertificateEmail(models.Model):
    _inherit = "quality.certificate"

    date_sent = fields.Datetime("Fecha de Envío Real", readonly=True, copy=False)
    sent_by = fields.Many2one("res.users", "Enviado por", readonly=True, copy=False)
    email_log_ids = fields.One2many(
        "quality.certificate.email.log", "certificate_id",
        string="Bitácora de Envíos")

    def _generate_certificate_attachment(self):
        self.ensure_one()
        report = self.env.ref(
            "quality_management.action_report_quality_certificate")
        pdf_content, _content_type = report._render_qweb_pdf(
            "quality_management.report_quality_certificate_document",
            res_ids=[self.id])
        filename = "Certificado_%s.pdf" % (self.name or "").replace("/", "-")
        attachment = self.env["ir.attachment"].create({
            "name": filename,
            "type": "binary",
            "datas": base64.b64encode(pdf_content),
            "res_model": "quality.certificate",
            "res_id": self.id,
            "mimetype": "application/pdf",
        })
        # Guardar también en report_pdf
        self.write({
            "report_pdf": base64.b64encode(pdf_content),
            "report_pdf_name": filename,
        })
        return attachment

    def action_send_email(self):
        """Override: adjunta PDF generado y precarga template."""
        self.ensure_one()
        if self.state == "borrador":
            raise UserError(_(
                "Genere primero el certificado antes de enviarlo."))

        attachment = self._generate_certificate_attachment()
        template = self.env.ref(
            "quality_management.email_template_quality_certificate",
            raise_if_not_found=False)
        compose = self.env.ref("mail.email_compose_message_wizard_form")
        ctx = {
            "default_model": "quality.certificate",
            "default_res_ids": self.ids,
            "default_template_id": template.id if template else False,
            "default_composition_mode": "comment",
            "default_attachment_ids": [(6, 0, [attachment.id])],
            "mark_so_as_sent": True,
            "force_email": True,
        }
        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(compose.id, "form")],
            "target": "new",
            "context": ctx,
        }

    def action_mark_sent(self):
        for rec in self:
            rec.state = "enviado"
            rec.date_sent = fields.Datetime.now()
            rec.sent_by = self.env.user
            self.env["quality.certificate.email.log"].create({
                "certificate_id": rec.id,
                "user_id": self.env.user.id,
                "recipient_email": rec.partner_id.email or "",
                "notes": _("Marcado como enviado manualmente."),
            })

    def message_post(self, **kwargs):
        """Detectar envíos vía mail.compose para registrar bitácora y fecha."""
        msg = super().message_post(**kwargs)
        try:
            if (kwargs.get("subtype_xmlid") == "mail.mt_comment"
                    and kwargs.get("partner_ids")
                    and self.state in ("generado", "enviado")):
                if not self.date_sent:
                    self.write({
                        "date_sent": fields.Datetime.now(),
                        "sent_by": self.env.user.id,
                        "state": "enviado",
                    })
                self.env["quality.certificate.email.log"].create({
                    "certificate_id": self.id,
                    "user_id": self.env.user.id,
                    "recipient_email": self.partner_id.email or "",
                    "message_id": msg.id if msg else False,
                    "notes": _("Envío registrado vía mensajería."),
                })
        except Exception:
            # Nunca romper el envío por la bitácora
            pass
        return msg


class QualityCertificateEmailLog(models.Model):
    _name = "quality.certificate.email.log"
    _description = "Bitácora de Envío de Certificados"
    _order = "date desc, id desc"

    certificate_id = fields.Many2one(
        "quality.certificate", required=True, ondelete="cascade", index=True)
    date = fields.Datetime("Fecha", default=fields.Datetime.now, readonly=True)
    user_id = fields.Many2one("res.users", "Enviado por")
    recipient_email = fields.Char("Destinatario")
    message_id = fields.Many2one("mail.message", "Mensaje", ondelete="set null")
    notes = fields.Text("Notas")
