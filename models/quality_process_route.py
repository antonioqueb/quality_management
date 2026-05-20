# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class QualityProcessRoute(models.Model):
    _name = "quality.process.route"
    _description = "Ruta de Proceso de Calidad"
    _order = "sequence, id"

    name = fields.Char("Nombre de la Ruta", required=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    product_tmpl_ids = fields.Many2many(
        "product.template",
        string="Productos Aplicables",
    )
    product_categ_ids = fields.Many2many(
        "product.category",
        string="Categorías Aplicables",
    )
    line_ids = fields.One2many(
        "quality.process.route.line",
        "route_id",
        string="Pasos",
    )
    notes = fields.Text("Notas")
    company_id = fields.Many2one(
        "res.company",
        default=lambda s: s.env.company,
    )

    def get_ordered_codes(self):
        self.ensure_one()
        return [
            line.process_type_id.code
            for line in self.line_ids.sorted("sequence")
            if line.process_type_id.code
        ]


class QualityProcessRouteLine(models.Model):
    _name = "quality.process.route.line"
    _description = "Paso de Ruta de Proceso"
    _order = "sequence, id"

    route_id = fields.Many2one(
        "quality.process.route",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer("Secuencia", default=10, required=True)
    process_type_id = fields.Many2one(
        "quality.process.type",
        "Tipo de Proceso",
        required=True,
    )
    is_optional = fields.Boolean(
        "Opcional",
        help="Si está marcado, este paso no bloquea al siguiente.",
    )
    notes = fields.Char("Observaciones")


class ProductTemplateRoute(models.Model):
    _inherit = "product.template"

    quality_route_id = fields.Many2one(
        "quality.process.route",
        "Ruta de Calidad",
        help="Define la secuencia de procesos que debe seguir este producto.",
    )


class QualityInspectionRoute(models.Model):
    _inherit = "quality.inspection"

    quality_route_id = fields.Many2one(
        "quality.process.route",
        compute="_compute_quality_route",
        store=True,
        help="Ruta resuelta para la inspección actual.",
    )

    @api.depends(
        "product_id",
        "product_id.product_tmpl_id",
        "product_id.product_tmpl_id.quality_route_id",
        "product_id.product_tmpl_id.categ_id",
    )
    def _compute_quality_route(self):
        Route = self.env["quality.process.route"]
        for rec in self:
            template = rec.product_id.product_tmpl_id
            route = template.quality_route_id if template else False

            if not route and template and template.categ_id:
                route = Route.search(
                    [
                        ("active", "=", True),
                        ("product_categ_ids", "in", template.categ_id.ids),
                    ],
                    limit=1,
                )

            rec.quality_route_id = route or False

    def _check_previous_process_hardening(self):
        """Usa ruta configurada si existe; si no existe, cae a la secuencia base."""
        # FOLIO-QM-ODOO18-026: el método anterior hacía return dentro del loop;
        # con múltiples inspecciones podía dejar registros sin validar.
        fallback_records = self.browse()

        for rec in self:
            route = rec.quality_route_id
            if not route:
                fallback_records |= rec
                continue

            route_lines = route.line_ids.sorted("sequence")
            codes = [
                line.process_type_id.code
                for line in route_lines
                if line.process_type_id.code
            ]
            current_code = rec.process_code

            if current_code not in codes:
                continue

            current_index = codes.index(current_code)
            if current_index == 0:
                continue

            previous_code = False
            for index in range(current_index - 1, -1, -1):
                line = route_lines[index]
                if not line.is_optional:
                    previous_code = line.process_type_id.code
                    break

            if not previous_code:
                continue

            previous_inspection = self.search(
                [
                    ("lot_id", "=", rec.lot_id.id),
                    ("process_code", "=", previous_code),
                    ("state", "=", "aceptado"),
                ],
                limit=1,
            )
            if not previous_inspection:
                raise UserError(
                    _(
                        "Ruta '%s': antes de liberar '%s' debe estar liberado "
                        "el proceso previo '%s' para el lote %s."
                    )
                    % (
                        route.name,
                        rec.process_type_id.name,
                        previous_code.replace("_", " ").title(),
                        rec.lot_id.name or "—",
                    )
                )

        if fallback_records:
            return super(QualityInspectionRoute, fallback_records)._check_previous_process_hardening()

        return True