# -*- coding: utf-8 -*-
import re
import unicodedata

from odoo import models, fields
from odoo.osv import expression


def _quality_slug(value):
    value = value or ""
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    value = re.sub(r"[^a-zA-Z0-9]+", "_", value.lower()).strip("_")
    return value


class QualityAttributeTemplate(models.Model):
    _name = 'quality.attribute.template'
    _description = 'Plantilla de Atributos de Calidad'
    _order = 'sequence, id'

    name = fields.Char('Nombre del Atributo', required=True)
    sequence = fields.Integer('Secuencia', default=10)
    process_type_id = fields.Many2one(
        'quality.process.type', 'Tipo de Proceso',
        ondelete='set null'
    )
    product_tmpl_id = fields.Many2one(
        'product.template', 'Producto',
        ondelete='cascade',
        help='Si se especifica, esta plantilla aplica solo a este producto.'
    )
    # Legacy - se mantiene para filtros rápidos
    inspection_type = fields.Selection([
        ('laminadora_remanejo', 'Laminadora y Remanejo'),
        ('octagono', 'Octágono'),
        ('guillotina_pegado', 'Guillotina y Pegado'),
        ('muestra', 'Muestra'),
        ('general', 'General'),
    ], string='Tipo (Legacy)')
    attribute_type = fields.Selection([
        ('float', 'Numérico'),
        ('selection', 'Selección'),
        ('boolean', 'Cumple/No Cumple'),
        ('char', 'Texto'),
    ], string='Tipo de Dato', required=True, default='float')
    selection_options = fields.Char(
        'Opciones de Selección',
        help='Valores separados por coma. Ej: buena,regular,mala'
    )
    min_value = fields.Float('Valor Mínimo')
    max_value = fields.Float('Valor Máximo')
    unit = fields.Char('Unidad de Medida', help='Ej: mm, %, kg')
    is_required = fields.Boolean('Obligatorio', default=True)
    active = fields.Boolean('Activo', default=True)
    company_id = fields.Many2one(
        'res.company', 'Compañía',
        default=lambda self: self.env.company
    )

    def _quality_template_key(self):
        self.ensure_one()
        normalized = getattr(self, "normalized_name", False) or _quality_slug(self.name)
        capture_zone = getattr(self, "capture_zone", False) or "additional"
        return normalized, capture_zone

    def _quality_template_priority(self, template, product_tmpl=False, process=False):
        if product_tmpl and template.product_tmpl_id.id == product_tmpl.id:
            return 0
        if process and template.process_type_id.id == process.id:
            return 1
        return 2

    def _sort_quality_templates(self, templates, product_tmpl=False, process=False):
        return templates.sorted(
            lambda template: (
                self._quality_template_priority(template, product_tmpl, process),
                template.sequence or 0,
                template.id,
            )
        )

    def _dedupe_quality_templates(self, templates, product_tmpl=False, process=False):
        selected = {}
        ordered = self._sort_quality_templates(templates, product_tmpl, process)

        for template in ordered:
            key = template._quality_template_key()
            if not key[0]:
                continue
            if key not in selected:
                selected[key] = template

        result = templates.browse([template.id for template in selected.values()])
        return result.sorted(
            lambda template: (
                template.sequence or 0,
                self._quality_template_priority(template, product_tmpl, process),
                template.id,
            )
        )

    def _resolve_quality_product_template(self, product=False):
        if not product:
            return self.env["product.template"].browse()

        if product._name == "product.template":
            return product

        if product._name == "product.product":
            return product.product_tmpl_id

        return self.env["product.template"].browse()

    def _company_domain_for_quality_templates(self):
        return [
            "|",
            ("company_id", "=", False),
            ("company_id", "=", self.env.company.id),
        ]

    def _get_applicable_templates_for_capture(
        self,
        product=False,
        process=False,
        include_general=False,
        strict_binary=False,
    ):
        """
        Devuelve las plantillas aplicables para una captura.

        Prioridad:
        1. Plantillas específicas del producto.
        2. Plantillas generales del proceso.
        3. Plantillas generales sin producto/proceso, si include_general=True.

        Si existe una plantilla de producto con el mismo nombre/zona que una del proceso,
        gana la del producto.
        """
        Template = self.sudo()
        product_tmpl = self._resolve_quality_product_template(product)
        domains = []

        base_domain = [
            ("active", "=", True),
        ] + self._company_domain_for_quality_templates()

        if product_tmpl:
            if process:
                domains.append(expression.AND([
                    base_domain,
                    [
                        ("product_tmpl_id", "=", product_tmpl.id),
                        "|",
                        ("process_type_id", "=", False),
                        ("process_type_id", "=", process.id),
                    ],
                ]))
            else:
                domains.append(expression.AND([
                    base_domain,
                    [
                        ("product_tmpl_id", "=", product_tmpl.id),
                    ],
                ]))

        if process:
            domains.append(expression.AND([
                base_domain,
                [
                    ("product_tmpl_id", "=", False),
                    ("process_type_id", "=", process.id),
                ],
            ]))

        if include_general:
            domains.append(expression.AND([
                base_domain,
                [
                    ("product_tmpl_id", "=", False),
                    ("process_type_id", "=", False),
                ],
            ]))

        if not domains:
            return Template.browse()

        templates = Template.search(expression.OR(domains))

        if strict_binary:
            templates = templates.filtered(lambda template: template.attribute_type == "boolean")

        return self._dedupe_quality_templates(
            templates,
            product_tmpl=product_tmpl,
            process=process,
        )
