# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


# FOLIO-QM-ODOO18-074:
# Secuencia estándar obligatoria. Aunque exista una ruta vieja sin Remanejo,
# estos procesos no pueden saltarse.
MANDATORY_STANDARD_SEQUENCE = [
    "octagono",
    "guillotina",
    "pegado",
    "laminadora",
    "remanejo",
    "troquelado_plano",
]


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
        default_route = self.env.ref(
            "quality_management.quality_route_estandar",
            raise_if_not_found=False,
        )

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

            # FOLIO-QM-ODOO18-074:
            # Si no hay ruta específica por producto/categoría, se usa la ruta estándar.
            rec.quality_route_id = route or default_route or False

    def _check_previous_process_hardening(self):
        """
        1) Siempre respeta la secuencia estándar obligatoria:
           Octágono -> Guillotina -> Pegado -> Laminadora -> Remanejo -> Troquelado Plano.
        2) Para procesos fuera de esa secuencia, usa la ruta configurable si aplica.
        """
        # FOLIO-QM-ODOO18-074: primero se ejecuta la validación estándar del hardening.
        super()._check_previous_process_hardening()

        for rec in self:
            current_code = rec.process_code

            # Los procesos estándar ya fueron validados por super() para evitar
            # que una ruta vieja sin Remanejo permita saltarse el flujo.
            if current_code in MANDATORY_STANDARD_SEQUENCE:
                continue

            route = rec.quality_route_id
            if not route:
                continue

            route_lines = route.line_ids.sorted("sequence")
            codes = [
                line.process_type_id.code
                for line in route_lines
                if line.process_type_id.code
            ]

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

            previous_inspection = rec._find_previous_inspection_hardening(previous_code)
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
                    previous_code.replace("_", " ").title(),
                )
            )

        return True