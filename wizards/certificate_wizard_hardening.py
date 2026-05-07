# -*- coding: utf-8 -*-

import re
import unicodedata

from odoo import models, _


def _slug(value):
    value = value or ""
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    value = re.sub(r"[^a-zA-Z0-9]+", "_", value.lower()).strip("_")
    return value


class QualityCertificateWizardHardening(models.TransientModel):
    _inherit = "quality.certificate.wizard"

    def _selection_label(self, record, field_name, value):
        if not value:
            return False
        return dict(record._fields[field_name].selection).get(value, value)

    def action_create_certificate(self):
        self.ensure_one()
        insp = self.inspection_id

        vals = {
            "inspection_id": insp.id,
            "partner_id": self.partner_id.id,
            "certified_by": self.env.user.id,
        }

        if self.include_largo and insp.largo:
            vals["certified_largo"] = insp.largo
        if self.include_ancho and (insp.ancho or getattr(insp, "oct_ancho", 0.0)):
            vals["certified_ancho"] = insp.ancho or insp.oct_ancho
        if self.include_espesor and insp.espesor:
            vals["certified_espesor"] = insp.espesor

        hex_value = insp.hexagono or getattr(insp, "oct_hexagono", False) or insp.tipo_hexagono
        if self.include_hexagono and hex_value:
            field_name = "hexagono" if insp.hexagono else "oct_hexagono" if getattr(insp, "oct_hexagono", False) else "tipo_hexagono"
            vals["certified_hexagono_label"] = self._selection_label(insp, field_name, hex_value)

        if self.include_resistencia and insp.resistencia:
            vals["certified_resistencia"] = insp.resistencia
        if self.include_apariencia and insp.apariencia:
            vals["certified_apariencia"] = self._selection_label(insp, "apariencia", insp.apariencia)
        if self.include_humedad and insp.humedad_pct:
            vals["certified_humedad"] = insp.humedad_pct

        if self.include_pegado:
            pegado_value = insp.pegado_result or getattr(insp, "oct_pegado", False)
            if pegado_value:
                field_name = "pegado_result" if insp.pegado_result else "oct_pegado"
                vals["certified_pegado"] = self._selection_label(insp, field_name, pegado_value)

        if self.include_retiramiento and (getattr(insp, "oct_retiramiento", 0.0) or getattr(insp, "reticula_extendida", 0.0)):
            vals["certified_retiramiento"] = insp.oct_retiramiento or insp.reticula_extendida
        if self.include_calibracion and insp.calibracion:
            vals["certified_calibracion"] = insp.calibracion
        if self.include_engomado and insp.engomado:
            vals["certified_engomado"] = self._selection_label(insp, "engomado", insp.engomado)

        cert = self.env["quality.certificate"].create(vals)

        if self.include_all_attributes and insp.line_ids:
            seen = set()
            unique_ids = []
            for line in insp.line_ids:
                key = line.normalized_name or _slug(line.name)
                if not key or key in seen:
                    continue
                if line.result not in ("cumple", "ok"):
                    continue
                if line.attribute_type == "float" and not line.allow_zero and not line.value_float:
                    continue
                seen.add(key)
                unique_ids.append(line.id)
            cert.attribute_ids = [(6, 0, unique_ids)]

        return {
            "type": "ir.actions.act_window",
            "name": _("Certificado"),
            "res_model": "quality.certificate",
            "res_id": cert.id,
            "view_mode": "form",
            "target": "current",
        }

