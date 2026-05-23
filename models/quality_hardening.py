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
STRICT_BINARY_RESULT_PROCESS_CODES = {
    "acabado_empaque",
    "impresion",
}

# FOLIO-QM-ODOO18-081:
# Resultados finales normalizados para evitar que N/A se use como valor
# automático cuando el atributo realmente debe capturarse.
PASS_RESULTS = {"cumple", "ok"}
FAIL_RESULTS = {"no_cumple", "no_ok"}
VALID_FINAL_RESULTS = PASS_RESULTS | FAIL_RESULTS
NA_RESULTS = {"na"}

CUMPLE_VALUES = {"cumple", "no_cumple"}
OK_VALUES = {"ok", "no_ok"}
OK_TO_CUMPLE_RESULT = {"ok": "cumple", "no_ok": "no_cumple"}


def _split_selection_options(value):
    """Convierte "A,B,C" en una lista limpia de opciones."""
    if not value:
        return []
    return [item.strip() for item in str(value).split(",") if item and item.strip()]


def _float_is_captured(value, allow_zero=False):
    if value in (False, None, ""):
        return False
    if float(value or 0.0) == 0.0 and not allow_zero:
        return False
    return True


def _quality_line_vals_has_user_content(vals):
    """
    Detecta si una línea manual tiene contenido real.

    Una línea creada accidentalmente por la lista editable suele llegar solo
    con defaults técnicos: attribute_type, result_mode, capture_zone, ceros, etc.
    Esa línea se puede ignorar. Si trae valor, rango, nota, resultado o N/A,
    entonces sí debe exigir Nombre del Atributo.
    """
    vals = vals or {}

    if vals.get("attribute_template_id"):
        return True

    if (vals.get("name") or "").strip():
        return True

    text_fields = (
        "value_char",
        "value_selection",
        "value_cumple",
        "value_cumple_required",
        "value_ok",
        "value_ok_required",
        "result",
        "result_required",
        "notes",
        "unit",
        "selection_options",
    )
    if any(vals.get(field_name) for field_name in text_fields):
        return True

    numeric_fields = ("value_float", "min_value", "max_value")
    for field_name in numeric_fields:
        try:
            if float(vals.get(field_name) or 0.0) != 0.0:
                return True
        except (TypeError, ValueError):
            return True

    if vals.get("allow_zero") or vals.get("allow_not_applicable") or vals.get("is_not_applicable"):
        return True

    return False


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
    allow_resistencia_na = fields.Boolean(
        "Permitir N/A en Resistencia",
        default=False,
        help=(
            "Si está activo, el proceso permite marcar Resistencia como No aplica. "
            "Si está apagado y el proceso muestra Resistencia, la captura es obligatoria."
        ),
    )
    allow_hexagono_na = fields.Boolean(
        "Permitir N/A en Hexágono",
        default=False,
        help=(
            "Si está activo, el proceso permite marcar Hexágono como No aplica. "
            "Si está apagado y el proceso muestra Hexágono, la captura es obligatoria."
        ),
    )


class QualityAttributeTemplateHardening(models.Model):
    _inherit = "quality.attribute.template"

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
            ("cumple", "Cumple / No Cumple"),
            ("ok", "OK / NO OK"),
        ],
        default="cumple",
        required=True,
        help=(
            "Define el par de resultados del atributo. N/A ya no se usa como "
            "opción automática; se habilita por separado con 'Permitir No aplica'."
        ),
    )
    allow_zero = fields.Boolean("Permitir valor cero", default=False)
    allow_not_applicable = fields.Boolean(
        "Permitir No aplica",
        default=False,
        help=(
            "Actívelo solo cuando el atributo realmente pueda quedar como N/A. "
            "Si está apagado, la captura queda obligatoria y no se acepta N/A."
        ),
    )

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

    def _normalize_template_vals_by_type(self, vals, current=False):
        vals = dict(vals or {})
        attribute_type = vals.get(
            "attribute_type",
            current.attribute_type if current else "float",
        )

        if attribute_type == "boolean":
            vals.update({
                "capture_zone": vals.get("capture_zone") or "additional",
                "min_value": 0.0,
                "max_value": 0.0,
                "unit": False,
                "selection_options": False,
                "allow_zero": False,
            })

        elif attribute_type == "selection":
            vals.update({
                "min_value": 0.0,
                "max_value": 0.0,
                "unit": False,
                "allow_zero": False,
            })

        elif attribute_type == "char":
            vals.update({
                "min_value": 0.0,
                "max_value": 0.0,
                "unit": False,
                "selection_options": False,
                "allow_zero": False,
            })

        elif attribute_type == "float":
            vals.update({
                "selection_options": False,
                "result_mode": "cumple",
            })

        return vals

    def _normalize_template_vals_for_strict_binary(self, vals):
        vals = dict(vals or {})
        vals.update({
            "attribute_type": "boolean",
            "capture_zone": "additional",
            "result_mode": "cumple",
            "allow_zero": False,
            "allow_not_applicable": False,
            "min_value": 0.0,
            "max_value": 0.0,
            "unit": False,
            "selection_options": False,
        })
        return vals

    @api.onchange("attribute_type")
    def _onchange_attribute_type_clean_config(self):
        for rec in self:
            if rec.attribute_type == "boolean":
                rec.min_value = 0.0
                rec.max_value = 0.0
                rec.unit = False
                rec.selection_options = False
                rec.allow_zero = False
            elif rec.attribute_type == "selection":
                rec.min_value = 0.0
                rec.max_value = 0.0
                rec.unit = False
                rec.allow_zero = False
            elif rec.attribute_type == "char":
                rec.min_value = 0.0
                rec.max_value = 0.0
                rec.unit = False
                rec.selection_options = False
                rec.allow_zero = False
            elif rec.attribute_type == "float":
                rec.selection_options = False
                rec.result_mode = "cumple"

    @api.onchange("process_type_id", "attribute_type", "result_mode", "allow_not_applicable")
    def _onchange_strict_binary_template(self):
        for rec in self:
            if rec.process_type_id and rec.process_type_id.code in STRICT_BINARY_RESULT_PROCESS_CODES:
                rec.attribute_type = "boolean"
                rec.capture_zone = "additional"
                rec.result_mode = "cumple"
                rec.allow_zero = False
                rec.allow_not_applicable = False
                rec.min_value = 0.0
                rec.max_value = 0.0
                rec.unit = False
                rec.selection_options = False

    @api.constrains(
        "attribute_type",
        "unit",
        "min_value",
        "max_value",
        "selection_options",
        "allow_zero",
        "allow_not_applicable",
        "process_type_id",
    )
    def _check_attribute_type_configuration_hardening(self):
        for rec in self:
            if rec.process_type_id and rec.process_type_id.code in STRICT_BINARY_RESULT_PROCESS_CODES:
                if (
                    rec.attribute_type != "boolean"
                    or rec.result_mode != "cumple"
                    or rec.allow_not_applicable
                    or rec.unit
                    or rec.min_value
                    or rec.max_value
                    or rec.selection_options
                ):
                    raise ValidationError(_(
                        "%s solo permite atributos adicionales Cumple/No Cumple; "
                        "no permite N/A, unidad, mínimo, máximo ni valor numérico."
                    ) % rec.process_type_id.display_name)

            if rec.attribute_type == "boolean":
                if rec.unit or rec.min_value or rec.max_value or rec.selection_options or rec.allow_zero:
                    raise ValidationError(_(
                        "El atributo '%s' es Cumple/No Cumple y no debe tener "
                        "unidad, mínimo, máximo, opciones de selección ni valor numérico."
                    ) % rec.name)

            if rec.attribute_type == "selection" and not rec.selection_options:
                raise ValidationError(_(
                    "El atributo de selección '%s' debe tener opciones separadas por coma."
                ) % rec.name)

            if rec.attribute_type != "float" and rec.allow_zero:
                raise ValidationError(_(
                    "Permitir cero solo aplica a atributos numéricos."
                ))

            if rec.attribute_type == "float" and rec.min_value and rec.max_value and rec.min_value > rec.max_value:
                raise ValidationError(_(
                    "En '%s', el valor mínimo no puede ser mayor que el máximo."
                ) % rec.name)

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
            else:
                vals = self._normalize_template_vals_by_type(vals)
            clean_vals_list.append(vals)

        return super().create(clean_vals_list)

    def write(self, vals):
        vals = dict(vals or {})
        if not vals:
            return super().write(vals)

        result = True
        for rec in self:
            write_vals = dict(vals)
            if rec._target_process_is_strict_binary(write_vals):
                write_vals = rec._normalize_template_vals_for_strict_binary(write_vals)
            else:
                write_vals = rec._normalize_template_vals_by_type(write_vals, current=rec)

            result = super(QualityAttributeTemplateHardening, rec).write(write_vals) and result

        return result


class QualityInspectionLineHardening(models.Model):
    _inherit = "quality.inspection.line"

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
            ("cumple", "Cumple / No Cumple"),
            ("ok", "OK / NO OK"),
        ],
        default="cumple",
        required=True,
    )

    value_cumple = fields.Selection(
        selection_add=[("na", "N/A")],
        ondelete={"na": "set default"},
        default=False,
    )
    value_cumple_required = fields.Selection(
        [
            ("cumple", "Cumple"),
            ("no_cumple", "No Cumple"),
        ],
        string="Cumple/No Cumple",
        default=False,
    )
    value_ok = fields.Selection(
        [
            ("ok", "OK"),
            ("no_ok", "NO OK"),
            ("na", "N/A"),
        ],
        string="OK/NO OK/N/A",
        default=False,
    )
    value_ok_required = fields.Selection(
        [
            ("ok", "OK"),
            ("no_ok", "NO OK"),
        ],
        string="OK/NO OK",
        default=False,
    )
    value_selection = fields.Char("Valor Selección")
    selection_options = fields.Char("Opciones de Selección")
    result_required = fields.Selection(
        [
            ("cumple", "Cumple"),
            ("no_cumple", "No Cumple"),
            ("ok", "OK"),
            ("no_ok", "NO OK"),
        ],
        string="Resultado",
        default=False,
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
        default=False,
    )
    allow_zero = fields.Boolean("Permitir cero")
    allow_not_applicable = fields.Boolean("Permitir No aplica")
    is_not_applicable = fields.Boolean("No aplica")

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

        cr.execute("""
            SELECT column_name
              FROM information_schema.columns
             WHERE table_name = 'quality_inspection'
        """)
        inspection_columns = {row[0] for row in cr.fetchall()}

        if "process_code" not in inspection_columns:
            return

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

        # Limpieza de datos heredados en procesos que no permiten N/A.
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

        optional_columns = {
            "value_cumple_required",
            "value_ok_required",
            "result_required",
            "is_not_applicable",
            "allow_not_applicable",
            "selection_options",
            "value_selection",
        }
        if optional_columns.issubset(line_columns):
            cr.execute("""
                UPDATE quality_inspection_line
                   SET value_cumple_required = CASE
                           WHEN value_cumple IN ('cumple','no_cumple') THEN value_cumple
                           WHEN result IN ('cumple','no_cumple') THEN result
                           ELSE NULL
                       END,
                       value_ok_required = CASE
                           WHEN value_ok IN ('ok','no_ok') THEN value_ok
                           WHEN result IN ('ok','no_ok') THEN result
                           ELSE NULL
                       END,
                       result_required = CASE
                           WHEN result IN ('cumple','no_cumple','ok','no_ok') THEN result
                           ELSE NULL
                       END,
                       is_not_applicable = CASE WHEN COALESCE(allow_not_applicable, FALSE) AND result = 'na' THEN TRUE ELSE FALSE END,
                       allow_not_applicable = COALESCE(allow_not_applicable, FALSE)
                 WHERE value_cumple_required IS NULL
                    OR value_ok_required IS NULL
                    OR result_required IS NULL
                    OR is_not_applicable IS NULL
            """)


            # Limpieza específica para Liberación de Muestras:
            # - Booleanos siempre quedan en Cumple/No Cumple.
            # - OK/NO OK histórico se mapea a Cumple/No Cumple.
            # - N/A solo permanece si allow_not_applicable=True y fue marcado.
            cr.execute("""
                WITH sample_boolean AS (
                    SELECT
                        id,
                        CASE
                            WHEN value_cumple_required IN ('cumple','no_cumple') THEN value_cumple_required
                            WHEN value_cumple IN ('cumple','no_cumple') THEN value_cumple
                            WHEN result_required IN ('cumple','no_cumple') THEN result_required
                            WHEN result IN ('cumple','no_cumple') THEN result
                            WHEN value_ok_required = 'ok' THEN 'cumple'
                            WHEN value_ok_required = 'no_ok' THEN 'no_cumple'
                            WHEN value_ok = 'ok' THEN 'cumple'
                            WHEN value_ok = 'no_ok' THEN 'no_cumple'
                            WHEN result_required = 'ok' THEN 'cumple'
                            WHEN result_required = 'no_ok' THEN 'no_cumple'
                            WHEN result = 'ok' THEN 'cumple'
                            WHEN result = 'no_ok' THEN 'no_cumple'
                            ELSE NULL
                        END AS normalized_result,
                        (
                            COALESCE(allow_not_applicable, FALSE)
                            AND (
                                COALESCE(is_not_applicable, FALSE)
                                OR value_cumple = 'na'
                                OR value_ok = 'na'
                                OR result = 'na'
                            )
                        ) AS keep_na
                    FROM quality_inspection_line
                    WHERE sample_release_id IS NOT NULL
                      AND attribute_type = 'boolean'
                )
                UPDATE quality_inspection_line AS line
                   SET result_mode = 'cumple',
                       capture_zone = 'additional',
                       value_ok = NULL,
                       value_ok_required = NULL,
                       value_float = 0,
                       value_char = NULL,
                       value_selection = NULL,
                       selection_options = NULL,
                       min_value = 0,
                       max_value = 0,
                       unit = NULL,
                       allow_zero = FALSE,
                       value_cumple = CASE
                           WHEN sample_boolean.normalized_result IS NOT NULL THEN sample_boolean.normalized_result
                           ELSE NULL
                       END,
                       value_cumple_required = CASE
                           WHEN sample_boolean.normalized_result IS NOT NULL THEN sample_boolean.normalized_result
                           ELSE NULL
                       END,
                       result = CASE
                           WHEN sample_boolean.normalized_result IS NOT NULL THEN sample_boolean.normalized_result
                           WHEN sample_boolean.keep_na THEN 'na'
                           ELSE NULL
                       END,
                       result_required = CASE
                           WHEN sample_boolean.normalized_result IS NOT NULL THEN sample_boolean.normalized_result
                           ELSE NULL
                       END,
                       is_not_applicable = CASE
                           WHEN sample_boolean.normalized_result IS NOT NULL THEN FALSE
                           WHEN sample_boolean.keep_na THEN TRUE
                           ELSE FALSE
                       END,
                       allow_not_applicable = COALESCE(line.allow_not_applicable, FALSE)
                  FROM sample_boolean
                 WHERE line.id = sample_boolean.id
            """)

            cr.execute("""
                UPDATE quality_inspection_line
                   SET result = NULL,
                       result_required = NULL,
                       is_not_applicable = FALSE,
                       value_cumple = CASE WHEN value_cumple = 'na' THEN NULL ELSE value_cumple END,
                       value_ok = CASE WHEN value_ok = 'na' THEN NULL ELSE value_ok END
                 WHERE sample_release_id IS NOT NULL
                   AND NOT COALESCE(allow_not_applicable, FALSE)
                   AND (
                       result = 'na'
                       OR COALESCE(is_not_applicable, FALSE)
                       OR value_cumple = 'na'
                       OR value_ok = 'na'
                   )
            """)

    @api.depends("inspection_id.process_code")
    def _compute_strict_binary_result(self):
        for line in self:
            line.strict_binary_result = (
                line.inspection_id.process_code in STRICT_BINARY_RESULT_PROCESS_CODES
                if line.inspection_id
                else False
            )

    @api.depends("name")
    def _compute_normalized_name(self):
        for line in self:
            line.normalized_name = _slug(line.name)

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

    def _apply_template_vals_to_line_create(self, vals):
        vals = dict(vals or {})
        template = (
            self.env["quality.attribute.template"].browse(vals["attribute_template_id"]).exists()
            if vals.get("attribute_template_id")
            else False
        )
        if not template:
            return vals

        defaults = {
            "name": template.name,
            "attribute_type": template.attribute_type,
            "capture_zone": getattr(template, "capture_zone", False) or "additional",
            "result_mode": getattr(template, "result_mode", False) or "cumple",
            "min_value": template.min_value,
            "max_value": template.max_value,
            "unit": template.unit,
            "allow_zero": getattr(template, "allow_zero", False),
            "allow_not_applicable": getattr(template, "allow_not_applicable", False),
            "selection_options": template.selection_options,
            "sequence": template.sequence,
        }
        for key, value in defaults.items():
            vals.setdefault(key, value)

        return vals

    def _normalize_vals_for_strict_binary_line(self, vals, reset_missing=False):
        vals = dict(vals or {})

        source = (
            vals.get("value_cumple_required")
            or vals.get("value_cumple")
            or vals.get("result")
        )
        if source not in CUMPLE_VALUES:
            source = False

        vals.update({
            "attribute_type": "boolean",
            "capture_zone": "additional",
            "result_mode": "cumple",
            "allow_not_applicable": False,
            "is_not_applicable": False,
            "value_ok": False,
            "value_ok_required": False,
            "value_float": 0.0,
            "value_char": False,
            "value_selection": False,
            "selection_options": False,
            "min_value": 0.0,
            "max_value": 0.0,
            "unit": False,
            "allow_zero": False,
        })

        if reset_missing or "value_cumple" in vals or "value_cumple_required" in vals or "result" in vals:
            vals["value_cumple"] = source or False
            vals["value_cumple_required"] = source or False
            vals["result"] = source or False
            vals["result_required"] = source or False

        return vals

    def _normalize_input_vals_hardening(self, vals):
        vals = dict(vals or {})

        if vals.get("is_not_applicable"):
            vals["result"] = "na"
            vals["result_required"] = False
            vals["value_cumple"] = False
            vals["value_cumple_required"] = False
            vals["value_ok"] = False
            vals["value_ok_required"] = False
            vals["value_float"] = 0.0
            vals["value_char"] = False
            vals["value_selection"] = False
            return vals

        if "is_not_applicable" in vals and not vals.get("is_not_applicable"):
            if vals.get("result") == "na" or "result" not in vals:
                vals["result"] = False
            if vals.get("result_required") == "na" or "result_required" not in vals:
                vals["result_required"] = False

        if vals.get("value_cumple_required") in CUMPLE_VALUES:
            vals["is_not_applicable"] = False
            vals["value_cumple"] = vals["value_cumple_required"]
            vals["result"] = vals["value_cumple_required"]
            vals["result_required"] = vals["value_cumple_required"]

        if vals.get("value_cumple") in CUMPLE_VALUES:
            vals["is_not_applicable"] = False
            vals["value_cumple_required"] = vals["value_cumple"]
            vals["result"] = vals["value_cumple"]
            vals["result_required"] = vals["value_cumple"]

        if vals.get("value_ok_required") in OK_VALUES:
            vals["is_not_applicable"] = False
            vals["value_ok"] = vals["value_ok_required"]
            vals["result"] = vals["value_ok_required"]
            vals["result_required"] = vals["value_ok_required"]

        if vals.get("value_ok") in OK_VALUES:
            vals["is_not_applicable"] = False
            vals["value_ok_required"] = vals["value_ok"]
            vals["result"] = vals["value_ok"]
            vals["result_required"] = vals["value_ok"]

        if vals.get("result_required") in VALID_FINAL_RESULTS:
            vals["is_not_applicable"] = False
            vals["result"] = vals["result_required"]

        if vals.get("result") in VALID_FINAL_RESULTS:
            vals["is_not_applicable"] = False
            vals["result_required"] = vals["result"]

        if "value_selection" in vals and vals.get("value_selection"):
            vals.setdefault("value_char", vals.get("value_selection"))

        return vals

    def _get_synced_vals_hardening(self):
        self.ensure_one()
        vals = {}

        def set_value(field_name, value):
            if field_name in self._fields and self[field_name] != value:
                vals[field_name] = value

        if self._is_strict_binary_result_line():
            source = (
                self.value_cumple_required
                or (self.value_cumple if self.value_cumple in CUMPLE_VALUES else False)
                or (self.result if self.result in CUMPLE_VALUES else False)
            )

            set_value("attribute_type", "boolean")
            set_value("capture_zone", "additional")
            set_value("result_mode", "cumple")
            set_value("allow_not_applicable", False)
            set_value("is_not_applicable", False)
            set_value("value_ok", False)
            set_value("value_ok_required", False)
            set_value("value_float", 0.0)
            set_value("value_char", False)
            set_value("value_selection", False)
            set_value("selection_options", False)
            set_value("min_value", 0.0)
            set_value("max_value", 0.0)
            set_value("unit", False)
            set_value("allow_zero", False)
            set_value("value_cumple", source or False)
            set_value("value_cumple_required", source or False)
            set_value("result", source or False)
            set_value("result_required", source or False)
            return vals

        if self.sample_release_id and self.attribute_type == "boolean":
            source = (
                self.value_cumple_required
                or (self.value_cumple if self.value_cumple in CUMPLE_VALUES else False)
                or (self.result_required if self.result_required in CUMPLE_VALUES else False)
                or (self.result if self.result in CUMPLE_VALUES else False)
            )
            if not source:
                ok_source = (
                    self.value_ok_required
                    or (self.value_ok if self.value_ok in OK_VALUES else False)
                    or (self.result_required if self.result_required in OK_VALUES else False)
                    or (self.result if self.result in OK_VALUES else False)
                )
                source = OK_TO_CUMPLE_RESULT.get(ok_source)

            wants_na = bool(
                self.allow_not_applicable
                and not source
                and (
                    self.is_not_applicable
                    or self.result == "na"
                    or self.value_cumple == "na"
                    or self.value_ok == "na"
                )
            )

            set_value("capture_zone", "additional")
            set_value("result_mode", "cumple")
            set_value("value_ok", False)
            set_value("value_ok_required", False)
            set_value("value_float", 0.0)
            set_value("value_char", False)
            set_value("value_selection", False)
            set_value("selection_options", False)
            set_value("min_value", 0.0)
            set_value("max_value", 0.0)
            set_value("unit", False)
            set_value("allow_zero", False)

            if wants_na:
                set_value("is_not_applicable", True)
                set_value("value_cumple", False)
                set_value("value_cumple_required", False)
                set_value("result", "na")
                set_value("result_required", False)
            else:
                set_value("is_not_applicable", False)
                set_value("value_cumple", source or False)
                set_value("value_cumple_required", source or False)
                set_value("result", source or False)
                set_value("result_required", source or False)

            return vals

        if self.result == "na" and self.allow_not_applicable and not self.is_not_applicable:
            set_value("is_not_applicable", True)

        if self.is_not_applicable:
            if self.allow_not_applicable:
                set_value("result", "na")
                set_value("result_required", False)
                set_value("value_cumple", False)
                set_value("value_cumple_required", False)
                set_value("value_ok", False)
                set_value("value_ok_required", False)
                set_value("value_float", 0.0)
                set_value("value_char", False)
                set_value("value_selection", False)
            else:
                set_value("is_not_applicable", False)
                set_value("result", False)
            return vals

        if self.result == "na" and not self.allow_not_applicable:
            set_value("result", False)

        if self.attribute_type == "boolean":
            if self.result_mode == "ok":
                source = (
                    self.value_ok_required
                    or (self.value_ok if self.value_ok in OK_VALUES else False)
                    or (self.result if self.result in OK_VALUES else False)
                )
                set_value("value_ok", source or False)
                set_value("value_ok_required", source or False)
                set_value("result", source or False)
                set_value("result_required", source or False)
                set_value("value_cumple", False)
                set_value("value_cumple_required", False)
            else:
                source = (
                    self.value_cumple_required
                    or (self.value_cumple if self.value_cumple in CUMPLE_VALUES else False)
                    or (self.result if self.result in CUMPLE_VALUES else False)
                )
                set_value("result_mode", "cumple")
                set_value("value_cumple", source or False)
                set_value("value_cumple_required", source or False)
                set_value("result", source or False)
                set_value("result_required", source or False)
                set_value("value_ok", False)
                set_value("value_ok_required", False)

            set_value("value_float", 0.0)
            set_value("value_char", False)
            set_value("value_selection", False)
            set_value("selection_options", False)
            set_value("min_value", 0.0)
            set_value("max_value", 0.0)
            set_value("unit", False)
            set_value("allow_zero", False)

        elif self.attribute_type == "float":
            set_value("result_mode", "cumple")
            set_value("value_cumple", False)
            set_value("value_cumple_required", False)
            set_value("value_ok", False)
            set_value("value_ok_required", False)
            set_value("value_char", False)
            set_value("value_selection", False)
            set_value("selection_options", False)

            if not _float_is_captured(self.value_float, allow_zero=self.allow_zero):
                set_value("result", False)
                set_value("result_required", False)
            elif not self.min_value and not self.max_value:
                set_value("result", False)
                set_value("result_required", False)
            elif self.min_value and self.value_float < self.min_value:
                set_value("result", "no_cumple")
                set_value("result_required", "no_cumple")
            elif self.max_value and self.value_float > self.max_value:
                set_value("result", "no_cumple")
                set_value("result_required", "no_cumple")
            else:
                set_value("result", "cumple")
                set_value("result_required", "cumple")

        elif self.attribute_type in ("selection", "char"):
            if self.attribute_type == "selection":
                if self.value_selection and self.value_char != self.value_selection:
                    set_value("value_char", self.value_selection)
                elif self.value_char and not self.value_selection:
                    set_value("value_selection", self.value_char)
                set_value("unit", False)
                set_value("min_value", 0.0)
                set_value("max_value", 0.0)
                set_value("allow_zero", False)
            else:
                set_value("value_selection", False)
                set_value("selection_options", False)
                set_value("unit", False)
                set_value("min_value", 0.0)
                set_value("max_value", 0.0)
                set_value("allow_zero", False)

            source = (
                self.result_required
                if self.result_required in VALID_FINAL_RESULTS
                else self.result if self.result in VALID_FINAL_RESULTS
                else False
            )
            set_value("result", source or False)
            set_value("result_required", source or False)
            set_value("value_cumple", False)
            set_value("value_cumple_required", False)
            set_value("value_ok", False)
            set_value("value_ok_required", False)

        return vals

    def _sync_line_result_hardening(self):
        if self.env.context.get("skip_quality_line_sync"):
            return
        for line in self:
            vals = line._get_synced_vals_hardening()
            if vals:
                line.with_context(skip_quality_line_sync=True).write(vals)

    def _clear_strict_na_values_hardening(self):
        self._sync_line_result_hardening()

    @api.model_create_multi
    def create(self, vals_list):
        clean_vals_list = []
        Inspection = self.env["quality.inspection"]

        for vals in vals_list:
            vals = self._apply_template_vals_to_line_create(vals)

            if not (vals.get("name") or "").strip():
                if vals.get("attribute_template_id"):
                    template = self.env["quality.attribute.template"].browse(
                        vals["attribute_template_id"]
                    ).exists()
                    if template and template.name:
                        vals["name"] = template.name

            if not (vals.get("name") or "").strip():
                raise ValidationError(_(
                    "Capture el Nombre del Atributo antes de guardar la línea de inspección. "
                    "Si no desea agregar un atributo manual, elimine la línea vacía."
                ))

            vals = self._normalize_input_vals_hardening(vals)

            inspection = (
                Inspection.browse(vals["inspection_id"])
                if vals.get("inspection_id")
                else False
            )
            if inspection and inspection.process_code in STRICT_BINARY_RESULT_PROCESS_CODES:
                vals = self._normalize_vals_for_strict_binary_line(vals, reset_missing=True)

            clean_vals_list.append(vals)

        records = super().create(clean_vals_list)
        records._sync_line_result_hardening()
        return records

    def write(self, vals):
        vals = dict(vals or {})
        if not vals:
            return super().write(vals)

        if self.env.context.get("skip_quality_line_sync"):
            return super().write(vals)

        writes_na = any(
            vals.get(field_name) == "na"
            for field_name in ("value_cumple", "value_ok", "result")
        )
        if writes_na:
            for line in self:
                if line._is_strict_binary_result_line() or not line.allow_not_applicable:
                    raise ValidationError(_(
                        "%s no permite N/A. Active 'Permitir No aplica' en el atributo "
                        "o capture un resultado real."
                    ) % (line.name or line._strict_binary_process_display_name()))

        vals = self._normalize_input_vals_hardening(vals)

        strict_lines = self.filtered(lambda line: line._is_strict_binary_result_line())
        other_lines = self - strict_lines

        res = True
        if other_lines:
            res = super(QualityInspectionLineHardening, other_lines).write(vals) and res

        if strict_lines:
            strict_vals = self._normalize_vals_for_strict_binary_line(vals, reset_missing=False)
            res = super(QualityInspectionLineHardening, strict_lines).write(strict_vals) and res

        self._sync_line_result_hardening()
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
            line.allow_not_applicable = getattr(template, "allow_not_applicable", False)
            line.selection_options = template.selection_options

            if line._is_strict_binary_result_line():
                line.attribute_type = "boolean"
                line.capture_zone = "additional"
                line.result_mode = "cumple"
                line.allow_not_applicable = False
                line.is_not_applicable = False
                line.value_ok = False
                line.value_ok_required = False
                line.value_float = 0.0
                line.value_char = False
                line.value_selection = False
                line.selection_options = False
                line.min_value = 0.0
                line.max_value = 0.0
                line.unit = False
                line.allow_zero = False
                if line.value_cumple == "na":
                    line.value_cumple = False
                if line.result == "na":
                    line.result = False

    @api.onchange("attribute_type", "result_mode", "allow_not_applicable")
    def _onchange_attribute_config_hardening(self):
        for line in self:
            if line._is_strict_binary_result_line():
                warning = False
                if (
                    line.attribute_type != "boolean"
                    or line.result_mode != "cumple"
                    or line.allow_not_applicable
                ):
                    warning = True

                line.attribute_type = "boolean"
                line.capture_zone = "additional"
                line.result_mode = "cumple"
                line.allow_not_applicable = False
                line.is_not_applicable = False
                line.value_ok = False
                line.value_ok_required = False
                line.value_float = 0.0
                line.value_char = False
                line.value_selection = False
                line.selection_options = False
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

            elif line.attribute_type == "boolean":
                line.min_value = 0.0
                line.max_value = 0.0
                line.unit = False
                line.value_float = 0.0
                line.value_char = False
                line.value_selection = False
                line.selection_options = False
                line.allow_zero = False
            elif line.attribute_type == "selection":
                line.min_value = 0.0
                line.max_value = 0.0
                line.unit = False
                line.allow_zero = False
            elif line.attribute_type == "char":
                line.min_value = 0.0
                line.max_value = 0.0
                line.unit = False
                line.value_selection = False
                line.selection_options = False
                line.allow_zero = False
            elif line.attribute_type == "float":
                line.result_mode = "cumple"
                line.selection_options = False

    @api.onchange(
        "value_float",
        "min_value",
        "max_value",
        "allow_zero",
        "attribute_type",
        "value_cumple",
        "value_cumple_required",
        "value_ok",
        "value_ok_required",
        "result",
        "result_required",
        "value_char",
        "value_selection",
        "is_not_applicable",
    )
    def _onchange_evaluate_result_hardening(self):
        for line in self:
            vals = line._get_synced_vals_hardening()
            for field_name, value in vals.items():
                line[field_name] = value

    def _quality_line_has_result_hardening(self):
        self.ensure_one()
        if self.is_not_applicable:
            return bool(self.allow_not_applicable and self.result == "na")
        return self.result in VALID_FINAL_RESULTS

    def _quality_line_is_missing_hardening(self):
        self.ensure_one()

        if self.is_not_applicable:
            return not (self.allow_not_applicable and self.result == "na")

        if self.result == "na":
            return not self.allow_not_applicable

        if self.attribute_type == "float":
            if not _float_is_captured(self.value_float, allow_zero=self.allow_zero):
                return True
            if not self.min_value and not self.max_value:
                return True
            return self.result not in VALID_FINAL_RESULTS

        if self.attribute_type == "boolean":
            if self.result_mode == "ok":
                return (
                    self.value_ok_required not in OK_VALUES
                    or self.result not in OK_VALUES
                )
            return (
                self.value_cumple_required not in CUMPLE_VALUES
                or self.result not in CUMPLE_VALUES
            )

        if self.attribute_type == "selection":
            captured = self.value_selection or self.value_char
            if not captured:
                return True
            return self.result not in VALID_FINAL_RESULTS

        if self.attribute_type == "char":
            if not self.value_char:
                return True
            return self.result not in VALID_FINAL_RESULTS

        return self.result not in VALID_FINAL_RESULTS

    def _quality_line_missing_reason_hardening(self):
        self.ensure_one()
        if self.attribute_type == "float" and not (self.min_value or self.max_value):
            return _("%s: configure mínimo y/o máximo para calcular el resultado") % self.name
        if self.attribute_type == "selection" and not (self.value_selection or self.value_char):
            return _("%s: capture el valor de selección") % self.name
        if self.attribute_type == "char" and not self.value_char:
            return _("%s: capture el valor") % self.name
        if self.attribute_type == "boolean":
            return _("%s: seleccione Cumple/No Cumple") % self.name
        return _("%s: capture resultado") % self.name

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
                or line.allow_not_applicable
            ):
                raise ValidationError(_(
                    "%s solo permite atributos adicionales de tipo Cumple/No Cumple."
                ) % line._strict_binary_process_display_name())

    @api.constrains(
        "attribute_type",
        "unit",
        "min_value",
        "max_value",
        "selection_options",
        "allow_zero",
        "allow_not_applicable",
        "is_not_applicable",
        "result",
        "value_cumple",
        "value_ok",
    )
    def _check_result_configuration_hardening(self):
        for line in self:
            if (line.is_not_applicable or line.result == "na" or line.value_cumple == "na" or line.value_ok == "na") and not line.allow_not_applicable:
                raise ValidationError(_(
                    "El atributo '%s' no permite N/A. Active 'Permitir No aplica' "
                    "en la plantilla o capture un resultado real."
                ) % line.name)

            if line.attribute_type == "boolean":
                if line.unit or line.min_value or line.max_value or line.selection_options or line.allow_zero:
                    raise ValidationError(_(
                        "El atributo '%s' es Cumple/No Cumple y no debe tener "
                        "unidad, mínimo, máximo, opciones ni valor numérico."
                    ) % line.name)

            if line.attribute_type == "selection":
                options = _split_selection_options(line.selection_options)
                value = (line.value_selection or line.value_char or "").strip()
                if options and value:
                    normalized_options = {item.lower() for item in options}
                    if value.lower() not in normalized_options:
                        raise ValidationError(_(
                            "El valor '%s' no está dentro de las opciones configuradas para '%s': %s"
                        ) % (value, line.name, ", ".join(options)))

            if line.attribute_type == "float" and line.min_value and line.max_value and line.min_value > line.max_value:
                raise ValidationError(_(
                    "En '%s', el valor mínimo no puede ser mayor que el máximo."
                ) % line.name)

    @api.constrains("value_float", "attribute_type", "allow_zero", "result", "is_not_applicable")
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

            if line.is_not_applicable and line.allow_not_applicable:
                continue

            if (
                line.attribute_type == "float"
                and not line.allow_zero
                and not line.value_float
            ):
                raise ValidationError(
                    _(
                        "El atributo numérico '%s' no puede quedar en cero. "
                        "Capture el valor real o marque No aplica si la plantilla lo permite."
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
        default=False,
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
        default=False,
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

    # FOLIO-QM-ODOO18-080:
    # Odoo hace web_save/autoguardado al cambiar muchos2uno/radio en registros nuevos.
    # Si estos campos siguen required=True a nivel ORM/SQL, el borrador falla antes
    # de que el onchange termine de persistir producto/lote desde la OP.
    # La obligatoriedad real se valida al iniciar/liberar la inspección.
    process_type_id = fields.Many2one(
        "quality.process.type",
        "Tipo de Proceso",
        required=False,
        tracking=True,
    )
    production_order_id = fields.Many2one(
        "mrp.production",
        "Orden de Producción",
        required=False,
        tracking=True,
    )
    lot_id = fields.Many2one(
        "stock.lot",
        "Lote de Fabricación",
        required=False,
        tracking=True,
    )
    product_id = fields.Many2one(
        "product.product",
        "Producto",
        required=False,
        tracking=True,
    )
    operator_id = fields.Many2one(
        "hr.employee",
        "Operador",
        required=False,
    )
    partner_id = fields.Many2one(
        "res.partner",
        "Cliente",
        required=False,
        tracking=True,
    )
    inspector_id = fields.Many2one(
        "res.users",
        "Inspector de Calidad",
        required=False,
        default=lambda s: s.env.user,
        tracking=True,
    )
    shift = fields.Selection(
        [
            ("turno_1", "Turno 1"),
            ("turno_2", "Turno 2"),
            ("turno_3", "Turno 3"),
        ],
        required=False,
    )
    plant = fields.Selection(
        [
            ("planta_1", "Planta 1"),
            ("planta_2", "Planta 2"),
            ("planta_3", "Planta 3"),
            ("planta_6", "Planta 6"),
            ("planta_7", "Planta 7"),
        ],
        required=False,
    )

    folio = fields.Char("Folio de Producción", required=False, help="")
    code = fields.Char("Código de Producto", required=False, help="")

    espesor = fields.Float("Espesor", digits=(16, 2))
    oct_espesor = fields.Float("Espesor Octágono (mm)", digits=(16, 2))

    ancho = fields.Float("Ancho (mm)", digits=(16, 2))
    oct_ancho = fields.Float("Ancho Octágono (mm)", digits=(16, 2))
    calibracion = fields.Float("Calibración", digits=(16, 4))
    papel_ancho = fields.Float("Ancho del Papel", digits=(16, 2))
    papel_gramaje = fields.Float("Gramaje del Papel", digits=(16, 2))
    oct_retiramiento = fields.Float("Retiramiento (cm) - Legacy", digits=(16, 2))
    reticula_extendida = fields.Float("Retiramiento / Retícula Extendida (cm)", digits=(16, 2))

    capture_mode = fields.Selection(
        related="process_type_id.capture_mode",
        store=True,
        readonly=True,
    )
    allow_resistencia_na = fields.Boolean(
        related="process_type_id.allow_resistencia_na",
        store=True,
        readonly=True,
    )
    allow_hexagono_na = fields.Boolean(
        related="process_type_id.allow_hexagono_na",
        store=True,
        readonly=True,
    )
    hexagono_na = fields.Boolean(
        "Hexágono No Aplica",
        help="Marcar únicamente cuando el proceso permita explícitamente N/A en Hexágono.",
    )
    date_started = fields.Datetime("Fecha de Inicio", readonly=True)
    date_closed = fields.Datetime("Fecha de Cierre", readonly=True)

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

    def init(self):
        super().init()
        cr = self.env.cr

        cr.execute("""
            SELECT EXISTS (
                SELECT 1
                  FROM information_schema.tables
                 WHERE table_name = 'quality_inspection'
            )
        """)
        if not cr.fetchone()[0]:
            return

        # FOLIO-QM-ODOO18-080:
        # Defensive DB migration. Odoo a veces conserva NOT NULL aunque el campo
        # se vuelva required=False en una herencia posterior.
        for column_name in (
            "process_type_id",
            "production_order_id",
            "product_id",
            "lot_id",
            "operator_id",
            "partner_id",
            "inspector_id",
            "folio",
            "code",
            "shift",
            "plant",
        ):
            cr.execute("""
                SELECT EXISTS (
                    SELECT 1
                      FROM information_schema.columns
                     WHERE table_name = 'quality_inspection'
                       AND column_name = %s
                )
            """, (column_name,))
            if cr.fetchone()[0]:
                cr.execute(
                    'ALTER TABLE "quality_inspection" '
                    'ALTER COLUMN "%s" DROP NOT NULL' % column_name
                )

    def _sanitize_line_commands_hardening(self, vals):
        """
        Evita que la lista editable de Atributos Adicionales intente crear
        líneas sin Nombre del Atributo.

        Casos:
        - Línea completamente vacía: se descarta.
        - Línea con plantilla: se completa el nombre desde la plantilla.
        - Línea manual con datos pero sin nombre: se bloquea con mensaje claro.
        """
        vals = dict(vals or {})
        commands = vals.get("line_ids")

        if not commands:
            return vals

        clean_commands = []

        for command in commands:
            if (
                not isinstance(command, (list, tuple))
                or len(command) < 3
                or command[0] != 0
            ):
                clean_commands.append(command)
                continue

            line_vals = dict(command[2] or {})

            if not (line_vals.get("name") or "").strip() and line_vals.get("attribute_template_id"):
                template = self.env["quality.attribute.template"].browse(
                    line_vals["attribute_template_id"]
                ).exists()
                if template and template.name:
                    line_vals["name"] = template.name

            if not (line_vals.get("name") or "").strip():
                if _quality_line_vals_has_user_content(line_vals):
                    raise UserError(_(
                        "Capture el Nombre del Atributo en la línea manual de inspección "
                        "antes de guardar. Si no desea agregarla, elimine la línea vacía."
                    ))
                # Línea vacía creada accidentalmente por la lista editable.
                continue

            clean_commands.append((command[0], command[1], line_vals))

        vals["line_ids"] = clean_commands
        return vals

    def _normalize_inspection_vals_hardening(self, vals):
        vals = dict(vals or {})
        if "espesor" in vals and vals.get("espesor") not in (False, None, ""):
            vals["espesor"] = round(float(vals["espesor"]), 2)
        if "calibracion" in vals and vals.get("calibracion") not in (False, None, ""):
            vals["calibracion"] = round(float(vals["calibracion"]), 4)
        return vals

    def _complete_vals_from_production_hardening(self, vals):
        vals = dict(vals or {})
        production_id = vals.get("production_order_id")

        if not production_id:
            return vals

        production = self.env["mrp.production"].sudo().browse(production_id).exists()
        if not production:
            return vals

        product = production.product_id

        if product and not vals.get("product_id"):
            vals["product_id"] = product.id

        if product and not vals.get("code"):
            vals["code"] = product.default_code or product.display_name or vals.get("code")

        if production.name and not vals.get("folio"):
            vals["folio"] = production.name

        if not vals.get("lot_id"):
            lot = getattr(production, "lot_producing_id", False)
            if lot:
                vals["lot_id"] = lot.id

        if not vals.get("partner_id") and production.origin:
            sale_order = self.env["sale.order"].sudo().search(
                [("name", "=", production.origin)],
                limit=1,
            )
            if sale_order and sale_order.partner_id:
                vals["partner_id"] = sale_order.partner_id.id

        return vals

    def _sync_missing_values_from_production_record_hardening(self):
        for rec in self:
            if not rec.production_order_id:
                continue

            vals = rec._complete_vals_from_production_hardening({
                "production_order_id": rec.production_order_id.id,
            })

            vals.pop("production_order_id", None)

            clean_vals = {}
            for field_name, value in vals.items():
                if not value:
                    continue
                if field_name in rec._fields and not rec[field_name]:
                    clean_vals[field_name] = value

            if clean_vals:
                super(QualityInspectionHardening, rec.with_context(
                    skip_quality_template_autoload=True,
                    skip_octagono_cleanup=True,
                )).write(clean_vals)

    def _get_quality_attribute_templates_hardening(self):
        self.ensure_one()

        process = self.process_type_id
        process_code = process.code or self.process_code
        strict_binary = process_code in STRICT_BINARY_RESULT_PROCESS_CODES
        Template = self.env["quality.attribute.template"]

        if hasattr(Template, "_get_applicable_templates_for_capture"):
            return Template._get_applicable_templates_for_capture(
                product=self.product_id,
                process=process,
                include_general=False,
                strict_binary=strict_binary,
            )

        templates = Template.browse()

        if process:
            templates |= process.attribute_template_ids.filtered(
                lambda template: not template.product_tmpl_id and template.active
            )

        if self.product_id and self.product_id.product_tmpl_id:
            product_tmpl = self.product_id.product_tmpl_id
            product_templates = Template.search([
                ("product_tmpl_id", "=", product_tmpl.id),
                "|",
                ("process_type_id", "=", False),
                ("process_type_id", "=", process.id if process else False),
                ("active", "=", True),
            ])
            templates |= product_templates

        if strict_binary:
            templates = templates.filtered(lambda template: template.attribute_type == "boolean")

        selected = {}
        for template in templates.sorted(lambda item: (
            0 if self.product_id and item.product_tmpl_id == self.product_id.product_tmpl_id else 1,
            item.sequence,
            item.id,
        )):
            key = (
                getattr(template, "normalized_name", False) or _slug(template.name),
                getattr(template, "capture_zone", False) or "additional",
            )
            if key[0] and key not in selected:
                selected[key] = template

        return Template.browse([template.id for template in selected.values()]).sorted(
            lambda item: (item.sequence, item.id)
        )

    def _prepare_quality_line_vals_from_template_hardening(self, template):
        self.ensure_one()

        process_code = self.process_type_id.code or self.process_code
        strict_binary = process_code in STRICT_BINARY_RESULT_PROCESS_CODES

        if strict_binary:
            return {
                "attribute_template_id": template.id,
                "name": template.name,
                "attribute_type": "boolean",
                "capture_zone": "additional",
                "result_mode": "cumple",
                "min_value": 0.0,
                "max_value": 0.0,
                "unit": False,
                "allow_zero": False,
                "allow_not_applicable": False,
                "is_not_applicable": False,
                "selection_options": False,
                "sequence": template.sequence,
                "value_cumple": False,
                "value_cumple_required": False,
                "value_ok": False,
                "value_ok_required": False,
                "result": False,
                "result_required": False,
            }

        result_mode = getattr(template, "result_mode", False) or "cumple"

        return {
            "attribute_template_id": template.id,
            "name": template.name,
            "attribute_type": template.attribute_type,
            "capture_zone": getattr(template, "capture_zone", False) or "additional",
            "result_mode": result_mode,
            "min_value": template.min_value,
            "max_value": template.max_value,
            "unit": template.unit if template.attribute_type == "float" else False,
            "allow_zero": getattr(template, "allow_zero", False) if template.attribute_type == "float" else False,
            "allow_not_applicable": getattr(template, "allow_not_applicable", False),
            "is_not_applicable": False,
            "selection_options": template.selection_options if template.attribute_type == "selection" else False,
            "sequence": template.sequence,
            "value_cumple": False,
            "value_cumple_required": False,
            "value_ok": False,
            "value_ok_required": False,
            "value_selection": False,
            "value_char": False,
            "result": False,
            "result_required": False,
        }

    def _build_quality_attribute_line_commands_hardening(self, clear_existing=True):
        self.ensure_one()

        commands = [(5, 0, 0)] if clear_existing else []
        templates = self._get_quality_attribute_templates_hardening()

        for template in templates:
            commands.append((0, 0, self._prepare_quality_line_vals_from_template_hardening(template)))

        return commands

    def _reload_quality_attribute_templates_hardening(self, clear_existing=True):
        for rec in self:
            if not rec.product_id and not rec.process_type_id:
                if clear_existing:
                    rec.line_ids = [(5, 0, 0)]
                continue

            commands = rec._build_quality_attribute_line_commands_hardening(
                clear_existing=clear_existing,
            )

            if clear_existing:
                rec.line_ids = commands or [(5, 0, 0)]
            elif commands:
                rec.line_ids = commands

    @api.model_create_multi
    def create(self, vals_list):
        clean_vals_list = []

        for vals in vals_list:
            vals = self._sanitize_line_commands_hardening(vals)
            vals = self._complete_vals_from_production_hardening(vals)
            vals = self._normalize_inspection_vals_hardening(vals)

            if vals.get("name", "Nuevo") == "Nuevo":
                vals["name"] = (
                    self.env["ir.sequence"].next_by_code("quality.inspection")
                    or "Nuevo"
                )

            clean_vals_list.append(vals)

        records = super().create(clean_vals_list)
        records._cleanup_octagono_not_applicable_hardening()

        for rec, vals in zip(records, clean_vals_list):
            if (
                not vals.get("line_ids")
                and not rec.line_ids
                and (rec.product_id or rec.process_type_id)
            ):
                rec.with_context(skip_quality_template_autoload=True)._reload_quality_attribute_templates_hardening(
                    clear_existing=False,
                )

        return records

    def write(self, vals):
        vals = self._sanitize_line_commands_hardening(vals)

        if "production_order_id" in vals:
            vals = self._complete_vals_from_production_hardening(vals)

        vals = self._normalize_inspection_vals_hardening(vals)

        reload_templates = (
            not self.env.context.get("skip_quality_template_autoload")
            and "line_ids" not in vals
            and any(field in vals for field in ("product_id", "process_type_id", "production_order_id"))
        )

        res = super().write(vals)

        if not self.env.context.get("skip_octagono_cleanup"):
            self._cleanup_octagono_not_applicable_hardening()

        if reload_templates:
            draft_records = self.filtered(lambda rec: rec.state == "borrador")
            draft_records.with_context(skip_quality_template_autoload=True)._reload_quality_attribute_templates_hardening(
                clear_existing=True,
            )

        return res

    def _cleanup_octagono_not_applicable_hardening(self):
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
                rec.espesor = 0.0
                rec.oct_espesor = 0.0
                rec.oct_retiramiento = 0.0
                rec.reticula_extendida = 0.0

    @api.onchange("hexagono_na")
    def _onchange_hexagono_na_hardening(self):
        for rec in self:
            if rec.hexagono_na:
                if not rec.allow_hexagono_na:
                    rec.hexagono_na = False
                    return {
                        "warning": {
                            "title": _("No aplica no permitido"),
                            "message": _("Este proceso no permite marcar Hexágono como N/A."),
                        }
                    }
                rec.hexagono = False
                rec.tipo_hexagono = False
                rec.oct_hexagono = False
                rec.oct_hexagono_tipo = False

    @api.onchange("resistencia_na")
    def _onchange_resistencia_na_hardening(self):
        for rec in self:
            if rec.resistencia_na:
                if not rec.allow_resistencia_na:
                    rec.resistencia_na = False
                    return {
                        "warning": {
                            "title": _("No aplica no permitido"),
                            "message": _("Este proceso no permite marcar Resistencia como N/A."),
                        }
                    }
                rec.resistencia = 0.0

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
            if rec.state == "borrador":
                continue
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
        for rec in self:
            if not rec.production_order_id:
                rec._reload_quality_attribute_templates_hardening(clear_existing=True)
                continue

            production = rec.production_order_id

            if production.product_id:
                rec.product_id = production.product_id
                rec.code = production.product_id.default_code or rec.code

            if not rec.folio and production.name:
                rec.folio = production.name

            if getattr(production, "lot_producing_id", False):
                rec.lot_id = production.lot_producing_id

            sale_order = (
                rec.env["sale.order"].search([("name", "=", production.origin)], limit=1)
                if production.origin
                else False
            )
            if sale_order and sale_order.partner_id:
                rec.partner_id = sale_order.partner_id

            rec._reload_quality_attribute_templates_hardening(clear_existing=True)

    @api.onchange("process_type_id", "product_id")
    def _onchange_load_attribute_templates(self):
        for rec in self:
            rec._reload_quality_attribute_templates_hardening(clear_existing=True)

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

    def _check_required_header_hardening(self):
        for rec in self:
            rec._sync_missing_values_from_production_record_hardening()

            missing = []

            if not rec.process_type_id:
                missing.append(_("Tipo de Proceso"))
            if not rec.production_order_id:
                missing.append(_("Orden de Producción"))
            if not rec.product_id:
                missing.append(_("Producto"))
            if not rec.lot_id:
                missing.append(_("Lote de Fabricación"))
            if not rec.operator_id:
                missing.append(_("Operador"))
            if not rec.inspector_id:
                missing.append(_("Inspector de Calidad"))
            if not rec.partner_id:
                missing.append(_("Cliente"))
            if not rec.folio:
                missing.append(_("Folio de Producción"))
            if not rec.code:
                missing.append(_("Código de Producto"))
            if not rec.shift:
                missing.append(_("Turno"))
            if not rec.plant:
                missing.append(_("Planta"))
            if not rec.sin_supervisor and not rec.supervisor_id:
                missing.append(_("Supervisor o marcar Sin Supervisor"))

            if missing:
                raise UserError(
                    _("Complete los datos generales antes de iniciar la inspección: %s.")
                    % ", ".join(missing)
                )

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

            required_lines._sync_line_result_hardening()

            strict_binary = rec.process_code in STRICT_BINARY_RESULT_PROCESS_CODES

            if strict_binary:
                invalid_type = required_lines.filtered(
                    lambda line: (
                        line.attribute_type != "boolean"
                        or line.result_mode != "cumple"
                        or line.capture_zone != "additional"
                        or line.allow_not_applicable
                    )
                )
                if invalid_type:
                    raise UserError(_(
                        "%s solo permite atributos adicionales de tipo Cumple/No Cumple. Revise: %s"
                    ) % (
                        rec.process_type_id.display_name,
                        ", ".join(invalid_type.mapped("name")),
                    ))

            missing_lines = required_lines.filtered(
                lambda line: line._quality_line_is_missing_hardening()
            )
            if missing_lines:
                raise UserError(
                    _("Hay atributos obligatorios sin captura válida: %s")
                    % "; ".join(
                        missing_lines.mapped(lambda line: line._quality_line_missing_reason_hardening())
                    )
                )

            not_allowed_na = required_lines.filtered(
                lambda line: (
                    (line.result == "na" or line.is_not_applicable)
                    and not line.allow_not_applicable
                )
            )
            if not_allowed_na:
                raise UserError(
                    _("Estos atributos no permiten N/A: %s")
                    % ", ".join(not_allowed_na.mapped("name"))
                )

            failing = required_lines.filtered(lambda line: line.result in FAIL_RESULTS)
            if failing:
                raise UserError(_(
                    "No se puede aceptar/liberar: hay atributo(s) No Cumple/NO OK. "
                    "Retenga o rechace la inspección. Revise: %s"
                ) % ", ".join(failing.mapped("name")))

    def _check_measures_captured_hardening(self):
        for rec in self:
            if rec.capture_mode == "additional_only" or rec.process_code in STRICT_BINARY_RESULT_PROCESS_CODES:
                continue

            if not rec.process_type_id.require_measures:
                continue

            if rec.resistencia_na and not rec.allow_resistencia_na:
                raise UserError(_("Este proceso no permite marcar Resistencia como N/A."))

            if rec.hexagono_na and not rec.allow_hexagono_na:
                raise UserError(_("Este proceso no permite marcar Hexágono como N/A."))

            if rec.process_code == "octagono":
                missing = []

                if not (rec.ancho or getattr(rec, "oct_ancho", 0.0)):
                    missing.append("Ancho")
                if not (
                    rec.hexagono
                    or getattr(rec, "oct_hexagono_tipo", False)
                    or getattr(rec, "oct_hexagono", False)
                    or rec.tipo_hexagono
                    or (rec.hexagono_na and rec.allow_hexagono_na)
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
                or (rec.hexagono_na and rec.allow_hexagono_na)
            ):
                missing.append("Hexágono")
            if rec.show_resistencia and not (
                rec.resistencia
                or (rec.resistencia_na and rec.allow_resistencia_na)
            ):
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
            if rec.show_tipo_hexagono and not (
                rec.tipo_hexagono
                or (rec.hexagono_na and rec.allow_hexagono_na)
            ):
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

            if rec.process_code == "troquelado_plano":
                if not rec.troquelado_ids:
                    missing.append("Pestaña Troquelado")
                else:
                    missing_troquel = rec.troquelado_ids.filtered(lambda line: not line.resultado)
                    if missing_troquel:
                        missing.append("Resultado en Troquelado")

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

    def _get_non_conformance_labels_hardening(self):
        self.ensure_one()
        labels = []

        self.line_ids._sync_line_result_hardening()

        for line in self.line_ids.filtered(lambda item: item.result in FAIL_RESULTS):
            result_label = dict(line._fields["result"].selection).get(line.result, line.result)
            labels.append("%s (%s)" % (line.name, result_label))

        native_fields = [
            ("apariencia", "Apariencia"),
            ("pegado_result", "Resultado de Pegado"),
            ("oct_alineacion", "Alineación"),
            ("oct_pegado", "Pegado Octágono"),
            ("engomado", "Engomado"),
        ]
        for field_name, label in native_fields:
            if field_name in self._fields and self[field_name] == "no_cumple":
                labels.append("%s (No Cumple)" % label)

        ranura_failing = self.ranurado_ids.filtered(lambda line: line.resultado == "no_cumple")
        for line in ranura_failing:
            labels.append("Ranurado/Corte Sierra: %s (No Cumple)" % (getattr(line, "concepto", False) or line.display_name))

        troquel_failing = self.troquelado_ids.filtered(lambda line: line.resultado == "no_cumple")
        for line in troquel_failing:
            labels.append("Troquelado #%s (No Cumple)" % (line.sequence or line.id))

        return labels

    def _check_no_failing_results_hardening(self):
        for rec in self:
            labels = rec._get_non_conformance_labels_hardening()
            if labels:
                raise UserError(_(
                    "No se puede aceptar/liberar la inspección porque existen resultados No Cumple/NO OK. "
                    "Use Retener si el producto será corregido o Rechazar si no procede. Revise: %s"
                ) % "; ".join(labels))

    def _notify_quality_non_conformance_hardening(self, action_label):
        for rec in self:
            labels = rec._get_non_conformance_labels_hardening()
            if not labels:
                continue

            partner_ids = set()

            supervisor_partner = False
            if hasattr(rec, "_get_supervisor_partner_hardening"):
                supervisor_partner = rec._get_supervisor_partner_hardening()
            elif rec.supervisor_id and rec.supervisor_id.user_id and rec.supervisor_id.user_id.partner_id:
                supervisor_partner = rec.supervisor_id.user_id.partner_id

            if supervisor_partner:
                partner_ids.update(supervisor_partner.ids)
                rec.message_subscribe(partner_ids=supervisor_partner.ids)

            if rec.inspector_id and rec.inspector_id.partner_id:
                partner_ids.add(rec.inspector_id.partner_id.id)

            manager_group = self.env.ref(
                "quality_management.group_quality_manager",
                raise_if_not_found=False,
            )
            if manager_group:
                for user in manager_group.users:
                    if user.partner_id:
                        partner_ids.add(user.partner_id.id)

            supervisor_user = rec._get_supervisor_user_hardening()
            if supervisor_user:
                rec.activity_schedule(
                    "mail.mail_activity_data_todo",
                    date_deadline=fields.Date.today(),
                    summary=_("Incumplimiento de calidad: %s") % rec.name,
                    user_id=supervisor_user.id,
                )

            rec.message_post(
                body=_(
                    "%(action)s por %(user)s debido a incumplimiento(s): %(items)s"
                ) % {
                    "action": action_label,
                    "user": self.env.user.name,
                    "items": "; ".join(labels),
                },
                partner_ids=list(partner_ids),
                subtype_xmlid="mail.mt_comment",
            )

    def _full_quality_validation_hardening(self):
        for rec in self:
            if rec.state != "en_proceso":
                raise UserError(_("Debe presionar 'INICIAR INSPECCIÓN' antes de liberar."))

            rec._check_required_header_hardening()
            rec._check_reserved_duplicate_attributes_hardening()
            rec._check_measures_captured_hardening()
            rec._check_required_additional_attributes_hardening()
            rec._check_no_failing_results_hardening()
            rec._check_previous_process_hardening()

    def _sync_strict_binary_lines_hardening(self):
        for rec in self.filtered(lambda item: item.process_code in STRICT_BINARY_RESULT_PROCESS_CODES):
            rec.line_ids._sync_line_result_hardening()

    def action_start(self):
        for rec in self:
            rec._sync_missing_values_from_production_record_hardening()
            rec._check_required_header_hardening()
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

            rec._notify_quality_non_conformance_hardening(_("Producto RETENIDO"))

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
            rec._notify_quality_non_conformance_hardening(_("Inspección RECHAZADA"))


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