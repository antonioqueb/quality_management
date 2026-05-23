# -*- coding: utf-8 -*-
"""
Ajustes QI-024 — Inspecciones de Ranura / Sierras y Ranuradoras.

FOLIO-QM-ODOO18-076:
- Ranurado y Corte Sierra no deben nacer como "Cumple" por default.
- Se permite seleccionar Cumple / No Cumple / N/A manualmente.
- Se agrega evaluación automática opcional por tolerancia: +/- 3 mm o +/- 1/8".

FOLIO-QM-ODOO18-077:
- Sierras y Ranuradoras sustituye al paso obligatorio legacy "Remanejo"
  dentro del flujo estándar posterior a Laminadora.

FOLIO-QM-ODOO18-078:
- Al retener, se suscribe al contacto real del supervisor seleccionado
  en hr.employee, evitando que el chatter agregue a un usuario equivocado.

FOLIO-QM-ODOO18-079:
- La búsqueda de Orden de Producción desde inspección se refuerza para
  encontrar referencias HMP1/HMPx por nombre, producto, código u origen.
"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression


RANURA_STANDARD_SEQUENCE = [
    "octagono",
    "guillotina",
    "pegado",
    "laminadora",
    "sierras_ranuradoras",
    "troquelado_plano",
]


class QualityInspectionRanuradoQI024(models.Model):
    _inherit = "quality.inspection.ranurado"

    tipo_operacion = fields.Selection(
        [
            ("ranurado", "Ranurado"),
            ("corte_sierra", "Corte Sierra"),
        ],
        string="Operación",
        required=True,
        default=lambda self: self.env.context.get("default_tipo_operacion", "ranurado"),
        index=True,
    )
    concepto = fields.Char(
        "Concepto",
        default="Largo",
        required=True,
        help="Ejemplo: Largo, Ancho, Profundidad, Corte Sierra.",
    )
    medida_esperada = fields.Float(
        "Medida esperada",
        digits=(16, 4),
        help="Valor nominal contra el que se evalúa la tolerancia.",
    )
    medida = fields.Float(
        "Medida real",
        required=True,
        digits=(16, 4),
    )
    unidad = fields.Selection(
        [
            ("mm", "mm"),
            ("cm", "cm"),
            ("in", "in"),
        ],
        string="Unidad",
        default=lambda self: self.env.context.get("default_unidad", "mm"),
        required=True,
    )
    tolerancia = fields.Float(
        "Tolerancia (+/-)",
        digits=(16, 4),
        default=lambda self: self._default_tolerancia_qi024(),
        help="Por defecto: +/- 3 mm, +/- 0.3 cm o +/- 1/8 in.",
    )
    evaluar_por_tolerancia = fields.Boolean(
        "Evaluar por tolerancia",
        default=True,
        help=(
            "Si está activo y existe medida esperada, el resultado se calcula "
            "automáticamente. Si está apagado, el inspector selecciona Cumple/No Cumple."
        ),
    )
    desviacion = fields.Float(
        "Desviación",
        compute="_compute_desviacion_qi024",
        store=True,
        digits=(16, 4),
    )
    resultado = fields.Selection(
        [
            ("cumple", "Cumple"),
            ("no_cumple", "No Cumple"),
            ("na", "N/A"),
        ],
        string="Resultado",
        default=False,
    )

    @api.model
    def _default_tolerancia_qi024(self):
        unit = self.env.context.get("default_unidad", "mm")
        if unit == "in":
            return 0.125
        if unit == "cm":
            return 0.3
        return 3.0

    @api.depends("medida", "medida_esperada")
    def _compute_desviacion_qi024(self):
        for rec in self:
            if rec.medida_esperada:
                rec.desviacion = abs((rec.medida or 0.0) - rec.medida_esperada)
            else:
                rec.desviacion = 0.0

    @api.onchange("unidad")
    def _onchange_unidad_tolerancia_qi024(self):
        for rec in self:
            # FOLIO-QM-ODOO18-076: tolerancias estándar solicitadas para Ranurado/Corte Sierra.
            if rec.unidad == "in":
                rec.tolerancia = 0.125
            elif rec.unidad == "cm":
                rec.tolerancia = 0.3
            else:
                rec.tolerancia = 3.0

    @api.onchange("medida", "medida_esperada", "tolerancia", "evaluar_por_tolerancia")
    def _onchange_evalua_tolerancia_qi024(self):
        for rec in self:
            if not rec.evaluar_por_tolerancia:
                continue

            if not rec.medida_esperada:
                # Sin nominal, no se fuerza resultado; debe seleccionarlo la inspectora.
                continue

            rec.desviacion = abs((rec.medida or 0.0) - rec.medida_esperada)
            rec.resultado = "cumple" if rec.desviacion <= (rec.tolerancia or 0.0) else "no_cumple"

    @api.constrains("medida", "resultado")
    def _check_medida_resultado_qi024(self):
        for rec in self:
            if rec.resultado != "na" and rec.medida <= 0:
                raise ValidationError(
                    _("La medida de %s debe ser mayor a cero o marcarse como N/A.")
                    % (dict(rec._fields["tipo_operacion"].selection).get(rec.tipo_operacion) or rec.tipo_operacion)
                )
            if not rec.resultado:
                raise ValidationError(
                    _("Seleccione Resultado en %s: Cumple, No Cumple o N/A.")
                    % (dict(rec._fields["tipo_operacion"].selection).get(rec.tipo_operacion) or rec.tipo_operacion)
                )

    @api.constrains("tolerancia", "evaluar_por_tolerancia")
    def _check_tolerancia_qi024(self):
        for rec in self:
            if rec.evaluar_por_tolerancia and rec.tolerancia < 0:
                raise ValidationError(_("La tolerancia no puede ser negativa."))


class QualityInspectionQI024(models.Model):
    _inherit = "quality.inspection"

    corte_sierra_ids = fields.One2many(
        "quality.inspection.ranurado",
        "inspection_id",
        string="Corte Sierra",
        domain=[("tipo_operacion", "=", "corte_sierra")],
    )

    def _get_previous_process_code_hardening(self):
        self.ensure_one()
        code = self.process_code
        if code not in RANURA_STANDARD_SEQUENCE:
            return False

        index = RANURA_STANDARD_SEQUENCE.index(code)
        if index <= 0:
            return False

        return RANURA_STANDARD_SEQUENCE[index - 1]

    def _check_previous_process_hardening(self):
        """
        FOLIO-QM-ODOO18-077:
        La ruta obligatoria queda:
        Octágono -> Guillotina -> Pegado -> Laminadora -> Sierras y Ranuradoras -> Troquelado Plano.
        No se exige Remanejo como paso intermedio.
        """
        for rec in self:
            previous_code = rec._get_previous_process_code_hardening()
            if previous_code:
                previous_inspection = rec._find_previous_inspection_hardening(previous_code)
                if not previous_inspection:
                    raise UserError(rec._build_previous_process_block_message_hardening(previous_code))

            # Mantiene validación por ruta configurable para procesos fuera de la secuencia estándar.
            if rec.process_code in RANURA_STANDARD_SEQUENCE:
                continue

            if "quality_route_id" not in rec._fields or not rec.quality_route_id:
                continue

            route = rec.quality_route_id
            route_lines = route.line_ids.sorted("sequence")
            codes = [
                line.process_type_id.code
                for line in route_lines
                if line.process_type_id.code
            ]

            if rec.process_code not in codes:
                continue

            current_index = codes.index(rec.process_code)
            if current_index == 0:
                continue

            previous_route_code = False
            for index in range(current_index - 1, -1, -1):
                line = route_lines[index]
                if not line.is_optional:
                    previous_route_code = line.process_type_id.code
                    break

            if not previous_route_code:
                continue

            previous_inspection = rec._find_previous_inspection_hardening(previous_route_code)
            if previous_inspection:
                continue

            raise UserError(
                _(
                    "Ruta '%s': antes de liberar '%s' debe estar liberado "
                    "el proceso previo '%s'."
                )
                % (
                    route.name,
                    rec.process_type_id.name,
                    previous_route_code.replace("_", " ").title(),
                )
            )

        return True

    def _get_ranura_quality_lines_qi024(self):
        self.ensure_one()
        return self.ranurado_ids.filtered(
            lambda line: line.tipo_operacion in ("ranurado", "corte_sierra")
        )

    def _check_ranura_corte_sierra_qi024(self):
        for rec in self.filtered(lambda item: item.process_code == "sierras_ranuradoras"):
            lines = rec._get_ranura_quality_lines_qi024()
            if not lines:
                raise UserError(
                    _("Capture al menos una línea en Ranurado o Corte Sierra antes de liberar.")
                )

            missing_result = lines.filtered(lambda line: not line.resultado)
            if missing_result:
                raise UserError(
                    _("Seleccione Cumple/No Cumple/N/A en: %s")
                    % ", ".join(missing_result.mapped("concepto"))
                )

            failing = lines.filtered(lambda line: line.resultado == "no_cumple")
            if failing:
                raise UserError(
                    _(
                        "No se puede aceptar/liberar con resultados No Cumple en "
                        "Ranurado/Corte Sierra: %s. Retenga o rechace la inspección."
                    )
                    % ", ".join(failing.mapped("concepto"))
                )

    def _check_measures_captured_hardening(self):
        for rec in self:
            if rec.process_code == "sierras_ranuradoras":
                rec._check_ranura_corte_sierra_qi024()
                continue

            super(QualityInspectionQI024, rec)._check_measures_captured_hardening()

    def _full_quality_validation_hardening(self):
        for rec in self:
            if rec.state != "en_proceso":
                raise UserError(_("Debe presionar 'INICIAR INSPECCIÓN' antes de liberar."))

            rec._check_required_header_hardening()
            rec._check_reserved_duplicate_attributes_hardening()
            rec._check_measures_captured_hardening()
            rec._check_required_additional_attributes_hardening()
            if hasattr(rec, "_check_no_failing_results_hardening"):
                rec._check_no_failing_results_hardening()
            rec._check_previous_process_hardening()

    def _get_supervisor_partner_hardening(self):
        """
        FOLIO-QM-ODOO18-078:
        Prioriza el contacto del empleado supervisor. Usar solamente user_id.partner_id
        puede suscribir a otro usuario si el empleado está mal enlazado.
        """
        self.ensure_one()
        supervisor = self.supervisor_id
        Partner = self.env["res.partner"].sudo()

        if not supervisor:
            return Partner.browse()

        work_contact = getattr(supervisor, "work_contact_id", False)
        if work_contact:
            return work_contact

        if supervisor.user_id and supervisor.user_id.partner_id:
            return supervisor.user_id.partner_id

        private_contact = getattr(supervisor, "address_home_id", False)
        if private_contact:
            return private_contact

        work_email = getattr(supervisor, "work_email", False)
        if work_email:
            partner = Partner.search([("email", "=", work_email)], limit=1)
            if partner:
                return partner

        return Partner.browse()

    def action_retain(self):
        """
        FOLIO-QM-ODOO18-078:
        Retiene y suscribe al supervisor real. Se replica el flujo de hardening +
        retention_flow para no perder bitácora ni subestado.
        """
        for rec in self:
            if rec.state != "en_proceso":
                raise UserError(_("Solo se puede retener una inspección en proceso."))

            rec._check_reserved_duplicate_attributes_hardening()
            rec.state = "retenido"

            if "retention_state" in rec._fields:
                rec.retention_state = "retenido"
                if hasattr(rec, "_log_retention"):
                    rec._log_retention(_("Producto retenido por Calidad."))

            supervisor_user = rec._get_supervisor_user_hardening()
            supervisor_partner = rec._get_supervisor_partner_hardening()
            partner_ids = supervisor_partner.ids

            if partner_ids:
                rec.message_subscribe(partner_ids=partner_ids)

            if supervisor_user:
                rec.activity_schedule(
                    "mail.mail_activity_data_todo",
                    date_deadline=fields.Date.today(),
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

            if hasattr(rec, "_notify_quality_non_conformance_hardening"):
                rec._notify_quality_non_conformance_hardening(_("Producto RETENIDO"))

    def action_correction_done(self):
        """
        FOLIO-QM-ODOO18-078:
        También refuerza la suscripción al supervisor en el momento en que
        Producción marca la corrección como hecha, cubriendo registros retenidos
        antes de instalar este ajuste.
        """
        for rec in self:
            if "retention_state" not in rec._fields:
                raise UserError(_("El flujo de retención no está disponible."))

            if rec.retention_state not in ("retenido", "en_correccion"):
                raise UserError(_("La inspección no está en estado de corrección."))

            rec.retention_state = "correccion_hecha"
            rec.retention_correction_done_by = self.env.user
            rec.retention_correction_done_date = fields.Datetime.now()

            if hasattr(rec, "_log_retention"):
                rec._log_retention(_("Supervisor/Producción marca corrección como HECHA."))

            partner_ids = []
            supervisor_partner = rec._get_supervisor_partner_hardening()
            if supervisor_partner:
                partner_ids.extend(supervisor_partner.ids)
                rec.message_subscribe(partner_ids=supervisor_partner.ids)

            inspector = rec.inspector_id
            if inspector:
                rec.activity_schedule(
                    "mail.mail_activity_data_todo",
                    date_deadline=fields.Date.today(),
                    summary=_("Reinspeccionar producto: %s") % rec.name,
                    user_id=inspector.id,
                )
                if inspector.partner_id:
                    partner_ids.append(inspector.partner_id.id)

            rec.message_post(
                body=_("Producción marcó corrección hecha. Calidad debe REINSPECCIONAR."),
                partner_ids=list(set(partner_ids)),
                subtype_xmlid="mail.mt_comment",
            )


class MrpProductionQI024(models.Model):
    _inherit = "mrp.production"

    @api.model
    def _name_search(
        self,
        name="",
        args=None,
        operator="ilike",
        limit=100,
        name_get_uid=None,
        order=None,
        **kwargs,
    ):
        """
        FOLIO-QM-ODOO18-079:
        Permite localizar OP HMP1/HMPx desde el selector de inspección buscando
        por referencia de OP, producto, código interno u origen.

        Se acepta **kwargs para tolerar variantes de firma entre Odoo 17/18
        donde el dominio puede llegar como args o como domain.
        """
        domain = kwargs.pop("domain", None)
        if args is None and domain is not None:
            args = domain
        args = list(args or [])

        if self.env.context.get("quality_inspection_mrp_search") and name:
            search_domain = [
                "|", "|", "|",
                ("name", operator, name),
                ("product_id.name", operator, name),
                ("product_id.default_code", operator, name),
                ("origin", operator, name),
            ]
            final_domain = expression.AND([args, search_domain])
            try:
                return self._search(
                    final_domain,
                    limit=limit,
                    order=order,
                    access_rights_uid=name_get_uid,
                )
            except TypeError:
                return self._search(
                    final_domain,
                    limit=limit,
                    access_rights_uid=name_get_uid,
                )

        try:
            return super()._name_search(
                name=name,
                args=args,
                operator=operator,
                limit=limit,
                name_get_uid=name_get_uid,
                order=order,
                **kwargs,
            )
        except TypeError:
            return super()._name_search(
                name=name,
                args=args,
                operator=operator,
                limit=limit,
                name_get_uid=name_get_uid,
                **kwargs,
            )