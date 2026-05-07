# -*- coding: utf-8 -*-
"""
Mejoras a 8D / acciones correctivas:
- Si origen = devolución/reclamación → responsable inicial = Ventas.
- Retorno de tarimas en días hábiles (lunes-viernes).
- Bloqueos finales más estrictos al cerrar.
"""
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import timedelta


def _business_days_between(d1, d2):
    """Días hábiles entre dos fechas (lunes=0 .. viernes=4)."""
    if not d1 or not d2:
        return 0
    if d2 < d1:
        d1, d2 = d2, d1
    days = 0
    cur = d1
    while cur <= d2:
        if cur.weekday() < 5:
            days += 1
        cur += timedelta(days=1)
    return days


class QualityCorrectiveActionExtra(models.Model):
    _inherit = "quality.corrective.action"

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            if rec.origin_type in ("devolucion", "reclamacion") and rec.origin_return_id:
                # Si hay vendedor en la SO original, asignarlo
                so = rec.origin_return_id.sale_order_id
                if so and so.user_id and rec.responsible_id != so.user_id:
                    rec.responsible_id = so.user_id
                    rec.message_post(
                        body=_("Responsable inicial reasignado a Ventas: %s")
                        % so.user_id.name,
                        subtype_xmlid="mail.mt_comment")
        return records


class QualityCustomerReturnExtra(models.Model):
    _inherit = "quality.customer.return"

    pallet_return_business_days = fields.Integer(
        "Días Hábiles para Retorno de Tarimas",
        compute="_compute_pallet_return_business_days", store=True)
    pallet_alert_15_business = fields.Boolean(
        "Alerta: >15 días hábiles",
        compute="_compute_pallet_return_business_days", store=True)

    @api.depends("pallet_return_date", "date_received", "pallets_returned")
    def _compute_pallet_return_business_days(self):
        for rec in self:
            if (rec.pallets_returned and rec.pallet_return_date
                    and rec.date_received):
                d = _business_days_between(rec.date_received, rec.pallet_return_date)
                rec.pallet_return_business_days = d
                rec.pallet_alert_15_business = d > 15
            else:
                rec.pallet_return_business_days = 0
                rec.pallet_alert_15_business = False

    def write(self, vals):
        """Bloquear guardado si falta formato de reclamación cuando ya no es borrador."""
        for rec in self:
            target_state = vals.get("state", rec.state)
            if target_state not in ("borrador", "no_procede"):
                claim_pdf = vals.get("claim_format_pdf", rec.claim_format_pdf)
                if not claim_pdf:
                    raise UserError(_(
                        "No se puede guardar la devolución '%s' sin el "
                        "Formato de Reclamación (PDF)."
                    ) % (rec.name or "Nueva"))
        return super().write(vals)
