# -*- coding: utf-8 -*-
"""
Historial campo a campo en inspecciones y líneas.

FOLIO-QM-ODOO18-073:
- Se conserva el modelo técnico de historial.
- Ya no se muestra una pestaña duplicada al usuario.
- Cada movimiento se publica también en el chatter inicial de la inspección,
  que queda como única sección visible de movimientos.
"""
from collections import defaultdict

from markupsafe import Markup, escape

from odoo import models, fields, api, _


TRACKED_INSPECTION_FIELDS = [
    "largo", "ancho", "espesor", "hexagono", "resistencia", "resistencia_na",
    "apariencia", "humedad_pct", "pegado_result", "oct_retiramiento",
    "calibracion", "engomado", "oct_ancho", "oct_espesor", "oct_hexagono",
    "oct_hexagono_tipo", "oct_alineacion", "oct_pegado",
    "reticula_extendida", "reticula_vueltas", "lote_reticula",
    "gramaje_reticula", "numero_corrida", "tipo_hexagono",
    "corte_guillotina", "papel_ancho", "papel_gramaje", "papel_proveedor_id",
    "adhesivo_lote1", "adhesivo_lote2", "state", "retention_state",
]

TRACKED_LINE_FIELDS = [
    "value_float", "value_char", "value_selection", "value_cumple",
    "value_cumple_required", "value_ok", "value_ok_required",
    "is_not_applicable", "result_required", "min_value", "max_value",
    "result", "notes",
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
        "Fecha de Cambio", default=fields.Datetime.now, readonly=True)
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

    if field.type == "boolean":
        return _("Sí") if val else _("No")

    return str(val)


def _safe_display(value):
    value = value if value not in (False, None, "") else "—"
    return escape(str(value))


def _post_quality_history_to_chatter(inspection, changes):
    """
    Publica cambios detallados en el chatter inicial.
    changes: list(dict(label, old, new, state))
    """
    if not inspection or not changes:
        return

    if inspection.env.context.get("skip_quality_history_chatter"):
        return

    items = []
    for change in changes:
        items.append(
            "<li>"
            "<b>%s</b>: "
            "<span style='color:#6b7280;'>%s</span> "
            "<span style='color:#9ca3af;'>→</span> "
            "<span>%s</span>"
            "<br/><small style='color:#6b7280;'>Estado: %s</small>"
            "</li>"
            % (
                _safe_display(change.get("label")),
                _safe_display(change.get("old")),
                _safe_display(change.get("new")),
                _safe_display(change.get("state")),
            )
        )

    body = Markup(
        "<p><b>%s</b></p><ul>%s</ul>"
        % (
            escape(_("Movimiento registrado en captura de calidad")),
            "".join(items),
        )
    )

    inspection.message_post(
        body=body,
        subtype_xmlid="mail.mt_comment",
    )


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
                changes_for_chatter = []

                for fname in tracked_keys:
                    new_val = _format_value(rec, fname)
                    old_val = old.get(fname, "")

                    if old_val == new_val:
                        continue

                    label = rec._fields[fname].string or fname
                    History.create({
                        "inspection_id": rec.id,
                        "field_name": fname,
                        "field_label": label,
                        "old_value": old_val,
                        "new_value": new_val,
                        "inspection_state_at_change": rec.state,
                    })
                    changes_for_chatter.append({
                        "label": label,
                        "old": old_val,
                        "new": new_val,
                        "state": rec.state,
                    })

                _post_quality_history_to_chatter(rec, changes_for_chatter)

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
            changes_by_inspection = defaultdict(list)

            for line in self:
                if not line.inspection_id:
                    continue

                old = snapshots.get(line.id, {})
                for fname in tracked_keys:
                    new_val = _format_value(line, fname)
                    old_val = old.get(fname, "")

                    if old_val == new_val:
                        continue

                    label = line._fields[fname].string or fname
                    full_label = "%s — %s" % (line.name or "", label)

                    History.create({
                        "inspection_id": line.inspection_id.id,
                        "line_id": line.id,
                        "field_name": "%s.%s" % (line.name or "Atributo", fname),
                        "field_label": full_label,
                        "old_value": old_val,
                        "new_value": new_val,
                        "inspection_state_at_change": line.inspection_id.state,
                    })

                    changes_by_inspection[line.inspection_id.id].append({
                        "label": full_label,
                        "old": old_val,
                        "new": new_val,
                        "state": line.inspection_id.state,
                    })

            Inspection = self.env["quality.inspection"]
            for inspection_id, changes in changes_by_inspection.items():
                _post_quality_history_to_chatter(
                    Inspection.browse(inspection_id),
                    changes,
                )

        return res