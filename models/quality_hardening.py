# -*- coding: utf-8 -*-
import re
import unicodedata
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


# FOLIO-QM-ODOO18-074:
# Secuencia obligatoria solicitada para impedir saltos de flujo.
PROCESS_SEQUENCE = [
    "octagono",
    "guillotina",
    "pegado",
    "laminadora",
    "remanejo",
    "troquelado_plano",
]

# FOLIO-QM-ODOO18-072 / 074:
# Alias exactos que no se pueden capturar como atributos adicionales
# cuando el proceso ya los captura en Medidas y Propiedades.
RESERVED_MEASURE_FIELD_ALIASES = {
    "largo": ("Largo", ("show_largo",)),
    "largo_mm": ("Largo", ("show_largo",)),
    "ancho": ("Ancho", ("show_ancho",)),
    "ancho_mm": ("Ancho", ("show_ancho",)),
    "espesor": ("Espesor", ("show_espesor",)),
    "espesor_mm": ("Espesor", ("show_espesor",)),
    "espesor_in": ("Espesor", ("show_espesor",)),
    "hexagono": ("Hexágono", ("show_hexagono", "show_tipo_hexagono")),
    "hexagono_tipo": ("Hexágono", ("show_hexagono", "show_tipo_hexagono")),
    "tipo_hexagono": ("Tipo de Hexágono", ("show_hexagono", "show_tipo_hexagono")),
    "tipo_de_hexagono": ("Tipo de Hexágono", ("show_hexagono", "show_tipo_hexagono")),
    "resistencia": ("Resistencia", ("show_resistencia",)),
    "resistencia_lbf": ("Resistencia", ("show_resistencia",)),
    "apariencia": ("Apariencia", ("show_apariencia",)),
    "humedad": ("Humedad", ("show_humedad",)),
    "humedad_pct": ("Humedad", ("show_humedad",)),
    "porcentaje_humedad": ("Humedad", ("show_humedad",)),
    "pegado": ("Resultado de Pegado", ("show_pegado",)),
    "resultado_pegado": ("Resultado de Pegado", ("show_pegado",)),
    "resultado_de_pegado": ("Resultado de Pegado", ("show_pegado",)),
    "retiramiento": ("Retiramiento", ("show_retiramiento",)),
    "restiramiento": ("Retiramiento", ("show_retiramiento",)),
    "reticula": ("Retícula", ("show_retiramiento",)),
    "reticula_extendida": ("Retícula Extendida", ("show_retiramiento",)),
    "calibracion": ("Calibración", ("show_calibracion",)),
    "engomado": ("Engomado", ("show_engomado",)),
    "alineacion": ("Alineación", ("show_alineacion",)),
}

# Compatibilidad con código anterior.
RESERVED_MEASURE_ATTRS = set(RESERVED_MEASURE_FIELD_ALIASES)

# FOLIO-QM-ODOO18-070 / FOLIO-QM-ODOO18-071:
# Procesos que solo aceptan atributos adicionales binarios Cumple/No Cumple.
# No permiten N/A, OK/NO OK/N/A, atributos de selección ni atributos numéricos.
STRICT_BINARY_RESULT_PROCESS_CODES = {
    "acabado_empaque",
    "impresion",
}

# FOLIO-QM-ODOO18-075:
# En Octágono estos conceptos son campos nativos obligatorios o no aplican
# en el proceso; no deben duplicarse como atributos adicionales.
OCTAGONO_RESERVED_FIELD_ALIASES = {
    "ancho": "Ancho",
    "ancho_mm": "Ancho",
    "hexagono": "Hexágono",
    "hexagono_tipo": "Hexágono",
    "tipo_hexagono": "Hexágono",
    "tipo_de_hexagono": "Hexágono",
    "numero_corrida": "Número de Corrida",
    "numero_de_corrida": "Número de Corrida",
    "corrida": "Número de Corrida",
    "papel": "Papel",
    "ancho_papel": "Ancho de Papel",
    "papel_ancho": "Ancho de Papel",
    "gramaje": "Gramaje de Papel",
    "gramaje_papel": "Gramaje de Papel",
    "papel_gramaje": "Gramaje de Papel",
    "proveedor": "Proveedor de Papel",
    "proveedor_papel": "Proveedor de Papel",
    "proveedor_de_rollos": "Proveedor de Rollos",
    "adhesivo": "Adhesivo",
    "lote_1": "Lote 1 Adhesivo",
    "lote1": "Lote 1 Adhesivo",
    "adhesivo_lote1": "Lote 1 Adhesivo",
    "lote_2": "Lote 2 Adhesivo",
    "lote2": "Lote 2 Adhesivo",
    "adhesivo_lote2": "Lote 2 Adhesivo",
    "calibracion": "Calibración",
    "engomado": "Engomado",
    "alineacion": "Alineación",
    "corte_guillotina": "Corte de Guillotina",
    "corte_de_guillotina": "Corte de Guillotina",
    "retiramiento": "Retiramiento no aplica en Octágono",
    "restiramiento": "Retiramiento no aplica en Octágono",
    "reticula": "Retiramiento no aplica en Octágono",
    "reticula_extendida": "Retiramiento no aplica en Octágono",
    "espesor": "Espesor no aplica en Octágono",
    "espesor_mm": "Espesor no aplica en Octágono",
    "espesor_in": "Espesor no aplica en Octágono",
}


def _slug(value):
    value = value or ""
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    value = re.sub(r"[^a-zA-Z0-9]+", "_", value.lower()).strip("_")
    return value


def _reserved_measure_label_for_inspection(inspection, normalized_key):
    if not inspection or not normalized_key:
        return False

    # FOLIO-QM-ODOO18-075:
    # Octágono tiene una matriz fija de captura. Estos conceptos no deben
    # aparecer como atributos adicionales, aunque la configuración legacy
    # del proceso aún no haya sido actualizada en la base.
    if inspection.process_code == "octagono":
        oct_label = OCTAGONO_RESERVED_FIELD_ALIASES.get(normalized_key)
        if oct_label:
            return oct_label

    alias = RESERVED_MEASURE_FIELD_ALIASES.get(normalized_key)
    if not alias:
        return False

    label, flag_names = alias
    if any(getattr(inspection, flag_name, False) for flag_name in flag_names):
        return label

    return False


class QualityProcessTypeHardening(models.Model):
    _inherit = "quality.process.type"

    capture_mode = fields.Selection(
        [
            ("full", "Medidas + Propiedades + Atributos"),
            ("additional_only", "Solo Atributos Adicionales"),
        ],
        default="full",
        required=True,
    )
    require_measures = fields.Boolean(
        "Requerir Medidas/Propiedades para liberar",
        default=True,
    )
    require_additional_attributes = fields.Boolean(
        "Requerir Atributos Adicionales para liberar",
        default=True,
    )
    zero_value_blocking = fields.Boolean(
        "Bloquear valores numéricos en cero",
        default=True,
    )


class QualityAttributeTemplateHardening(models.Model):
    _inherit = "quality.attribute.template"

    # FOLIO-QM-ODOO18-075: soporta rangos finos como 0.0010 en plantillas numéricas.
    min_value = fields.Float("Valor Mínimo", digits=(16, 4))
    max_value = fields.Float("Valor Máximo", digits=(16, 4))

    normalized_name = fields.Char(
        "Nombre Normalizado",
        compute="_compute_normalized_name",
        store=True,
        index=True,
    )
    capture_zone = fields.Selection(
        [
            ("additional", "Atributos Adicionales"),
            ("measures", "Medidas y Propiedades"),
            ("ranurado", "Ranurado"),
            ("troquelado", "Troquelado"),
            ("production", "Datos de Producción"),
        ],
        default="additional",
        required=True,
    )
    result_mode = fields.Selection(
        [
            ("cumple", "Cumple / No Cumple / N/A"),
            ("ok", "OK / NO OK / N/A"),
        ],
        default="cumple",
        required=True,
    )
    allow_zero = fields.Boolean("Permitir valor cero", default=False)

    @api.depends("name")
    def _compute_normalized_name(self):
        for rec in self:
            rec.normalized_name = _slug(rec.name)

    def _target_process_is_strict_binary(self, vals=None):
        self.ensure_one()
        vals = vals or {}

        if "process_type_id" in vals:
            process = (
                self.env["quality.process.type"].browse(vals["process_type_id"])
                if vals.get("process_type_id")
                else False
            )
        else:
            process = self.process_type_id

        return bool(process and process.code in STRICT_BINARY_RESULT_PROCESS_CODES)

    def _normalize_template_vals_for_strict_binary(self, vals):
        vals = dict(vals or {})
        vals.update({
            "attribute_type": "boolean",
            "capture_zone": "additional",
            "result_mode": "cumple",
            "allow_zero": False,
            "min_value": 0.0,
            "max_value": 0.0,
            "unit": False,
            "selection_options": False,
        })
        return vals

    @api.onchange("process_type_id", "attribute_type", "result_mode")
    def _onchange_strict_binary_template(self):
        for rec in self:
            if rec.process_type_id and rec.process_type_id.code in STRICT_BINARY_RESULT_PROCESS_CODES:
                # FOLIO-QM-ODOO18-071: Impresión y Acabado no permiten configurar OK/NO OK/N/A, selección ni numéricos.
                rec.attribute_type = "boolean"
                rec.capture_zone = "additional"
                rec.result_mode = "cumple"
                rec.allow_zero = False
                rec.min_value = 0.0
                rec.max_value = 0.0
                rec.unit = False
                rec.selection_options = False

    @api.model_create_multi
    def create(self, vals_list):
        clean_vals_list = []
        Process = self.env["quality.process.type"]

        for vals in vals_list:
            vals = dict(vals or {})
            process = (
                Process.browse(vals["process_type_id"])
                if vals.get("process_type_id")
                else False
            )
            if process and process.code in STRICT_BINARY_RESULT_PROCESS_CODES:
                vals = self._normalize_template_vals_for_strict_binary(vals)
            clean_vals_list.append(vals)

        return super().create(clean_vals_list)

    def write(self, vals):
        vals = dict(vals or {})
        if not vals:
            return super().write(vals)

        strict_records = self.filtered(lambda rec: rec._target_process_is_strict_binary(vals))
        other_records = self - strict_records

        result = True
        if other_records:
            result = super(QualityAttributeTemplateHardening, other_records).write(vals) and result

        if strict_records:
            strict_vals = self._normalize_template_vals_for_strict_binary(vals)
            result = super(QualityAttributeTemplateHardening, strict_records).write(strict_vals) and result

        return result


class QualityInspectionLineHardening(models.Model):
    _inherit = "quality.inspection.line"

    # FOLIO-QM-ODOO18-075:
    # Permite capturas finas como 0.0010 en calibración sin que la lista
    # editable ni los reportes redondeen visualmente a cero.
    value_float = fields.Float("Valor Numérico", digits=(16, 4))
    min_value = fields.Float("Mínimo", digits=(16, 4))
    max_value = fields.Float("Máximo", digits=(16, 4))

    normalized_name = fields.Char(
        "Nombre Normalizado",
        compute="_compute_normalized_name",
        store=True,
        index=True,
    )
    capture_zone = fields.Selection(
        [
            ("additional", "Atributos Adicionales"),
            ("measures", "Medidas y Propiedades"),
            ("ranurado", "Ranurado"),
            ("troquelado", "Troquelado"),
            ("production", "Datos de Producción"),
        ],
        default="additional",
        required=True,
    )
    result_mode = fields.Selection(
        [
            ("cumple", "Cumple / No Cumple / N/A"),
            ("ok", "OK / NO OK / N/A"),
        ],
        default="cumple",
        required=True,
    )

    # FOLIO-QM-ODOO18-018: se extiende el campo existente con N/A sin redefinirlo
    # por completo, evitando conflictos de upgrade en Odoo 18.
    value_cumple = fields.Selection(
        selection_add=[("na", "N/A")],
        ondelete={"na": "set default"},
        default="na",
    )
    value_ok = fields.Selection(
        [
            ("ok", "OK"),
            ("no_ok", "NO OK"),
            ("na", "N/A"),
        ],
        string="OK/NO OK/N/A",
        default="na",
    )
    result = fields.Selection(
        selection_add=[
            ("ok", "OK"),
            ("no_ok", "NO OK"),
        ],
        ondelete={
            "ok": "set default",
            "no_ok": "set default",
        },
    )
    allow_zero = fields.Boolean("Permitir cero")

    # FOLIO-QM-ODOO18-070 / FOLIO-QM-ODOO18-071:
    # Permite que vistas, validaciones y reportes identifiquen líneas pertenecientes
    # a procesos estrictamente Cumple/No Cumple.
    process_code = fields.Char(
        related="inspection_id.process_code",
        store=True,
        readonly=True,
    )
    strict_binary_result = fields.Boolean(
        compute="_compute_strict_binary_result",
        store=False,
    )

    def init(self):
        """
        FOLIO-QM-ODOO18-071:
        Normaliza líneas existentes de Impresión y Acabado/Empaque durante upgrade.
        Esto corrige capturas previas donde las líneas quedaron como OK/NO OK/N/A,
        numéricas o con Resultado = N/A.
        """
        super().init()
        cr = self.env.cr

        cr.execute("""
            SELECT EXISTS (
                SELECT 1
                  FROM information_schema.tables
                 WHERE table_name = 'quality_inspection_line'
            )
        """)
        line_table_exists = cr.fetchone()[0]

        cr.execute("""
            SELECT EXISTS (
                SELECT 1
                  FROM information_schema.tables
                 WHERE table_name = 'quality_inspection'
            )
        """)
        inspection_table_exists = cr.fetchone()[0]

        if not line_table_exists or not inspection_table_exists:
            return

        cr.execute("""
            SELECT column_name
              FROM information_schema.columns
             WHERE table_name = 'quality_inspection_line'
        """)
        line_columns = {row[0] for row in cr.fetchall()}

        required_line_columns = {
            "inspection_id",
            "attribute_type",
            "capture_zone",
            "result_mode",
            "value_float",
            "value_char",
            "value_cumple",
            "value_ok",
            "result",
            "min_value",
            "max_value",
            "unit",
            "allow_zero",
        }
        if not required_line_columns.issubset(line_columns):
            return

        cr.execute("""
            SELECT column_name
              FROM information_schema.columns
             WHERE table_name = 'quality_inspection'
        """)
        inspection_columns = {row[0] for row in cr.fetchall()}

        if "process_code" not in inspection_columns:
            return

        cr.execute("""
            UPDATE quality_inspection_line AS line
               SET attribute_type = 'boolean',
                   capture_zone = 'additional',
                   result_mode = 'cumple',
                   value_float = 0,
                   value_char = NULL,
                   value_ok = NULL,
                   min_value = 0,
                   max_value = 0,
                   unit = NULL,
                   allow_zero = FALSE,
                   value_cumple = CASE
                       WHEN line.value_cumple IN ('cumple', 'no_cumple') THEN line.value_cumple
                       WHEN line.result IN ('cumple', 'no_cumple') THEN line.result
                       ELSE NULL
                   END,
                   result = CASE
                       WHEN line.value_cumple IN ('cumple', 'no_cumple') THEN line.value_cumple
                       WHEN line.result IN ('cumple', 'no_cumple') THEN line.result
                       ELSE NULL
                   END
              FROM quality_inspection AS inspection
             WHERE line.inspection_id = inspection.id
               AND inspection.process_code IN ('acabado_empaque', 'impresion')
        """)

    @api.depends("inspection_id.process_code")
    def _compute_strict_binary_result(self):
        for line in self:
            line.strict_binary_result = (
                line.inspection_id.process_code in STRICT_BINARY_RESULT_PROCESS_CODES
                if line.inspection_id
                else False
            )

    def _is_strict_binary_result_line(self):
        self.ensure_one()
        return bool(
            self.inspection_id
            and self.inspection_id.process_code in STRICT_BINARY_RESULT_PROCESS_CODES
        )

    def _strict_binary_process_display_name(self):
        self.ensure_one()
        if self.inspection_id and self.inspection_id.process_type_id:
            return self.inspection_id.process_type_id.display_name
        return _("Este proceso")

    def _normalize_vals_for_strict_binary_line(self, vals, reset_missing=False):
        vals = dict(vals or {})

        vals.update({
            "attribute_type": "boolean",
            "capture_zone": "additional",
            "result_mode": "cumple",
            "value_ok": False,
            "value_float": 0.0,
            "value_char": False,
            "min_value": 0.0,
            "max_value": 0.0,
            "unit": False,
            "allow_zero": False,
        })

        if reset_missing or "value_cumple" in vals:
            if vals.get("value_cumple") not in ("cumple", "no_cumple"):
                vals["value_cumple"] = False

        if reset_missing or "result" in vals:
            if vals.get("result") not in ("cumple", "no_cumple"):
                vals["result"] = False

        if vals.get("value_cumple") in ("cumple", "no_cumple"):
            vals["result"] = vals["value_cumple"]
        elif vals.get("result") in ("cumple", "no_cumple"):
            vals["value_cumple"] = vals["result"]

        return vals

    def _clear_strict_na_values_hardening(self):
        for line in self:
            if not line._is_strict_binary_result_line():
                continue

            vals = {}
            if line.attribute_type != "boolean":
                vals["attribute_type"] = "boolean"
            if line.capture_zone != "additional":
                vals["capture_zone"] = "additional"
            if line.result_mode != "cumple":
                vals["result_mode"] = "cumple"
            if line.value_ok:
                vals["value_ok"] = False
            if line.value_float:
                vals["value_float"] = 0.0
            if line.value_char:
                vals["value_char"] = False
            if line.min_value:
                vals["min_value"] = 0.0
            if line.max_value:
                vals["max_value"] = 0.0
            if line.unit:
                vals["unit"] = False
            if line.allow_zero:
                vals["allow_zero"] = False

            if line.value_cumple == "na":
                vals["value_cumple"] = False
            if line.result == "na":
                vals["result"] = False

            if line.value_cumple in ("cumple", "no_cumple") and line.result != line.value_cumple:
                vals["result"] = line.value_cumple
            elif line.result in ("cumple", "no_cumple") and line.value_cumple != line.result:
                vals["value_cumple"] = line.result

            if vals:
                line.with_context(skip_strict_binary_cleanup=True).write(vals)

    @api.depends("name")
    def _compute_normalized_name(self):
        for line in self:
            line.normalized_name = _slug(line.name)

    @api.model_create_multi
    def create(self, vals_list):
        clean_vals_list = []
        Inspection = self.env["quality.inspection"]

        for vals in vals_list:
            vals = dict(vals or {})
            inspection = (
                Inspection.browse(vals["inspection_id"])
                if vals.get("inspection_id")
                else False
            )
            if inspection and inspection.process_code in STRICT_BINARY_RESULT_PROCESS_CODES:
                vals = self._normalize_vals_for_strict_binary_line(vals, reset_missing=True)
            clean_vals_list.append(vals)

        records = super().create(clean_vals_list)
        records._clear_strict_na_values_hardening()
        return records

    def write(self, vals):
        vals = dict(vals or {})
        if not vals:
            return super().write(vals)

        if not self.env.context.get("skip_strict_binary_cleanup"):
            writes_na = any(
                vals.get(field_name) == "na"
                for field_name in ("value_cumple", "value_ok", "result")
            )
            if writes_na:
                for line in self:
                    if line._is_strict_binary_result_line():
                        raise ValidationError(_(
                            "%s no permite N/A. Seleccione únicamente Cumple o No Cumple."
                        ) % line._strict_binary_process_display_name())

        strict_lines = self.filtered(lambda line: line._is_strict_binary_result_line())
        other_lines = self - strict_lines

        res = True
        if other_lines:
            res = super(QualityInspectionLineHardening, other_lines).write(vals) and res

        if strict_lines:
            strict_vals = self._normalize_vals_for_strict_binary_line(vals, reset_missing=False)
            res = super(QualityInspectionLineHardening, strict_lines).write(strict_vals) and res

        if not self.env.context.get("skip_strict_binary_cleanup"):
            self._clear_strict_na_values_hardening()

        return res

    @api.onchange("attribute_template_id")
    def _onchange_template_hardening(self):
        for line in self:
            template = line.attribute_template_id
            if not template:
                continue

            line.name = template.name
            line.attribute_type = template.attribute_type
            line.capture_zone = template.capture_zone
            line.result_mode = template.result_mode
            line.min_value = template.min_value
            line.max_value = template.max_value
            line.unit = template.unit
            line.allow_zero = template.allow_zero

            if line._is_strict_binary_result_line():
                # FOLIO-QM-ODOO18-071: Impresión y Acabado se fuerzan a Cumple/No Cumple.
                line.attribute_type = "boolean"
                line.capture_zone = "additional"
                line.result_mode = "cumple"
                line.value_ok = False
                line.value_float = 0.0
                line.value_char = False
                line.min_value = 0.0
                line.max_value = 0.0
                line.unit = False
                line.allow_zero = False
                if line.value_cumple == "na":
                    line.value_cumple = False
                if line.result == "na":
                    line.result = False

    @api.onchange("attribute_type", "result_mode")
    def _onchange_strict_binary_attribute_config(self):
        for line in self:
            if not line._is_strict_binary_result_line():
                continue

            warning = False
            if line.attribute_type != "boolean" or line.result_mode != "cumple":
                warning = True

            line.attribute_type = "boolean"
            line.capture_zone = "additional"
            line.result_mode = "cumple"
            line.value_ok = False
            line.value_float = 0.0
            line.value_char = False
            line.min_value = 0.0
            line.max_value = 0.0
            line.unit = False
            line.allow_zero = False
            if line.value_cumple == "na":
                line.value_cumple = False
            if line.result == "na":
                line.result = False

            if warning:
                return {
                    "warning": {
                        "title": _("Configuración no permitida"),
                        "message": _(
                            "%s solo permite atributos adicionales de tipo Cumple/No Cumple."
                        ) % line._strict_binary_process_display_name(),
                    }
                }

    @api.onchange("value_float", "min_value", "max_value", "attribute_type")
    def _onchange_evaluate_result_hardening(self):
        for line in self:
            if line._is_strict_binary_result_line():
                if line.attribute_type != "boolean":
                    line.attribute_type = "boolean"
                    line.capture_zone = "additional"
                    line.result_mode = "cumple"
                    line.value_float = 0.0
                    line.min_value = 0.0
                    line.max_value = 0.0
                    line.unit = False
                    line.result = line.value_cumple if line.value_cumple in ("cumple", "no_cumple") else False
                continue

            if line.attribute_type != "float":
                continue

            if not line.value_float and not line.allow_zero:
                line.result = "na"
                continue

            if line.min_value and line.value_float < line.min_value:
                line.result = "no_cumple"
            elif line.max_value and line.value_float > line.max_value:
                line.result = "no_cumple"
            else:
                line.result = "cumple"

    @api.onchange("value_cumple", "attribute_type", "result_mode")
    def _onchange_value_cumple_hardening(self):
        for line in self:
            if line.attribute_type == "boolean" and line.result_mode == "cumple":
                if line._is_strict_binary_result_line():
                    if line.value_cumple == "na":
                        line.value_cumple = False
                        line.result = False
                        return {
                            "warning": {
                                "title": _("Valor no permitido"),
                                "message": _(
                                    "%s no permite N/A. Seleccione Cumple o No Cumple."
                                ) % line._strict_binary_process_display_name(),
                            }
                        }
                    line.result = line.value_cumple or False
                else:
                    line.result = line.value_cumple or "na"

    @api.onchange("value_ok", "attribute_type", "result_mode")
    def _onchange_value_ok_hardening(self):
        for line in self:
            if line._is_strict_binary_result_line():
                if line.value_ok:
                    line.value_ok = False
                    line.result_mode = "cumple"
                    line.attribute_type = "boolean"
                    return {
                        "warning": {
                            "title": _("Modo no permitido"),
                            "message": _(
                                "%s no permite OK/NO OK/N/A. Use únicamente Cumple o No Cumple."
                            ) % line._strict_binary_process_display_name(),
                        }
                    }
                continue

            if line.attribute_type == "boolean" and line.result_mode == "ok":
                line.result = line.value_ok or "na"

    @api.constrains(
        "inspection_id",
        "sample_release_id",
        "normalized_name",
        "capture_zone",
    )
    def _check_duplicate_attribute_hardening(self):
        for line in self:
            if not line.normalized_name:
                continue

            domain = [
                ("id", "!=", line.id),
                ("normalized_name", "=", line.normalized_name),
                ("capture_zone", "=", line.capture_zone),
            ]

            if line.inspection_id:
                domain.append(("inspection_id", "=", line.inspection_id.id))
            elif line.sample_release_id:
                domain.append(("sample_release_id", "=", line.sample_release_id.id))
            else:
                continue

            if self.search_count(domain):
                raise ValidationError(
                    _("Atributo duplicado: '%s'. No se permite repetir atributos.")
                    % line.name
                )

    @api.constrains("name", "normalized_name", "capture_zone", "inspection_id")
    def _check_reserved_measure_attribute_line_hardening(self):
        """
        FOLIO-QM-ODOO18-072:
        Evita capturar en Atributos Adicionales conceptos que ya existen
        en Medidas y Propiedades del proceso actual.
        """
        for line in self:
            if not line.inspection_id or line.capture_zone != "additional":
                continue

            key = line.normalized_name or _slug(line.name)
            duplicated_label = _reserved_measure_label_for_inspection(
                line.inspection_id,
                key,
            )
            if duplicated_label:
                raise ValidationError(_(
                    "No puede capturar '%s' como Atributo Adicional porque "
                    "ya existe como campo nativo del proceso o no aplica en este proceso."
                ) % duplicated_label)

    @api.constrains("attribute_type", "result_mode", "capture_zone", "inspection_id")
    def _check_strict_binary_attribute_config(self):
        for line in self:
            if not line._is_strict_binary_result_line():
                continue

            if (
                line.attribute_type != "boolean"
                or line.result_mode != "cumple"
                or line.capture_zone != "additional"
            ):
                raise ValidationError(_(
                    "%s solo permite atributos adicionales de tipo Cumple/No Cumple."
                ) % line._strict_binary_process_display_name())

    @api.constrains("value_float", "attribute_type", "allow_zero", "result")
    def _check_zero_numeric_hardening(self):
        for line in self:
            if line._is_strict_binary_result_line():
                continue

            parent_state = (
                line.inspection_id.state
                if line.inspection_id
                else line.sample_release_id.state
                if line.sample_release_id
                else False
            )
            if parent_state in ("borrador", False):
                continue

            if (
                line.attribute_type == "float"
                and not line.allow_zero
                and not line.value_float
                and line.result != "na"
            ):
                raise ValidationError(
                    _(
                        "El atributo numérico '%s' no puede quedar en cero. "
                        "Capture el valor real o marque N/A."
                    )
                    % line.name
                )


class QualityInspectionRanuradoHardening(models.Model):
    _inherit = "quality.inspection.ranurado"

    concepto = fields.Char("Concepto", default="Largo")
    unidad = fields.Selection(
        selection_add=[("cm", "cm")],
        ondelete={"cm": "set default"},
    )
    resultado = fields.Selection(
        selection_add=[("na", "N/A")],
        ondelete={"na": "set default"},
    )

    @api.constrains("medida", "resultado")
    def _check_medida_gt_zero(self):
        for rec in self:
            if rec.resultado != "na" and rec.medida <= 0:
                raise ValidationError(
                    _("La medida debe ser mayor a cero o marcarse como N/A.")
                )


class QualityInspectionTroqueladoHardening(models.Model):
    _inherit = "quality.inspection.troquelado"

    unidad = fields.Selection(
        [
            ("mm", "mm"),
            ("cm", "cm"),
            ("in", "in"),
        ],
        default="mm",
        required=True,
    )
    resultado = fields.Selection(
        selection_add=[("na", "N/A")],
        ondelete={"na": "set default"},
    )

    @api.constrains("medida", "resultado")
    def _check_medida_gt_zero(self):
        for rec in self:
            if rec.resultado != "na" and rec.medida <= 0:
                raise ValidationError(
                    _("La medida de troquelado debe ser mayor a cero o marcarse como N/A.")
                )


class QualityInspectionHardening(models.Model):
    _inherit = "quality.inspection"

    # FOLIO-QM-ODOO18-075:
    # Leyendas se trasladan a la vista para evitar los íconos de interrogación
    # que no aportaban acción al usuario final.
    folio = fields.Char("Folio de Producción", required=True, help="")
    code = fields.Char("Código de Producto", required=True, help="")

    # FOLIO-QM-ODOO18-072 / 075:
    # Espesor no aplica en Octágono; se conserva para otros procesos.
    espesor = fields.Float("Espesor", digits=(16, 2))
    oct_espesor = fields.Float("Espesor Octágono (mm)", digits=(16, 2))

    # FOLIO-QM-ODOO18-075:
    # Octágono requiere precisión visual y de persistencia en calibración.
    ancho = fields.Float("Ancho (mm)", digits=(16, 2))
    oct_ancho = fields.Float("Ancho Octágono (mm)", digits=(16, 2))
    calibracion = fields.Float("Calibración", digits=(16, 4))
    papel_ancho = fields.Float("Ancho del Papel", digits=(16, 2))
    papel_gramaje = fields.Float("Gramaje del Papel", digits=(16, 2))
    oct_retiramiento = fields.Float("Retiramiento (cm) - Legacy", digits=(16, 2))
    reticula_extendida = fields.Float("Retiramiento / Retícula Extendida (cm)", digits=(16, 2))

    # FOLIO-QM-ODOO18-019: se evita redeclarar campos base con otro tipo
    # en hardening; solo se agregan campos nuevos o relacionados.
    capture_mode = fields.Selection(
        related="process_type_id.capture_mode",
        store=True,
        readonly=True,
    )
    date_started = fields.Datetime("Fecha de Inicio", readonly=True)
    date_closed = fields.Datetime("Fecha de Cierre", readonly=True)

    # FOLIO-QM-ODOO18-074: campos informativos para bloquear/habilitar captura por flujo.
    previous_process_type_id = fields.Many2one(
        "quality.process.type",
        string="Proceso Previo Requerido",
        compute="_compute_process_gate_hardening",
        store=False,
    )
    previous_process_inspection_id = fields.Many2one(
        "quality.inspection",
        string="Inspección Previa Liberada",
        compute="_compute_process_gate_hardening",
        store=False,
    )
    process_gate_open = fields.Boolean(
        "Ruta Habilitada",
        compute="_compute_process_gate_hardening",
        store=False,
    )
    process_gate_message = fields.Char(
        "Mensaje de Bloqueo de Ruta",
        compute="_compute_process_gate_hardening",
        store=False,
    )

    def _normalize_inspection_vals_hardening(self, vals):
        vals = dict(vals or {})
        if "espesor" in vals and vals.get("espesor") not in (False, None, ""):
            vals["espesor"] = round(float(vals["espesor"]), 2)
        if "calibracion" in vals and vals.get("calibracion") not in (False, None, ""):
            vals["calibracion"] = round(float(vals["calibracion"]), 4)
        return vals

    @api.model_create_multi
    def create(self, vals_list):
        clean_vals_list = [
            self._normalize_inspection_vals_hardening(vals)
            for vals in vals_list
        ]
        records = super().create(clean_vals_list)
        records._cleanup_octagono_not_applicable_hardening()
        return records

    def write(self, vals):
        vals = self._normalize_inspection_vals_hardening(vals)
        res = super().write(vals)
        if not self.env.context.get("skip_octagono_cleanup"):
            self._cleanup_octagono_not_applicable_hardening()
        return res

    def _cleanup_octagono_not_applicable_hardening(self):
        """
        FOLIO-QM-ODOO18-075:
        Octágono no debe conservar Espesor ni Retiramiento. Si quedaron valores
        legacy por capturas previas o por una configuración antigua, se limpian.
        """
        for rec in self.filtered(lambda item: item.process_code == "octagono"):
            vals = {}
            if rec.espesor:
                vals["espesor"] = 0.0
            if getattr(rec, "oct_espesor", 0.0):
                vals["oct_espesor"] = 0.0
            if getattr(rec, "oct_retiramiento", 0.0):
                vals["oct_retiramiento"] = 0.0
            if getattr(rec, "reticula_extendida", 0.0):
                vals["reticula_extendida"] = 0.0
            if vals:
                super(QualityInspectionHardening, rec.with_context(skip_octagono_cleanup=True)).write(vals)

    @api.onchange("espesor")
    def _onchange_round_espesor_hardening(self):
        for rec in self:
            if rec.espesor not in (False, None):
                rec.espesor = round(rec.espesor, 2)

    @api.onchange("calibracion")
    def _onchange_round_calibracion_hardening(self):
        for rec in self:
            if rec.calibracion not in (False, None):
                rec.calibracion = round(rec.calibracion, 4)

    @api.onchange("process_type_id")
    def _onchange_process_type_octagono_hardening(self):
        for rec in self:
            if rec.process_type_id and rec.process_type_id.code == "octagono":
                # FOLIO-QM-ODOO18-075: Espesor y Retiramiento no aplican en Octágono.
                rec.espesor = 0.0
                rec.oct_espesor = 0.0
                rec.oct_retiramiento = 0.0
                rec.reticula_extendida = 0.0

    @api.onchange("product_id")
    def _onchange_product_code_hardening(self):
        for rec in self:
            if rec.product_id and rec.product_id.default_code:
                rec.code = rec.product_id.default_code

    @api.depends(
        "process_type_id",
        "production_order_id",
        "lot_id",
        "folio",
        "product_id",
    )
    def _compute_process_gate_hardening(self):
        Process = self.env["quality.process.type"].sudo()
        for rec in self:
            previous_code = rec._get_previous_process_code_hardening()
            rec.previous_process_type_id = False
            rec.previous_process_inspection_id = False
            rec.process_gate_open = True
            rec.process_gate_message = False

            if not previous_code:
                continue

            previous_process = Process.search([
                ("code", "=", previous_code),
                "|",
                ("company_id", "=", rec.company_id.id),
                ("company_id", "=", False),
            ], limit=1)
            rec.previous_process_type_id = previous_process

            previous_inspection = rec._find_previous_inspection_hardening(previous_code)
            if previous_inspection:
                rec.previous_process_inspection_id = previous_inspection
                rec.process_gate_open = True
                continue

            rec.process_gate_open = False
            rec.process_gate_message = rec._build_previous_process_block_message_hardening(previous_code)

    @api.constrains("sin_supervisor", "supervisor_id")
    def _check_supervisor_or_no_supervisor(self):
        for rec in self:
            if not rec.sin_supervisor and not rec.supervisor_id:
                raise ValidationError(
                    _("Seleccione un supervisor o marque 'Sin Supervisor'.")
                )

    @api.onchange("sin_supervisor")
    def _onchange_sin_supervisor(self):
        if self.sin_supervisor:
            self.supervisor_id = False

    @api.onchange("production_order_id")
    def _onchange_production_order(self):
        # FOLIO-QM-ODOO18-020 / 075:
        # Se consolida el enlace OP -> Producto/Lote/Cliente/Código para que
        # Octágono no dependa de seleccionar productos al azar.
        if not self.production_order_id:
            return

        production = self.production_order_id
        if production.product_id:
            self.product_id = production.product_id
            self.code = production.product_id.default_code or self.code

        if not self.folio and production.name:
            self.folio = production.name

        if getattr(production, "lot_producing_id", False):
            self.lot_id = production.lot_producing_id

        sale_order = (
            self.env["sale.order"].search([("name", "=", production.origin)], limit=1)
            if production.origin
            else False
        )
        if sale_order and sale_order.partner_id:
            self.partner_id = sale_order.partner_id

    @api.onchange("process_type_id", "product_id")
    def _onchange_load_attribute_templates(self):
        # FOLIO-QM-ODOO18-070 / FOLIO-QM-ODOO18-071:
        # Acabado y Empaque e Impresión solo cargan atributos booleanos Cumple/No Cumple
        # y nunca inicializan líneas con N/A.
        if not self.process_type_id and not self.product_id:
            return

        process_code = self.process_type_id.code or self.process_code
        strict_binary = process_code in STRICT_BINARY_RESULT_PROCESS_CODES

        templates = self.env["quality.attribute.template"]
        if self.process_type_id:
            templates |= self.process_type_id.attribute_template_ids.filtered(
                lambda template: not template.product_tmpl_id and template.active
            )

        if self.product_id and self.product_id.product_tmpl_id:
            templates |= self.env["quality.attribute.template"].search(
                [
                    ("product_tmpl_id", "=", self.product_id.product_tmpl_id.id),
                    ("active", "=", True),
                ]
            )

        if strict_binary:
            templates = templates.filtered(lambda template: template.attribute_type == "boolean")

        if not templates:
            return

        lines = [(5, 0, 0)]
        seen = set()
        for template in templates.sorted(lambda item: (item.sequence, item.id)):
            key = template.normalized_name or _slug(template.name)
            if not key or key in seen:
                continue

            seen.add(key)

            if strict_binary:
                value_cumple = False
                value_ok = False
                result = False
                attribute_type = "boolean"
                result_mode = "cumple"
                capture_zone = "additional"
                min_value = 0.0
                max_value = 0.0
                unit = False
                allow_zero = False
            else:
                value_cumple = "na"
                value_ok = "na"
                result = "na"
                attribute_type = template.attribute_type
                result_mode = template.result_mode
                capture_zone = template.capture_zone
                min_value = template.min_value
                max_value = template.max_value
                unit = template.unit
                allow_zero = template.allow_zero

            lines.append(
                (
                    0,
                    0,
                    {
                        "attribute_template_id": template.id,
                        "name": template.name,
                        "attribute_type": attribute_type,
                        "capture_zone": capture_zone,
                        "result_mode": result_mode,
                        "min_value": min_value,
                        "max_value": max_value,
                        "unit": unit,
                        "allow_zero": allow_zero,
                        "sequence": template.sequence,
                        "value_cumple": value_cumple,
                        "value_ok": value_ok,
                        "result": result,
                    },
                )
            )

        self.line_ids = lines

    def _get_previous_process_code_hardening(self):
        self.ensure_one()
        code = self.process_code
        if code not in PROCESS_SEQUENCE:
            return False

        index = PROCESS_SEQUENCE.index(code)
        if index <= 0:
            return False

        return PROCESS_SEQUENCE[index - 1]

    def _get_process_context_domains_hardening(self):
        self.ensure_one()
        domains = []

        if self.production_order_id:
            domains.append((
                [("production_order_id", "=", self.production_order_id.id)],
                _("orden de producción %s") % self.production_order_id.display_name,
            ))

        if self.lot_id:
            domains.append((
                [("lot_id", "=", self.lot_id.id)],
                _("lote %s") % (self.lot_id.display_name or "—"),
            ))

        if self.folio and self.product_id:
            domains.append((
                [
                    ("folio", "=", self.folio),
                    ("product_id", "=", self.product_id.id),
                ],
                _("folio %s y producto %s") % (
                    self.folio,
                    self.product_id.display_name,
                ),
            ))

        return domains

    def _find_previous_inspection_hardening(self, previous_code, states=("aceptado",)):
        self.ensure_one()
        Inspection = self.env["quality.inspection"].sudo()

        base_domain = [
            ("id", "!=", self.id),
            ("process_code", "=", previous_code),
            ("state", "in", list(states)),
        ]

        for context_domain, _context_label in self._get_process_context_domains_hardening():
            found = Inspection.search(
                base_domain + context_domain,
                order="date_inspection desc, id desc",
                limit=1,
            )
            if found:
                return found

        return Inspection.browse()

    def _build_previous_process_block_message_hardening(self, previous_code):
        self.ensure_one()

        Process = self.env["quality.process.type"].sudo()
        previous_process = Process.search([
            ("code", "=", previous_code),
            "|",
            ("company_id", "=", self.company_id.id),
            ("company_id", "=", False),
        ], limit=1)

        previous_name = previous_process.display_name or previous_code.replace("_", " ").title()
        current_name = self.process_type_id.display_name or self.process_code or _("este proceso")

        blocking_previous = self._find_previous_inspection_hardening(
            previous_code,
            states=("borrador", "en_proceso", "retenido", "rechazado"),
        )

        if blocking_previous:
            state_label = dict(blocking_previous._fields["state"].selection).get(
                blocking_previous.state,
                blocking_previous.state,
            )
            if blocking_previous.state in ("retenido", "rechazado"):
                return _(
                    "Secuencia bloqueada: el proceso previo '%s' existe como %s "
                    "pero está en estado '%s'. No se permite movimiento ni captura "
                    "hasta que Producción marque la corrección como hecha y Calidad "
                    "lo libere."
                ) % (
                    previous_name,
                    blocking_previous.name,
                    state_label,
                )

            return _(
                "Secuencia bloqueada: el proceso previo '%s' existe como %s, "
                "pero aún no está liberado. Debe quedar Aceptado/Liberado antes "
                "de iniciar o liberar '%s'."
            ) % (
                previous_name,
                blocking_previous.name,
                current_name,
            )

        context_labels = [
            label for _domain, label in self._get_process_context_domains_hardening()
        ]
        context_text = ", ".join(context_labels) if context_labels else _("la misma orden/lote/folio")

        return _(
            "Secuencia bloqueada: antes de iniciar o liberar '%s' debe existir "
            "una inspección aceptada/liberada del proceso previo '%s' para %s."
        ) % (
            current_name,
            previous_name,
            context_text,
        )

    def _check_previous_process_hardening(self):
        for rec in self:
            previous_code = rec._get_previous_process_code_hardening()
            if not previous_code:
                continue

            previous_inspection = rec._find_previous_inspection_hardening(previous_code)
            if not previous_inspection:
                raise UserError(rec._build_previous_process_block_message_hardening(previous_code))

        return True

    def _check_reserved_duplicate_attributes_hardening(self):
        for rec in self:
            duplicates = []
            for line in rec.line_ids.filtered(lambda item: item.capture_zone == "additional"):
                key = line.normalized_name or _slug(line.name)
                duplicated_label = _reserved_measure_label_for_inspection(rec, key)
                if duplicated_label:
                    duplicates.append(duplicated_label)

            if duplicates:
                raise UserError(
                    _(
                        "Estos atributos no deben capturarse como adicionales porque "
                        "ya pertenecen al formulario del proceso o no aplican aquí: %s"
                    )
                    % ", ".join(sorted(set(duplicates)))
                )

    def _check_required_additional_attributes_hardening(self):
        for rec in self:
            if not rec.process_type_id.require_additional_attributes:
                continue

            required_lines = rec.line_ids.filtered(
                lambda line: line.attribute_template_id.is_required
                if line.attribute_template_id
                else True
            )
            if not required_lines:
                raise UserError(_("Debe capturar los atributos adicionales del proceso."))

            strict_binary = rec.process_code in STRICT_BINARY_RESULT_PROCESS_CODES

            if strict_binary:
                invalid_type = required_lines.filtered(
                    lambda line: (
                        line.attribute_type != "boolean"
                        or line.result_mode != "cumple"
                        or line.capture_zone != "additional"
                    )
                )
                if invalid_type:
                    raise UserError(_(
                        "%s solo permite atributos adicionales de tipo Cumple/No Cumple. Revise: %s"
                    ) % (
                        rec.process_type_id.display_name,
                        ", ".join(invalid_type.mapped("name")),
                    ))

                for line in required_lines:
                    if line.value_cumple in ("cumple", "no_cumple") and line.result != line.value_cumple:
                        line.result = line.value_cumple

                missing_binary = required_lines.filtered(
                    lambda line: (
                        line.value_cumple not in ("cumple", "no_cumple")
                        or line.result not in ("cumple", "no_cumple")
                    )
                )
                if missing_binary:
                    raise UserError(_(
                        "%s no permite N/A ni resultados vacíos. Seleccione Cumple o No Cumple en: %s"
                    ) % (
                        rec.process_type_id.display_name,
                        ", ".join(missing_binary.mapped("name")),
                    ))

                continue

            missing_result = required_lines.filtered(
                lambda line: not line.result
            )
            if missing_result:
                raise UserError(
                    _("Hay atributos adicionales sin dictamen: %s")
                    % ", ".join(missing_result.mapped("name"))
                )

            numeric_zero = required_lines.filtered(
                lambda line: (
                    line.attribute_type == "float"
                    and not line.allow_zero
                    and not line.value_float
                    and line.result != "na"
                )
            )
            if numeric_zero:
                raise UserError(
                    _("Se detectan atributos numéricos con valor igual a cero. Rectifique: %s")
                    % ", ".join(numeric_zero.mapped("name"))
                )

    def _check_measures_captured_hardening(self):
        for rec in self:
            # FOLIO-QM-ODOO18-070 / FOLIO-QM-ODOO18-071:
            # Procesos solo adicionales no deben validar medidas, aunque la base conserve banderas show_* antiguas.
            if rec.capture_mode == "additional_only" or rec.process_code in STRICT_BINARY_RESULT_PROCESS_CODES:
                continue

            if not rec.process_type_id.require_measures:
                continue

            # FOLIO-QM-ODOO18-075:
            # Octágono se valida por su matriz propia, sin Espesor ni Retiramiento.
            if rec.process_code == "octagono":
                missing = []

                if not (rec.ancho or getattr(rec, "oct_ancho", 0.0)):
                    missing.append("Ancho")
                if not (
                    rec.hexagono
                    or getattr(rec, "oct_hexagono_tipo", False)
                    or getattr(rec, "oct_hexagono", False)
                    or rec.tipo_hexagono
                ):
                    missing.append("Hexágono")
                if not rec.numero_corrida:
                    missing.append("Número de Corrida")
                if not rec.papel_ancho:
                    missing.append("Ancho de Papel")
                if not rec.papel_gramaje:
                    missing.append("Gramaje de Papel")
                if not rec.papel_proveedor_id:
                    missing.append("Proveedor de Rollos")
                if not rec.adhesivo_lote1:
                    missing.append("Lote 1 Adhesivo")
                if not rec.adhesivo_lote2:
                    missing.append("Lote 2 Adhesivo")
                if not rec.calibracion:
                    missing.append("Calibración")
                if not rec.engomado:
                    missing.append("Engomado")
                if not rec.oct_alineacion:
                    missing.append("Alineación")
                if rec.corte_guillotina not in ("si", "no"):
                    missing.append("Corte de Guillotina (Sí/No)")

                if missing:
                    raise UserError(
                        _("Capture la información obligatoria de Octágono antes de liberar. Faltan: %s")
                        % ", ".join(missing)
                    )
                continue

            missing = []

            if rec.show_largo and not rec.largo:
                missing.append("Largo")
            if rec.show_ancho and not (rec.ancho or getattr(rec, "oct_ancho", 0.0)):
                missing.append("Ancho")
            if rec.show_espesor and not (rec.espesor or getattr(rec, "oct_espesor", 0.0)):
                missing.append("Espesor")
            if rec.show_hexagono and not (
                rec.hexagono
                or getattr(rec, "tipo_hexagono", False)
                or getattr(rec, "oct_hexagono_tipo", False)
                or getattr(rec, "oct_hexagono", False)
            ):
                missing.append("Hexágono")
            if rec.show_resistencia and not rec.resistencia_na and not rec.resistencia:
                missing.append("Resistencia")
            if rec.show_apariencia and not rec.apariencia:
                missing.append("Apariencia")
            if rec.show_humedad and not rec.humedad_pct:
                missing.append("Humedad")
            if rec.show_pegado and not rec.pegado_result:
                missing.append("Resultado de Pegado")
            if rec.show_retiramiento and not (
                getattr(rec, "oct_retiramiento", 0.0)
                or getattr(rec, "reticula_extendida", 0.0)
            ):
                missing.append("Retícula Extendida / Restiramiento")
            if rec.show_calibracion and not rec.calibracion:
                missing.append("Calibración")
            if rec.show_engomado and not rec.engomado:
                missing.append("Engomado")
            if rec.show_alineacion and not rec.oct_alineacion:
                missing.append("Alineación")
            if rec.show_numero_corrida and not rec.numero_corrida:
                missing.append("Número de Corrida")
            if rec.show_tipo_hexagono and not rec.tipo_hexagono:
                missing.append("Tipo de Hexágono")

            if rec.show_papel:
                if not rec.papel_ancho:
                    missing.append("Ancho de Papel")
                if not rec.papel_gramaje:
                    missing.append("Gramaje de Papel")
                if not rec.papel_proveedor_id:
                    missing.append("Proveedor de Papel")

            if rec.show_adhesivo and not (rec.adhesivo_lote1 or rec.adhesivo_lote2):
                missing.append("Lote de Adhesivo")

            if rec.show_corte_guillotina and not rec.corte_guillotina:
                missing.append("Corte en Guillotina")

            if rec.process_code == "troquelado_plano" and not rec.troquelado_ids:
                missing.append("Pestaña Troquelado")

            if (
                rec.process_code == "sierras_ranuradoras"
                and rec.show_ranurado
                and not rec.ranurado_ids
            ):
                missing.append("Pestaña Ranurado / Corte Sierra")

            if missing:
                raise UserError(
                    _("Capture la información obligatoria antes de liberar. Faltan: %s")
                    % ", ".join(missing)
                )

    def _full_quality_validation_hardening(self):
        for rec in self:
            if rec.state != "en_proceso":
                raise UserError(_("Debe presionar 'INICIAR INSPECCIÓN' antes de liberar."))

            rec._check_reserved_duplicate_attributes_hardening()
            rec._check_measures_captured_hardening()
            rec._check_required_additional_attributes_hardening()
            rec._check_previous_process_hardening()

    def _sync_strict_binary_lines_hardening(self):
        for rec in self.filtered(lambda item: item.process_code in STRICT_BINARY_RESULT_PROCESS_CODES):
            for line in rec.line_ids:
                vals = {}

                if line.attribute_type != "boolean":
                    vals["attribute_type"] = "boolean"
                if line.capture_zone != "additional":
                    vals["capture_zone"] = "additional"
                if line.result_mode != "cumple":
                    vals["result_mode"] = "cumple"
                if line.value_ok:
                    vals["value_ok"] = False
                if line.value_float:
                    vals["value_float"] = 0.0
                if line.value_char:
                    vals["value_char"] = False
                if line.min_value:
                    vals["min_value"] = 0.0
                if line.max_value:
                    vals["max_value"] = 0.0
                if line.unit:
                    vals["unit"] = False
                if line.allow_zero:
                    vals["allow_zero"] = False

                if line.value_cumple == "na":
                    vals["value_cumple"] = False
                if line.value_ok == "na":
                    vals["value_ok"] = False
                if line.result == "na":
                    vals["result"] = False

                if line.value_cumple in ("cumple", "no_cumple") and line.result != line.value_cumple:
                    vals["result"] = line.value_cumple
                elif line.result in ("cumple", "no_cumple") and line.value_cumple != line.result:
                    vals["value_cumple"] = line.result

                if vals:
                    line.write(vals)

    def action_start(self):
        for rec in self:
            # FOLIO-QM-ODOO18-074: no se permite iniciar captura si el proceso previo no está liberado.
            rec._check_previous_process_hardening()
            rec.date_started = fields.Datetime.now()
            rec.state = "en_proceso"
            rec._sync_strict_binary_lines_hardening()
            rec.message_post(
                body=_("Inspección iniciada."),
                subtype_xmlid="mail.mt_comment",
            )

    def action_accept(self):
        for rec in self:
            rec._full_quality_validation_hardening()
            rec.state = "aceptado"
            rec.date_closed = fields.Datetime.now()
            rec.message_post(
                body=_("Inspección ACEPTADA/LIBERADA por %s.") % self.env.user.name,
                subtype_xmlid="mail.mt_comment",
            )

    def _get_supervisor_user_hardening(self):
        self.ensure_one()
        if self.supervisor_id and self.supervisor_id.user_id:
            return self.supervisor_id.user_id
        return False

    def action_retain(self):
        for rec in self:
            if rec.state != "en_proceso":
                raise UserError(_("Solo se puede retener una inspección en proceso."))

            rec._check_reserved_duplicate_attributes_hardening()
            rec.state = "retenido"

            supervisor_user = rec._get_supervisor_user_hardening()
            partner_ids = []

            if supervisor_user and supervisor_user.partner_id:
                partner_ids = [supervisor_user.partner_id.id]
                rec.message_subscribe(partner_ids=partner_ids)
                rec.activity_schedule(
                    "mail.mail_activity_data_todo",
                    date_deadline=fields.Date.today() + timedelta(days=1),
                    summary=_("Producto retenido en Calidad: %s") % rec.name,
                    user_id=supervisor_user.id,
                )

            rec.message_post(
                body=_(
                    "Producto RETENIDO por %s. Supervisor en turno: %s. "
                    "Cuando Producción marque HECHO, Calidad debe validar nuevamente."
                )
                % (
                    self.env.user.name,
                    rec.supervisor_id.name if rec.supervisor_id else "Sin supervisor",
                ),
                partner_ids=partner_ids,
                subtype_xmlid="mail.mt_comment",
            )

    def action_reject(self):
        for rec in self:
            if rec.state != "en_proceso":
                raise UserError(_("Solo se puede rechazar una inspección en proceso."))
            rec.state = "rechazado"
            rec.date_closed = fields.Datetime.now()
            rec.message_post(
                body=_("Inspección RECHAZADA por %s.") % self.env.user.name,
                subtype_xmlid="mail.mt_comment",
            )


class QualityCertificateHardening(models.Model):
    _inherit = "quality.certificate"

    certified_hexagono_label = fields.Char("Hexágono")
    certified_retiramiento = fields.Float("Retiramiento", digits=(16, 2))
    certified_calibracion = fields.Float("Calibración", digits=(16, 4))

    @api.constrains("inspection_id")
    def _check_inspection_accepted_hardening(self):
        for rec in self:
            if rec.inspection_id and rec.inspection_id.state != "aceptado":
                raise ValidationError(_("Solo se puede certificar una inspección aceptada."))

    @api.constrains("attribute_ids")
    def _check_attribute_dedup_and_source_hardening(self):
        for rec in self:
            names = []
            for line in rec.attribute_ids:
                if line.inspection_id != rec.inspection_id:
                    raise ValidationError(
                        _("El certificado solo puede contener atributos de la inspección fuente.")
                    )

                key = line.normalized_name or _slug(line.name)
                if key:
                    names.append(key)

                if line.attribute_type == "float" and not line.allow_zero and not line.value_float:
                    raise ValidationError(
                        _("No se puede certificar el atributo '%s' con valor 0.")
                        % line.name
                    )

                if line.result not in ("cumple", "ok"):
                    raise ValidationError(
                        _("Solo se pueden certificar atributos con resultado Cumple/OK.")
                    )

            if len(names) != len(set(names)):
                raise ValidationError(_("Hay atributos repetidos en el certificado."))

    def action_generate(self):
        for rec in self:
            if rec.inspection_id.state != "aceptado":
                raise UserError(_("Solo se puede generar certificado desde inspección aceptada."))
            rec.state = "generado"


class QualityActionLineHardening(models.Model):
    _inherit = "quality.action.line"

    def write(self, vals):
        res = super().write(vals)
        if "evidence_ids" in vals:
            for line in self:
                if line.evidence_ids and line.state == "pendiente":
                    line.state = "en_proceso"
        return res

    def action_complete(self):
        for rec in self:
            if not rec.evidence_ids:
                raise UserError(_("No se puede completar la acción sin adjuntar evidencia."))
            rec.state = "completada"
            rec.date_completed = fields.Date.today()


class QualityCustomerDocumentHardening(models.Model):
    _inherit = "quality.customer.document"

    def action_send(self):
        for rec in self:
            has_doc = (
                rec.main_pdf
                or rec.main_image
                or rec.result_document_ids
                or rec.client_format_ids
            )
            if not has_doc:
                raise UserError(
                    _("No puede marcar como enviado si no existe documento cargado.")
                )
            rec.state = "enviado"