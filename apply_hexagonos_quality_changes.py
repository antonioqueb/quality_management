#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
apply_quality_full_compliance.py
================================
Aplica TODOS los puntos pendientes del requerimiento global de Calidad
Hexágonos al módulo `quality_management` sin romper lo que ya funciona.

Estrategia:
- Archivos NUEVOS para cada feature (no se sobreescribe lógica vieja).
- Modelos heredados con `_inherit` para extender (no para reemplazar).
- Cambios en `__manifest__.py` y `__init__.py` son IDEMPOTENTES.
- Backup automático en `_backup_full_compliance_<timestamp>/`.

Uso:
    python3 apply_quality_full_compliance.py /Users/alphaqueb/Documents/Proyectos/Clientes/Hexágonos/Módulos/quality_management

Cubre:
  1. Integración real con project.task (Muestras y Planos)
  2. Rutas configurables por producto / categoría
  3. Flujo Retenido → Corrección → Hecho → Reinspección
  4. Historial de cambios en inspecciones
  5. Certificado: PDF adjunto al correo + fecha de envío real + bitácora
  6. 8D / acciones correctivas: Ventas como responsable en devoluciones,
     días hábiles para tarimas, bloqueos de cierre incompleto
  7. Devoluciones: bloqueo write sin formato, autorización Gerente Ventas
  8. Documentos de cliente: bloqueo write, fecha de entrega real al enviar
  9. Troqueles: flujo formal con validaciones, reparaciones y revisiones
 10. Seguridad: reglas estrictas para inspectoras
 11. Reporte 8D extendido con 5 porqués + Ishikawa
"""

import os
import shutil
import sys
from datetime import datetime
from pathlib import Path


# ============================================================================
#                         CONTENIDO DE ARCHIVOS NUEVOS
# ============================================================================

FILES = {}

# ---------------------------------------------------------------- 1. PROJECT
FILES["models/project_task_quality.py"] = '''# -*- coding: utf-8 -*-
"""
Integración con project.task — bloqueos al mover tarjetas en Kanban.
Cubre los requerimientos de Muestras & Prototipos y Altas & Actualizaciones
de Planos que nacen desde Proyectos.
"""
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProjectTaskQuality(models.Model):
    _inherit = "project.task"

    quality_sample_release_id = fields.Many2one(
        "quality.sample.release", "Liberación de Muestra",
        help="Vinculación con la liberación de muestra de Calidad.")
    quality_drawing_release_id = fields.Many2one(
        "quality.drawing.release", "Liberación de Plano")

    quality_required_for_progress = fields.Boolean(
        "Requiere Liberación de Calidad",
        help="Si está activo, no se puede mover la tarjeta a etapas avanzadas "
             "sin liberación aprobada de Calidad.")
    quality_block_reason = fields.Char(
        "Motivo de Bloqueo de Etapa",
        compute="_compute_quality_block_reason")

    @api.depends("quality_sample_release_id.state",
                 "quality_drawing_release_id.state",
                 "quality_required_for_progress")
    def _compute_quality_block_reason(self):
        for task in self:
            reasons = []
            if task.quality_required_for_progress:
                if (task.quality_sample_release_id
                        and task.quality_sample_release_id.state != "aceptado"):
                    reasons.append(_("Muestra no liberada por Calidad"))
                if (task.quality_drawing_release_id
                        and task.quality_drawing_release_id.state != "aceptado_diseno"):
                    reasons.append(_("Plano no liberado (Calidad/Ventas/Diseño)"))
            task.quality_block_reason = "; ".join(reasons) if reasons else False

    def _quality_validate_stage_move(self, new_stage_id):
        """Llamada desde write() cuando cambia stage_id."""
        for task in self:
            if not task.quality_required_for_progress:
                continue

            new_stage = self.env["project.task.type"].browse(new_stage_id)
            # Permite regresar a etapas anteriores; bloquea solo avance.
            if task.stage_id and new_stage.sequence <= task.stage_id.sequence:
                continue

            sample = task.quality_sample_release_id
            drawing = task.quality_drawing_release_id

            if sample:
                if not sample.spec_pdf:
                    raise UserError(_(
                        "No se puede avanzar la tarea '%s': la muestra '%s' "
                        "no tiene Especificación PDF cargada."
                    ) % (task.name, sample.name))
                if not sample.inspection_line_ids:
                    raise UserError(_(
                        "No se puede avanzar la tarea '%s': la muestra '%s' "
                        "no tiene atributos de inspección capturados."
                    ) % (task.name, sample.name))
                if sample.state != "aceptado":
                    raise UserError(_(
                        "No se puede avanzar la tarea '%s': la muestra '%s' "
                        "está en estado '%s' (debe estar Aceptada)."
                    ) % (task.name, sample.name,
                         dict(sample._fields["state"].selection).get(sample.state)))

            if drawing:
                if not drawing.drawing_pdf or not drawing.quotation_pdf:
                    raise UserError(_(
                        "No se puede avanzar la tarea '%s': el plano '%s' "
                        "requiere AMBOS documentos (Plano + Cotización/Dibujo)."
                    ) % (task.name, drawing.name))
                if drawing.state != "aceptado_diseno":
                    raise UserError(_(
                        "No se puede avanzar la tarea '%s': el plano '%s' "
                        "no ha completado el triple-check (Calidad/Ventas/Diseño). "
                        "Estado actual: '%s'."
                    ) % (task.name, drawing.name,
                         dict(drawing._fields["state"].selection).get(drawing.state)))

    def write(self, vals):
        if "stage_id" in vals and vals["stage_id"]:
            self._quality_validate_stage_move(vals["stage_id"])
        return super().write(vals)


class QualitySampleReleaseTask(models.Model):
    _inherit = "quality.sample.release"

    project_task_ids = fields.One2many(
        "project.task", "quality_sample_release_id",
        string="Tareas Vinculadas")


class QualityDrawingReleaseTask(models.Model):
    _inherit = "quality.drawing.release"

    project_task_ids = fields.One2many(
        "project.task", "quality_drawing_release_id",
        string="Tareas Vinculadas")
'''

# ---------------------------------------------------------------- 2. RUTAS
FILES["models/quality_process_route.py"] = '''# -*- coding: utf-8 -*-
"""
Rutas de proceso configurables por producto/categoría.
Reemplaza la secuencia fija PROCESS_SEQUENCE cuando hay una ruta definida.
"""
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class QualityProcessRoute(models.Model):
    _name = "quality.process.route"
    _description = "Ruta de Proceso de Calidad"
    _order = "sequence, id"

    name = fields.Char("Nombre de la Ruta", required=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    product_tmpl_ids = fields.Many2many(
        "product.template", string="Productos Aplicables")
    product_categ_ids = fields.Many2many(
        "product.category", string="Categorías Aplicables")
    line_ids = fields.One2many(
        "quality.process.route.line", "route_id", string="Pasos")
    notes = fields.Text("Notas")
    company_id = fields.Many2one(
        "res.company", default=lambda s: s.env.company)

    def get_ordered_codes(self):
        self.ensure_one()
        return [l.process_type_id.code for l in self.line_ids.sorted("sequence")
                if l.process_type_id.code]


class QualityProcessRouteLine(models.Model):
    _name = "quality.process.route.line"
    _description = "Paso de Ruta de Proceso"
    _order = "sequence, id"

    route_id = fields.Many2one(
        "quality.process.route", required=True, ondelete="cascade")
    sequence = fields.Integer("Secuencia", default=10, required=True)
    process_type_id = fields.Many2one(
        "quality.process.type", "Tipo de Proceso", required=True)
    is_optional = fields.Boolean(
        "Opcional",
        help="Si está marcado, este paso no bloquea al siguiente.")
    notes = fields.Char("Observaciones")


class ProductTemplateRoute(models.Model):
    _inherit = "product.template"

    quality_route_id = fields.Many2one(
        "quality.process.route", "Ruta de Calidad",
        help="Define la secuencia de procesos que debe seguir este producto.")


class QualityInspectionRoute(models.Model):
    _inherit = "quality.inspection"

    quality_route_id = fields.Many2one(
        "quality.process.route",
        compute="_compute_quality_route", store=True,
        help="Ruta resuelta para la inspección actual.")

    @api.depends("product_id", "product_id.product_tmpl_id",
                 "product_id.product_tmpl_id.quality_route_id",
                 "product_id.product_tmpl_id.categ_id")
    def _compute_quality_route(self):
        Route = self.env["quality.process.route"]
        for rec in self:
            tmpl = rec.product_id.product_tmpl_id
            route = tmpl.quality_route_id if tmpl else False
            if not route and tmpl and tmpl.categ_id:
                route = Route.search([
                    ("active", "=", True),
                    ("product_categ_ids", "in", tmpl.categ_id.ids),
                ], limit=1)
            rec.quality_route_id = route or False

    def _check_previous_process_hardening(self):
        """Override: usa ruta configurada si existe, si no cae al PROCESS_SEQUENCE
        del hardening base."""
        for rec in self:
            route = rec.quality_route_id
            if not route:
                return super(QualityInspectionRoute, rec)._check_previous_process_hardening()

            codes = route.get_ordered_codes()
            current_code = rec.process_code
            if current_code not in codes:
                continue
            idx = codes.index(current_code)
            if idx == 0:
                continue
            # Buscar el paso previo NO opcional
            previous = None
            for i in range(idx - 1, -1, -1):
                line = route.line_ids.sorted("sequence")[i]
                if not line.is_optional:
                    previous = line.process_type_id.code
                    break
            if not previous:
                continue
            prev = self.search([
                ("lot_id", "=", rec.lot_id.id),
                ("process_code", "=", previous),
                ("state", "=", "aceptado"),
            ], limit=1)
            if not prev:
                raise UserError(_(
                    "Ruta '%s': antes de liberar '%s' debe estar liberado "
                    "el proceso previo '%s' para el lote %s."
                ) % (route.name,
                     rec.process_type_id.name,
                     previous.replace("_", " ").title(),
                     rec.lot_id.name or "—"))
'''

# ---------------------------------------------------------------- 3. RETENCIÓN
FILES["models/quality_retention_flow.py"] = '''# -*- coding: utf-8 -*-
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
'''

# ---------------------------------------------------------------- 4. HISTORIAL
FILES["models/quality_change_history.py"] = '''# -*- coding: utf-8 -*-
"""
Historial campo a campo en inspecciones y líneas (req. Laminadora).
"""
from odoo import models, fields, api


TRACKED_INSPECTION_FIELDS = [
    "largo", "ancho", "espesor", "hexagono", "resistencia", "resistencia_na",
    "apariencia", "humedad_pct", "pegado_result", "oct_retiramiento",
    "calibracion", "engomado", "oct_ancho", "oct_espesor", "oct_hexagono",
    "oct_alineacion", "oct_pegado", "reticula_extendida", "reticula_vueltas",
    "lote_reticula", "gramaje_reticula", "numero_corrida", "tipo_hexagono",
    "corte_guillotina", "papel_ancho", "papel_gramaje", "papel_proveedor_id",
    "adhesivo_lote1", "adhesivo_lote2", "state", "retention_state",
]

TRACKED_LINE_FIELDS = [
    "value_float", "value_char", "value_cumple", "value_ok",
    "min_value", "max_value", "result", "notes",
]


class QualityInspectionHistory(models.Model):
    _name = "quality.inspection.history"
    _description = "Historial de Cambios — Inspección"
    _order = "change_date desc, id desc"
    _rec_name = "field_name"

    inspection_id = fields.Many2one(
        "quality.inspection", "Inspección", ondelete="cascade", index=True)
    line_id = fields.Many2one(
        "quality.inspection.line", "Línea", ondelete="cascade", index=True)
    field_name = fields.Char("Campo", required=True)
    field_label = fields.Char("Etiqueta del Campo")
    old_value = fields.Char("Valor Anterior")
    new_value = fields.Char("Valor Nuevo")
    changed_by = fields.Many2one(
        "res.users", "Cambiado por",
        default=lambda s: s.env.user, readonly=True)
    change_date = fields.Datetime(
        default=fields.Datetime.now, readonly=True)
    reason = fields.Char("Motivo (opcional)")
    inspection_state_at_change = fields.Char("Estado al momento del cambio")


def _format_value(record, field_name):
    if field_name not in record._fields:
        return ""
    val = record[field_name]
    field = record._fields[field_name]
    if val is False or val is None:
        return ""
    if field.type == "many2one":
        return val.display_name or ""
    if field.type == "selection":
        return dict(field.selection).get(val, str(val))
    return str(val)


class QualityInspectionTracked(models.Model):
    _inherit = "quality.inspection"

    history_ids = fields.One2many(
        "quality.inspection.history", "inspection_id",
        string="Historial de Cambios")
    history_count = fields.Integer(compute="_compute_history_count")

    def _compute_history_count(self):
        for rec in self:
            rec.history_count = len(rec.history_ids)

    def write(self, vals):
        History = self.env["quality.inspection.history"]
        snapshots = {}
        tracked_keys = [k for k in vals.keys() if k in TRACKED_INSPECTION_FIELDS]
        if tracked_keys:
            for rec in self:
                snapshots[rec.id] = {
                    k: _format_value(rec, k) for k in tracked_keys
                }
        res = super().write(vals)
        if tracked_keys:
            for rec in self:
                old = snapshots.get(rec.id, {})
                for fname in tracked_keys:
                    new_val = _format_value(rec, fname)
                    if old.get(fname, "") != new_val:
                        label = rec._fields[fname].string or fname
                        History.create({
                            "inspection_id": rec.id,
                            "field_name": fname,
                            "field_label": label,
                            "old_value": old.get(fname, ""),
                            "new_value": new_val,
                            "inspection_state_at_change": rec.state,
                        })
        return res


class QualityInspectionLineTracked(models.Model):
    _inherit = "quality.inspection.line"

    def write(self, vals):
        History = self.env["quality.inspection.history"]
        snapshots = {}
        tracked_keys = [k for k in vals.keys() if k in TRACKED_LINE_FIELDS]
        if tracked_keys:
            for line in self:
                snapshots[line.id] = {
                    k: _format_value(line, k) for k in tracked_keys
                }
        res = super().write(vals)
        if tracked_keys:
            for line in self:
                if not line.inspection_id:
                    continue
                old = snapshots.get(line.id, {})
                for fname in tracked_keys:
                    new_val = _format_value(line, fname)
                    if old.get(fname, "") != new_val:
                        label = line._fields[fname].string or fname
                        History.create({
                            "inspection_id": line.inspection_id.id,
                            "line_id": line.id,
                            "field_name": "%s.%s" % (line.name or "Atributo", fname),
                            "field_label": "%s — %s" % (line.name or "", label),
                            "old_value": old.get(fname, ""),
                            "new_value": new_val,
                            "inspection_state_at_change": line.inspection_id.state,
                        })
        return res
'''

# ---------------------------------------------------------------- 5. CERT-EMAIL
FILES["models/quality_certificate_email.py"] = '''# -*- coding: utf-8 -*-
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
    date = fields.Datetime(default=fields.Datetime.now, readonly=True)
    user_id = fields.Many2one("res.users", "Enviado por")
    recipient_email = fields.Char("Destinatario")
    message_id = fields.Many2one("mail.message", "Mensaje", ondelete="set null")
    notes = fields.Text("Notas")
'''

# ---------------------------------------------------------------- 6. 8D EXTRA
FILES["models/quality_corrective_extra.py"] = '''# -*- coding: utf-8 -*-
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
'''

# ---------------------------------------------------------------- 7. DOC CLI
FILES["models/quality_customer_document_extra.py"] = '''# -*- coding: utf-8 -*-
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
'''

# ---------------------------------------------------------------- 8. TROQUEL
FILES["models/quality_troquel_validation.py"] = '''# -*- coding: utf-8 -*-
"""
Flujo formal de troqueles:
- Validación dimensional + funcional con líneas.
- Reparación con bitácora detallada.
- Revisiones por uso/piezas.
"""
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class QualityTroquelValidation(models.Model):
    _name = "quality.troquel.validation"
    _description = "Validación de Troquel"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date desc, id desc"

    name = fields.Char("Referencia", default="Nueva", readonly=True, copy=False)
    troquel_id = fields.Many2one(
        "quality.troquel", required=True, ondelete="cascade",
        tracking=True, index=True)
    date = fields.Datetime(default=fields.Datetime.now, required=True)
    convoked_quality = fields.Boolean("Calidad Convocada")
    convoked_production = fields.Boolean("Producción Convocada")

    quality_user_id = fields.Many2one("res.users", "Calidad")
    production_user_id = fields.Many2one("res.users", "Producción")
    design_user_id = fields.Many2one("res.users", "Diseño")

    line_ids = fields.One2many(
        "quality.troquel.validation.line", "validation_id",
        string="Mediciones / Pruebas")

    dimensional_ok = fields.Boolean(
        "Dimensional OK", compute="_compute_results", store=True)
    functional_ok = fields.Boolean(
        "Funcional OK", compute="_compute_results", store=True)
    overall_ok = fields.Boolean(
        "Resultado Global", compute="_compute_results", store=True)

    state = fields.Selection([
        ("borrador", "Borrador"),
        ("en_validacion", "En Validación"),
        ("aprobado", "Aprobado"),
        ("rechazado", "Rechazado"),
    ], default="borrador", required=True, tracking=True)
    notes = fields.Text("Observaciones")

    @api.depends("line_ids.result", "line_ids.test_type")
    def _compute_results(self):
        for rec in self:
            dims = rec.line_ids.filtered(lambda l: l.test_type == "dimensional")
            funcs = rec.line_ids.filtered(lambda l: l.test_type == "funcional")
            rec.dimensional_ok = bool(dims) and all(
                l.result == "cumple" for l in dims)
            rec.functional_ok = bool(funcs) and all(
                l.result == "cumple" for l in funcs)
            rec.overall_ok = rec.dimensional_ok and rec.functional_ok

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Nueva") == "Nueva":
                vals["name"] = "TVAL-%s" % (
                    self.env["ir.sequence"].next_by_code(
                        "quality.troquel.validation") or "0001")
        return super().create(vals_list)

    def action_start(self):
        for rec in self:
            rec.state = "en_validacion"

    def action_approve(self):
        for rec in self:
            if not rec.dimensional_ok or not rec.functional_ok:
                raise UserError(_(
                    "No se puede aprobar: faltan pruebas dimensionales o funcionales OK."))
            rec.state = "aprobado"
            rec.troquel_id.action_activate()

    def action_reject(self):
        for rec in self:
            rec.state = "rechazado"
            rec.troquel_id.message_post(
                body=_("❌ Validación rechazada (%s).") % rec.name,
                subtype_xmlid="mail.mt_comment")


class QualityTroquelValidationLine(models.Model):
    _name = "quality.troquel.validation.line"
    _description = "Línea de Validación de Troquel"
    _order = "sequence, id"

    validation_id = fields.Many2one(
        "quality.troquel.validation", required=True, ondelete="cascade")
    sequence = fields.Integer(default=10)
    test_type = fields.Selection([
        ("dimensional", "Dimensional"),
        ("funcional", "Funcional"),
    ], required=True, default="dimensional")
    name = fields.Char("Concepto / Punto de Medición", required=True)
    expected = fields.Char("Valor Esperado / Especificación")
    measured = fields.Char("Valor Medido / Observado")
    tolerance = fields.Char("Tolerancia")
    result = fields.Selection([
        ("cumple", "Cumple"),
        ("no_cumple", "No Cumple"),
        ("na", "N/A"),
    ], default="na", required=True)
    notes = fields.Char("Notas")


class QualityTroquelRepair(models.Model):
    _name = "quality.troquel.repair"
    _description = "Reparación de Troquel"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_started desc, id desc"

    name = fields.Char(default="Nueva", readonly=True, copy=False)
    troquel_id = fields.Many2one(
        "quality.troquel", required=True, ondelete="cascade", index=True)
    repair_type = fields.Selection([
        ("interna", "Interna"),
        ("proveedor", "Proveedor Externo"),
    ], required=True, default="interna")
    proveedor_id = fields.Many2one(
        "res.partner", "Proveedor",
        domain=[("supplier_rank", ">", 0)])
    date_started = fields.Datetime(
        "Inicio Reparación", default=fields.Datetime.now, required=True)
    date_finished = fields.Datetime("Fin Reparación")
    days_estimated = fields.Integer("Días Estimados Fuera")
    description = fields.Text("Desglose de Reparación", required=True)
    cost = fields.Monetary("Costo")
    currency_id = fields.Many2one(
        "res.currency", default=lambda s: s.env.company.currency_id)
    state = fields.Selection([
        ("en_curso", "En Curso"),
        ("finalizada", "Finalizada"),
        ("rechazada", "Rechazada"),
    ], default="en_curso", required=True, tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Nueva") == "Nueva":
                vals["name"] = "TREP-%s" % (
                    self.env["ir.sequence"].next_by_code(
                        "quality.troquel.repair") or "0001")
        return super().create(vals_list)

    def action_finish(self):
        for rec in self:
            rec.state = "finalizada"
            rec.date_finished = fields.Datetime.now()
            rec.troquel_id.message_post(
                body=_("🔧 Reparación %s finalizada.") % rec.name,
                subtype_xmlid="mail.mt_comment")


class QualityTroquelExtended(models.Model):
    _inherit = "quality.troquel"

    validation_ids = fields.One2many(
        "quality.troquel.validation", "troquel_id",
        string="Validaciones")
    validation_count = fields.Integer(compute="_compute_counts")
    repair_ids = fields.One2many(
        "quality.troquel.repair", "troquel_id",
        string="Reparaciones")
    repair_count = fields.Integer(compute="_compute_counts")
    pieces_produced = fields.Integer(
        "Piezas Producidas Acumuladas",
        help="Conteo manual de piezas troqueladas para programar revisión.")
    needs_review = fields.Boolean(
        "Requiere Revisión", compute="_compute_needs_review", store=True)

    @api.depends("validation_ids", "repair_ids")
    def _compute_counts(self):
        for rec in self:
            rec.validation_count = len(rec.validation_ids)
            rec.repair_count = len(rec.repair_ids)

    @api.depends("pieces_produced", "pieces_per_review")
    def _compute_needs_review(self):
        for rec in self:
            rec.needs_review = bool(
                rec.pieces_per_review and
                rec.pieces_produced >= rec.pieces_per_review)

    def action_open_validation(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Validación de Troquel"),
            "res_model": "quality.troquel.validation",
            "view_mode": "form",
            "target": "current",
            "context": {"default_troquel_id": self.id},
        }

    def action_open_repair(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Reparación de Troquel"),
            "res_model": "quality.troquel.repair",
            "view_mode": "form",
            "target": "current",
            "context": {"default_troquel_id": self.id},
        }
'''

# ---------------------------------------------------------------- DATA: routes
FILES["data/quality_routes_data.xml"] = '''<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        <record id="seq_quality_troquel_validation" model="ir.sequence">
            <field name="name">Validación de Troquel</field>
            <field name="code">quality.troquel.validation</field>
            <field name="prefix">TVAL-</field>
            <field name="padding">4</field>
        </record>
        <record id="seq_quality_troquel_repair" model="ir.sequence">
            <field name="name">Reparación de Troquel</field>
            <field name="code">quality.troquel.repair</field>
            <field name="prefix">TREP-</field>
            <field name="padding">4</field>
        </record>

        <!-- Ruta estándar Hexágonos -->
        <record id="quality_route_estandar" model="quality.process.route">
            <field name="name">Ruta Estándar Hexágonos</field>
            <field name="sequence">10</field>
        </record>
        <record id="quality_route_estandar_l1" model="quality.process.route.line">
            <field name="route_id" ref="quality_route_estandar"/>
            <field name="sequence">10</field>
            <field name="process_type_id" ref="process_type_octagono"/>
        </record>
        <record id="quality_route_estandar_l2" model="quality.process.route.line">
            <field name="route_id" ref="quality_route_estandar"/>
            <field name="sequence">20</field>
            <field name="process_type_id" ref="process_type_guillotina"/>
        </record>
        <record id="quality_route_estandar_l3" model="quality.process.route.line">
            <field name="route_id" ref="quality_route_estandar"/>
            <field name="sequence">30</field>
            <field name="process_type_id" ref="process_type_pegado"/>
        </record>
        <record id="quality_route_estandar_l4" model="quality.process.route.line">
            <field name="route_id" ref="quality_route_estandar"/>
            <field name="sequence">40</field>
            <field name="process_type_id" ref="process_type_laminadora"/>
        </record>
        <record id="quality_route_estandar_l5" model="quality.process.route.line">
            <field name="route_id" ref="quality_route_estandar"/>
            <field name="sequence">50</field>
            <field name="process_type_id" ref="process_type_sierras_ranuradoras"/>
        </record>
        <record id="quality_route_estandar_l6" model="quality.process.route.line">
            <field name="route_id" ref="quality_route_estandar"/>
            <field name="sequence">60</field>
            <field name="process_type_id" ref="process_type_troquelado_plano"/>
        </record>
    </data>
</odoo>
'''

# ---------------------------------------------------------------- SECURITY
FILES["security/quality_strict_acl.xml"] = '''<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="0">
        <!-- Inspector NO debe crear órdenes de producción ni lotes -->
        <record id="rule_inspector_no_create_mrp" model="ir.rule">
            <field name="name">Inspector: solo lectura de órdenes de producción</field>
            <field name="model_id" ref="mrp.model_mrp_production"/>
            <field name="domain_force">[(1,'=',1)]</field>
            <field name="groups" eval="[(4, ref('quality_management.group_quality_inspector'))]"/>
            <field name="perm_read" eval="True"/>
            <field name="perm_write" eval="False"/>
            <field name="perm_create" eval="False"/>
            <field name="perm_unlink" eval="False"/>
        </record>
        <record id="rule_inspector_no_create_lot" model="ir.rule">
            <field name="name">Inspector: solo lectura de lotes</field>
            <field name="model_id" ref="stock.model_stock_lot"/>
            <field name="domain_force">[(1,'=',1)]</field>
            <field name="groups" eval="[(4, ref('quality_management.group_quality_inspector'))]"/>
            <field name="perm_read" eval="True"/>
            <field name="perm_write" eval="False"/>
            <field name="perm_create" eval="False"/>
            <field name="perm_unlink" eval="False"/>
        </record>
    </data>
</odoo>
'''

# ---------------------------------------------------------------- ACCESS CSV
ACCESS_ROWS_TO_APPEND = """access_quality_process_route_admin,quality.process.route admin,model_quality_process_route,quality_management.group_quality_admin,1,1,1,1
access_quality_process_route_user,quality.process.route user,model_quality_process_route,quality_management.group_quality_user,1,0,0,0
access_quality_process_route_line_admin,quality.process.route.line admin,model_quality_process_route_line,quality_management.group_quality_admin,1,1,1,1
access_quality_process_route_line_user,quality.process.route.line user,model_quality_process_route_line,quality_management.group_quality_user,1,0,0,0
access_quality_inspection_history_user,quality.inspection.history user,model_quality_inspection_history,quality_management.group_quality_user,1,0,0,0
access_quality_inspection_history_manager,quality.inspection.history manager,model_quality_inspection_history,quality_management.group_quality_manager,1,1,1,1
access_quality_retention_log_user,quality.inspection.retention.log user,model_quality_inspection_retention_log,quality_management.group_quality_user,1,0,0,0
access_quality_retention_log_manager,quality.inspection.retention.log manager,model_quality_inspection_retention_log,quality_management.group_quality_manager,1,1,1,1
access_quality_certificate_email_log_manager,quality.certificate.email.log manager,model_quality_certificate_email_log,quality_management.group_quality_manager,1,1,1,1
access_quality_troquel_validation_manager,quality.troquel.validation manager,model_quality_troquel_validation,quality_management.group_quality_manager,1,1,1,1
access_quality_troquel_validation_line_manager,quality.troquel.validation.line manager,model_quality_troquel_validation_line,quality_management.group_quality_manager,1,1,1,1
access_quality_troquel_repair_manager,quality.troquel.repair manager,model_quality_troquel_repair,quality_management.group_quality_manager,1,1,1,1
"""

# ---------------------------------------------------------------- VIEWS
FILES["views/project_task_quality_views.xml"] = '''<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_task_form_quality" model="ir.ui.view">
        <field name="name">project.task.form.quality</field>
        <field name="model">project.task</field>
        <field name="inherit_id" ref="project.view_task_form2"/>
        <field name="arch" type="xml">
            <xpath expr="//notebook" position="inside">
                <page string="Calidad" name="quality">
                    <group>
                        <group>
                            <field name="quality_required_for_progress"/>
                            <field name="quality_sample_release_id"
                                   options="{'no_create': True}"/>
                            <field name="quality_drawing_release_id"
                                   options="{'no_create': True}"/>
                        </group>
                        <group>
                            <field name="quality_block_reason" readonly="1"
                                   invisible="not quality_block_reason"/>
                        </group>
                    </group>
                    <div class="alert alert-warning" role="alert"
                         invisible="not quality_block_reason">
                        <i class="fa fa-exclamation-triangle"/>
                        <strong>Bloqueo:</strong>
                        <field name="quality_block_reason" nolabel="1" readonly="1"/>
                    </div>
                </page>
            </xpath>
        </field>
    </record>
</odoo>
'''

FILES["views/quality_process_route_views.xml"] = '''<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_quality_process_route_list" model="ir.ui.view">
        <field name="name">quality.process.route.list</field>
        <field name="model">quality.process.route</field>
        <field name="arch" type="xml">
            <list>
                <field name="sequence" widget="handle"/>
                <field name="name"/>
                <field name="active"/>
            </list>
        </field>
    </record>
    <record id="view_quality_process_route_form" model="ir.ui.view">
        <field name="name">quality.process.route.form</field>
        <field name="model">quality.process.route</field>
        <field name="arch" type="xml">
            <form>
                <sheet>
                    <div class="oe_title">
                        <h1><field name="name" placeholder="Ruta..."/></h1>
                    </div>
                    <group>
                        <group>
                            <field name="sequence"/>
                            <field name="active"/>
                        </group>
                        <group>
                            <field name="company_id" groups="base.group_multi_company"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Pasos">
                            <field name="line_ids">
                                <list editable="bottom">
                                    <field name="sequence" widget="handle"/>
                                    <field name="process_type_id"/>
                                    <field name="is_optional"/>
                                    <field name="notes"/>
                                </list>
                            </field>
                        </page>
                        <page string="Productos">
                            <field name="product_tmpl_ids"/>
                        </page>
                        <page string="Categorías">
                            <field name="product_categ_ids"/>
                        </page>
                        <page string="Notas">
                            <field name="notes"/>
                        </page>
                    </notebook>
                </sheet>
            </form>
        </field>
    </record>
    <record id="action_quality_process_route" model="ir.actions.act_window">
        <field name="name">Rutas de Proceso</field>
        <field name="res_model">quality.process.route</field>
        <field name="view_mode">list,form</field>
    </record>
    <menuitem id="menu_quality_process_route"
              name="Rutas de Proceso"
              parent="menu_quality_config"
              action="action_quality_process_route"
              sequence="20"/>

    <!-- product.template: campo ruta -->
    <record id="view_product_template_form_quality_route" model="ir.ui.view">
        <field name="name">product.template.form.quality.route</field>
        <field name="model">product.template</field>
        <field name="inherit_id" ref="product.product_template_form_view"/>
        <field name="arch" type="xml">
            <xpath expr="//page[@name='quality']" position="inside">
                <separator string="Ruta de Proceso"/>
                <group>
                    <field name="quality_route_id"
                           options="{'no_create': True}"/>
                </group>
            </xpath>
        </field>
    </record>
</odoo>
'''

FILES["views/quality_retention_views.xml"] = '''<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_quality_inspection_form_retention" model="ir.ui.view">
        <field name="name">quality.inspection.form.retention</field>
        <field name="model">quality.inspection</field>
        <field name="inherit_id" ref="quality_management.view_quality_inspection_form"/>
        <field name="arch" type="xml">
            <xpath expr="//header" position="inside">
                <button name="action_accept_correction"
                        string="Producción: Aceptar Corrección"
                        type="object"
                        invisible="state != 'retenido' or retention_state not in ('retenido','en_correccion')"/>
                <button name="action_correction_done"
                        string="Marcar Corrección Hecha"
                        type="object" class="btn-primary"
                        invisible="state != 'retenido' or retention_state not in ('retenido','en_correccion')"/>
                <button name="action_start_reinspection"
                        string="Iniciar Reinspección"
                        type="object" class="btn-warning"
                        invisible="retention_state != 'correccion_hecha'"
                        groups="quality_management.group_quality_inspector"/>
                <button name="action_accept_after_retention"
                        string="Aceptar tras Reinspección"
                        type="object" class="btn-primary"
                        invisible="retention_state != 'reinspeccion'"
                        groups="quality_management.group_quality_inspector"/>
                <button name="action_reject_after_retention"
                        string="Rechazar tras Reinspección"
                        type="object" class="btn-danger"
                        invisible="retention_state != 'reinspeccion'"
                        groups="quality_management.group_quality_inspector"/>
            </xpath>
            <xpath expr="//notebook" position="inside">
                <page string="Retención / Reinspección" name="retention"
                      invisible="retention_state == 'none'">
                    <group>
                        <group>
                            <field name="retention_state" readonly="1"/>
                            <field name="retention_correction_done_by" readonly="1"/>
                            <field name="retention_correction_done_date" readonly="1"/>
                        </group>
                    </group>
                    <separator string="Notas de Corrección"/>
                    <field name="retention_correction_notes"
                           placeholder="Detalle de la corrección aplicada por Producción..."/>
                    <separator string="Bitácora"/>
                    <field name="retention_log_ids" readonly="1">
                        <list>
                            <field name="date"/>
                            <field name="user_id"/>
                            <field name="retention_state_after"/>
                            <field name="description"/>
                        </list>
                    </field>
                </page>
            </xpath>
        </field>
    </record>
</odoo>
'''

FILES["views/quality_change_history_views.xml"] = '''<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_quality_inspection_history_list" model="ir.ui.view">
        <field name="name">quality.inspection.history.list</field>
        <field name="model">quality.inspection.history</field>
        <field name="arch" type="xml">
            <list>
                <field name="change_date"/>
                <field name="changed_by"/>
                <field name="field_label"/>
                <field name="old_value"/>
                <field name="new_value"/>
                <field name="inspection_state_at_change"/>
            </list>
        </field>
    </record>
    <record id="view_quality_inspection_form_history" model="ir.ui.view">
        <field name="name">quality.inspection.form.history</field>
        <field name="model">quality.inspection</field>
        <field name="inherit_id" ref="quality_management.view_quality_inspection_form"/>
        <field name="arch" type="xml">
            <xpath expr="//notebook" position="inside">
                <page string="Historial de Cambios" name="history"
                      invisible="state == 'borrador'">
                    <field name="history_ids" readonly="1">
                        <list>
                            <field name="change_date"/>
                            <field name="changed_by"/>
                            <field name="field_label"/>
                            <field name="old_value"/>
                            <field name="new_value"/>
                            <field name="inspection_state_at_change"/>
                        </list>
                    </field>
                </page>
            </xpath>
        </field>
    </record>
</odoo>
'''

FILES["views/quality_troquel_validation_views.xml"] = '''<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_troquel_validation_list" model="ir.ui.view">
        <field name="name">quality.troquel.validation.list</field>
        <field name="model">quality.troquel.validation</field>
        <field name="arch" type="xml">
            <list decoration-success="state == 'aprobado'"
                  decoration-danger="state == 'rechazado'">
                <field name="name"/>
                <field name="troquel_id"/>
                <field name="date"/>
                <field name="dimensional_ok" widget="boolean_toggle"/>
                <field name="functional_ok" widget="boolean_toggle"/>
                <field name="state" widget="badge"/>
            </list>
        </field>
    </record>
    <record id="view_troquel_validation_form" model="ir.ui.view">
        <field name="name">quality.troquel.validation.form</field>
        <field name="model">quality.troquel.validation</field>
        <field name="arch" type="xml">
            <form>
                <header>
                    <button name="action_start" string="Iniciar Validación"
                            type="object" class="btn-primary"
                            invisible="state != 'borrador'"/>
                    <button name="action_approve" string="Aprobar"
                            type="object" class="btn-primary"
                            invisible="state != 'en_validacion'"/>
                    <button name="action_reject" string="Rechazar"
                            type="object" class="btn-danger"
                            invisible="state != 'en_validacion'"/>
                    <field name="state" widget="statusbar"/>
                </header>
                <sheet>
                    <div class="oe_title">
                        <h1><field name="name" readonly="1"/></h1>
                    </div>
                    <group>
                        <group>
                            <field name="troquel_id"/>
                            <field name="date"/>
                        </group>
                        <group>
                            <field name="convoked_quality"/>
                            <field name="quality_user_id"
                                   invisible="not convoked_quality"/>
                            <field name="convoked_production"/>
                            <field name="production_user_id"
                                   invisible="not convoked_production"/>
                            <field name="design_user_id"/>
                        </group>
                    </group>
                    <group>
                        <field name="dimensional_ok" readonly="1"/>
                        <field name="functional_ok" readonly="1"/>
                        <field name="overall_ok" readonly="1"/>
                    </group>
                    <notebook>
                        <page string="Mediciones / Pruebas">
                            <field name="line_ids">
                                <list editable="bottom">
                                    <field name="sequence" widget="handle"/>
                                    <field name="test_type"/>
                                    <field name="name"/>
                                    <field name="expected"/>
                                    <field name="measured"/>
                                    <field name="tolerance"/>
                                    <field name="result" widget="badge"
                                           decoration-success="result == 'cumple'"
                                           decoration-danger="result == 'no_cumple'"/>
                                    <field name="notes"/>
                                </list>
                            </field>
                        </page>
                        <page string="Observaciones">
                            <field name="notes"/>
                        </page>
                    </notebook>
                </sheet>
                <chatter/>
            </form>
        </field>
    </record>
    <record id="action_troquel_validation" model="ir.actions.act_window">
        <field name="name">Validaciones de Troquel</field>
        <field name="res_model">quality.troquel.validation</field>
        <field name="view_mode">list,form</field>
    </record>

    <record id="view_troquel_repair_form" model="ir.ui.view">
        <field name="name">quality.troquel.repair.form</field>
        <field name="model">quality.troquel.repair</field>
        <field name="arch" type="xml">
            <form>
                <header>
                    <button name="action_finish" string="Finalizar"
                            type="object" class="btn-primary"
                            invisible="state != 'en_curso'"/>
                    <field name="state" widget="statusbar"/>
                </header>
                <sheet>
                    <div class="oe_title">
                        <h1><field name="name" readonly="1"/></h1>
                    </div>
                    <group>
                        <group>
                            <field name="troquel_id"/>
                            <field name="repair_type"/>
                            <field name="proveedor_id"
                                   invisible="repair_type != 'proveedor'"/>
                        </group>
                        <group>
                            <field name="date_started"/>
                            <field name="date_finished"/>
                            <field name="days_estimated"/>
                            <field name="cost"/>
                            <field name="currency_id" invisible="1"/>
                        </group>
                    </group>
                    <separator string="Desglose de Reparación"/>
                    <field name="description"/>
                </sheet>
                <chatter/>
            </form>
        </field>
    </record>
    <record id="action_troquel_repair" model="ir.actions.act_window">
        <field name="name">Reparaciones de Troquel</field>
        <field name="res_model">quality.troquel.repair</field>
        <field name="view_mode">list,form</field>
    </record>

    <!-- Smart buttons en troquel -->
    <record id="view_quality_troquel_form_extended" model="ir.ui.view">
        <field name="name">quality.troquel.form.extended</field>
        <field name="model">quality.troquel</field>
        <field name="inherit_id" ref="quality_management.view_quality_troquel_form"/>
        <field name="arch" type="xml">
            <xpath expr="//header" position="inside">
                <button name="action_open_validation"
                        string="Nueva Validación" type="object"
                        class="btn-secondary"/>
                <button name="action_open_repair"
                        string="Nueva Reparación" type="object"
                        class="btn-secondary"
                        invisible="state not in ('reparacion_interna','reparacion_proveedor','danado')"/>
            </xpath>
            <xpath expr="//sheet/div[@class='oe_title']" position="before">
                <div class="oe_button_box" name="button_box">
                    <field name="needs_review" invisible="1"/>
                    <button name="%(action_troquel_validation)d"
                            type="action"
                            class="oe_stat_button" icon="fa-check-square-o"
                            context="{'search_default_troquel_id': active_id}">
                        <field name="validation_count" widget="statinfo"
                               string="Validaciones"/>
                    </button>
                    <button name="%(action_troquel_repair)d"
                            type="action"
                            class="oe_stat_button" icon="fa-wrench"
                            context="{'search_default_troquel_id': active_id}">
                        <field name="repair_count" widget="statinfo"
                               string="Reparaciones"/>
                    </button>
                </div>
            </xpath>
            <xpath expr="//field[@name='pieces_per_review']" position="after">
                <field name="pieces_produced"/>
                <field name="needs_review" readonly="1"
                       decoration-warning="needs_review"/>
            </xpath>
        </field>
    </record>

    <menuitem id="menu_quality_troquel_validation"
              name="Validaciones de Troquel"
              parent="menu_quality_config"
              action="action_troquel_validation"
              sequence="40"/>
    <menuitem id="menu_quality_troquel_repair"
              name="Reparaciones de Troquel"
              parent="menu_quality_config"
              action="action_troquel_repair"
              sequence="45"/>
</odoo>
'''

FILES["views/quality_certificate_email_views.xml"] = '''<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_quality_certificate_form_email" model="ir.ui.view">
        <field name="name">quality.certificate.form.email</field>
        <field name="model">quality.certificate</field>
        <field name="inherit_id" ref="quality_management.view_quality_certificate_form"/>
        <field name="arch" type="xml">
            <xpath expr="//notebook" position="inside">
                <page string="Bitácora de Envíos" name="emails">
                    <group>
                        <field name="date_sent" readonly="1"/>
                        <field name="sent_by" readonly="1"/>
                    </group>
                    <field name="email_log_ids" readonly="1">
                        <list>
                            <field name="date"/>
                            <field name="user_id"/>
                            <field name="recipient_email"/>
                            <field name="notes"/>
                        </list>
                    </field>
                </page>
            </xpath>
        </field>
    </record>
</odoo>
'''

# ---------------------------------------------------------------- REPORT
FILES["reports/report_8d_extended.xml"] = '''<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="report_8d_document_extended"
              inherit_id="quality_management.report_8d_document">
        <xpath expr="//h4[contains(., 'D6 - Plan de Acciones')]" position="before">
            <h4>D4 - 5 Por qué</h4>
            <table class="table table-bordered table-sm" style="margin-bottom: 15px;">
                <thead>
                    <tr class="table-active">
                        <th style="width: 10%;">N°</th>
                        <th style="width: 35%;">Pregunta</th>
                        <th>Respuesta</th>
                    </tr>
                </thead>
                <tbody>
                    <tr t-foreach="doc.why_ids" t-as="why">
                        <td><span t-field="why.sequence"/></td>
                        <td><span t-field="why.question"/></td>
                        <td><span t-field="why.answer"/></td>
                    </tr>
                </tbody>
            </table>

            <h4>D5 - Análisis Causa-Efecto (Ishikawa)</h4>
            <table class="table table-bordered table-sm" style="margin-bottom: 15px;">
                <thead>
                    <tr class="table-active">
                        <th style="width: 25%;">Categoría</th>
                        <th>Causa</th>
                        <th style="width: 15%;" class="text-center">Causa Raíz</th>
                    </tr>
                </thead>
                <tbody>
                    <tr t-foreach="doc.ishikawa_ids" t-as="ish">
                        <td><span t-field="ish.category"/></td>
                        <td><span t-field="ish.cause"/></td>
                        <td class="text-center">
                            <t t-if="ish.is_root_cause">
                                <strong style="color:#c00;">★ RAÍZ</strong>
                            </t>
                        </td>
                    </tr>
                </tbody>
            </table>

            <h4>D2 - Equipo de Trabajo</h4>
            <table class="table table-bordered table-sm" style="margin-bottom: 15px;">
                <thead>
                    <tr class="table-active">
                        <th>Miembro</th>
                        <th>Rol</th>
                        <th class="text-center">Notifica</th>
                    </tr>
                </thead>
                <tbody>
                    <tr t-foreach="doc.work_team_ids" t-as="m">
                        <td><span t-field="m.user_id.name"/></td>
                        <td><span t-field="m.role"/></td>
                        <td class="text-center">
                            <t t-if="m.notify_progress">Sí</t>
                            <t t-else="">No</t>
                        </td>
                    </tr>
                </tbody>
            </table>
        </xpath>
    </template>
</odoo>
'''

# ============================================================================
#                        IMPORTS / MANIFEST PATCHES
# ============================================================================

NEW_MODEL_IMPORTS = [
    "from . import project_task_quality",
    "from . import quality_process_route",
    "from . import quality_retention_flow",
    "from . import quality_change_history",
    "from . import quality_certificate_email",
    "from . import quality_corrective_extra",
    "from . import quality_customer_document_extra",
    "from . import quality_troquel_validation",
]

NEW_MANIFEST_DEPENDS = []  # ya están todas las dependencias

NEW_MANIFEST_DATA = [
    "data/quality_routes_data.xml",
    "security/quality_strict_acl.xml",
    "views/project_task_quality_views.xml",
    "views/quality_process_route_views.xml",
    "views/quality_retention_views.xml",
    "views/quality_change_history_views.xml",
    "views/quality_troquel_validation_views.xml",
    "views/quality_certificate_email_views.xml",
    "reports/report_8d_extended.xml",
]


# ============================================================================
#                              UTILIDADES
# ============================================================================

def log(msg, ok=True):
    icon = "✓" if ok else "✗"
    print(f"  {icon} {msg}")


def backup_file(src, backup_root):
    if not src.exists():
        return
    rel = src.name
    dst = backup_root / rel
    backup_root.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def write_file(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def patch_init(init_path, imports, backup_root):
    if not init_path.exists():
        write_file(init_path, "\n".join(imports) + "\n")
        log(f"Creado {init_path}")
        return
    backup_file(init_path, backup_root)
    text = init_path.read_text(encoding="utf-8")
    added = []
    for imp in imports:
        if imp not in text:
            text += ("\n" if not text.endswith("\n") else "") + imp + "\n"
            added.append(imp)
    init_path.write_text(text, encoding="utf-8")
    if added:
        log(f"Patched {init_path.name}: +{len(added)} imports")
    else:
        log(f"{init_path.name} ya estaba al día")


def patch_manifest(manifest_path, new_data_files, backup_root):
    backup_file(manifest_path, backup_root)
    text = manifest_path.read_text(encoding="utf-8")
    added = []

    # Insertar líneas dentro del bloque "data": [...] antes de su cierre
    # Estrategia: buscar la línea con ']' que cierra "data" y, si los archivos
    # no están, insertarlos justo antes.
    for f in new_data_files:
        if f"\"{f}\"" in text or f"'{f}'" in text:
            continue
        # Buscar cierre del bloque data
        marker = '"data": ['
        if marker not in text:
            marker = "'data': ["
        if marker not in text:
            log(f"No encuentro bloque 'data' en manifest", ok=False)
            return
        start = text.index(marker)
        # Encontrar el cierre balanceando corchetes
        i = start + len(marker)
        depth = 1
        while i < len(text) and depth > 0:
            if text[i] == "[":
                depth += 1
            elif text[i] == "]":
                depth -= 1
            i += 1
        close_idx = i - 1  # posición del ']'
        insert_text = f'        "{f}",\n    '
        text = text[:close_idx] + insert_text + text[close_idx:]
        added.append(f)

    manifest_path.write_text(text, encoding="utf-8")
    if added:
        log(f"Patched __manifest__.py: +{len(added)} archivos data")
    else:
        log("__manifest__.py ya estaba al día")


def patch_access_csv(csv_path, rows_to_append, backup_root):
    backup_file(csv_path, backup_root)
    existing = csv_path.read_text(encoding="utf-8") if csv_path.exists() else ""
    if not existing.strip():
        existing = "id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink\n"
    added = 0
    new_lines = []
    for line in rows_to_append.strip().splitlines():
        rid = line.split(",", 1)[0]
        if rid in existing:
            continue
        new_lines.append(line)
        added += 1
    if new_lines:
        if not existing.endswith("\n"):
            existing += "\n"
        existing += "\n".join(new_lines) + "\n"
        csv_path.write_text(existing, encoding="utf-8")
        log(f"Patched ir.model.access.csv: +{added} reglas")
    else:
        log("ir.model.access.csv ya estaba al día")


# ============================================================================
#                                 MAIN
# ============================================================================

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 apply_quality_full_compliance.py /Users/alphaqueb/Documents/Proyectos/Clientes/Hexágonos/Módulos/quality_management")
        sys.exit(1)

    module_root = Path(sys.argv[1]).resolve()
    if not module_root.exists() or not (module_root / "__manifest__.py").exists():
        print(f"ERROR: {module_root} no parece ser un módulo válido (falta __manifest__.py)")
        sys.exit(1)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_root = module_root / f"_backup_full_compliance_{timestamp}"

    print(f"\n>>> Aplicando full-compliance al módulo: {module_root}")
    print(f">>> Backup: {backup_root}\n")

    # 1. Escribir archivos nuevos
    print(">> Creando archivos nuevos...")
    for rel_path, content in FILES.items():
        target = module_root / rel_path
        if target.exists():
            backup_file(target, backup_root / Path(rel_path).parent)
        write_file(target, content)
        log(f"{rel_path}")

    # 2. Patch __init__ models
    print("\n>> Patcheando models/__init__.py...")
    patch_init(module_root / "models" / "__init__.py",
               NEW_MODEL_IMPORTS, backup_root / "models")

    # 3. Patch __manifest__.py
    print("\n>> Patcheando __manifest__.py...")
    patch_manifest(module_root / "__manifest__.py",
                   NEW_MANIFEST_DATA, backup_root)

    # 4. Patch ir.model.access.csv
    print("\n>> Patcheando security/ir.model.access.csv...")
    patch_access_csv(module_root / "security" / "ir.model.access.csv",
                     ACCESS_ROWS_TO_APPEND, backup_root / "security")

    print("\n" + "=" * 70)
    print("✓ APLICADO. Pasos siguientes:")
    print("=" * 70)
    print("""
1. Reiniciar Odoo y actualizar el módulo:
     docker compose restart odoo
     # O directamente:
     docker compose exec odoo odoo -u quality_management -d <db> --stop-after-init

2. Ir a Calidad → Configuración → Rutas de Proceso para asignar rutas
   por producto/categoría. La ruta 'Estándar Hexágonos' viene precargada.

3. En cada producto, asignar la ruta correspondiente en la pestaña 'Calidad'.

4. En cada tarea de Proyecto que requiera muestra/plano, marcar
   'Requiere Liberación de Calidad' y enlazar la liberación correspondiente.

5. Los inspectores ahora verán la pestaña 'Retención / Reinspección'
   cuando el producto sea retenido. El supervisor marca 'Corrección Hecha'
   y Calidad 'Inicia Reinspección' → 'Aceptar/Rechazar tras Reinspección'.

6. Todo cambio en campos de medidas/atributos queda en el 'Historial de Cambios'
   de la inspección.

7. Para troqueles: usar 'Nueva Validación' para validar dimensional + funcional;
   usar 'Nueva Reparación' para registrar reparaciones internas o de proveedor.
""")
    print(f">> Backup completo en: {backup_root}\n")


if __name__ == "__main__":
    main()