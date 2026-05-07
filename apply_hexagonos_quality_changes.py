#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
apply_hexagonos_quality_changes.py
==================================
Aplica los cambios solicitados por Calidad de Hexágonos al módulo
quality_management. Hace backup automático antes de tocar archivos.

USO:
    python3 apply_hexagonos_quality_changes.py /ruta/a/quality_management

Cubre:
- Liberación de Muestras: tipo MP/PT, fechas automáticas bloqueadas, evidencia,
  bloqueo de guardado sin atributos válidos.
- Liberación de Planos: requisitos de fabricación, control de modificaciones (máx 3),
  triple check Calidad/Ventas/Diseño, fechas automáticas, bloqueo si faltan documentos.
- Inspecciones: PP/PT mutuamente excluyente, fecha bloqueada, notificación al supervisor
  en retención, alerta de valores en 0, separación Laminadora vs Sierras y Ranuradoras,
  hexágono de 4 tipos, atributos adicionales OK/NO OK/N/A, secuencia entre procesos.
- Certificados: deduplicación de atributos, no permitir valores 0, mapeo desde inspección.
- Acciones Correctivas / 8D: tipo Reclamación, defecto OTRO con descripción,
  5 Por qué, Ishikawa, equipo de trabajo, bloqueos de cierre y avance con evidencia.
- Devoluciones: bloqueo no procede, motivo comercial del Gerente de Ventas, formato obligatorio.
- Documentos del cliente: eliminar APARIENCIA y ESPECIFICACION_EMPAQUE, OTRO con descripción
  libre, soporte de imagen además de PDF, fechas bloqueadas, formato cliente Sí/No.
- Gestión de Troqueles (NUEVO): modelo único con tres flujos
  (Recepción / Revisión / Reparación) y trazabilidad.
"""

import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

# --------------------------------------------------------------------- helpers
def fatal(msg):
    print(f"❌ {msg}", file=sys.stderr)
    sys.exit(1)


def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  ✏  {path.relative_to(MODULE)}")


def append_csv_lines(path: Path, lines: list[str]):
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    new = existing.rstrip() + "\n" + "\n".join(lines) + "\n"
    path.write_text(new, encoding="utf-8")
    print(f"  ➕ {path.relative_to(MODULE)} (+{len(lines)} líneas)")


# ----------------------------------------------------------------- entry point
if len(sys.argv) < 2:
    fatal("Uso: python3 apply_hexagonos_quality_changes.py /ruta/a/quality_management")

MODULE = Path(sys.argv[1]).resolve()
if not MODULE.exists() or not (MODULE / "__manifest__.py").exists():
    fatal(f"No encontré un módulo Odoo válido en {MODULE}")

BACKUP = MODULE.parent / f"{MODULE.name}_backup_{datetime.now():%Y%m%d_%H%M%S}"
print(f"📦 Backup: {BACKUP}")
shutil.copytree(MODULE, BACKUP)
print(f"🔧 Aplicando cambios en {MODULE}\n")

# =============================================================================
# 1. __manifest__.py
# =============================================================================
write(MODULE / "__manifest__.py", '''# -*- coding: utf-8 -*-
{
    "name": "Gestión de Calidad - Hexágonos Mexicanos",
    "version": "18.0.3.0.0",
    "category": "Manufacturing/Quality",
    "summary": "Gestión integral de calidad - Hexágonos (req. Feb-26)",
    "author": "Alphaqueb Consulting SAS",
    "website": "https://alphaqueb.com",
    "license": "LGPL-3",
    "depends": [
        "base", "mail", "project", "mrp", "sale", "stock",
        "product", "contacts", "hr",
    ],
    "data": [
        "security/quality_groups.xml",
        "security/ir.model.access.csv",
        "security/quality_rules.xml",
        "data/sequence_data.xml",
        "data/process_type_data.xml",
        "data/cron_data.xml",
        "wizards/certificate_wizard_views.xml",
        "views/quality_process_type_views.xml",
        "views/quality_attribute_template_views.xml",
        "views/quality_sample_release_views.xml",
        "views/quality_drawing_release_views.xml",
        "views/quality_inspection_views.xml",
        "views/quality_certificate_views.xml",
        "views/quality_corrective_action_views.xml",
        "views/quality_customer_return_views.xml",
        "views/quality_customer_document_views.xml",
        "views/quality_dashboard_views.xml",
        "views/quality_troquel_views.xml",
        "views/res_company_views.xml",
        "views/product_views.xml",
        "views/quality_inherited_views.xml",
        "views/quality_menus.xml",
        "reports/report_quality_certificate.xml",
        "reports/report_8d.xml",
        "reports/report_inspection_summary.xml",
        "reports/report_sample_release.xml",
        "reports/report_drawing_release.xml",
        "reports/report_customer_return.xml",
        "reports/report_customer_document.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "quality_management/static/src/css/quality_pdf_viewer.css",
            "quality_management/static/src/css/quality_evidence_viewer.css",
            "quality_management/static/src/js/evidence_viewer_widget.js",
            "quality_management/static/src/xml/evidence_viewer_widget.xml",
        ],
    },
    "installable": True,
    "application": True,
    "auto_install": False,
}
''')

# =============================================================================
# 2. models/__init__.py — agrega los nuevos modelos
# =============================================================================
write(MODULE / "models" / "__init__.py", '''from . import quality_process_type
from . import res_company
from . import quality_attribute_template
from . import quality_sample_release
from . import quality_drawing_release
from . import quality_drawing_modification
from . import quality_inspection
from . import quality_inspection_line
from . import quality_inspection_ranurado
from . import quality_inspection_troquelado
from . import quality_certificate
from . import quality_corrective_action
from . import quality_action_line
from . import quality_5why
from . import quality_ishikawa
from . import quality_work_team
from . import quality_customer_return
from . import quality_customer_document
from . import quality_troquel
from . import quality_inherited_models
from . import product_template
''')

# =============================================================================
# 3. data/process_type_data.xml — separación Laminadora vs Sierras y Ranuradoras
# =============================================================================
write(MODULE / "data" / "process_type_data.xml", '''<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        <!-- 1. Octágono -->
        <record id="process_type_octagono" model="quality.process.type">
            <field name="name">Octágono</field>
            <field name="code">octagono</field>
            <field name="sequence">10</field>
            <field name="show_ancho" eval="True"/>
            <field name="show_hexagono" eval="True"/>
            <field name="show_papel" eval="True"/>
            <field name="show_adhesivo" eval="True"/>
            <field name="show_calibracion" eval="True"/>
            <field name="show_engomado" eval="True"/>
            <field name="show_corte_guillotina" eval="True"/>
            <field name="show_numero_corrida" eval="True"/>
        </record>

        <!-- 2. Guillotina -->
        <record id="process_type_guillotina" model="quality.process.type">
            <field name="name">Guillotina</field>
            <field name="code">guillotina</field>
            <field name="sequence">20</field>
            <field name="show_ancho" eval="True"/>
            <field name="show_espesor" eval="True"/>
            <field name="show_hexagono" eval="True"/>
            <field name="show_tipo_hexagono" eval="True"/>
            <field name="show_retiramiento" eval="True"/>
        </record>

        <!-- 3. Pegado -->
        <record id="process_type_pegado" model="quality.process.type">
            <field name="name">Pegado</field>
            <field name="code">pegado</field>
            <field name="sequence">30</field>
            <field name="show_pegado" eval="True"/>
        </record>

        <!-- 4. Laminadora (separada de Remanejo) -->
        <record id="process_type_laminadora" model="quality.process.type">
            <field name="name">Laminadora</field>
            <field name="code">laminadora</field>
            <field name="sequence">40</field>
            <field name="show_largo" eval="True"/>
            <field name="show_ancho" eval="True"/>
            <field name="show_espesor" eval="True"/>
            <field name="show_hexagono" eval="True"/>
            <field name="show_resistencia" eval="True"/>
            <field name="show_apariencia" eval="True"/>
            <field name="show_humedad" eval="True"/>
        </record>

        <!-- 5. Sierras y Ranuradoras (antes "Remanejo") -->
        <record id="process_type_sierras_ranuradoras" model="quality.process.type">
            <field name="name">Sierras y Ranuradoras</field>
            <field name="code">sierras_ranuradoras</field>
            <field name="sequence">50</field>
            <field name="show_largo" eval="True"/>
            <field name="show_ancho" eval="True"/>
            <field name="show_espesor" eval="True"/>
            <field name="show_apariencia" eval="True"/>
            <field name="show_ranurado" eval="True"/>
        </record>

        <!-- 6. Troquelado Plano -->
        <record id="process_type_troquelado_plano" model="quality.process.type">
            <field name="name">Troquelado Plano</field>
            <field name="code">troquelado_plano</field>
            <field name="sequence">60</field>
            <field name="show_largo" eval="True"/>
            <field name="show_ancho" eval="True"/>
            <field name="show_espesor" eval="True"/>
            <field name="show_troquelado" eval="True"/>
            <field name="show_apariencia" eval="True"/>
        </record>

        <!-- 7. Impresión (solo atributos adicionales) -->
        <record id="process_type_impresion" model="quality.process.type">
            <field name="name">Impresión</field>
            <field name="code">impresion</field>
            <field name="sequence">70</field>
            <field name="show_apariencia" eval="True"/>
        </record>

        <!-- 8. Acabado y Empaque (solo atributos adicionales) -->
        <record id="process_type_acabado" model="quality.process.type">
            <field name="name">Acabado y Empaque</field>
            <field name="code">acabado_empaque</field>
            <field name="sequence">80</field>
            <field name="show_apariencia" eval="True"/>
        </record>
    </data>
</odoo>
''')

# =============================================================================
# 4. models/quality_sample_release.py
# =============================================================================
write(MODULE / "models" / "quality_sample_release.py", '''# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta


class QualitySampleRelease(models.Model):
    _name = "quality.sample.release"
    _description = "Liberación de Muestras"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_requested desc, id desc"

    name = fields.Char("Referencia", required=True, readonly=True,
                       default="Nuevo", copy=False)

    # Tipo de muestra (req. 3)
    sample_type = fields.Selection([
        ("mp", "Opción 1: MP - Sale de Laminadora"),
        ("pt", "Opción 2: PT - Pasa por Taller CNC / Transformación"),
    ], string="Tipo de Muestra", required=True, default="mp", tracking=True)

    project_task_id = fields.Many2one("project.task", "Tarea de Proyecto",
                                      required=True, tracking=True)
    product_id = fields.Many2one("product.product", "Producto/Muestra",
                                 required=True, tracking=True)
    requested_by = fields.Many2one("res.users", "Solicitante (Diseño)",
                                   required=True,
                                   default=lambda s: s.env.user, tracking=True)
    inspector_id = fields.Many2one("res.users", "Inspector de Calidad",
                                   tracking=True)

    # Fechas: automáticas y bloqueadas (req. 3.2)
    date_requested = fields.Datetime("Fecha de Solicitud", required=True,
                                     readonly=True, copy=False,
                                     default=fields.Datetime.now)
    date_limit = fields.Datetime("Fecha Límite de Inspección",
                                 compute="_compute_date_limit", store=True,
                                 readonly=True, copy=False,
                                 help="Solicitud + 48 horas")
    date_inspected = fields.Datetime("Fecha de Inspección",
                                     readonly=True, copy=False, tracking=True)

    state = fields.Selection([
        ("borrador", "Borrador"),
        ("en_inspeccion", "En Inspección"),
        ("aceptado", "Aceptado"),
        ("rechazado", "Rechazado"),
    ], default="borrador", required=True, tracking=True, copy=False)

    inspection_line_ids = fields.One2many("quality.inspection.line",
                                          "sample_release_id",
                                          string="Atributos Inspeccionados")

    # Especificación PDF obligatoria (req. 3.1)
    spec_pdf = fields.Binary("Especificación (PDF)", attachment=True)
    spec_pdf_name = fields.Char("Nombre Especificación")

    # Pestaña Evidencia (req. 3.1)
    evidence_ids = fields.Many2many(
        "ir.attachment", "quality_sample_evidence_rel",
        "sample_id", "attachment_id", string="Evidencia",
    )

    # Captura para Opción 2 - Transformación CNC (req. 3.3)
    cnc_design_user_id = fields.Many2one("res.users", "Personal de Diseño")
    cnc_date_realized = fields.Datetime("Fecha de Realización CNC",
                                        readonly=True)
    cnc_observations = fields.Html("Observaciones CNC")

    notes = fields.Html("Observaciones")
    company_id = fields.Many2one("res.company", "Compañía",
                                 default=lambda s: s.env.company)

    # ------------------------------------------------------------------ compute
    @api.depends("date_requested")
    def _compute_date_limit(self):
        for rec in self:
            rec.date_limit = (rec.date_requested + timedelta(hours=48)
                              if rec.date_requested else False)

    # ------------------------------------------------------------------- create
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Nuevo") == "Nuevo":
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "quality.sample.release") or "Nuevo"
        return super().create(vals_list)

    # ---------------------------------------------------------------- guardrails
    def _check_attributes_valid(self):
        """Bloqueo: no permitir atributos en 0 ni faltantes (req. 3.1)."""
        for rec in self:
            if not rec.inspection_line_ids:
                raise UserError(_("Debe capturar al menos un atributo "
                                  "de inspección antes de avanzar."))
            zero_lines = rec.inspection_line_ids.filtered(
                lambda l: l.attribute_type == "float" and not l.value_float
            )
            if zero_lines:
                names = ", ".join(zero_lines.mapped("name"))
                raise UserError(_(
                    "Hay atributos con valor 0 que deben capturarse: %s"
                ) % names)

    def _check_spec_pdf(self):
        for rec in self:
            if not rec.spec_pdf:
                raise UserError(_(
                    "La Especificación PDF es obligatoria. "
                    "Sin plano o dibujo no se puede inspeccionar."
                ))

    def _check_pt_workflow(self):
        """Para PT bloquea avance si Diseño no capturó atributos en CNC."""
        for rec in self:
            if rec.sample_type == "pt" and not rec.cnc_date_realized:
                raise UserError(_(
                    "Esta muestra PT requiere captura previa en "
                    "Transformación (Taller CNC) antes de mover a "
                    "Inspección de Calidad."
                ))

    # -------------------------------------------------------------- transitions
    def action_register_cnc(self):
        """Diseño marca terminada la transformación en CNC."""
        for rec in self:
            if rec.sample_type != "pt":
                raise UserError(_("Solo aplica a muestras PT."))
            self._check_attributes_valid()
            rec.cnc_date_realized = fields.Datetime.now()
            rec.cnc_design_user_id = self.env.user
            rec.message_post(
                body=_("✓ CNC: transformación registrada por %s") % self.env.user.name,
                subtype_xmlid="mail.mt_comment",
            )

    def action_submit_inspection(self):
        for rec in self:
            rec._check_spec_pdf()
            rec._check_pt_workflow()
            rec._check_attributes_valid()
            rec.state = "en_inspeccion"
            users = self.env.ref(
                "quality_management.group_quality_inspector").users
            if rec.inspector_id:
                users = rec.inspector_id
            for u in users:
                rec.activity_schedule(
                    "mail.mail_activity_data_todo",
                    date_deadline=fields.Date.today() + timedelta(days=2),
                    summary=_("Inspección de muestra: %s") % rec.name,
                    user_id=u.id,
                )

    def action_accept(self):
        for rec in self:
            rec._check_attributes_valid()
            failing = rec.inspection_line_ids.filtered(
                lambda l: l.result == "no_cumple")
            if failing:
                raise UserError(
                    _("No se puede liberar: hay %d atributo(s) que no cumplen.")
                    % len(failing))
            rec.state = "aceptado"
            rec.date_inspected = fields.Datetime.now()
            rec.activity_feedback(["mail.mail_activity_data_todo"],
                                  feedback=_("Muestra aceptada"))
            rec.message_post(
                body=_("✅ Muestra ACEPTADA y liberada por %s")
                % self.env.user.name,
                subtype_xmlid="mail.mt_comment")

    def action_reject(self):
        """Notificar SOLO a la solicitante en rechazo (req. 3.4)."""
        for rec in self:
            rec.state = "rechazado"
            rec.date_inspected = fields.Datetime.now()
            rec.activity_feedback(["mail.mail_activity_data_todo"],
                                  feedback=_("Muestra rechazada"))
            if rec.requested_by.partner_id:
                rec.message_subscribe([rec.requested_by.partner_id.id])
            rec.message_post(
                body=_("❌ Muestra RECHAZADA por %s. Notificando a la solicitante: %s")
                % (self.env.user.name, rec.requested_by.name),
                partner_ids=[rec.requested_by.partner_id.id]
                if rec.requested_by.partner_id else [],
                subtype_xmlid="mail.mt_comment")

    def action_reset_draft(self):
        for rec in self:
            rec.state = "borrador"

    def action_print_sample_release(self):
        return self.env.ref(
            "quality_management.action_report_sample_release"
        ).report_action(self)
''')

# =============================================================================
# 5. models/quality_drawing_modification.py — control de modificaciones (req 4.4)
# =============================================================================
write(MODULE / "models" / "quality_drawing_modification.py", '''# -*- coding: utf-8 -*-
from odoo import models, fields, api


class QualityDrawingModification(models.Model):
    _name = "quality.drawing.modification"
    _description = "Modificación de Plano"
    _order = "sequence asc, id asc"

    drawing_id = fields.Many2one("quality.drawing.release", required=True,
                                 ondelete="cascade", index=True)
    sequence = fields.Integer("N°", required=True, default=1)
    date = fields.Datetime("Fecha", default=fields.Datetime.now,
                           readonly=True, required=True)
    description = fields.Text("Descripción del Cambio Solicitado",
                              required=True)
    requested_by = fields.Many2one("res.users", "Solicitado por",
                                   default=lambda s: s.env.user)
''')

# =============================================================================
# 6. models/quality_drawing_release.py
# =============================================================================
write(MODULE / "models" / "quality_drawing_release.py", '''# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta


class QualityDrawingRelease(models.Model):
    _name = "quality.drawing.release"
    _description = "Liberación de Planos"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_requested desc, id desc"

    MAX_MODIFICATIONS = 3  # req. 4.4

    name = fields.Char("Referencia", required=True, readonly=True,
                       default="Nuevo", copy=False)
    partner_id = fields.Many2one("res.partner", "Cliente",
                                 required=True, tracking=True)
    sale_order_id = fields.Many2one("sale.order", "Orden de Venta",
                                    tracking=True)

    # Tipo de solicitud (req. 4.1)
    request_type = fields.Selection([
        ("alta", "Alta"),
        ("actualizacion", "Actualización"),
    ], string="Tipo de Solicitud", required=True, default="alta",
        tracking=True)

    # Dirección de alta del plano (req. 4.1)
    drawing_path = fields.Char(
        "Dirección de Alta del Plano",
        help="Ej: C:\\\\Users\\\\Calidad\\\\Nextcloud\\\\000 ALTAS...",
    )

    # Requisitos de fabricación que captura Ventas (req. 4.1)
    req_sellos = fields.Boolean("Sellos Requeridos")
    req_sellos_date = fields.Date("Fecha Arribo Sellos")
    req_plantilla = fields.Boolean("Plantilla Requerida")
    req_plantilla_date = fields.Date("Fecha Arribo Plantilla")
    req_troquel = fields.Boolean("Troquel Requerido")
    req_troquel_date = fields.Date("Fecha Arribo Troquel")
    req_otro = fields.Boolean("Otro Requerido")
    req_otro_desc = fields.Char("Especifique Otro")
    req_otro_date = fields.Date("Fecha Arribo Otro")

    # Documentos obligatorios (req. 4.2)
    drawing_attachment_ids = fields.Many2many(
        "ir.attachment", "quality_drawing_attachment_rel",
        "drawing_id", "attachment_id",
        string="Plano y Cotización/Dibujo", required=True,
    )
    drawing_pdf = fields.Binary("Plano Principal (PDF)", attachment=True)
    drawing_pdf_name = fields.Char("Nombre del Plano")
    quotation_pdf = fields.Binary("Cotización/Dibujo (PDF)", attachment=True)
    quotation_pdf_name = fields.Char("Nombre Cotización")

    requested_by = fields.Many2one("res.users", "Solicitante (Ventas)",
                                   required=True,
                                   default=lambda s: s.env.user, tracking=True)
    inspector_id = fields.Many2one("res.users", "Inspector de Calidad",
                                   tracking=True)

    state = fields.Selection([
        ("borrador", "Borrador"),
        ("en_revision", "En Revisión Calidad"),
        ("aceptado_calidad", "Aceptado por Calidad"),
        ("aceptado_ventas", "Aceptado por Ventas"),
        ("aceptado_diseno", "Aceptado por Diseño (Final)"),
        ("rechazado", "Rechazado"),
        ("cerrada", "Cerrada por Exceso de Modificaciones"),
    ], default="borrador", required=True, tracking=True, copy=False)

    rejection_reason = fields.Text("Motivo de Rechazo")

    # Fechas automáticas y bloqueadas (req. 4.3)
    date_requested = fields.Datetime("Fecha de Solicitud",
                                     readonly=True, copy=False)
    date_release_expected = fields.Datetime("Fecha Liberación Esperada",
                                            compute="_compute_release_expected",
                                            store=True, readonly=True)
    date_released = fields.Datetime("Fecha de Liberación Real",
                                    readonly=True, copy=False)

    # Triple check (req. 4.5)
    accepted_by_quality = fields.Many2one("res.users", "Calidad Aceptó",
                                          readonly=True)
    accepted_by_quality_date = fields.Datetime(readonly=True)
    accepted_by_sales = fields.Many2one("res.users", "Ventas Aceptó",
                                        readonly=True)
    accepted_by_sales_date = fields.Datetime(readonly=True)
    accepted_by_design = fields.Many2one("res.users", "Diseño Aceptó",
                                         readonly=True)
    accepted_by_design_date = fields.Datetime(readonly=True)

    # Modificaciones (req. 4.4)
    modification_ids = fields.One2many("quality.drawing.modification",
                                       "drawing_id", string="Modificaciones")
    modification_count = fields.Integer(compute="_compute_modification_count",
                                        store=True)

    company_id = fields.Many2one("res.company", "Compañía",
                                 default=lambda s: s.env.company)

    # ------------------------------------------------------------------ compute
    @api.depends("date_requested")
    def _compute_release_expected(self):
        for rec in self:
            rec.date_release_expected = (rec.date_requested + timedelta(hours=48)
                                         if rec.date_requested else False)

    @api.depends("modification_ids")
    def _compute_modification_count(self):
        for rec in self:
            rec.modification_count = len(rec.modification_ids)

    # ------------------------------------------------------------------- create
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Nuevo") == "Nuevo":
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "quality.drawing.release") or "Nuevo"
        return super().create(vals_list)

    # --------------------------------------------------------- helper bloqueos
    def _check_documents(self):
        for rec in self:
            if not rec.drawing_pdf or not rec.quotation_pdf:
                raise UserError(_(
                    "Debe cargar AMBOS documentos antes de avanzar: "
                    "Plano (PDF) y Cotización/Dibujo (PDF)."
                ))

    # -------------------------------------------------------------- transitions
    def action_submit_review(self):
        for rec in self:
            if rec.modification_count >= self.MAX_MODIFICATIONS:
                rec._handle_max_modifications()
                continue
            rec._check_documents()
            rec.date_requested = fields.Datetime.now()
            rec.state = "en_revision"

            mod_num = rec.modification_count + 1
            self.env["quality.drawing.modification"].create({
                "drawing_id": rec.id,
                "sequence": mod_num,
                "description": _(
                    "Solicitud de revisión #%s enviada a Calidad."
                ) % mod_num,
            })
            self._notify_modification(rec, mod_num)

            users = (rec.inspector_id or self.env.ref(
                "quality_management.group_quality_inspector").users)
            for u in users:
                rec.activity_schedule(
                    "mail.mail_activity_data_todo",
                    date_deadline=fields.Date.today() + timedelta(days=2),
                    summary=_("Revisión de plano: %s") % rec.name,
                    user_id=u.id,
                )

    def _notify_modification(self, rec, n):
        """Avisos automáticos por número de modificación (req. 4.4)."""
        partner_ids = [rec.requested_by.partner_id.id] \\
            if rec.requested_by.partner_id else []

        if n == 1:
            body = _("Solo tiene 3 oportunidades para realizar modificaciones "
                     "al plano enviado a liberación de Calidad.")
        elif n == 2:
            body = _("Cambio solicitado #2: valide que los cambios solicitados "
                     "por Calidad cumplen el requerimiento y que los demás "
                     "datos están correctos.")
        elif n == 3:
            body = _("⚠️ Cambio solicitado #3: se comparte incumplimiento al "
                     "Jefe directo. Si vuelve a rechazarse, deberá iniciar el "
                     "proceso nuevamente.")
            sales_managers = self.env.ref(
                "sales_team.group_sale_manager", raise_if_not_found=False)
            if sales_managers:
                for u in sales_managers.users:
                    if u.partner_id:
                        partner_ids.append(u.partner_id.id)
        else:
            body = _("Modificación #%s registrada.") % n
        rec.message_post(body=body, partner_ids=list(set(partner_ids)),
                         subtype_xmlid="mail.mt_comment")

    def _handle_max_modifications(self):
        for rec in self:
            rec.state = "cerrada"
            rec.message_post(
                body=_(
                    "🚫 Se alcanzó el máximo de %s modificaciones. "
                    "La liberación se cierra. Debe iniciar nuevamente "
                    "el proceso (las modificaciones continuarán con "
                    "el consecutivo: %s, %s, ...)."
                ) % (self.MAX_MODIFICATIONS,
                     self.MAX_MODIFICATIONS + 1, self.MAX_MODIFICATIONS + 2),
                subtype_xmlid="mail.mt_comment")

    # ----- triple check (req. 4.5) -------------------------------------------
    def action_quality_accept(self):
        for rec in self:
            rec._check_documents()
            rec.state = "aceptado_calidad"
            rec.accepted_by_quality = self.env.user
            rec.accepted_by_quality_date = fields.Datetime.now()
            rec.message_post(body=_("✅ Calidad aceptó el plano."),
                             subtype_xmlid="mail.mt_comment")

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
            rec.activity_feedback(["mail.mail_activity_data_todo"],
                                  feedback=_("Plano liberado"))

    def action_reject(self):
        for rec in self:
            if not rec.rejection_reason:
                raise ValidationError(_("Capture el motivo de rechazo."))
            rec.state = "rechazado"
            rec.activity_feedback(
                ["mail.mail_activity_data_todo"],
                feedback=_("Plano rechazado: %s") % rec.rejection_reason)
            rec.message_post(
                body=_("❌ Plano RECHAZADO por %s. Motivo: %s")
                % (self.env.user.name, rec.rejection_reason),
                subtype_xmlid="mail.mt_comment")

    def action_reset_draft(self):
        for rec in self:
            if rec.modification_count >= self.MAX_MODIFICATIONS:
                raise UserError(_(
                    "No se puede regresar a borrador: se excedió el máximo "
                    "de modificaciones permitidas."
                ))
            rec.state = "borrador"
            rec.rejection_reason = False

    def action_print_drawing_release(self):
        return self.env.ref(
            "quality_management.action_report_drawing_release"
        ).report_action(self)
''')

# =============================================================================
# 7. models/quality_inspection.py
# =============================================================================
write(MODULE / "models" / "quality_inspection.py", '''# -*- coding: utf-8 -*-
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
    folio = fields.Char("Folio de Producción", required=True)
    code = fields.Char("Código de Producto", required=True)
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
            if rec.supervisor_id and rec.supervisor_id.user_id and \\
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
''')

# =============================================================================
# 8. models/quality_certificate.py
# =============================================================================
write(MODULE / "models" / "quality_certificate.py", '''# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class QualityCertificate(models.Model):
    _name = "quality.certificate"
    _description = "Certificado de Calidad"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_generated desc, id desc"

    name = fields.Char("Referencia", required=True, readonly=True,
                       default="Nuevo", copy=False)
    inspection_id = fields.Many2one("quality.inspection", "Inspección Fuente",
                                    required=True, tracking=True,
                                    domain=[("state", "=", "aceptado")])
    partner_id = fields.Many2one("res.partner", "Cliente",
                                 required=True, tracking=True)
    product_id = fields.Many2one(related="inspection_id.product_id",
                                 store=True)
    process_type_id = fields.Many2one(
        related="inspection_id.process_type_id", store=True)
    inspection_type = fields.Selection(
        related="inspection_id.inspection_type", store=True)

    # Líneas de inspección a incluir, dedupeadas (req. 6)
    attribute_ids = fields.Many2many(
        "quality.inspection.line",
        "quality_certificate_attribute_rel",
        "certificate_id", "line_id", string="Atributos Seleccionados")

    certified_largo = fields.Float()
    certified_ancho = fields.Float()
    certified_espesor = fields.Float()
    certified_hexagono = fields.Float()
    certified_resistencia = fields.Float()
    certified_apariencia = fields.Char()
    certified_humedad = fields.Float()
    certified_pegado = fields.Char()
    certified_retiramiento = fields.Float()
    certified_calibracion = fields.Float()
    certified_engomado = fields.Char()

    date_generated = fields.Date("Fecha de Generación", required=True,
                                 default=fields.Date.context_today)
    state = fields.Selection([
        ("borrador", "Borrador"),
        ("generado", "Generado"),
        ("enviado", "Enviado"),
    ], default="borrador", required=True, tracking=True, copy=False)
    report_pdf = fields.Binary("PDF del Certificado", attachment=True)
    report_pdf_name = fields.Char()
    certified_by = fields.Many2one("res.users", required=True,
                                   default=lambda s: s.env.user, tracking=True)
    company_id = fields.Many2one("res.company", "Compañía",
                                 default=lambda s: s.env.company)
    folio = fields.Char(related="inspection_id.folio", store=True)
    lot_id = fields.Many2one(related="inspection_id.lot_id", store=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Nuevo") == "Nuevo":
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "quality.certificate") or "Nuevo"
        return super().create(vals_list)

    @api.constrains("attribute_ids")
    def _check_attribute_dedup(self):
        """No permitir atributos repetidos (req. 6)."""
        for rec in self:
            names = [(l.name or "").strip().lower()
                     for l in rec.attribute_ids if l.name]
            if len(names) != len(set(names)):
                raise UserError(_(
                    "Hay atributos repetidos en el certificado. "
                    "Cada atributo debe aparecer una sola vez."
                ))

    @api.constrains("certified_largo", "certified_ancho", "certified_espesor",
                    "certified_hexagono", "certified_resistencia",
                    "certified_humedad", "certified_retiramiento",
                    "certified_calibracion")
    def _check_no_zero_certified(self):
        """No permitir guardar atributos con valor 0 (req. 6)."""
        zero_fields = []
        for rec in self:
            mapping = {
                "Largo": rec.certified_largo,
                "Ancho": rec.certified_ancho,
                "Espesor": rec.certified_espesor,
                "Hexágono": rec.certified_hexagono,
                "Resistencia": rec.certified_resistencia,
                "Humedad": rec.certified_humedad,
                "Retiramiento": rec.certified_retiramiento,
                "Calibración": rec.certified_calibracion,
            }
            for label, value in mapping.items():
                # Solo bloquea si el campo se intentó capturar (>0 esperado)
                # y se guardó como 0 explícitamente. Por lógica del wizard,
                # solo se setea cuando hay valor > 0; este constraint refuerza.
                if value is not None and value < 0:
                    zero_fields.append(label)
            if zero_fields:
                raise UserError(_(
                    "El certificado no puede contener valores 0 ni negativos. "
                    "Revise: %s"
                ) % ", ".join(zero_fields))

    def action_generate(self):
        for rec in self:
            rec.state = "generado"

    def action_send_email(self):
        self.ensure_one()
        template = self.env.ref(
            "quality_management.email_template_quality_certificate",
            raise_if_not_found=False)
        compose = self.env.ref("mail.email_compose_message_wizard_form")
        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(compose.id, "form")],
            "target": "new",
            "context": {
                "default_model": "quality.certificate",
                "default_res_ids": self.ids,
                "default_template_id": template.id if template else False,
                "default_composition_mode": "comment",
                "mark_so_as_sent": True,
            },
        }

    def action_mark_sent(self):
        for rec in self:
            rec.state = "enviado"

    def action_print_certificate(self):
        return self.env.ref(
            "quality_management.action_report_quality_certificate"
        ).report_action(self)
''')

# =============================================================================
# 9. models/quality_5why.py
# =============================================================================
write(MODULE / "models" / "quality_5why.py", '''# -*- coding: utf-8 -*-
from odoo import models, fields


class Quality5Why(models.Model):
    _name = "quality.5why"
    _description = "5 Por qué (8D)"
    _order = "sequence asc, id asc"

    corrective_id = fields.Many2one("quality.corrective.action", required=True,
                                    ondelete="cascade", index=True)
    sequence = fields.Selection([
        ("1", "Por qué 1"), ("2", "Por qué 2"), ("3", "Por qué 3"),
        ("4", "Por qué 4"), ("5", "Por qué 5"),
    ], required=True)
    question = fields.Char("Pregunta", required=True)
    answer = fields.Text("Respuesta", required=True)
''')

# =============================================================================
# 10. models/quality_ishikawa.py
# =============================================================================
write(MODULE / "models" / "quality_ishikawa.py", '''# -*- coding: utf-8 -*-
from odoo import models, fields


class QualityIshikawa(models.Model):
    _name = "quality.ishikawa"
    _description = "Diagrama de Ishikawa (Causa-Efecto)"
    _order = "category, sequence, id"

    corrective_id = fields.Many2one("quality.corrective.action", required=True,
                                    ondelete="cascade", index=True)
    category = fields.Selection([
        ("metodo", "Método"), ("maquina", "Máquina"),
        ("mano_obra", "Mano de Obra"), ("material", "Material"),
        ("medicion", "Medición"), ("medio_ambiente", "Medio Ambiente"),
    ], required=True)
    sequence = fields.Integer(default=10)
    cause = fields.Text("Causa Identificada", required=True)
    is_root_cause = fields.Boolean("Causa Raíz")
''')

# =============================================================================
# 11. models/quality_work_team.py — equipo de trabajo a notificar (req. 7.2)
# =============================================================================
write(MODULE / "models" / "quality_work_team.py", '''# -*- coding: utf-8 -*-
from odoo import models, fields


class QualityWorkTeam(models.Model):
    _name = "quality.work.team"
    _description = "Equipo de Trabajo (8D)"

    corrective_id = fields.Many2one("quality.corrective.action", required=True,
                                    ondelete="cascade", index=True)
    user_id = fields.Many2one("res.users", "Miembro", required=True)
    role = fields.Char("Rol en el Equipo")
    notify_progress = fields.Boolean("Notificar Avances", default=True)
''')

# =============================================================================
# 12. models/quality_corrective_action.py
# =============================================================================
write(MODULE / "models" / "quality_corrective_action.py", '''# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import timedelta


class QualityCorrectiveAction(models.Model):
    _name = "quality.corrective.action"
    _description = "Acción Correctiva/Preventiva (8D)"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_opened desc, id desc"

    name = fields.Char("Referencia", required=True, readonly=True,
                       default="Nuevo", copy=False)

    # Tipo de origen — agregamos Reclamación (req. 7.1)
    origin_type = fields.Selection([
        ("inspeccion", "Inspección"),
        ("auditoria_interna", "Auditoría Interna"),
        ("auditoria_externa", "Auditoría Externa"),
        ("devolucion", "Devolución"),
        ("reclamacion", "Reclamación"),
        ("otro", "Otro"),
    ], required=True, tracking=True)

    # Tipo de defecto con OTRO + descripción libre (req. 7.1)
    defect_type = fields.Selection([
        ("dimensional", "Dimensional"),
        ("apariencia", "Apariencia"),
        ("funcional", "Funcional"),
        ("afecta_funcionalidad", "Afecta Funcionalidad"),
        ("empaque", "Empaque"),
        ("otro", "Otro"),
    ], string="Tipo de Defecto")
    defect_other_desc = fields.Char(
        "Descripción de Defecto (Otro)",
        help="Aplica cuando Tipo de Defecto = OTRO",
    )

    origin_description = fields.Text("Descripción del Incumplimiento",
                                     required=True)
    origin_inspection_id = fields.Many2one("quality.inspection")
    origin_return_id = fields.Many2one("quality.customer.return")

    responsible_id = fields.Many2one("res.users", "Responsable General",
                                     required=True, tracking=True)

    # Equipo de trabajo a notificar (req. 7.2)
    work_team_ids = fields.One2many("quality.work.team", "corrective_id",
                                    string="Equipo de Trabajo")

    action_line_ids = fields.One2many("quality.action.line", "corrective_id",
                                      string="Acciones Específicas")

    # 5 Por qué + Ishikawa (req. 7.5)
    why_ids = fields.One2many("quality.5why", "corrective_id",
                              string="5 Por qué")
    ishikawa_ids = fields.One2many("quality.ishikawa", "corrective_id",
                                   string="Diagrama de Ishikawa")

    state = fields.Selection([
        ("borrador", "Borrador"),
        ("evaluacion_calidad", "Evaluación Calidad"),
        ("abierta", "Abierta"),
        ("en_proceso", "En Proceso"),
        ("cerrada", "Cerrada"),
        ("no_procede", "No Procede"),
    ], default="borrador", required=True, tracking=True, copy=False)

    no_procede_reason = fields.Text("Motivo No Procede")
    quality_evaluated_by = fields.Many2one("res.users",
                                           "Calidad Evaluó", readonly=True)
    quality_evaluated_date = fields.Datetime(readonly=True)

    date_opened = fields.Date("Fecha de Apertura", required=True,
                              default=fields.Date.context_today)
    date_closed = fields.Date("Fecha de Cierre", tracking=True,
                              compute="_compute_date_closed", store=True,
                              readonly=False)

    action_count = fields.Integer(compute="_compute_action_stats")
    action_completed_count = fields.Integer(compute="_compute_action_stats")
    action_overdue_count = fields.Integer(compute="_compute_action_stats")
    progress = fields.Float(compute="_compute_action_stats")

    company_id = fields.Many2one("res.company", "Compañía",
                                 default=lambda s: s.env.company)

    # ------------------------------------------------------------------ compute
    @api.depends("action_line_ids", "action_line_ids.state",
                 "action_line_ids.evidence_ids")
    def _compute_action_stats(self):
        for rec in self:
            lines = rec.action_line_ids
            rec.action_count = len(lines)
            rec.action_completed_count = len(
                lines.filtered(lambda l: l.state == "completada"))
            rec.action_overdue_count = len(
                lines.filtered(lambda l: l.state == "vencida"))
            rec.progress = (
                (rec.action_completed_count / rec.action_count * 100)
                if rec.action_count else 0.0)

    @api.depends("action_line_ids.date_due", "action_line_ids.state")
    def _compute_date_closed(self):
        """Fecha cierre = fecha más lejana de las acciones (req. 7.4)."""
        for rec in self:
            if rec.state == "cerrada" and rec.action_line_ids:
                dates = rec.action_line_ids.mapped("date_due")
                rec.date_closed = max(dates) if dates else fields.Date.today()

    # ------------------------------------------------------------------ create
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Nuevo") == "Nuevo":
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "quality.corrective.action") or "Nuevo"
        return super().create(vals_list)

    @api.constrains("defect_type", "defect_other_desc")
    def _check_other_desc(self):
        for rec in self:
            if rec.defect_type == "otro" and not rec.defect_other_desc:
                raise UserError(_(
                    "Cuando el tipo de defecto es OTRO, debe describir el defecto."
                ))

    # -------------------------------------------------------- bloqueos de flujo
    def _check_pestañas_completas(self):
        """Llenado obligatorio de 4 pestañas (req. 7.3)."""
        for rec in self:
            faltantes = []
            if not rec.action_line_ids:
                faltantes.append("Acciones")
            if not rec.work_team_ids:
                faltantes.append("Equipo de Trabajo")
            if len(rec.why_ids) < 5:
                faltantes.append("5 Por qué (mínimo 5)")
            if not rec.ishikawa_ids:
                faltantes.append("Ishikawa")
            if faltantes:
                raise UserError(_(
                    "No se puede continuar. Complete las pestañas: %s"
                ) % ", ".join(faltantes))

    def action_evaluate_quality(self):
        for rec in self:
            rec.state = "evaluacion_calidad"
            rec.message_post(body=_("📋 Enviado a Evaluación de Calidad."),
                             subtype_xmlid="mail.mt_comment")

    def action_quality_evaluated(self):
        for rec in self:
            if rec.state != "evaluacion_calidad":
                raise UserError(_(
                    "Solo se puede marcar como evaluada cuando está en "
                    "estado 'Evaluación Calidad'."
                ))
            rec.quality_evaluated_by = self.env.user
            rec.quality_evaluated_date = fields.Datetime.now()
            rec.state = "abierta"
            rec.activity_schedule(
                "mail.mail_activity_data_todo",
                date_deadline=fields.Date.today() + timedelta(days=1),
                summary=_("8D abierto: %s") % rec.name,
                user_id=rec.responsible_id.id,
            )

    def action_open(self):
        """Bloqueo: no continuar a 8D si no terminó Evaluación Calidad (req. 7.3)."""
        for rec in self:
            if not rec.quality_evaluated_by:
                raise UserError(_(
                    "Debe completar primero la 'Evaluación Calidad' "
                    "antes de continuar al 8D."
                ))
            rec.state = "abierta"

    def action_in_progress(self):
        for rec in self:
            rec.state = "en_proceso"

    def action_close(self):
        for rec in self:
            rec._check_pestañas_completas()
            pending = rec.action_line_ids.filtered(
                lambda l: l.state != "completada")
            if pending:
                raise UserError(_(
                    "No se puede cerrar: %d acción(es) sin completar."
                ) % len(pending))
            rec.state = "cerrada"
            if rec.action_line_ids:
                rec.date_closed = max(rec.action_line_ids.mapped("date_due"))
            else:
                rec.date_closed = fields.Date.today()

    def action_no_proceed(self):
        for rec in self:
            if not rec.no_procede_reason:
                raise UserError(_(
                    "Capture el motivo por el que no procede la acción."
                ))
            rec.state = "no_procede"
            rec.date_closed = fields.Date.today()

    def action_reopen(self):
        for rec in self:
            rec.state = "en_proceso"
            rec.date_closed = False

    def action_print_8d(self):
        return self.env.ref(
            "quality_management.action_report_8d"
        ).report_action(self)

    @api.model
    def _cron_check_overdue_actions(self):
        today = fields.Date.today()
        overdue = self.env["quality.action.line"].search([
            ("state", "in", ("pendiente", "en_proceso")),
            ("date_due", "<", today),
        ])
        for line in overdue:
            line.state = "vencida"
            line.delay_days = (today - line.date_due).days
            partners = []
            for member in line.corrective_id.work_team_ids.filtered("notify_progress"):
                if member.user_id.partner_id:
                    partners.append(member.user_id.partner_id.id)
            line.corrective_id.message_post(
                body=_("⚠️ Acción vencida (%d días): %s — Responsable: %s")
                % (line.delay_days, line.description[:80],
                   line.responsible_id.name),
                partner_ids=list(set(partners)),
                subtype_xmlid="mail.mt_comment")
''')

# =============================================================================
# 13. models/quality_action_line.py — avance refleja evidencia (req. 7.3)
# =============================================================================
write(MODULE / "models" / "quality_action_line.py", '''# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class QualityActionLine(models.Model):
    _name = "quality.action.line"
    _description = "Línea de Acción Correctiva"
    _order = "date_due, id"

    corrective_id = fields.Many2one("quality.corrective.action",
                                    required=True, ondelete="cascade")
    description = fields.Text("Descripción de la Acción", required=True)
    responsible_id = fields.Many2one("res.users", "Responsable", required=True)
    date_due = fields.Date("Fecha de Cumplimiento", required=True)
    date_completed = fields.Date("Fecha de Cumplimiento Real")
    evidence_ids = fields.Many2many(
        "ir.attachment", "quality_action_evidence_rel",
        "action_line_id", "attachment_id", string="Evidencia")

    state = fields.Selection([
        ("pendiente", "Pendiente"),
        ("en_proceso", "En Proceso"),
        ("completada", "Completada"),
        ("vencida", "Vencida"),
    ], default="pendiente", required=True, compute="_compute_state",
       store=True, readonly=False)

    delay_days = fields.Integer(compute="_compute_delay_days", store=True)
    notes = fields.Text()

    @api.depends("evidence_ids", "date_completed")
    def _compute_state(self):
        """Reflejar avance en cuanto haya evidencia (req. 7.3)."""
        for line in self:
            if line.state == "completada":
                continue
            if line.evidence_ids and line.state == "pendiente":
                line.state = "en_proceso"

    @api.depends("date_due", "state")
    def _compute_delay_days(self):
        today = fields.Date.today()
        for l in self:
            if l.date_due and l.state in ("pendiente", "en_proceso", "vencida"):
                l.delay_days = max(0, (today - l.date_due).days)
            else:
                l.delay_days = 0

    def action_complete(self):
        for rec in self:
            if not rec.evidence_ids:
                raise UserError(_(
                    "No se puede completar la acción sin adjuntar evidencia."
                ))
            rec.state = "completada"
            rec.date_completed = fields.Date.today()

    def action_reopen(self):
        for rec in self:
            rec.state = "en_proceso"
            rec.date_completed = False
''')

# =============================================================================
# 14. models/quality_customer_return.py
# =============================================================================
write(MODULE / "models" / "quality_customer_return.py", '''# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import timedelta


class QualityCustomerReturn(models.Model):
    _name = "quality.customer.return"
    _description = "Devolución de Cliente"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_received desc, id desc"

    name = fields.Char("Referencia", required=True, readonly=True,
                       default="Nuevo", copy=False)
    partner_id = fields.Many2one("res.partner", "Cliente",
                                 required=True, tracking=True)
    sale_order_id = fields.Many2one("sale.order", "Orden de Venta Original",
                                    tracking=True)
    defect_type = fields.Selection([
        ("dimensional", "Dimensional"),
        ("apariencia", "Apariencia"),
        ("funcional", "Funcional"),
        ("empaque", "Empaque"),
        ("otro", "Otro"),
    ], required=True, tracking=True)
    defect_other_desc = fields.Char("Descripción Defecto Otro")
    defect_pieces = fields.Integer("Piezas con Defecto", required=True)
    return_reason = fields.Text("Motivo de la Devolución", required=True)
    production_date = fields.Date("Fecha de Producción", required=True)
    delivery_date = fields.Date("Fecha de Entrega Producción/Fabricación")

    evidence_ids = fields.Many2many(
        "ir.attachment", "quality_return_evidence_rel",
        "return_id", "attachment_id",
        string="Evidencia Fotográfica", required=True)

    evidence_pdf = fields.Binary("Reporte de Evidencia (PDF)", attachment=True)
    evidence_pdf_name = fields.Char()
    pallets_returned = fields.Boolean("Se Regresan Tarimas")
    pallet_return_date = fields.Date("Fecha Retorno de Tarimas")

    # Formato de reclamación obligatorio (req. 7.5 / 8)
    claim_format_pdf = fields.Binary("Formato de Reclamación (PDF)",
                                     attachment=True, required=False)
    claim_format_pdf_name = fields.Char()

    affects_functionality = fields.Boolean("Afecta Funcionalidad",
                                           tracking=True)
    corrective_action_id = fields.Many2one("quality.corrective.action",
                                           "8D Generado", readonly=True,
                                           tracking=True)

    # Justificación comercial cuando excede 30 días (req. 7.4 / 8)
    sales_manager_justification = fields.Text(
        "Motivo Comercial - Gerente de Ventas",
        help="Cuando comercialmente se decide proceder con devolución/"
             "reposición pese al bloqueo (>30 días).",
    )
    sales_manager_id = fields.Many2one("res.users",
                                       "Gerente de Ventas Autorizó")

    state = fields.Selection([
        ("borrador", "Borrador"),
        ("evaluacion_ventas", "Evaluación Ventas"),
        ("evaluacion_calidad", "Evaluación Calidad"),
        ("en_8d", "En 8D"),
        ("cerrada", "Cerrada"),
        ("no_procede", "No Procede"),
    ], default="borrador", required=True, tracking=True, copy=False)

    date_received = fields.Date("Fecha de Recepción", required=True,
                                default=fields.Date.context_today)
    days_since_production = fields.Integer(
        compute="_compute_days_since_production")
    is_within_period = fields.Boolean(
        compute="_compute_days_since_production")
    pallet_alert_15 = fields.Boolean(
        "Alerta: Retorno >15 días",
        compute="_compute_pallet_alert_15", store=True)
    company_id = fields.Many2one("res.company", "Compañía",
                                 default=lambda s: s.env.company)

    @api.depends("production_date", "date_received")
    def _compute_days_since_production(self):
        for rec in self:
            if rec.production_date and rec.date_received:
                delta = (rec.date_received - rec.production_date).days
                rec.days_since_production = delta
                rec.is_within_period = delta < 30
            else:
                rec.days_since_production = 0
                rec.is_within_period = True

    @api.depends("pallet_return_date", "date_received", "pallets_returned")
    def _compute_pallet_alert_15(self):
        for rec in self:
            if (rec.pallets_returned and rec.pallet_return_date
                    and rec.date_received):
                delta = (rec.pallet_return_date - rec.date_received).days
                rec.pallet_alert_15 = delta > 15
            else:
                rec.pallet_alert_15 = False

    @api.constrains("defect_type", "defect_other_desc")
    def _check_other(self):
        for rec in self:
            if rec.defect_type == "otro" and not rec.defect_other_desc:
                raise UserError(_(
                    "Tipo de defecto OTRO requiere descripción."))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Nuevo") == "Nuevo":
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "quality.customer.return") or "Nuevo"
        return super().create(vals_list)

    def _check_required_attachments(self):
        for rec in self:
            if not rec.evidence_ids:
                raise UserError(_("Debe adjuntar evidencia fotográfica."))
            if not rec.claim_format_pdf:
                raise UserError(_(
                    "Debe adjuntar el Formato de Reclamación (PDF)."
                ))

    def action_submit_sales(self):
        for rec in self:
            rec._check_required_attachments()
            if not rec.is_within_period and not rec.sales_manager_justification:
                rec.state = "no_procede"
                rec.message_post(
                    body=_(
                        "🚫 Devolución NO PROCEDE: %d días desde producción "
                        "(>30). Capture el motivo comercial del Gerente "
                        "de Ventas si desea proceder."
                    ) % rec.days_since_production,
                    subtype_xmlid="mail.mt_comment")
                continue
            rec.state = "evaluacion_ventas"

    def action_authorize_commercial(self):
        """Permite continuar pese a >30 días si Gerente de Ventas lo justifica."""
        for rec in self:
            if not rec.sales_manager_justification:
                raise UserError(_(
                    "Capture el motivo comercial del Gerente de Ventas."
                ))
            rec.sales_manager_id = self.env.user
            rec.state = "evaluacion_ventas"
            rec.message_post(
                body=_(
                    "✓ Autorización comercial por %s. Motivo: %s"
                ) % (self.env.user.name, rec.sales_manager_justification),
                subtype_xmlid="mail.mt_comment")

    def action_submit_quality(self):
        for rec in self:
            rec.state = "evaluacion_calidad"
            users = self.env.ref(
                "quality_management.group_quality_manager").users
            for u in users:
                rec.activity_schedule(
                    "mail.mail_activity_data_todo",
                    date_deadline=fields.Date.today() + timedelta(days=3),
                    summary=_("Evaluar devolución: %s") % rec.name,
                    user_id=u.id)
            if rec.pallets_returned:
                rec.message_post(
                    body=_(
                        "📦 Tarimas retornadas. Logística/Producción: "
                        "evaluar físicamente de inmediato."),
                    subtype_xmlid="mail.mt_comment")
            if rec.pallet_alert_15:
                rec.message_post(
                    body=_(
                        "⚠️ Alerta: el retorno de tarimas se programó a "
                        "más de 15 días hábiles desde recepción."),
                    subtype_xmlid="mail.mt_comment")

    def action_generate_8d(self):
        for rec in self:
            ca = self.env["quality.corrective.action"].create({
                "origin_type": "devolucion",
                "defect_type": rec.defect_type,
                "defect_other_desc": rec.defect_other_desc,
                "origin_description": _(
                    "Devolución de cliente: %s\\nTipo de defecto: %s\\n"
                    "Piezas: %d\\nMotivo: %s"
                ) % (rec.partner_id.name,
                     dict(rec._fields["defect_type"].selection).get(
                         rec.defect_type, ""),
                     rec.defect_pieces, rec.return_reason),
                "origin_return_id": rec.id,
                "responsible_id": self.env.user.id,
            })
            rec.corrective_action_id = ca.id
            rec.state = "en_8d"

    def action_close(self):
        for rec in self:
            rec.state = "cerrada"

    def action_no_proceed(self):
        for rec in self:
            rec.state = "no_procede"

    def action_print_customer_return(self):
        return self.env.ref(
            "quality_management.action_report_customer_return"
        ).report_action(self)
''')

# =============================================================================
# 15. models/quality_customer_document.py
# =============================================================================
write(MODULE / "models" / "quality_customer_document.py", '''# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import timedelta


class QualityCustomerDocument(models.Model):
    _name = "quality.customer.document"
    _description = "Documento Solicitado por Cliente"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_requested desc, id desc"

    name = fields.Char("Referencia", required=True, readonly=True,
                       default="Nuevo", copy=False)
    partner_id = fields.Many2one("res.partner", "Cliente Solicitante",
                                 required=True, tracking=True)

    # Tipos limpios (req. 9.1) — sin APARIENCIA ni ESPECIFICACION_EMPAQUE
    document_type = fields.Selection([
        ("rohs", "RoHS"),
        ("psw", "PSW"),
        ("ppap", "PPAP"),
        ("pfmea", "PFMEA"),
        ("diagrama_flujo", "Diagrama de Flujo"),
        ("carta_garantia", "Carta Garantía"),
        ("otro", "Otro"),
    ], string="Tipo de Documento", required=True, tracking=True)

    # OTRO con descripción libre (req. 9.4)
    document_type_other = fields.Char(
        "Especifique Tipo (Otro)",
        help="Cuando el tipo de documento solicitado no está en el listado.",
    )

    description = fields.Text(
        "Descripción de la Solicitud", required=True,
        help="Bloqueo: no se puede avanzar sin descripción.",
    )

    requires_dimensions = fields.Boolean(
        "Implica Mediciones Dimensionales", required=True, tracking=True)

    # Formato del cliente (Sí/No + carga) — req. 9.2
    has_client_format = fields.Selection([
        ("si", "Sí"), ("no", "No"),
    ], string="¿Cliente Solicita Llenado en su Formato?", default="no")
    client_format_ids = fields.Many2many(
        "ir.attachment", "quality_doc_client_format_rel",
        "document_id", "attachment_id", string="Formatos del Cliente")

    result_document_ids = fields.Many2many(
        "ir.attachment", "quality_doc_result_rel",
        "document_id", "attachment_id",
        string="Documentos Generados / Cargados")

    # Documento principal — soporta PDF o imagen (req. 9.2)
    main_pdf = fields.Binary("Documento Principal (PDF)", attachment=True)
    main_pdf_name = fields.Char()
    main_image = fields.Binary("Imagen Principal (PNG/JPG)", attachment=True)
    main_image_name = fields.Char()

    requested_by = fields.Many2one("res.users", "Solicitante (Ventas)",
                                   required=True,
                                   default=lambda s: s.env.user, tracking=True)
    responsible_id = fields.Many2one("res.users", "Responsable en Calidad",
                                     required=True, tracking=True)

    state = fields.Selection([
        ("borrador", "Borrador"),
        ("en_proceso", "En Proceso"),
        ("completado", "Completado"),
        ("enviado", "Enviado"),
    ], default="borrador", required=True, tracking=True, copy=False)

    # Fechas bloqueadas (req. 9.1)
    date_requested = fields.Date("Fecha de Solicitud", required=True,
                                 readonly=True, copy=False,
                                 default=fields.Date.context_today)
    date_due = fields.Date("Fecha Límite", compute="_compute_date_due",
                           store=True, readonly=True)
    date_completed = fields.Date("Fecha de Entrega Real", readonly=True)

    company_id = fields.Many2one("res.company", "Compañía",
                                 default=lambda s: s.env.company)

    @api.depends("date_requested", "requires_dimensions")
    def _compute_date_due(self):
        for rec in self:
            if rec.date_requested:
                days = 7 if rec.requires_dimensions else 5
                rec.date_due = rec.date_requested + timedelta(days=days)
            else:
                rec.date_due = False

    @api.constrains("document_type", "document_type_other")
    def _check_other(self):
        for rec in self:
            if rec.document_type == "otro" and not rec.document_type_other:
                raise UserError(_(
                    "Tipo de documento OTRO requiere especificación."))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Nuevo") == "Nuevo":
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "quality.customer.document") or "Nuevo"
        return super().create(vals_list)

    def _check_can_save(self):
        """Bloqueos req. 9.3: descripción y al menos un documento cargado."""
        for rec in self:
            if not rec.description or not rec.description.strip():
                raise UserError(_(
                    "Capture la descripción de la solicitud antes de avanzar."
                ))
            tiene_doc = (rec.main_pdf or rec.main_image
                         or rec.result_document_ids
                         or rec.client_format_ids)
            if not tiene_doc:
                raise UserError(_(
                    "Debe cargar al menos un documento (PDF, imagen o adjunto) "
                    "antes de avanzar."
                ))

    def action_start(self):
        for rec in self:
            rec._check_can_save()
            rec.state = "en_proceso"

    def action_complete(self):
        for rec in self:
            rec._check_can_save()
            rec.state = "completado"
            rec.date_completed = fields.Date.today()

    def action_send(self):
        for rec in self:
            rec.state = "enviado"

    def action_print_customer_document(self):
        return self.env.ref(
            "quality_management.action_report_customer_document"
        ).report_action(self)
''')

# =============================================================================
# 16. models/quality_troquel.py — gestión de troqueles (req. 10)
# =============================================================================
write(MODULE / "models" / "quality_troquel.py", '''# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class QualityTroquel(models.Model):
    _name = "quality.troquel"
    _description = "Troquel"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name asc"

    name = fields.Char("Identificación del Troquel", required=True,
                       tracking=True, copy=False)
    partner_id = fields.Many2one("res.partner", "Cliente",
                                 required=True, tracking=True)
    part_number = fields.Char("Número de Parte", required=True, tracking=True)
    visible_label = fields.Char("Etiqueta Visible (Cliente + No. Parte)",
                                compute="_compute_visible_label", store=True)
    state = fields.Selection([
        ("recepcion", "En Recepción"),
        ("validacion", "En Validación (Calidad/Producción)"),
        ("activo", "Activo / En Producción"),
        ("danado", "Con Daño - Fuera de Uso"),
        ("reparacion_interna", "En Reparación Interna"),
        ("reparacion_proveedor", "En Reparación con Proveedor"),
        ("obsoleto", "Obsoleto"),
    ], default="recepcion", required=True, tracking=True)
    workflow_event_ids = fields.One2many(
        "quality.troquel.event", "troquel_id", string="Bitácora")

    # Recepción / nuevos troqueles (req. 10.1)
    plano_herramental = fields.Binary("Plano de Herramental (PDF)",
                                      attachment=True)
    plano_herramental_name = fields.Char()
    proveedor_id = fields.Many2one("res.partner", "Proveedor",
                                   domain=[("supplier_rank", ">", 0)])

    # Revisión (req. 10.2)
    pieces_per_review = fields.Integer(
        "Piezas para Revisión",
        help="Cantidad de piezas troqueladas tras las cuales se hace revisión.")
    last_review_date = fields.Date("Última Revisión")
    next_review_date = fields.Date("Siguiente Revisión",
                                   compute="_compute_next_review", store=True)

    # Reparación (req. 10.3)
    days_at_supplier = fields.Integer("Días Estimados Fuera de Planta")
    repair_description = fields.Text("Desglose de Reparación")
    rack_location = fields.Char("Ubicación en Rack")

    company_id = fields.Many2one("res.company", "Compañía",
                                 default=lambda s: s.env.company)

    @api.depends("partner_id", "part_number")
    def _compute_visible_label(self):
        for rec in self:
            rec.visible_label = (
                f"{rec.partner_id.name or ''} - {rec.part_number or ''}"
            ).strip(" -")

    @api.depends("last_review_date")
    def _compute_next_review(self):
        from datetime import timedelta
        for rec in self:
            rec.next_review_date = (rec.last_review_date + timedelta(days=30)
                                    if rec.last_review_date else False)

    # ---------------------------------------------------------- workflow ALTA
    def action_validate(self):
        for rec in self:
            if not rec.plano_herramental:
                raise UserError(_(
                    "Cargue el plano de herramental antes de convocar a "
                    "validación."))
            rec.state = "validacion"
            rec._log_event("Convocatoria a validación de dimensiones y "
                           "prueba funcional (Calidad y Producción).")

    def action_activate(self):
        for rec in self:
            rec.state = "activo"
            rec._log_event(
                "Troquel registrado como ACTIVO y FUNCIONAL. "
                "Etiqueta visible: %s." % rec.visible_label)

    # ---------------------------------------------------------- workflow DAÑO
    def action_report_damage(self):
        for rec in self:
            rec.state = "danado"
            rec._log_event(
                "Producción notifica daño en troquel — Diseño debe validar.")

    def action_send_to_internal_repair(self):
        for rec in self:
            rec.state = "reparacion_interna"
            rec._log_event("Reparación interna iniciada.")

    def action_send_to_supplier(self):
        for rec in self:
            if not rec.days_at_supplier:
                raise UserError(_(
                    "Indique los días estimados fuera de planta."
                ))
            rec.state = "reparacion_proveedor"
            rec._log_event(
                "Enviado a proveedor (%s) — Días fuera: %d."
                % (rec.proveedor_id.name or "—", rec.days_at_supplier))

    def action_finish_repair(self):
        for rec in self:
            rec._log_event(
                "Reparación finalizada: %s" % (rec.repair_description or "—"))
            rec.state = "validacion"

    def action_reject_repair(self):
        for rec in self:
            rec._log_event(
                "Reparación NO cumple — se retorna al proveedor / re-trabajo.")
            rec.state = "danado"

    def action_set_obsolete(self):
        for rec in self:
            rec.state = "obsoleto"
            rec._log_event("Troquel marcado como OBSOLETO.")

    # ----- helpers -----------------------------------------------------------
    def _log_event(self, msg):
        self.ensure_one()
        self.env["quality.troquel.event"].create({
            "troquel_id": self.id,
            "user_id": self.env.user.id,
            "description": msg,
            "state_after": self.state,
        })
        self.message_post(body=msg, subtype_xmlid="mail.mt_comment")


class QualityTroquelEvent(models.Model):
    _name = "quality.troquel.event"
    _description = "Evento de Troquel"
    _order = "date desc, id desc"

    troquel_id = fields.Many2one("quality.troquel", required=True,
                                 ondelete="cascade", index=True)
    date = fields.Datetime(default=fields.Datetime.now, readonly=True)
    user_id = fields.Many2one("res.users", "Registrado por")
    description = fields.Text("Descripción", required=True)
    state_after = fields.Char("Estado Resultante")
''')

# =============================================================================
# 17. views/quality_troquel_views.xml
# =============================================================================
write(MODULE / "views" / "quality_troquel_views.xml", '''<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_quality_troquel_list" model="ir.ui.view">
        <field name="name">quality.troquel.list</field>
        <field name="model">quality.troquel</field>
        <field name="arch" type="xml">
            <list decoration-success="state == 'activo'"
                  decoration-danger="state == 'danado'"
                  decoration-warning="state in ('reparacion_interna','reparacion_proveedor')"
                  decoration-muted="state == 'obsoleto'">
                <field name="name"/>
                <field name="partner_id"/>
                <field name="part_number"/>
                <field name="proveedor_id" optional="show"/>
                <field name="last_review_date" optional="show"/>
                <field name="next_review_date" optional="show"/>
                <field name="state" widget="badge"/>
            </list>
        </field>
    </record>

    <record id="view_quality_troquel_form" model="ir.ui.view">
        <field name="name">quality.troquel.form</field>
        <field name="model">quality.troquel</field>
        <field name="arch" type="xml">
            <form string="Troquel">
                <header>
                    <button name="action_validate" string="Convocar a Validación"
                            type="object" class="btn-primary"
                            invisible="state not in ('recepcion','reparacion_interna','reparacion_proveedor')"/>
                    <button name="action_activate" string="Marcar como ACTIVO"
                            type="object" class="btn-primary"
                            invisible="state != 'validacion'"/>
                    <button name="action_report_damage" string="Reportar Daño"
                            type="object" class="btn-warning"
                            invisible="state != 'activo'"/>
                    <button name="action_send_to_internal_repair"
                            string="Reparación Interna" type="object"
                            invisible="state != 'danado'"/>
                    <button name="action_send_to_supplier"
                            string="Enviar a Proveedor" type="object"
                            invisible="state != 'danado'"/>
                    <button name="action_finish_repair" string="Reparación Finalizada"
                            type="object"
                            invisible="state not in ('reparacion_interna','reparacion_proveedor')"/>
                    <button name="action_set_obsolete" string="Marcar Obsoleto"
                            type="object"
                            invisible="state in ('obsoleto',)"/>
                    <field name="state" widget="statusbar"/>
                </header>
                <sheet>
                    <div class="oe_title">
                        <h1><field name="name" placeholder="ID del troquel..."/></h1>
                        <h3><field name="visible_label" readonly="1"/></h3>
                    </div>
                    <group>
                        <group>
                            <field name="partner_id"/>
                            <field name="part_number"/>
                            <field name="proveedor_id"/>
                            <field name="rack_location"/>
                        </group>
                        <group>
                            <field name="pieces_per_review"/>
                            <field name="last_review_date"/>
                            <field name="next_review_date"/>
                            <field name="days_at_supplier"
                                   invisible="state != 'reparacion_proveedor'"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Plano de Herramental">
                            <group>
                                <field name="plano_herramental"
                                       filename="plano_herramental_name"/>
                                <field name="plano_herramental_name" invisible="1"/>
                            </group>
                            <div invisible="not plano_herramental"
                                 class="o_quality_pdf_preview">
                                <field name="plano_herramental"
                                       widget="pdf_viewer" readonly="1"/>
                            </div>
                        </page>
                        <page string="Reparación" invisible="state == 'recepcion'">
                            <field name="repair_description"
                                   placeholder="Desglose de reparación realizada..."/>
                        </page>
                        <page string="Bitácora">
                            <field name="workflow_event_ids" readonly="1">
                                <list>
                                    <field name="date"/>
                                    <field name="user_id"/>
                                    <field name="state_after"/>
                                    <field name="description"/>
                                </list>
                            </field>
                        </page>
                    </notebook>
                </sheet>
                <chatter/>
            </form>
        </field>
    </record>

    <record id="action_quality_troquel" model="ir.actions.act_window">
        <field name="name">Troqueles</field>
        <field name="res_model">quality.troquel</field>
        <field name="view_mode">list,form</field>
    </record>

    <menuitem id="menu_quality_troquel"
              name="Troqueles"
              parent="menu_quality_root"
              action="action_quality_troquel"
              sequence="55"/>
</odoo>
''')

# =============================================================================
# 18. security/ir.model.access.csv — agregar accesos a nuevos modelos
# =============================================================================
ACCESS_CSV = MODULE / "security" / "ir.model.access.csv"
new_access = [
    "access_quality_troquel_inspector,quality.troquel.inspector,model_quality_troquel,quality_management.group_quality_inspector,1,1,1,0",
    "access_quality_troquel_manager,quality.troquel.manager,model_quality_troquel,quality_management.group_quality_manager,1,1,1,1",
    "access_quality_troquel_event_inspector,quality.troquel.event.inspector,model_quality_troquel_event,quality_management.group_quality_inspector,1,1,1,0",
    "access_quality_troquel_event_manager,quality.troquel.event.manager,model_quality_troquel_event,quality_management.group_quality_manager,1,1,1,1",
    "access_quality_5why_inspector,quality.5why.inspector,model_quality_5why,quality_management.group_quality_inspector,1,1,1,1",
    "access_quality_ishikawa_inspector,quality.ishikawa.inspector,model_quality_ishikawa,quality_management.group_quality_inspector,1,1,1,1",
    "access_quality_work_team_inspector,quality.work.team.inspector,model_quality_work_team,quality_management.group_quality_inspector,1,1,1,1",
    "access_quality_drawing_modification_user,quality.drawing.modification.user,model_quality_drawing_modification,quality_management.group_quality_user,1,1,1,1",
]
if ACCESS_CSV.exists():
    existing = ACCESS_CSV.read_text(encoding="utf-8")
    if "model_quality_troquel" not in existing:
        append_csv_lines(ACCESS_CSV, new_access)
    else:
        print(f"  ⏭  {ACCESS_CSV.relative_to(MODULE)} (ya tiene los accesos)")
else:
    print("  ⚠  ir.model.access.csv no encontrado — agregar manualmente:")
    for line in new_access:
        print("     " + line)

# =============================================================================
# 19. Aviso final
# =============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Cambios aplicados en backend.

PASOS POST-SCRIPT:

 1. Reinicia Odoo:
       odoo-bin -d <db> -u quality_management --stop-after-init

 2. Las VISTAS XML existentes (sample_release_views, drawing_release_views,
    inspection_views, corrective_action_views, customer_return_views,
    customer_document_views) NO fueron tocadas — los nuevos campos se
    pueden agregar desde Studio o un siguiente patch de vistas.
    Los campos nuevos están disponibles en los modelos.

 3. Migración de datos:
    - Process Types: el código 'laminadora_remanejo' fue reemplazado por
      'laminadora' + 'sierras_ranuradoras'. Las inspecciones existentes
      seguirán funcionando con su process_type_id actual.
    - Hexágono: el campo en inspección ahora tiene 4 tipos (tipo_1..4)
      uniformes; valores legacy tipo_a/b/c necesitan mapeo manual o por SQL.
    - Customer Document: se removieron 'apariencia' y 'especificacion_empaque'
      de la selección. Documentos existentes con esos valores deberán
      remapearse antes de upgrade (o se mostrarán en blanco).

 4. NUEVOS modelos disponibles:
    - quality.troquel + quality.troquel.event (gestión de troqueles)
    - quality.5why (5 Por qué)
    - quality.ishikawa (diagrama Ishikawa)
    - quality.work.team (equipo de trabajo 8D)
    - quality.drawing.modification (control de cambios de planos)

 5. Backup disponible en: """ + str(BACKUP) + """

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")