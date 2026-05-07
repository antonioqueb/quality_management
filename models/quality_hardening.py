# -*- coding: utf-8 -*-

import re
import unicodedata
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


PROCESS_SEQUENCE = [
    "octagono",
    "guillotina",
    "pegado",
    "laminadora",
    "sierras_ranuradoras",
    "troquelado_plano",
]

RESERVED_MEASURE_ATTRS = {
    "largo", "ancho", "espesor", "hexagono", "hexágono",
    "resistencia", "apariencia", "humedad", "pegado",
    "retiramiento", "restiramiento", "reticula", "retícula",
    "reticula_extendida", "retícula_extendida",
    "calibracion", "calibración", "engomado",
    "alineacion", "alineación",
}


def _slug(value):
    value = value or ""
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    value = re.sub(r"[^a-zA-Z0-9]+", "_", value.lower()).strip("_")
    return value


class QualityProcessTypeHardening(models.Model):
    _inherit = "quality.process.type"

    capture_mode = fields.Selection([
        ("full", "Medidas + Propiedades + Atributos"),
        ("additional_only", "Solo Atributos Adicionales"),
    ], default="full", required=True)

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

    normalized_name = fields.Char(
        "Nombre Normalizado",
        compute="_compute_normalized_name",
        store=True,
        index=True,
    )
    capture_zone = fields.Selection([
        ("additional", "Atributos Adicionales"),
        ("measures", "Medidas y Propiedades"),
        ("ranurado", "Ranurado"),
        ("troquelado", "Troquelado"),
        ("production", "Datos de Producción"),
    ], default="additional", required=True)

    result_mode = fields.Selection([
        ("cumple", "Cumple / No Cumple / N/A"),
        ("ok", "OK / NO OK / N/A"),
    ], default="cumple", required=True)

    allow_zero = fields.Boolean("Permitir valor cero", default=False)

    @api.depends("name")
    def _compute_normalized_name(self):
        for rec in self:
            rec.normalized_name = _slug(rec.name)


class QualityInspectionLineHardening(models.Model):
    _inherit = "quality.inspection.line"

    normalized_name = fields.Char(
        "Nombre Normalizado",
        compute="_compute_normalized_name",
        store=True,
        index=True,
    )

    capture_zone = fields.Selection([
        ("additional", "Atributos Adicionales"),
        ("measures", "Medidas y Propiedades"),
        ("ranurado", "Ranurado"),
        ("troquelado", "Troquelado"),
        ("production", "Datos de Producción"),
    ], default="additional", required=True)

    result_mode = fields.Selection([
        ("cumple", "Cumple / No Cumple / N/A"),
        ("ok", "OK / NO OK / N/A"),
    ], default="cumple", required=True)

    value_cumple = fields.Selection([
        ("cumple", "Cumple"),
        ("no_cumple", "No Cumple"),
        ("na", "N/A"),
    ], string="Cumple/No Cumple/N/A", default="na")

    value_ok = fields.Selection([
        ("ok", "OK"),
        ("no_ok", "NO OK"),
        ("na", "N/A"),
    ], string="OK/NO OK/N/A", default="na")

    result = fields.Selection(selection_add=[
        ("ok", "OK"),
        ("no_ok", "NO OK"),
    ], ondelete={
        "ok": "set default",
        "no_ok": "set default",
    })

    allow_zero = fields.Boolean("Permitir cero")

    @api.depends("name")
    def _compute_normalized_name(self):
        for line in self:
            line.normalized_name = _slug(line.name)

    @api.onchange("attribute_template_id")
    def _onchange_template_hardening(self):
        for line in self:
            tmpl = line.attribute_template_id
            if tmpl:
                line.name = tmpl.name
                line.attribute_type = tmpl.attribute_type
                line.capture_zone = tmpl.capture_zone
                line.result_mode = tmpl.result_mode
                line.min_value = tmpl.min_value
                line.max_value = tmpl.max_value
                line.unit = tmpl.unit
                line.allow_zero = tmpl.allow_zero

    @api.onchange("value_float", "min_value", "max_value", "attribute_type")
    def _onchange_evaluate_result_hardening(self):
        for line in self:
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
                line.result = line.value_cumple or "na"

    @api.onchange("value_ok", "attribute_type", "result_mode")
    def _onchange_value_ok_hardening(self):
        for line in self:
            if line.attribute_type == "boolean" and line.result_mode == "ok":
                line.result = line.value_ok or "na"

    @api.constrains("inspection_id", "sample_release_id", "normalized_name", "capture_zone")
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
                raise ValidationError(_(
                    "Atributo duplicado: '%s'. No se permite repetir atributos."
                ) % line.name)

    @api.constrains("value_float", "attribute_type", "allow_zero", "result")
    def _check_zero_numeric_hardening(self):
        for line in self:
            parent_state = (
                line.inspection_id.state if line.inspection_id
                else line.sample_release_id.state if line.sample_release_id
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
                raise ValidationError(_(
                    "El atributo numérico '%s' no puede quedar en cero. "
                    "Capture el valor real o marque N/A."
                ) % line.name)


class QualityInspectionRanuradoHardening(models.Model):
    _inherit = "quality.inspection.ranurado"

    concepto = fields.Char("Concepto", default="Largo")
    unidad = fields.Selection(selection_add=[
        ("cm", "cm"),
    ], ondelete={"cm": "set default"})

    resultado = fields.Selection(selection_add=[
        ("na", "N/A"),
    ], ondelete={"na": "set default"})

    @api.constrains("medida", "resultado")
    def _check_medida_gt_zero(self):
        for rec in self:
            if rec.resultado != "na" and rec.medida <= 0:
                raise ValidationError(_(
                    "La medida debe ser mayor a cero o marcarse como N/A."
                ))


class QualityInspectionTroqueladoHardening(models.Model):
    _inherit = "quality.inspection.troquelado"

    unidad = fields.Selection([
        ("mm", "mm"),
        ("cm", "cm"),
        ("in", "in"),
    ], default="mm", required=True)

    resultado = fields.Selection(selection_add=[
        ("na", "N/A"),
    ], ondelete={"na": "set default"})

    @api.constrains("medida", "resultado")
    def _check_medida_gt_zero(self):
        for rec in self:
            if rec.resultado != "na" and rec.medida <= 0:
                raise ValidationError(_(
                    "La medida de troquelado debe ser mayor a cero o marcarse como N/A."
                ))


class QualityInspectionHardening(models.Model):
    _inherit = "quality.inspection"

    process_code = fields.Char(
        related="process_type_id.code",
        store=True,
        readonly=True,
        index=True,
    )
    capture_mode = fields.Selection(
        related="process_type_id.capture_mode",
        store=True,
        readonly=True,
    )

    sin_supervisor = fields.Boolean("Sin Supervisor")
    date_started = fields.Datetime("Fecha de Inicio", readonly=True)
    date_closed = fields.Datetime("Fecha de Cierre", readonly=True)

    hexagono = fields.Selection([
        ("tipo_1", "Tipo 1"),
        ("tipo_2", "Tipo 2"),
        ("tipo_3", "Tipo 3"),
        ("tipo_4", "Tipo 4"),
    ], string="Hexágono")

    oct_hexagono = fields.Selection([
        ("tipo_1", "Tipo 1"),
        ("tipo_2", "Tipo 2"),
        ("tipo_3", "Tipo 3"),
        ("tipo_4", "Tipo 4"),
    ], string="Tipo de Hexágono Octágono")

    pegado_result = fields.Selection([
        ("cumple", "Cumple"),
        ("no_cumple", "No Cumple"),
        ("na", "N/A"),
    ], string="Resultado de Pegado")

    engomado = fields.Selection([
        ("cumple", "Cumple"),
        ("no_cumple", "No Cumple"),
        ("na", "N/A"),
    ], string="Engomado")

    corte_guillotina = fields.Selection([
        ("si", "Sí"),
        ("no", "No"),
        ("na", "N/A"),
    ], string="Corte en Guillotina")

    @api.constrains("sin_supervisor", "supervisor_id")
    def _check_supervisor_or_no_supervisor(self):
        for rec in self:
            if not rec.sin_supervisor and not rec.supervisor_id:
                raise ValidationError(_("Seleccione un supervisor o marque 'Sin Supervisor'."))

    @api.onchange("sin_supervisor")
    def _onchange_sin_supervisor(self):
        if self.sin_supervisor:
            self.supervisor_id = False

    @api.onchange("production_order_id")
    def _onchange_production_order_hardening(self):
        if not self.production_order_id:
            return

        mo = self.production_order_id
        if mo.product_id:
            self.product_id = mo.product_id
            self.code = mo.product_id.default_code or self.code

        if getattr(mo, "lot_producing_id", False):
            self.lot_id = mo.lot_producing_id

        origin_so = self.env["sale.order"].search(
            [("name", "=", mo.origin)],
            limit=1,
        ) if mo.origin else False

        if origin_so and origin_so.partner_id:
            self.partner_id = origin_so.partner_id

    @api.onchange("process_type_id", "product_id")
    def _onchange_load_attribute_templates_hardening(self):
        if not self.process_type_id and not self.product_id:
            return

        templates = self.env["quality.attribute.template"]
        if self.process_type_id:
            templates |= self.process_type_id.attribute_template_ids.filtered(
                lambda t: not t.product_tmpl_id and t.active
            )

        if self.product_id and self.product_id.product_tmpl_id:
            templates |= self.env["quality.attribute.template"].search([
                ("product_tmpl_id", "=", self.product_id.product_tmpl_id.id),
                ("active", "=", True),
            ])

        if templates:
            lines = [(5, 0, 0)]
            seen = set()
            for t in templates.sorted(lambda x: (x.sequence, x.id)):
                key = t.normalized_name or _slug(t.name)
                if not key or key in seen:
                    continue
                seen.add(key)
                lines.append((0, 0, {
                    "attribute_template_id": t.id,
                    "name": t.name,
                    "attribute_type": t.attribute_type,
                    "capture_zone": t.capture_zone,
                    "result_mode": t.result_mode,
                    "min_value": t.min_value,
                    "max_value": t.max_value,
                    "unit": t.unit,
                    "allow_zero": t.allow_zero,
                    "sequence": t.sequence,
                    "value_cumple": "na",
                    "value_ok": "na",
                    "result": "na",
                }))
            self.line_ids = lines

    def _check_previous_process_hardening(self):
        for rec in self:
            code = rec.process_code
            if code not in PROCESS_SEQUENCE:
                continue

            idx = PROCESS_SEQUENCE.index(code)
            if idx == 0:
                continue

            previous = PROCESS_SEQUENCE[idx - 1]
            prev = self.search([
                ("lot_id", "=", rec.lot_id.id),
                ("process_code", "=", previous),
                ("state", "=", "aceptado"),
            ], limit=1)

            if not prev:
                raise UserError(_(
                    "Secuencia bloqueada: antes de liberar '%s' debe estar liberado "
                    "el proceso previo '%s' para el lote %s."
                ) % (
                    rec.process_type_id.name,
                    previous.replace("_", " ").title(),
                    rec.lot_id.name or "—",
                ))

    def _check_reserved_duplicate_attributes_hardening(self):
        for rec in self:
            duplicates = []
            for line in rec.line_ids:
                key = line.normalized_name or _slug(line.name)
                if key in RESERVED_MEASURE_ATTRS:
                    duplicates.append(line.name)

            if duplicates:
                raise UserError(_(
                    "Estos atributos no deben capturarse como adicionales porque ya "
                    "pertenecen a Medidas y Propiedades: %s"
                ) % ", ".join(sorted(set(duplicates))))

    def _check_required_additional_attributes_hardening(self):
        for rec in self:
            if not rec.process_type_id.require_additional_attributes:
                continue

            required_lines = rec.line_ids.filtered(
                lambda l: l.attribute_template_id.is_required if l.attribute_template_id else True
            )
            if not required_lines:
                raise UserError(_("Debe capturar los atributos adicionales del proceso."))

            pending = required_lines.filtered(lambda l: l.result == "na")
            if pending:
                raise UserError(_(
                    "Hay atributos adicionales sin dictamen. Capture Cumple/No Cumple, "
                    "OK/NO OK o marque N/A cuando aplique: %s"
                ) % ", ".join(pending.mapped("name")))

            numeric_zero = required_lines.filtered(
                lambda l: l.attribute_type == "float" and not l.allow_zero and not l.value_float
            )
            if numeric_zero:
                raise UserError(_(
                    "Se detectan atributos numéricos con valor igual a cero. Rectifique: %s"
                ) % ", ".join(numeric_zero.mapped("name")))

    def _check_measures_captured_hardening(self):
        for rec in self:
            if rec.capture_mode == "additional_only":
                continue
            if not rec.process_type_id.require_measures:
                continue

            missing = []

            if rec.show_largo and not rec.largo:
                missing.append("Largo")
            if rec.show_ancho and not (rec.ancho or getattr(rec, "oct_ancho", 0.0)):
                missing.append("Ancho")
            if rec.show_espesor and not rec.espesor:
                missing.append("Espesor")
            if rec.show_hexagono and not rec.hexagono:
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
                getattr(rec, "oct_retiramiento", 0.0) or getattr(rec, "reticula_extendida", 0.0)
            ):
                missing.append("Retícula Extendida / Restiramiento")
            if rec.show_calibracion and not rec.calibracion:
                missing.append("Calibración")
            if rec.show_engomado and not rec.engomado:
                missing.append("Engomado")
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

            if rec.process_code == "sierras_ranuradoras" and rec.show_ranurado and not rec.ranurado_ids:
                missing.append("Pestaña Ranurado / Corte Sierra")

            if missing:
                raise UserError(_(
                    "Capture la información obligatoria antes de liberar. Faltan: %s"
                ) % ", ".join(missing))

    def _full_quality_validation_hardening(self):
        for rec in self:
            if rec.state != "en_proceso":
                raise UserError(_("Debe presionar 'INICIAR INSPECCIÓN' antes de liberar."))

            rec._check_reserved_duplicate_attributes_hardening()
            rec._check_measures_captured_hardening()
            rec._check_required_additional_attributes_hardening()
            rec._check_previous_process_hardening()

    def action_start(self):
        for rec in self:
            rec.date_started = fields.Datetime.now()
            rec.state = "en_proceso"
            rec.message_post(body=_("Inspección iniciada."), subtype_xmlid="mail.mt_comment")

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
                ) % (
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
                    raise ValidationError(_("El certificado solo puede contener atributos de la inspección fuente."))

                key = line.normalized_name or _slug(line.name)
                if key:
                    names.append(key)

                if line.attribute_type == "float" and not line.allow_zero and not line.value_float:
                    raise ValidationError(_("No se puede certificar el atributo '%s' con valor 0.") % line.name)

                if line.result not in ("cumple", "ok"):
                    raise ValidationError(_("Solo se pueden certificar atributos con resultado Cumple/OK."))

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
            has_doc = rec.main_pdf or rec.main_image or rec.result_document_ids or rec.client_format_ids
            if not has_doc:
                raise UserError(_("No puede marcar como enviado si no existe documento cargado."))
            rec.state = "enviado"
