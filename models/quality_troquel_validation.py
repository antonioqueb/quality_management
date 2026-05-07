# -*- coding: utf-8 -*-
"""
Flujo formal de troqueles:
- Validación dimensional + funcional con líneas.
- Reparación con bitácora detallada.
- Revisiones por uso/piezas.
"""
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class QualityTroquelValidation(models.Model):
    _name = "quality.troquel.validation"
    _description = "Validación de Troquel"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date desc, id desc"

    name = fields.Char("Referencia", default="Nueva", readonly=True, copy=False)
    troquel_id = fields.Many2one(
        "quality.troquel", required=True, ondelete="cascade",
        tracking=True, index=True)
    date = fields.Datetime(default=fields.Datetime.now, required=True)
    convoked_quality = fields.Boolean("Calidad Convocada")
    convoked_production = fields.Boolean("Producción Convocada")

    quality_user_id = fields.Many2one("res.users", "Calidad")
    production_user_id = fields.Many2one("res.users", "Producción")
    design_user_id = fields.Many2one("res.users", "Diseño")

    line_ids = fields.One2many(
        "quality.troquel.validation.line", "validation_id",
        string="Mediciones / Pruebas")

    dimensional_ok = fields.Boolean(
        "Dimensional OK", compute="_compute_results", store=True)
    functional_ok = fields.Boolean(
        "Funcional OK", compute="_compute_results", store=True)
    overall_ok = fields.Boolean(
        "Resultado Global", compute="_compute_results", store=True)

    state = fields.Selection([
        ("borrador", "Borrador"),
        ("en_validacion", "En Validación"),
        ("aprobado", "Aprobado"),
        ("rechazado", "Rechazado"),
    ], default="borrador", required=True, tracking=True)
    notes = fields.Text("Observaciones")

    @api.depends("line_ids.result", "line_ids.test_type")
    def _compute_results(self):
        for rec in self:
            dims = rec.line_ids.filtered(lambda l: l.test_type == "dimensional")
            funcs = rec.line_ids.filtered(lambda l: l.test_type == "funcional")
            rec.dimensional_ok = bool(dims) and all(
                l.result == "cumple" for l in dims)
            rec.functional_ok = bool(funcs) and all(
                l.result == "cumple" for l in funcs)
            rec.overall_ok = rec.dimensional_ok and rec.functional_ok

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Nueva") == "Nueva":
                vals["name"] = "TVAL-%s" % (
                    self.env["ir.sequence"].next_by_code(
                        "quality.troquel.validation") or "0001")
        return super().create(vals_list)

    def action_start(self):
        for rec in self:
            rec.state = "en_validacion"

    def action_approve(self):
        for rec in self:
            if not rec.dimensional_ok or not rec.functional_ok:
                raise UserError(_(
                    "No se puede aprobar: faltan pruebas dimensionales o funcionales OK."))
            rec.state = "aprobado"
            rec.troquel_id.action_activate()

    def action_reject(self):
        for rec in self:
            rec.state = "rechazado"
            rec.troquel_id.message_post(
                body=_("❌ Validación rechazada (%s).") % rec.name,
                subtype_xmlid="mail.mt_comment")


class QualityTroquelValidationLine(models.Model):
    _name = "quality.troquel.validation.line"
    _description = "Línea de Validación de Troquel"
    _order = "sequence, id"

    validation_id = fields.Many2one(
        "quality.troquel.validation", required=True, ondelete="cascade")
    sequence = fields.Integer(default=10)
    test_type = fields.Selection([
        ("dimensional", "Dimensional"),
        ("funcional", "Funcional"),
    ], required=True, default="dimensional")
    name = fields.Char("Concepto / Punto de Medición", required=True)
    expected = fields.Char("Valor Esperado / Especificación")
    measured = fields.Char("Valor Medido / Observado")
    tolerance = fields.Char("Tolerancia")
    result = fields.Selection([
        ("cumple", "Cumple"),
        ("no_cumple", "No Cumple"),
        ("na", "N/A"),
    ], default="na", required=True)
    notes = fields.Char("Notas")


class QualityTroquelRepair(models.Model):
    _name = "quality.troquel.repair"
    _description = "Reparación de Troquel"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_started desc, id desc"

    name = fields.Char(default="Nueva", readonly=True, copy=False)
    troquel_id = fields.Many2one(
        "quality.troquel", required=True, ondelete="cascade", index=True)
    repair_type = fields.Selection([
        ("interna", "Interna"),
        ("proveedor", "Proveedor Externo"),
    ], required=True, default="interna")
    proveedor_id = fields.Many2one(
        "res.partner", "Proveedor",
        domain=[("supplier_rank", ">", 0)])
    date_started = fields.Datetime(
        "Inicio Reparación", default=fields.Datetime.now, required=True)
    date_finished = fields.Datetime("Fin Reparación")
    days_estimated = fields.Integer("Días Estimados Fuera")
    description = fields.Text("Desglose de Reparación", required=True)
    cost = fields.Monetary("Costo")
    currency_id = fields.Many2one(
        "res.currency", default=lambda s: s.env.company.currency_id)
    state = fields.Selection([
        ("en_curso", "En Curso"),
        ("finalizada", "Finalizada"),
        ("rechazada", "Rechazada"),
    ], default="en_curso", required=True, tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Nueva") == "Nueva":
                vals["name"] = "TREP-%s" % (
                    self.env["ir.sequence"].next_by_code(
                        "quality.troquel.repair") or "0001")
        return super().create(vals_list)

    def action_finish(self):
        for rec in self:
            rec.state = "finalizada"
            rec.date_finished = fields.Datetime.now()
            rec.troquel_id.message_post(
                body=_("🔧 Reparación %s finalizada.") % rec.name,
                subtype_xmlid="mail.mt_comment")


class QualityTroquelExtended(models.Model):
    _inherit = "quality.troquel"

    validation_ids = fields.One2many(
        "quality.troquel.validation", "troquel_id",
        string="Validaciones")
    validation_count = fields.Integer(compute="_compute_counts")
    repair_ids = fields.One2many(
        "quality.troquel.repair", "troquel_id",
        string="Reparaciones")
    repair_count = fields.Integer(compute="_compute_counts")
    pieces_produced = fields.Integer(
        "Piezas Producidas Acumuladas",
        help="Conteo manual de piezas troqueladas para programar revisión.")
    needs_review = fields.Boolean(
        "Requiere Revisión", compute="_compute_needs_review", store=True)

    @api.depends("validation_ids", "repair_ids")
    def _compute_counts(self):
        for rec in self:
            rec.validation_count = len(rec.validation_ids)
            rec.repair_count = len(rec.repair_ids)

    @api.depends("pieces_produced", "pieces_per_review")
    def _compute_needs_review(self):
        for rec in self:
            rec.needs_review = bool(
                rec.pieces_per_review and
                rec.pieces_produced >= rec.pieces_per_review)

    def action_open_validation(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Validación de Troquel"),
            "res_model": "quality.troquel.validation",
            "view_mode": "form",
            "target": "current",
            "context": {"default_troquel_id": self.id},
        }

    def action_open_repair(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Reparación de Troquel"),
            "res_model": "quality.troquel.repair",
            "view_mode": "form",
            "target": "current",
            "context": {"default_troquel_id": self.id},
        }
