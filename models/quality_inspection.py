# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta


# Secuencia obligatoria entre procesos (req. 5.2)
PROCESS_SEQUENCE = [
    "octagono", "guillotina", "pegado", "laminadora",
    "sierras_ranuradoras", "troquelado_plano",
]


class QualityInspection(models.Model):
    _name = "quality.inspection"
    _description = "Inspección de PP/PT"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_inspection desc, id desc"

    name = fields.Char("Referencia", required=True, readonly=True,
                       default="Nuevo", copy=False)

    process_type_id = fields.Many2one("quality.process.type",
                                      "Tipo de Proceso",
                                      required=True, tracking=True)
    inspection_type = fields.Selection([
        ("laminadora_remanejo", "Laminadora y Remanejo"),
        ("octagono", "Octágono"),
        ("guillotina_pegado", "Guillotina y Pegado"),
    ], compute="_compute_inspection_type", store=True)

    # Visibilidad dinámica
    show_largo = fields.Boolean(related="process_type_id.show_largo")
    show_ancho = fields.Boolean(related="process_type_id.show_ancho")
    show_espesor = fields.Boolean(related="process_type_id.show_espesor")
    show_hexagono = fields.Boolean(related="process_type_id.show_hexagono")
    show_resistencia = fields.Boolean(related="process_type_id.show_resistencia")
    show_apariencia = fields.Boolean(related="process_type_id.show_apariencia")
    show_humedad = fields.Boolean(related="process_type_id.show_humedad")
    show_pegado = fields.Boolean(related="process_type_id.show_pegado")
    show_retiramiento = fields.Boolean(related="process_type_id.show_retiramiento")
    show_calibracion = fields.Boolean(related="process_type_id.show_calibracion")
    show_engomado = fields.Boolean(related="process_type_id.show_engomado")
    show_alineacion = fields.Boolean(related="process_type_id.show_alineacion")
    show_ranurado = fields.Boolean(related="process_type_id.show_ranurado")
    show_troquelado = fields.Boolean(related="process_type_id.show_troquelado")
    show_papel = fields.Boolean(related="process_type_id.show_papel")
    show_adhesivo = fields.Boolean(related="process_type_id.show_adhesivo")
    show_tipo_hexagono = fields.Boolean(related="process_type_id.show_tipo_hexagono")
    show_corte_guillotina = fields.Boolean(related="process_type_id.show_corte_guillotina")
    show_numero_corrida = fields.Boolean(related="process_type_id.show_numero_corrida")

    # Datos generales (req. 5.1)
    production_order_id = fields.Many2one("mrp.production",
                                          "Orden de Producción",
                                          tracking=True,
                                          required=True)
    lot_id = fields.Many2one("stock.lot", "Lote de Fabricación",
                             tracking=True, required=True)
    product_id = fields.Many2one("product.product", "Producto",
                                 required=True, tracking=True)
    operator_id = fields.Many2one("hr.employee", "Operador", required=True)
    supervisor_id = fields.Many2one("hr.employee", "Supervisor", required=True)
    partner_id = fields.Many2one("res.partner", "Cliente",
                                 required=True, tracking=True)
    folio = fields.Char(
        "Folio de Producción", required=True,
        help="Formato: letras y/o números (ej. F-2026-001). "
             "Capture exactamente el folio impreso en el lote.")
    code = fields.Char(
        "Código de Producto", required=True,
        help="Código interno del producto (alfanumérico, sin espacios).")
    shift = fields.Selection([
        ("turno_1", "Turno 1"), ("turno_2", "Turno 2"), ("turno_3", "Turno 3"),
    ], required=True)
    plant = fields.Selection([
        ("planta_1", "Planta 1"), ("planta_2", "Planta 2"),
        ("planta_3", "Planta 3"), ("planta_6", "Planta 6"),
        ("planta_7", "Planta 7"),
    ], required=True)
    inspector_id = fields.Many2one("res.users", "Inspector de Calidad",
                                   required=True,
                                   default=lambda s: s.env.user, tracking=True)

    # Fecha automática y bloqueada (req. 5.1)
    date_inspection = fields.Datetime("Fecha y Hora de Inspección",
                                      required=True, readonly=True,
                                      default=fields.Datetime.now)

    state = fields.Selection([
        ("borrador", "Borrador"),
        ("en_proceso", "En Proceso"),
        ("aceptado", "Aceptado"),
        ("retenido", "Retenido"),
        ("rechazado", "Rechazado"),
    ], default="borrador", required=True, tracking=True, copy=False)

    # PP/PT mutuamente excluyente (req. 5.1)
    pp_pt = fields.Selection([
        ("pp", "Producto en Proceso (PP)"),
        ("pt", "Producto Terminado (PT)"),
    ], string="PP / PT", required=True, default="pp", tracking=True)
    is_pp = fields.Boolean(compute="_compute_is_pp_pt")
    is_pt = fields.Boolean(compute="_compute_is_pp_pt")

    line_ids = fields.One2many("quality.inspection.line", "inspection_id",
                               string="Atributos Capturados")

    # Medidas
    largo = fields.Float("Largo (mm)")
    ancho = fields.Float("Ancho (mm)")
    espesor = fields.Float("Espesor")
    espesor_unit = fields.Selection([
        ("in", "Pulgadas (in)"), ("mm", "Milímetros (mm)"),
    ], default="in")
    espesor_label = fields.Char(compute="_compute_espesor_label")

    # Hexágono unificado a 4 tipos (req. 5.1)
    hexagono = fields.Selection([
        ("tipo_1", "Tipo 1"), ("tipo_2", "Tipo 2"),
        ("tipo_3", "Tipo 3"), ("tipo_4", "Tipo 4"),
    ])

    resistencia = fields.Float("Resistencia (Lbf)")
    resistencia_na = fields.Boolean("Resistencia No Aplica")
    apariencia = fields.Selection([
        ("cumple", "Cumple"), ("no_cumple", "No Cumple"),
    ])
    humedad_pct = fields.Float("% Humedad")
    ranurado_unit = fields.Selection([
        ("mm", "Milímetros (mm)"), ("in", "Pulgadas (in)"),
    ], default="mm")
    ranurado_ids = fields.One2many("quality.inspection.ranurado",
                                   "inspection_id", string="Ranurado")
    troquelado_ids = fields.One2many("quality.inspection.troquelado",
                                     "inspection_id", string="Troquelado")
    pegado_result = fields.Selection([
        ("cumple", "Cumple"), ("no_cumple", "No Cumple"),
    ])

    # Octágono - campos extendidos (req. 5.5)
    oct_ancho = fields.Float("Ancho Octágono (mm)")
    oct_espesor = fields.Float("Espesor Octágono (mm)")
    oct_hexagono = fields.Float("Hexágono Octágono")
    oct_retiramiento = fields.Float("Retiramiento (cm)")
    oct_alineacion = fields.Selection([
        ("cumple", "Cumple"), ("no_cumple", "No Cumple"),
    ], string="Alineación")
    oct_pegado = fields.Selection([
        ("cumple", "Cumple"), ("no_cumple", "No Cumple"),
    ], string="Pegado Octágono")

    # Datos de Producción
    numero_corrida = fields.Char("Número de Corrida")
    papel_ancho = fields.Float("Ancho del Papel")
    papel_gramaje = fields.Float("Gramaje del Papel")
    papel_proveedor_id = fields.Many2one(
        "res.partner", "Proveedor del Papel",
        domain=[("supplier_rank", ">", 0)])
    adhesivo_lote1 = fields.Char("Lote 1 Adhesivo")
    adhesivo_lote2 = fields.Char("Lote 2 Adhesivo")
    tipo_hexagono = fields.Selection([
        ("tipo_1", "Tipo 1"), ("tipo_2", "Tipo 2"),
        ("tipo_3", "Tipo 3"), ("tipo_4", "Tipo 4"),
    ])
    calibracion = fields.Float("Calibración", digits=(16, 6))
    engomado = fields.Selection([
        ("cumple", "Cumple"), ("no_cumple", "No Cumple"),
    ])
    corte_guillotina = fields.Selection([
        ("si", "Sí"), ("no", "No"),
    ], string="Corte en Guillotina")

    # Guillotina extras (req. 5.6)
    reticula_extendida = fields.Float("Retícula Extendida (cm)")
    reticula_vueltas = fields.Integer("Cantidad de Vueltas")
    lote_reticula = fields.Char("Lote de Retícula")
    gramaje_reticula = fields.Float("Gramaje de Retícula")
    sin_supervisor = fields.Boolean("Sin Supervisor")

    # Evidencia
    evidence_pdf = fields.Binary("Evidencia (PDF)", attachment=True)
    evidence_pdf_name = fields.Char()
    evidence_image_ids = fields.Many2many(
        "ir.attachment", "quality_inspection_evidence_rel",
        "inspection_id", "attachment_id", string="Evidencia (Imágenes)",
        help="Hasta 10 imágenes",
    )

    notes = fields.Html("Observaciones")
    certificate_ids = fields.One2many("quality.certificate",
                                      "inspection_id", string="Certificados")
    certificate_count = fields.Integer(compute="_compute_certificate_count")
    company_id = fields.Many2one("res.company", "Compañía",
                                 default=lambda s: s.env.company)

    # ------------------------------------------------------------------ compute
    @api.depends("process_type_id", "process_type_id.code")
    def _compute_inspection_type(self):
        legacy = ("laminadora_remanejo", "octagono", "guillotina_pegado")
        for rec in self:
            code = rec.process_type_id.code
            rec.inspection_type = code if code in legacy else False

    @api.depends("certificate_ids")
    def _compute_certificate_count(self):
        for rec in self:
            rec.certificate_count = len(rec.certificate_ids)

    @api.depends("espesor_unit")
    def _compute_espesor_label(self):
        for rec in self:
            rec.espesor_label = ("Espesor (mm)" if rec.espesor_unit == "mm"
                                 else "Espesor (in)")

    @api.depends("pp_pt")
    def _compute_is_pp_pt(self):
        for rec in self:
            rec.is_pp = rec.pp_pt == "pp"
            rec.is_pt = rec.pp_pt == "pt"

    @api.constrains("evidence_image_ids")
    def _check_image_count(self):
        for rec in self:
            if len(rec.evidence_image_ids) > 10:
                raise ValidationError(_(
                    "Máximo 10 imágenes de evidencia por inspección."
                ))

    @api.onchange("resistencia_na")
    def _onchange_resistencia_na(self):
        if self.resistencia_na:
            self.resistencia = 0.0

    @api.onchange("largo", "ancho", "espesor", "humedad_pct", "resistencia",
                  "calibracion")
    def _onchange_alert_zero(self):
        """Alerta cuando se ingresan valores en cero (req. 5.1)."""
        zeros = []
        if self.show_largo and self.largo == 0:
            zeros.append("Largo")
        if self.show_ancho and self.ancho == 0:
            zeros.append("Ancho")
        if self.show_espesor and self.espesor == 0:
            zeros.append("Espesor")
        if self.show_humedad and self.humedad_pct == 0:
            zeros.append("Humedad")
        if (self.show_resistencia and not self.resistencia_na
                and self.resistencia == 0):
            zeros.append("Resistencia")
        if zeros:
            return {
                "warning": {
                    "title": _("Valores en cero"),
                    "message": _(
                        "Atención: %s en 0. Verifique la captura."
                    ) % ", ".join(zeros),
                }
            }

    @api.onchange("production_order_id")
    def _onchange_production_order(self):
        """Auto-enlazar cliente y producto desde la OP (req. 5.7)."""
        if self.production_order_id:
            mo = self.production_order_id
            if mo.product_id:
                self.product_id = mo.product_id
            # En MRP la OP no tiene partner directo, lo tomamos de la SO si existe
            origin_so = self.env["sale.order"].search([
                ("name", "=", mo.origin)], limit=1) if mo.origin else False
            if origin_so and origin_so.partner_id:
                self.partner_id = origin_so.partner_id

    @api.onchange("product_id")
    def _onchange_product_partner(self):
        """Si hay producto y aún no hay cliente, NO sobrescribir.
        Solo registrar que el cliente debe coincidir con la OP."""
        # Hook reservado para reglas adicionales por cliente.
        pass

    @api.onchange("process_type_id", "product_id")
    def _onchange_load_attribute_templates(self):
        if not self.process_type_id and not self.product_id:
            return
        templates = self.env["quality.attribute.template"]
        if self.process_type_id:
            templates |= self.process_type_id.attribute_template_ids.filtered(
                lambda t: not t.product_tmpl_id and t.active)
        if self.product_id and self.product_id.product_tmpl_id:
            templates |= self.env["quality.attribute.template"].search([
                ("product_tmpl_id", "=", self.product_id.product_tmpl_id.id),
                ("active", "=", True),
            ])
        if templates:
            lines = [(5, 0, 0)]
            seen_names = set()
            for t in templates:
                # Detección de duplicados (req. 5.1)
                if t.name.strip().lower() in seen_names:
                    continue
                seen_names.add(t.name.strip().lower())
                lines.append((0, 0, {
                    "attribute_template_id": t.id,
                    "name": t.name,
                    "attribute_type": t.attribute_type,
                    "min_value": t.min_value,
                    "max_value": t.max_value,
                    "unit": t.unit,
                    "sequence": t.sequence,
                }))
            self.line_ids = lines

    # ------------------------------------------------------------------- create
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Nuevo") == "Nuevo":
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "quality.inspection") or "Nuevo"
        return super().create(vals_list)

    # ---------------------------------------------------------- helpers bloqueo
    def _check_previous_process(self):
        """Secuencia obligatoria entre procesos (req. 5.2)."""
        for rec in self:
            code = rec.process_type_id.code
            if code not in PROCESS_SEQUENCE:
                continue
            idx = PROCESS_SEQUENCE.index(code)
            if idx == 0:
                continue
            previous = PROCESS_SEQUENCE[idx - 1]
            prev = self.search([
                ("lot_id", "=", rec.lot_id.id),
                ("process_type_id.code", "=", previous),
                ("state", "=", "aceptado"),
            ], limit=1)
            if not prev:
                raise UserError(_(
                    "Secuencia bloqueada: para liberar este proceso primero "
                    "debe estar liberado el proceso previo (%s) para el lote %s."
                ) % (previous.replace("_", " ").title(),
                     rec.lot_id.name or "—"))

    def _check_measures_captured(self):
        """Bloqueo guardar si no se capturan Medidas y Propiedades (req. 5.1)."""
        for rec in self:
            checks = []
            # Troquelado: obligatorio capturar al menos una línea (req. 5.7)
            if (rec.process_type_id.code == "troquelado_plano"
                    and not rec.troquelado_ids):
                raise UserError(_(
                    "Proceso Troquelado: debe capturar al menos una medida "
                    "en la pestaña Troquelado antes de liberar."
                ))
            # Sierras y Ranuradoras: obligatorio capturar al menos una línea
            if (rec.process_type_id.code == "sierras_ranuradoras"
                    and rec.show_ranurado and not rec.ranurado_ids):
                raise UserError(_(
                    "Proceso Sierras y Ranuradoras: capture al menos una "
                    "medida en la pestaña Ranurado antes de liberar."
                ))
            if rec.show_largo and not rec.largo:
                checks.append("Largo")
            if rec.show_ancho and not (rec.ancho or rec.oct_ancho):
                checks.append("Ancho")
            if rec.show_espesor and not (rec.espesor or rec.oct_espesor):
                checks.append("Espesor")
            if rec.show_hexagono and not rec.hexagono:
                checks.append("Hexágono")
            if (rec.show_resistencia and not rec.resistencia_na
                    and not rec.resistencia):
                checks.append("Resistencia")
            if rec.show_apariencia and not rec.apariencia:
                checks.append("Apariencia")
            if rec.show_humedad and not rec.humedad_pct:
                checks.append("Humedad")
            if checks:
                raise UserError(_(
                    "Capture Medidas y Propiedades antes de cerrar la "
                    "inspección. Faltan: %s"
                ) % ", ".join(checks))

    # ----- transiciones ------------------------------------------------------
    def action_start(self):
        for rec in self:
            rec.state = "en_proceso"
            rec.message_post(body=_("⏱ Inspección iniciada."),
                             subtype_xmlid="mail.mt_comment")

    def action_accept(self):
        for rec in self:
            if rec.state != "en_proceso":
                raise UserError(_(
                    "Debe presionar 'INICIAR INSPECCION' antes de liberar."))
            rec._check_measures_captured()
            rec._check_previous_process()
            rec.state = "aceptado"
            rec.message_post(
                body=_("✅ Inspección ACEPTADA por %s") % self.env.user.name,
                subtype_xmlid="mail.mt_comment")

    def action_retain(self):
        for rec in self:
            rec.state = "retenido"
            partners = []
            if rec.supervisor_id and rec.supervisor_id.user_id and \
                    rec.supervisor_id.user_id.partner_id:
                partners.append(rec.supervisor_id.user_id.partner_id.id)
                rec.message_subscribe([rec.supervisor_id.user_id.partner_id.id])
            rec.message_post(
                body=_(
                    "⚠️ Producto RETENIDO por %s. Lote: %s. "
                    "Notificando al supervisor en turno: %s."
                ) % (self.env.user.name, rec.lot_id.name or "N/A",
                     rec.supervisor_id.name or "—"),
                partner_ids=partners,
                subtype_xmlid="mail.mt_comment")
            if rec.production_order_id and rec.production_order_id.user_id:
                rec.activity_schedule(
                    "mail.mail_activity_data_todo",
                    date_deadline=fields.Date.today() + timedelta(days=1),
                    summary=_("Producto retenido en Calidad: %s") % rec.name,
                    user_id=rec.production_order_id.user_id.id,
                )

    def action_reject(self):
        for rec in self:
            rec.state = "rechazado"

    def action_reset_draft(self):
        for rec in self:
            rec.state = "borrador"

    def action_create_certificate(self):
        self.ensure_one()
        if self.state != "aceptado":
            raise UserError(_(
                "Solo se pueden crear certificados de inspecciones aceptadas."))
        return {
            "type": "ir.actions.act_window",
            "name": _("Crear Certificado"),
            "res_model": "quality.certificate.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_inspection_id": self.id,
                "default_partner_id": self.partner_id.id,
            },
        }

    def action_view_certificates(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Certificados"),
            "res_model": "quality.certificate",
            "view_mode": "list,form",
            "domain": [("inspection_id", "=", self.id)],
            "context": {"default_inspection_id": self.id},
        }

    def action_print_inspection(self):
        return self.env.ref(
            "quality_management.action_report_inspection_summary"
        ).report_action(self)
