# -*- coding: utf-8 -*-
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


class QualityInspection(models.Model):
    _name = "quality.inspection"
    _description = "Inspección de PP/PT"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_inspection desc, id desc"

    # FOLIO-QM-ODOO18-022: se define process_code en el archivo base para que
    # vistas heredadas, rutas y reportes puedan depender de un campo estable.
    process_code = fields.Char(
        related="process_type_id.code",
        store=True,
        readonly=True,
        index=True,
    )

    name = fields.Char(
        "Referencia",
        required=True,
        readonly=True,
        default="Nuevo",
        copy=False,
    )

    process_type_id = fields.Many2one(
        "quality.process.type",
        "Tipo de Proceso",
        required=True,
        tracking=True,
    )
    inspection_type = fields.Selection(
        [
            ("laminadora_remanejo", "Laminadora y Remanejo"),
            ("octagono", "Octágono"),
            ("guillotina_pegado", "Guillotina y Pegado"),
        ],
        compute="_compute_inspection_type",
        store=True,
    )

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

    production_order_id = fields.Many2one(
        "mrp.production",
        "Orden de Producción",
        tracking=True,
        required=True,
    )
    lot_id = fields.Many2one(
        "stock.lot",
        "Lote de Fabricación",
        tracking=True,
        required=True,
    )
    product_id = fields.Many2one(
        "product.product",
        "Producto",
        required=True,
        tracking=True,
    )
    operator_id = fields.Many2one(
        "hr.employee",
        "Operador",
        required=True,
    )
    # FOLIO-QM-ODOO18-023: supervisor deja de ser required a nivel ORM para permitir
    # la opción formal "Sin Supervisor"; el bloqueo real queda en constraint hardening.
    supervisor_id = fields.Many2one(
        "hr.employee",
        "Supervisor",
    )
    partner_id = fields.Many2one(
        "res.partner",
        "Cliente",
        required=True,
        tracking=True,
    )
    folio = fields.Char(
        "Folio de Producción",
        required=True,
        help="Formato: letras y/o números. Capture exactamente el folio impreso en el lote.",
    )
    code = fields.Char(
        "Código de Producto",
        required=True,
        help="Código interno del producto.",
    )
    shift = fields.Selection(
        [
            ("turno_1", "Turno 1"),
            ("turno_2", "Turno 2"),
            ("turno_3", "Turno 3"),
        ],
        required=True,
    )
    plant = fields.Selection(
        [
            ("planta_1", "Planta 1"),
            ("planta_2", "Planta 2"),
            ("planta_3", "Planta 3"),
            ("planta_6", "Planta 6"),
            ("planta_7", "Planta 7"),
        ],
        required=True,
    )
    inspector_id = fields.Many2one(
        "res.users",
        "Inspector de Calidad",
        required=True,
        default=lambda s: s.env.user,
        tracking=True,
    )

    date_inspection = fields.Datetime(
        "Fecha y Hora de Inspección",
        required=True,
        readonly=True,
        default=fields.Datetime.now,
    )

    state = fields.Selection(
        [
            ("borrador", "Borrador"),
            ("en_proceso", "En Proceso"),
            ("aceptado", "Aceptado"),
            ("retenido", "Retenido"),
            ("rechazado", "Rechazado"),
        ],
        default="borrador",
        required=True,
        tracking=True,
        copy=False,
    )

    pp_pt = fields.Selection(
        [
            ("pp", "Producto en Proceso (PP)"),
            ("pt", "Producto Terminado (PT)"),
        ],
        string="PP / PT",
        required=True,
        default="pp",
        tracking=True,
    )
    is_pp = fields.Boolean(compute="_compute_is_pp_pt")
    is_pt = fields.Boolean(compute="_compute_is_pp_pt")

    line_ids = fields.One2many(
        "quality.inspection.line",
        "inspection_id",
        string="Atributos Capturados",
    )

    largo = fields.Float("Largo (mm)")
    ancho = fields.Float("Ancho (mm)")
    espesor = fields.Float("Espesor")
    espesor_unit = fields.Selection(
        [
            ("in", "Pulgadas (in)"),
            ("mm", "Milímetros (mm)"),
        ],
        default="in",
    )
    espesor_label = fields.Char(compute="_compute_espesor_label")

    hexagono = fields.Selection(
        [
            ("tipo_1", "Tipo 1"),
            ("tipo_2", "Tipo 2"),
            ("tipo_3", "Tipo 3"),
            ("tipo_4", "Tipo 4"),
        ],
        string="Hexágono",
    )

    resistencia = fields.Float("Resistencia (Lbf)")
    resistencia_na = fields.Boolean("Resistencia No Aplica")
    apariencia = fields.Selection(
        [
            ("cumple", "Cumple"),
            ("no_cumple", "No Cumple"),
            ("na", "N/A"),
        ]
    )
    humedad_pct = fields.Float("% Humedad")
    ranurado_unit = fields.Selection(
        [
            ("mm", "Milímetros (mm)"),
            ("in", "Pulgadas (in)"),
        ],
        default="mm",
    )
    ranurado_ids = fields.One2many(
        "quality.inspection.ranurado",
        "inspection_id",
        string="Ranurado",
    )
    troquelado_ids = fields.One2many(
        "quality.inspection.troquelado",
        "inspection_id",
        string="Troquelado",
    )
    pegado_result = fields.Selection(
        [
            ("cumple", "Cumple"),
            ("no_cumple", "No Cumple"),
            ("na", "N/A"),
        ],
        string="Resultado de Pegado",
    )

    oct_ancho = fields.Float("Ancho Octágono (mm)")
    oct_espesor = fields.Float("Espesor Octágono (mm)")
    # FOLIO-QM-ODOO18-024: se conserva Float porque el módulo ya pudo haber
    # creado la columna como double precision; cambiarla a Selection rompe upgrade.
    oct_hexagono = fields.Float("Hexágono Octágono")
    oct_retiramiento = fields.Float("Retiramiento (cm)")
    oct_alineacion = fields.Selection(
        [
            ("cumple", "Cumple"),
            ("no_cumple", "No Cumple"),
            ("na", "N/A"),
        ],
        string="Alineación",
    )
    oct_pegado = fields.Selection(
        [
            ("cumple", "Cumple"),
            ("no_cumple", "No Cumple"),
            ("na", "N/A"),
        ],
        string="Pegado Octágono",
    )

    numero_corrida = fields.Char("Número de Corrida")
    papel_ancho = fields.Float("Ancho del Papel")
    papel_gramaje = fields.Float("Gramaje del Papel")
    papel_proveedor_id = fields.Many2one(
        "res.partner",
        "Proveedor del Papel",
        domain=[("supplier_rank", ">", 0)],
    )
    adhesivo_lote1 = fields.Char("Lote 1 Adhesivo")
    adhesivo_lote2 = fields.Char("Lote 2 Adhesivo")
    tipo_hexagono = fields.Selection(
        [
            ("tipo_1", "Tipo 1"),
            ("tipo_2", "Tipo 2"),
            ("tipo_3", "Tipo 3"),
            ("tipo_4", "Tipo 4"),
        ]
    )
    calibracion = fields.Float("Calibración", digits=(16, 6))
    engomado = fields.Selection(
        [
            ("cumple", "Cumple"),
            ("no_cumple", "No Cumple"),
            ("na", "N/A"),
        ]
    )
    corte_guillotina = fields.Selection(
        [
            ("si", "Sí"),
            ("no", "No"),
            ("na", "N/A"),
        ],
        string="Corte en Guillotina",
    )

    reticula_extendida = fields.Float("Retícula Extendida (cm)")
    reticula_vueltas = fields.Integer("Cantidad de Vueltas")
    lote_reticula = fields.Char("Lote de Retícula")
    gramaje_reticula = fields.Float("Gramaje de Retícula")
    sin_supervisor = fields.Boolean("Sin Supervisor")

    evidence_pdf = fields.Binary("Evidencia (PDF)", attachment=True)
    evidence_pdf_name = fields.Char()
    evidence_image_ids = fields.Many2many(
        "ir.attachment",
        "quality_inspection_evidence_rel",
        "inspection_id",
        "attachment_id",
        string="Evidencia (Imágenes)",
        help="Hasta 10 imágenes",
    )

    notes = fields.Html("Observaciones")
    certificate_ids = fields.One2many(
        "quality.certificate",
        "inspection_id",
        string="Certificados",
    )
    certificate_count = fields.Integer(compute="_compute_certificate_count")
    company_id = fields.Many2one(
        "res.company",
        "Compañía",
        default=lambda s: s.env.company,
    )

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
            rec.espesor_label = "Espesor (mm)" if rec.espesor_unit == "mm" else "Espesor (in)"

    @api.depends("pp_pt")
    def _compute_is_pp_pt(self):
        for rec in self:
            rec.is_pp = rec.pp_pt == "pp"
            rec.is_pt = rec.pp_pt == "pt"

    @api.constrains("evidence_image_ids")
    def _check_image_count(self):
        for rec in self:
            if len(rec.evidence_image_ids) > 10:
                raise ValidationError(_("Máximo 10 imágenes de evidencia por inspección."))

    @api.onchange("resistencia_na")
    def _onchange_resistencia_na(self):
        if self.resistencia_na:
            self.resistencia = 0.0

    @api.onchange(
        "largo",
        "ancho",
        "espesor",
        "humedad_pct",
        "resistencia",
        "calibracion",
    )
    def _onchange_alert_zero(self):
        zeros = []
        if self.show_largo and self.largo == 0:
            zeros.append("Largo")
        if self.show_ancho and self.ancho == 0:
            zeros.append("Ancho")
        if self.show_espesor and self.espesor == 0:
            zeros.append("Espesor")
        if self.show_humedad and self.humedad_pct == 0:
            zeros.append("Humedad")
        if self.show_resistencia and not self.resistencia_na and self.resistencia == 0:
            zeros.append("Resistencia")
        if zeros:
            return {
                "warning": {
                    "title": _("Valores en cero"),
                    "message": _("Atención: %s en 0. Verifique la captura.")
                    % ", ".join(zeros),
                }
            }
        return {}

    @api.onchange("production_order_id")
    def _onchange_production_order(self):
        if self.production_order_id:
            production = self.production_order_id
            if production.product_id:
                self.product_id = production.product_id

            sale_order = (
                self.env["sale.order"].search([("name", "=", production.origin)], limit=1)
                if production.origin
                else False
            )
            if sale_order and sale_order.partner_id:
                self.partner_id = sale_order.partner_id

    @api.onchange("product_id")
    def _onchange_product_partner(self):
        pass

    @api.onchange("process_type_id", "product_id")
    def _onchange_load_attribute_templates(self):
        if not self.process_type_id and not self.product_id:
            return

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

        if templates:
            lines = [(5, 0, 0)]
            seen_names = set()
            for template in templates.sorted(lambda item: (item.sequence, item.id)):
                key = (template.name or "").strip().lower()
                if key in seen_names:
                    continue
                seen_names.add(key)
                lines.append(
                    (
                        0,
                        0,
                        {
                            "attribute_template_id": template.id,
                            "name": template.name,
                            "attribute_type": template.attribute_type,
                            "min_value": template.min_value,
                            "max_value": template.max_value,
                            "unit": template.unit,
                            "sequence": template.sequence,
                        },
                    )
                )
            self.line_ids = lines

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Nuevo") == "Nuevo":
                vals["name"] = (
                    self.env["ir.sequence"].next_by_code("quality.inspection")
                    or "Nuevo"
                )
        return super().create(vals_list)

    def _check_previous_process(self):
        for rec in self:
            code = rec.process_type_id.code
            if code not in PROCESS_SEQUENCE:
                continue

            index = PROCESS_SEQUENCE.index(code)
            if index == 0:
                continue

            previous = PROCESS_SEQUENCE[index - 1]
            previous_inspection = self.search(
                [
                    ("lot_id", "=", rec.lot_id.id),
                    ("process_type_id.code", "=", previous),
                    ("state", "=", "aceptado"),
                ],
                limit=1,
            )
            if not previous_inspection:
                raise UserError(
                    _(
                        "Secuencia bloqueada: para liberar este proceso primero "
                        "debe estar liberado el proceso previo (%s) para el lote %s."
                    )
                    % (
                        previous.replace("_", " ").title(),
                        rec.lot_id.name or "—",
                    )
                )

    def _check_measures_captured(self):
        for rec in self:
            checks = []
            if rec.process_type_id.code == "troquelado_plano" and not rec.troquelado_ids:
                raise UserError(
                    _(
                        "Proceso Troquelado: debe capturar al menos una medida "
                        "en la pestaña Troquelado antes de liberar."
                    )
                )
            if (
                rec.process_type_id.code == "sierras_ranuradoras"
                and rec.show_ranurado
                and not rec.ranurado_ids
            ):
                raise UserError(
                    _(
                        "Proceso Sierras y Ranuradoras: capture al menos una "
                        "medida en la pestaña Ranurado antes de liberar."
                    )
                )
            if rec.show_largo and not rec.largo:
                checks.append("Largo")
            if rec.show_ancho and not (rec.ancho or rec.oct_ancho):
                checks.append("Ancho")
            if rec.show_espesor and not (rec.espesor or rec.oct_espesor):
                checks.append("Espesor")
            # FOLIO-QM-ODOO18-059: compatibilidad con registros instalados antes,
            # donde Octágono podía guardar el valor histórico en oct_hexagono.
            if rec.show_hexagono and not (
                rec.hexagono or rec.tipo_hexagono or rec.oct_hexagono
            ):
                checks.append("Hexágono")
            if rec.show_resistencia and not rec.resistencia_na and not rec.resistencia:
                checks.append("Resistencia")
            if rec.show_apariencia and not rec.apariencia:
                checks.append("Apariencia")
            if rec.show_humedad and not rec.humedad_pct:
                checks.append("Humedad")

            if checks:
                raise UserError(
                    _(
                        "Capture Medidas y Propiedades antes de cerrar la inspección. "
                        "Faltan: %s"
                    )
                    % ", ".join(checks)
                )

    def action_start(self):
        for rec in self:
            rec.state = "en_proceso"
            rec.message_post(
                body=_("Inspección iniciada."),
                subtype_xmlid="mail.mt_comment",
            )

    def action_accept(self):
        for rec in self:
            if rec.state != "en_proceso":
                raise UserError(_("Debe presionar 'INICIAR INSPECCION' antes de liberar."))
            rec._check_measures_captured()
            rec._check_previous_process()
            rec.state = "aceptado"
            rec.message_post(
                body=_("Inspección ACEPTADA por %s") % self.env.user.name,
                subtype_xmlid="mail.mt_comment",
            )

    def action_retain(self):
        for rec in self:
            rec.state = "retenido"
            partners = []
            if (
                rec.supervisor_id
                and rec.supervisor_id.user_id
                and rec.supervisor_id.user_id.partner_id
            ):
                partner_id = rec.supervisor_id.user_id.partner_id.id
                partners.append(partner_id)
                # FOLIO-QM-ODOO18-025: se usa el argumento explícito partner_ids
                # para evitar ambigüedad en message_subscribe.
                rec.message_subscribe(partner_ids=[partner_id])

            rec.message_post(
                body=_(
                    "Producto RETENIDO por %s. Lote: %s. "
                    "Notificando al supervisor en turno: %s."
                )
                % (
                    self.env.user.name,
                    rec.lot_id.name or "N/A",
                    rec.supervisor_id.name or "—",
                ),
                partner_ids=partners,
                subtype_xmlid="mail.mt_comment",
            )

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
        # FOLIO-QM-ODOO18-060: los grupos en vistas no son seguridad real;
        # se agrega validación backend para evitar RPC manual no autorizado.
        if not self.env.user.has_group("quality_management.group_quality_manager"):
            raise UserError(_("Solo Responsable de Calidad puede regresar inspecciones a borrador."))
        for rec in self:
            rec.state = "borrador"

    def action_create_certificate(self):
        self.ensure_one()
        if self.state != "aceptado":
            raise UserError(_("Solo se pueden crear certificados de inspecciones aceptadas."))
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