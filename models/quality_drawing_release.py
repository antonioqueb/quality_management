# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class QualityDrawingRelease(models.Model):
    _name = "quality.drawing.release"
    _description = "Liberación de Planos"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_requested desc, id desc"

    MAX_MODIFICATIONS = 3

    name = fields.Char(
        "Referencia",
        required=True,
        readonly=True,
        default="Nuevo",
        copy=False,
    )
    partner_id = fields.Many2one(
        "res.partner",
        "Cliente",
        required=True,
        tracking=True,
    )
    sale_order_id = fields.Many2one(
        "sale.order",
        "Orden de Venta",
        tracking=True,
        domain="[('partner_id', '=', partner_id)]",
    )

    request_type = fields.Selection(
        [
            ("alta", "Alta"),
            ("actualizacion", "Actualización"),
        ],
        string="Tipo de Solicitud",
        required=True,
        default="alta",
        tracking=True,
    )

    drawing_path = fields.Char(
        "Dirección de Alta del Plano",
        help="Ej: C:\\Users\\Calidad\\Nextcloud\\000 ALTAS...",
    )

    req_sellos = fields.Boolean("Sellos Requeridos")
    req_sellos_date = fields.Date("Fecha Arribo Sellos")
    req_plantilla = fields.Boolean("Plantilla Requerida")
    req_plantilla_date = fields.Date("Fecha Arribo Plantilla")
    req_troquel = fields.Boolean("Troquel Requerido")
    req_troquel_date = fields.Date("Fecha Arribo Troquel")
    req_otro = fields.Boolean("Otro Requerido")
    req_otro_desc = fields.Char("Especifique Otro")
    req_otro_date = fields.Date("Fecha Arribo Otro")

    drawing_attachment_ids = fields.Many2many(
        "ir.attachment",
        "quality_drawing_attachment_rel",
        "drawing_id",
        "attachment_id",
        string="Plano y Cotización/Dibujo",
        required=True,
    )
    drawing_pdf = fields.Binary("Plano Principal (PDF)", attachment=True)
    drawing_pdf_name = fields.Char("Nombre del Plano")
    quotation_pdf = fields.Binary("Cotización/Dibujo (PDF)", attachment=True)
    quotation_pdf_name = fields.Char("Nombre Cotización")

    requested_by = fields.Many2one(
        "res.users",
        "Solicitante (Ventas)",
        required=True,
        default=lambda s: s.env.user,
        tracking=True,
    )
    inspector_id = fields.Many2one(
        "res.users",
        "Inspector de Calidad",
        tracking=True,
        domain="[('groups_id', 'in', [ref('quality_management.group_quality_inspector')])]",
    )

    state = fields.Selection(
        [
            ("borrador", "Borrador"),
            ("en_revision", "En Revisión Calidad"),
            ("aceptado_calidad", "Aceptado por Calidad"),
            ("aceptado_ventas", "Aceptado por Ventas"),
            ("aceptado_diseno", "Aceptado por Diseño (Final)"),
            ("rechazado", "Rechazado"),
            ("cerrada", "Cerrada por Exceso de Modificaciones"),
        ],
        default="borrador",
        required=True,
        tracking=True,
        copy=False,
    )

    rejection_reason = fields.Text("Motivo de Rechazo")

    date_requested = fields.Datetime(
        "Fecha de Solicitud",
        readonly=True,
        copy=False,
    )
    date_release_expected = fields.Datetime(
        "Fecha Liberación Esperada",
        compute="_compute_release_expected",
        store=True,
        readonly=True,
    )
    date_released = fields.Datetime(
        "Fecha de Liberación Real",
        readonly=True,
        copy=False,
    )

    accepted_by_quality = fields.Many2one(
        "res.users",
        "Calidad Aceptó",
        readonly=True,
    )
    accepted_by_quality_date = fields.Datetime("Fecha Aceptación Calidad", readonly=True)
    accepted_by_sales = fields.Many2one(
        "res.users",
        "Ventas Aceptó",
        readonly=True,
    )
    accepted_by_sales_date = fields.Datetime("Fecha Aceptación Ventas", readonly=True)
    accepted_by_design = fields.Many2one(
        "res.users",
        "Diseño Aceptó",
        readonly=True,
    )
    accepted_by_design_date = fields.Datetime("Fecha Aceptación Diseño", readonly=True)

    modification_ids = fields.One2many(
        "quality.drawing.modification",
        "drawing_id",
        string="Modificaciones",
    )
    modification_count = fields.Integer(
        compute="_compute_modification_count",
        store=True,
    )

    company_id = fields.Many2one(
        "res.company",
        "Compañía",
        default=lambda s: s.env.company,
    )

    @api.depends("date_requested")
    def _compute_release_expected(self):
        for rec in self:
            rec.date_release_expected = (
                rec.date_requested + timedelta(hours=48)
                if rec.date_requested
                else False
            )

    @api.depends("modification_ids")
    def _compute_modification_count(self):
        for rec in self:
            rec.modification_count = len(rec.modification_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Nuevo") == "Nuevo":
                vals["name"] = (
                    self.env["ir.sequence"].next_by_code("quality.drawing.release")
                    or "Nuevo"
                )
        return super().create(vals_list)

    @api.constrains(
        "req_sellos",
        "req_sellos_date",
        "req_plantilla",
        "req_plantilla_date",
        "req_troquel",
        "req_troquel_date",
        "req_otro",
        "req_otro_desc",
        "req_otro_date",
    )
    def _check_required_arrival_dates(self):
        for rec in self:
            # FOLIO-QM-ODOO18-015: si Ventas marca requisitos de fabricación,
            # debe capturar sus fechas/detalles antes de enviar a Calidad.
            missing = []
            if rec.req_sellos and not rec.req_sellos_date:
                missing.append(_("Fecha Arribo Sellos"))
            if rec.req_plantilla and not rec.req_plantilla_date:
                missing.append(_("Fecha Arribo Plantilla"))
            if rec.req_troquel and not rec.req_troquel_date:
                missing.append(_("Fecha Arribo Troquel"))
            if rec.req_otro and not rec.req_otro_desc:
                missing.append(_("Descripción de Otro Requerido"))
            if rec.req_otro and not rec.req_otro_date:
                missing.append(_("Fecha Arribo Otro"))

            if missing:
                raise ValidationError(
                    _("Complete los requisitos de fabricación: %s")
                    % ", ".join(missing)
                )

    def _check_documents(self):
        for rec in self:
            # FOLIO-QM-ODOO18-016: se valida explícitamente que existan ambos documentos
            # fuente, no solo adjuntos genéricos.
            if not rec.drawing_pdf or not rec.quotation_pdf:
                raise UserError(
                    _(
                        "Debe cargar AMBOS documentos antes de avanzar: "
                        "Plano (PDF) y Cotización/Dibujo (PDF)."
                    )
                )

    def action_submit_review(self):
        for rec in self:
            if rec.modification_count >= self.MAX_MODIFICATIONS:
                rec._handle_max_modifications()
                continue

            rec._check_documents()
            rec.date_requested = fields.Datetime.now()
            rec.state = "en_revision"

            modification_number = rec.modification_count + 1
            self.env["quality.drawing.modification"].create(
                {
                    "drawing_id": rec.id,
                    "sequence": modification_number,
                    "description": _(
                        "Solicitud de revisión #%s enviada a Calidad."
                    )
                    % modification_number,
                }
            )
            self._notify_modification(rec, modification_number)

            users = rec.inspector_id
            if not users:
                group = self.env.ref(
                    "quality_management.group_quality_inspector",
                    raise_if_not_found=False,
                )
                users = group.users if group else self.env["res.users"]

            for user in users:
                rec.activity_schedule(
                    "mail.mail_activity_data_todo",
                    date_deadline=fields.Date.today() + timedelta(days=2),
                    summary=_("Revisión de plano: %s") % rec.name,
                    user_id=user.id,
                )

    def _notify_modification(self, rec, modification_number):
        """Avisos automáticos por número de modificación."""
        partner_ids = []
        if rec.requested_by.partner_id:
            partner_ids.append(rec.requested_by.partner_id.id)

        if modification_number == 1:
            body = _(
                "Solo tiene 3 oportunidades para realizar modificaciones "
                "al plano enviado a liberación de Calidad."
            )
        elif modification_number == 2:
            body = _(
                "Cambio solicitado #2: valide que los cambios solicitados "
                "por Calidad cumplen el requerimiento y que los demás datos "
                "están correctos."
            )
        elif modification_number == 3:
            body = _(
                "Cambio solicitado #3: se comparte incumplimiento al Jefe directo. "
                "Si vuelve a rechazarse, deberá iniciar el proceso nuevamente."
            )
            sales_managers = self.env.ref(
                "sales_team.group_sale_manager",
                raise_if_not_found=False,
            )
            if sales_managers:
                for user in sales_managers.users:
                    if user.partner_id:
                        partner_ids.append(user.partner_id.id)
        else:
            body = _("Modificación #%s registrada.") % modification_number

        rec.message_post(
            body=body,
            partner_ids=list(set(partner_ids)),
            subtype_xmlid="mail.mt_comment",
        )

    def _handle_max_modifications(self):
        for rec in self:
            # FOLIO-QM-ODOO18-017: al alcanzar el máximo de modificaciones,
            # el flujo debe cerrarse formalmente y no quedarse reintentando revisión.
            rec.state = "cerrada"
            rec.message_post(
                body=_(
                    "Se alcanzó el máximo de %s modificaciones. "
                    "La liberación se cierra. Debe iniciar nuevamente el proceso "
                    "(las modificaciones continuarán con el consecutivo: %s, %s, ...)."
                )
                % (
                    self.MAX_MODIFICATIONS,
                    self.MAX_MODIFICATIONS + 1,
                    self.MAX_MODIFICATIONS + 2,
                ),
                subtype_xmlid="mail.mt_comment",
            )

    def action_quality_accept(self):
        for rec in self:
            rec._check_documents()
            rec.state = "aceptado_calidad"
            rec.accepted_by_quality = self.env.user
            rec.accepted_by_quality_date = fields.Datetime.now()
            rec.message_post(
                body=_("Calidad aceptó el plano."),
                subtype_xmlid="mail.mt_comment",
            )

    def action_sales_accept(self):
        for rec in self:
            if rec.state != "aceptado_calidad":
                raise UserError(_("Calidad debe aceptar primero."))
            rec.state = "aceptado_ventas"
            rec.accepted_by_sales = self.env.user
            rec.accepted_by_sales_date = fields.Datetime.now()

    def action_design_accept(self):
        for rec in self:
            if rec.state != "aceptado_ventas":
                raise UserError(_("Ventas debe aceptar primero."))
            rec.state = "aceptado_diseno"
            rec.accepted_by_design = self.env.user
            rec.accepted_by_design_date = fields.Datetime.now()
            rec.date_released = fields.Datetime.now()
            rec.activity_feedback(
                ["mail.mail_activity_data_todo"],
                feedback=_("Plano liberado"),
            )

    def action_reject(self):
        for rec in self:
            if not rec.rejection_reason:
                raise ValidationError(_("Capture el motivo de rechazo."))
            rec.state = "rechazado"
            rec.activity_feedback(
                ["mail.mail_activity_data_todo"],
                feedback=_("Plano rechazado: %s") % rec.rejection_reason,
            )
            rec.message_post(
                body=_("Plano RECHAZADO por %s. Motivo: %s")
                % (self.env.user.name, rec.rejection_reason),
                subtype_xmlid="mail.mt_comment",
            )

    def action_reset_draft(self):
        for rec in self:
            if rec.modification_count >= self.MAX_MODIFICATIONS:
                raise UserError(
                    _(
                        "No se puede regresar a borrador: se excedió el máximo "
                        "de modificaciones permitidas."
                    )
                )
            rec.state = "borrador"
            rec.rejection_reason = False

    def action_print_drawing_release(self):
        return self.env.ref(
            "quality_management.action_report_drawing_release"
        ).report_action(self)