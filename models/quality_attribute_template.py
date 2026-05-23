# -*- coding: utf-8 -*-
import re
import unicodedata

from odoo import api, fields, models
from odoo.osv import expression


def _quality_slug(value):
    value = value or ""
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    value = re.sub(r"[^a-zA-Z0-9]+", "_", value.lower()).strip("_")
    return value


class QualityAttributeTemplate(models.Model):
    _name = "quality.attribute.template"
    _description = "Plantilla de Atributos de Calidad"
    _order = "sequence, id"

    name = fields.Char("Nombre del Atributo", required=True)
    sequence = fields.Integer("Secuencia", default=10)

    process_type_id = fields.Many2one(
        "quality.process.type",
        "Tipo de Proceso",
        ondelete="set null",
        help=(
            "Si se especifica sin Producto, esta plantilla aplica de forma general "
            "a todas las inspecciones de este proceso. Si se combina con Producto, "
            "solo aplica a ese producto dentro de este proceso."
        ),
    )

    product_tmpl_id = fields.Many2one(
        "product.template",
        "Producto",
        ondelete="cascade",
        help=(
            "Si se especifica, esta plantilla aplica solo a este producto. "
            "Puede dejar Tipo de Proceso vacío para que aplique al producto en "
            "cualquier proceso, o indicar un proceso específico."
        ),
    )

    # Legacy - se mantiene para filtros rápidos
    inspection_type = fields.Selection(
        [
            ("laminadora_remanejo", "Laminadora y Remanejo"),
            ("octagono", "Octágono"),
            ("guillotina_pegado", "Guillotina y Pegado"),
            ("muestra", "Muestra"),
            ("general", "General"),
        ],
        string="Tipo (Legacy)",
    )

    attribute_type = fields.Selection(
        [
            ("float", "Numérico"),
            ("selection", "Selección"),
            ("boolean", "Cumple/No Cumple"),
            ("char", "Texto"),
        ],
        string="Tipo de Dato",
        required=True,
        default="float",
    )

    selection_options = fields.Char(
        "Opciones de Selección",
        help="Valores separados por coma. Ej: buena,regular,mala",
    )
    min_value = fields.Float("Valor Mínimo")
    max_value = fields.Float("Valor Máximo")
    unit = fields.Char("Unidad de Medida", help="Ej: mm, %, kg")
    is_required = fields.Boolean("Obligatorio", default=True)
    active = fields.Boolean("Activo", default=True)

    company_id = fields.Many2one(
        "res.company",
        "Compañía",
        default=lambda self: self.env.company,
    )

    def _resolve_quality_product_template(self, product=False):
        if not product:
            return self.env["product.template"].browse()

        if product._name == "product.template":
            return product

        if product._name == "product.product":
            return product.product_tmpl_id

        return self.env["product.template"].browse()

    def _quality_template_key(self):
        self.ensure_one()
        normalized = getattr(self, "normalized_name", False) or _quality_slug(self.name)
        capture_zone = getattr(self, "capture_zone", False) or "additional"
        return normalized, capture_zone

    def _quality_template_scope_rank(self, product_tmpl=False, process=False):
        """
        Prioridad de aplicación cuando dos plantillas generan el mismo atributo.

        0. Producto + proceso exacto.
        1. Producto sin proceso: aplica al producto en cualquier proceso.
        2. Proceso sin producto: atributo general del proceso.
        3. General global: sin producto ni proceso, solo si se solicita.
        """
        self.ensure_one()

        if product_tmpl and process:
            if self.product_tmpl_id.id == product_tmpl.id and self.process_type_id.id == process.id:
                return 0

        if product_tmpl and self.product_tmpl_id.id == product_tmpl.id and not self.process_type_id:
            return 1

        if process and self.process_type_id.id == process.id and not self.product_tmpl_id:
            return 2

        return 3

    def _sort_quality_templates_for_capture(self, templates, product_tmpl=False, process=False):
        return templates.sorted(
            lambda template: (
                template.sequence or 0,
                template._quality_template_scope_rank(product_tmpl=product_tmpl, process=process),
                template.id,
            )
        )

    def _dedupe_quality_templates_for_capture(self, templates, product_tmpl=False, process=False):
        """
        Deduplica por nombre normalizado + zona de captura.

        Si hay una plantilla general de proceso y otra específica del producto con
        el mismo nombre, gana la específica del producto. La salida se reordena por
        secuencia para conservar una captura lógica en pantalla.
        """
        selected = {}

        for template in templates.sorted(
            lambda item: (
                item._quality_template_scope_rank(product_tmpl=product_tmpl, process=process),
                item.sequence or 0,
                item.id,
            )
        ):
            key = template._quality_template_key()
            if not key[0]:
                continue
            if key not in selected:
                selected[key] = template

        result = templates.browse([template.id for template in selected.values()])
        return self._sort_quality_templates_for_capture(
            result,
            product_tmpl=product_tmpl,
            process=process,
        )

    @api.model
    def _get_applicable_templates_for_capture(
        self,
        product=False,
        process=False,
        include_general=False,
        strict_binary=False,
    ):
        """
        Plantillas aplicables para una captura de calidad.

        Soporta estas configuraciones:
        - Atributo general por proceso:
          product_tmpl_id = False y process_type_id = proceso actual.
        - Atributo específico por producto para todos los procesos:
          product_tmpl_id = producto y process_type_id = False.
        - Atributo específico por producto y proceso:
          product_tmpl_id = producto y process_type_id = proceso actual.
        - Atributo global sin producto/proceso:
          solo se incluye cuando include_general=True.
        """
        Template = self.sudo()
        product_tmpl = self._resolve_quality_product_template(product)
        domains = []

        base_domain = [
            ("active", "=", True),
            "|",
            ("company_id", "=", False),
            ("company_id", "=", self.env.company.id),
        ]

        if product_tmpl:
            if process:
                domains.append(
                    expression.AND(
                        [
                            base_domain,
                            [
                                ("product_tmpl_id", "=", product_tmpl.id),
                                "|",
                                ("process_type_id", "=", False),
                                ("process_type_id", "=", process.id),
                            ],
                        ]
                    )
                )
            else:
                domains.append(
                    expression.AND(
                        [
                            base_domain,
                            [("product_tmpl_id", "=", product_tmpl.id)],
                        ]
                    )
                )

        if process:
            domains.append(
                expression.AND(
                    [
                        base_domain,
                        [
                            ("product_tmpl_id", "=", False),
                            ("process_type_id", "=", process.id),
                        ],
                    ]
                )
            )

        if include_general:
            domains.append(
                expression.AND(
                    [
                        base_domain,
                        [
                            ("product_tmpl_id", "=", False),
                            ("process_type_id", "=", False),
                        ],
                    ]
                )
            )

        if not domains:
            return Template.browse()

        templates = Template.search(expression.OR(domains))

        if strict_binary:
            templates = templates.filtered(lambda template: template.attribute_type == "boolean")

        return Template._dedupe_quality_templates_for_capture(
            templates,
            product_tmpl=product_tmpl,
            process=process,
        )
