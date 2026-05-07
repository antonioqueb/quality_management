# -*- coding: utf-8 -*-
"""
Rutas de proceso configurables por producto/categoría.
Reemplaza la secuencia fija PROCESS_SEQUENCE cuando hay una ruta definida.
"""
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class QualityProcessRoute(models.Model):
    _name = "quality.process.route"
    _description = "Ruta de Proceso de Calidad"
    _order = "sequence, id"

    name = fields.Char("Nombre de la Ruta", required=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    product_tmpl_ids = fields.Many2many(
        "product.template", string="Productos Aplicables")
    product_categ_ids = fields.Many2many(
        "product.category", string="Categorías Aplicables")
    line_ids = fields.One2many(
        "quality.process.route.line", "route_id", string="Pasos")
    notes = fields.Text("Notas")
    company_id = fields.Many2one(
        "res.company", default=lambda s: s.env.company)

    def get_ordered_codes(self):
        self.ensure_one()
        return [l.process_type_id.code for l in self.line_ids.sorted("sequence")
                if l.process_type_id.code]


class QualityProcessRouteLine(models.Model):
    _name = "quality.process.route.line"
    _description = "Paso de Ruta de Proceso"
    _order = "sequence, id"

    route_id = fields.Many2one(
        "quality.process.route", required=True, ondelete="cascade")
    sequence = fields.Integer("Secuencia", default=10, required=True)
    process_type_id = fields.Many2one(
        "quality.process.type", "Tipo de Proceso", required=True)
    is_optional = fields.Boolean(
        "Opcional",
        help="Si está marcado, este paso no bloquea al siguiente.")
    notes = fields.Char("Observaciones")


class ProductTemplateRoute(models.Model):
    _inherit = "product.template"

    quality_route_id = fields.Many2one(
        "quality.process.route", "Ruta de Calidad",
        help="Define la secuencia de procesos que debe seguir este producto.")


class QualityInspectionRoute(models.Model):
    _inherit = "quality.inspection"

    quality_route_id = fields.Many2one(
        "quality.process.route",
        compute="_compute_quality_route", store=True,
        help="Ruta resuelta para la inspección actual.")

    @api.depends("product_id", "product_id.product_tmpl_id",
                 "product_id.product_tmpl_id.quality_route_id",
                 "product_id.product_tmpl_id.categ_id")
    def _compute_quality_route(self):
        Route = self.env["quality.process.route"]
        for rec in self:
            tmpl = rec.product_id.product_tmpl_id
            route = tmpl.quality_route_id if tmpl else False
            if not route and tmpl and tmpl.categ_id:
                route = Route.search([
                    ("active", "=", True),
                    ("product_categ_ids", "in", tmpl.categ_id.ids),
                ], limit=1)
            rec.quality_route_id = route or False

    def _check_previous_process_hardening(self):
        """Override: usa ruta configurada si existe, si no cae al PROCESS_SEQUENCE
        del hardening base."""
        for rec in self:
            route = rec.quality_route_id
            if not route:
                return super(QualityInspectionRoute, rec)._check_previous_process_hardening()

            codes = route.get_ordered_codes()
            current_code = rec.process_code
            if current_code not in codes:
                continue
            idx = codes.index(current_code)
            if idx == 0:
                continue
            # Buscar el paso previo NO opcional
            previous = None
            for i in range(idx - 1, -1, -1):
                line = route.line_ids.sorted("sequence")[i]
                if not line.is_optional:
                    previous = line.process_type_id.code
                    break
            if not previous:
                continue
            prev = self.search([
                ("lot_id", "=", rec.lot_id.id),
                ("process_code", "=", previous),
                ("state", "=", "aceptado"),
            ], limit=1)
            if not prev:
                raise UserError(_(
                    "Ruta '%s': antes de liberar '%s' debe estar liberado "
                    "el proceso previo '%s' para el lote %s."
                ) % (route.name,
                     rec.process_type_id.name,
                     previous.replace("_", " ").title(),
                     rec.lot_id.name or "—"))
