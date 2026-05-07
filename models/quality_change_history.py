# -*- coding: utf-8 -*-
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
