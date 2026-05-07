#!/usr/bin/env python3
"""
Aplicador de correcciones críticas para quality_management.

Coloca este script en la raíz del módulo (junto a __manifest__.py) y ejecútalo:
    python3 apply_critical_fixes.py

Aplica los siguientes cambios (idempotentes — seguros de re-ejecutar):
    1. 8D completo: D3 (Contención), D7 (Prevención), D8 (Reconocimiento)
    2. value_cumple con opción N/A
    3. Atributos preconfigurados por proceso (Guillotina/Pegado/Troquelado/Impresión/Acabado)
    4. Bloqueo de troquelado_ids vacío al liberar
    5. Cliente auto-enlazado en Troquelado desde OP/Producto
    6. show_alineacion en Octágono (campo huérfano expuesto)
    7. Dedupe automático en wizard de certificado
    8. Help text en Folio y Código
"""

import shutil
import sys
from datetime import datetime
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent

# ───────────────────────────────────────────────────────────── helpers ──
def banner(msg):
    print(f"\n{'═' * 70}\n  {msg}\n{'═' * 70}")


def step(msg):
    print(f"\n▸ {msg}")


def info(msg):
    print(f"  · {msg}")


def ok(msg):
    print(f"  ✓ {msg}")


def warn(msg):
    print(f"  ⚠ {msg}")


def fail(msg):
    print(f"  ✗ {msg}")


def backup():
    """Backup completo del módulo antes de tocar nada."""
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bk = MODULE_DIR.parent / f"{MODULE_DIR.name}_backup_{stamp}"
    shutil.copytree(
        MODULE_DIR,
        bk,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
    )
    ok(f"Backup creado en: {bk}")
    return bk


def patch_file(rel_path, old, new, marker_already=None, count=1):
    """
    Reemplaza `old` por `new` en `rel_path`. Idempotente:
    si `marker_already` ya está en el archivo, no toca nada.
    """
    f = MODULE_DIR / rel_path
    if not f.exists():
        fail(f"No existe: {rel_path}")
        return False
    txt = f.read_text(encoding="utf-8")
    if marker_already and marker_already in txt:
        info(f"{rel_path}: ya aplicado")
        return False
    if old not in txt:
        fail(f"{rel_path}: patrón no encontrado")
        return False
    new_txt = txt.replace(old, new, count)
    f.write_text(new_txt, encoding="utf-8")
    ok(f"{rel_path}")
    return True


def write_file(rel_path, content, overwrite=False):
    f = MODULE_DIR / rel_path
    if f.exists() and not overwrite:
        info(f"{rel_path}: ya existe, skip")
        return False
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(content, encoding="utf-8")
    ok(f"creado {rel_path}")
    return True


# ──────────────────────────────────── FIX 1: 8D completo (D3, D7, D8) ──
def fix_8d_disciplines():
    step("[1] 8D completo — agregando D3 / D7 / D8")

    # 1.1 Modelo: nuevos campos
    patch_file(
        "models/quality_corrective_action.py",
        old='    # 5 Por qué + Ishikawa (req. 7.5)\n    why_ids = fields.One2many("quality.5why", "corrective_id",\n                              string="5 Por qué")',
        new='''    # D3 — Contención
    containment_actions = fields.Text(
        "D3 - Acciones de Contención",
        help="Acciones inmediatas para contener el problema y proteger al cliente.")
    containment_date = fields.Date("Fecha de Contención")
    containment_responsible_id = fields.Many2one(
        "res.users", "Responsable Contención")

    # D7 — Prevención
    prevention_actions = fields.Text(
        "D7 - Acciones Preventivas Sistémicas",
        help="Cambios al sistema (procedimientos, controles, capacitación) "
             "para evitar recurrencia.")
    prevention_implemented_date = fields.Date(
        "Fecha de Implementación de Prevención")
    prevention_responsible_id = fields.Many2one(
        "res.users", "Responsable Prevención")

    # D8 — Reconocimiento al equipo
    team_recognition = fields.Text(
        "D8 - Reconocimiento al Equipo",
        help="Reconocimiento al equipo y aprendizajes documentados.")
    d8_closing_date = fields.Date("Fecha de Cierre D8")

    # 5 Por qué + Ishikawa (req. 7.5)
    why_ids = fields.One2many("quality.5why", "corrective_id",
                              string="5 Por qué")''',
        marker_already="containment_actions",
    )

    # 1.2 Validación de las 4 pestañas → ahora son 7 (D3+4D7D8 críticas para cierre)
    patch_file(
        "models/quality_corrective_action.py",
        old='''    def _check_pestañas_completas(self):
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
                ) % ", ".join(faltantes))''',
        new='''    def _check_pestañas_completas(self):
        """Llenado obligatorio de las 8 disciplinas (req. 7.3 + 7.5)."""
        for rec in self:
            faltantes = []
            if not rec.work_team_ids:
                faltantes.append("D2 Equipo de Trabajo")
            if not rec.containment_actions:
                faltantes.append("D3 Contención")
            if len(rec.why_ids) < 5:
                faltantes.append("D4 5 Por qué (mínimo 5)")
            if not rec.ishikawa_ids:
                faltantes.append("D5 Ishikawa")
            if not rec.action_line_ids:
                faltantes.append("D6 Acciones")
            if not rec.prevention_actions:
                faltantes.append("D7 Prevención")
            if not rec.team_recognition:
                faltantes.append("D8 Reconocimiento")
            if faltantes:
                raise UserError(_(
                    "No se puede cerrar. Complete: %s"
                ) % ", ".join(faltantes))''',
        marker_already='faltantes.append("D3 Contención")',
    )

    # 1.3 Vista: nuevas pestañas
    patch_file(
        "views/quality_corrective_action_views.xml",
        old='''                        <page string="D2 - Equipo de Trabajo" name="team">''',
        new='''                        <page string="D3 - Contención" name="containment">
                            <p class="text-muted">
                                <i class="fa fa-info-circle"/>
                                Acciones inmediatas para proteger al cliente.
                            </p>
                            <group>
                                <field name="containment_responsible_id"/>
                                <field name="containment_date"/>
                            </group>
                            <field name="containment_actions"
                                   placeholder="Describa las acciones de contención inmediatas..."/>
                        </page>
                        <page string="D7 - Prevención" name="prevention">
                            <p class="text-muted">
                                <i class="fa fa-info-circle"/>
                                Cambios sistémicos para evitar recurrencia.
                            </p>
                            <group>
                                <field name="prevention_responsible_id"/>
                                <field name="prevention_implemented_date"/>
                            </group>
                            <field name="prevention_actions"
                                   placeholder="Cambios a procedimientos, controles, capacitación..."/>
                        </page>
                        <page string="D8 - Reconocimiento" name="recognition">
                            <p class="text-muted">
                                <i class="fa fa-info-circle"/>
                                Reconocimiento al equipo y aprendizajes documentados.
                            </p>
                            <group>
                                <field name="d8_closing_date"/>
                            </group>
                            <field name="team_recognition"
                                   placeholder="Reconocimiento al equipo, lecciones aprendidas..."/>
                        </page>
                        <page string="D2 - Equipo de Trabajo" name="team">''',
        marker_already='<page string="D3 - Contención"',
    )

    # 1.4 Reporte 8D: agregar D3, D7, D8
    patch_file(
        "reports/report_8d.xml",
        old='''                        <h4>D3 - Plan de Acciones</h4>''',
        new='''                        <h4>D3 - Contención</h4>
                        <table class="table table-bordered table-sm" style="margin-bottom: 15px;">
                            <tbody>
                                <tr>
                                    <td class="fw-bold" style="width: 30%;">Responsable:</td>
                                    <td><span t-field="doc.containment_responsible_id.name"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Fecha:</td>
                                    <td><span t-field="doc.containment_date"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Acciones:</td>
                                    <td><span t-field="doc.containment_actions"/></td>
                                </tr>
                            </tbody>
                        </table>

                        <h4>D6 - Plan de Acciones</h4>''',
        marker_already="<h4>D3 - Contención</h4>",
    )

    patch_file(
        "reports/report_8d.xml",
        old='''                        <div style="margin-top: 40px;">
                            <div class="row">
                                <div class="col-4 text-center">
                                    <p>____________________________</p>
                                    <p class="fw-bold"><span t-field="doc.responsible_id.name"/></p>
                                    <p>Responsable</p>
                                </div>
                                <div class="col-4 text-center">
                                    <p>____________________________</p>
                                    <p>Calidad</p>
                                </div>
                                <div class="col-4 text-center">
                                    <p>____________________________</p>
                                    <p>Dirección</p>
                                </div>
                            </div>
                        </div>''',
        new='''                        <h4>D7 - Acciones Preventivas Sistémicas</h4>
                        <table class="table table-bordered table-sm" style="margin-bottom: 15px;">
                            <tbody>
                                <tr>
                                    <td class="fw-bold" style="width: 30%;">Responsable:</td>
                                    <td><span t-field="doc.prevention_responsible_id.name"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Fecha de Implementación:</td>
                                    <td><span t-field="doc.prevention_implemented_date"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Acciones:</td>
                                    <td><span t-field="doc.prevention_actions"/></td>
                                </tr>
                            </tbody>
                        </table>

                        <h4>D8 - Reconocimiento al Equipo</h4>
                        <table class="table table-bordered table-sm" style="margin-bottom: 15px;">
                            <tbody>
                                <tr>
                                    <td class="fw-bold" style="width: 30%;">Fecha de Cierre:</td>
                                    <td><span t-field="doc.d8_closing_date"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Reconocimiento:</td>
                                    <td><span t-field="doc.team_recognition"/></td>
                                </tr>
                            </tbody>
                        </table>

                        <div style="margin-top: 40px;">
                            <div class="row">
                                <div class="col-4 text-center">
                                    <p>____________________________</p>
                                    <p class="fw-bold"><span t-field="doc.responsible_id.name"/></p>
                                    <p>Responsable</p>
                                </div>
                                <div class="col-4 text-center">
                                    <p>____________________________</p>
                                    <p>Calidad</p>
                                </div>
                                <div class="col-4 text-center">
                                    <p>____________________________</p>
                                    <p>Dirección</p>
                                </div>
                            </div>
                        </div>''',
        marker_already="<h4>D7 - Acciones Preventivas",
    )


# ────────────────────────────────────────── FIX 2: value_cumple con N/A ──
def fix_value_cumple_na():
    step("[2] value_cumple — agregando opción N/A")
    patch_file(
        "models/quality_inspection_line.py",
        old='''    value_cumple = fields.Selection([
        ('cumple', 'Cumple'),
        ('no_cumple', 'No Cumple'),
    ], string='Valor Cumple/No Cumple')''',
        new='''    value_cumple = fields.Selection([
        ('cumple', 'Cumple'),
        ('no_cumple', 'No Cumple'),
        ('na', 'N/A'),
    ], string='Valor Cumple/No Cumple/N/A')''',
        marker_already="('na', 'N/A'),",
    )


# ──────────────────────────── FIX 3: Atributos preconfigurados por proceso ──
ATTRIBUTE_PRESET_XML = """<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">

        <!-- ═══════════════ GUILLOTINA ═══════════════ -->
        <record id="attr_guillotina_medidas" model="quality.attribute.template">
            <field name="name">Medidas correctas</field>
            <field name="process_type_id" ref="process_type_guillotina"/>
            <field name="attribute_type">boolean</field>
            <field name="sequence">10</field>
            <field name="is_required" eval="True"/>
        </record>
        <record id="attr_guillotina_amarre" model="quality.attribute.template">
            <field name="name">Amarre de paquetes</field>
            <field name="process_type_id" ref="process_type_guillotina"/>
            <field name="attribute_type">boolean</field>
            <field name="sequence">20</field>
            <field name="is_required" eval="True"/>
        </record>
        <record id="attr_guillotina_etiquetado" model="quality.attribute.template">
            <field name="name">Etiquetado</field>
            <field name="process_type_id" ref="process_type_guillotina"/>
            <field name="attribute_type">boolean</field>
            <field name="sequence">30</field>
            <field name="is_required" eval="True"/>
        </record>

        <!-- ═══════════════ PEGADO ═══════════════ -->
        <record id="attr_pegado_aplicacion" model="quality.attribute.template">
            <field name="name">Aplicación de adhesivo</field>
            <field name="process_type_id" ref="process_type_pegado"/>
            <field name="attribute_type">boolean</field>
            <field name="sequence">10</field>
            <field name="is_required" eval="True"/>
        </record>
        <record id="attr_pegado_medidas" model="quality.attribute.template">
            <field name="name">Medidas correctas</field>
            <field name="process_type_id" ref="process_type_pegado"/>
            <field name="attribute_type">boolean</field>
            <field name="sequence">20</field>
            <field name="is_required" eval="True"/>
        </record>
        <record id="attr_pegado_amarre" model="quality.attribute.template">
            <field name="name">Amarre de paquetes</field>
            <field name="process_type_id" ref="process_type_pegado"/>
            <field name="attribute_type">boolean</field>
            <field name="sequence">30</field>
            <field name="is_required" eval="True"/>
        </record>
        <record id="attr_pegado_etiquetado" model="quality.attribute.template">
            <field name="name">Etiquetado</field>
            <field name="process_type_id" ref="process_type_pegado"/>
            <field name="attribute_type">boolean</field>
            <field name="sequence">40</field>
            <field name="is_required" eval="True"/>
        </record>

        <!-- ═══════════════ TROQUELADO ═══════════════ -->
        <record id="attr_troq_medidas" model="quality.attribute.template">
            <field name="name">Medidas correctas</field>
            <field name="process_type_id" ref="process_type_troquelado_plano"/>
            <field name="attribute_type">boolean</field>
            <field name="sequence">10</field>
            <field name="is_required" eval="True"/>
        </record>
        <record id="attr_troq_descuadre" model="quality.attribute.template">
            <field name="name">Sin descuadre</field>
            <field name="process_type_id" ref="process_type_troquelado_plano"/>
            <field name="attribute_type">boolean</field>
            <field name="sequence">20</field>
            <field name="is_required" eval="True"/>
        </record>
        <record id="attr_troq_pandeo" model="quality.attribute.template">
            <field name="name">Sin pandeo</field>
            <field name="process_type_id" ref="process_type_troquelado_plano"/>
            <field name="attribute_type">boolean</field>
            <field name="sequence">30</field>
            <field name="is_required" eval="True"/>
        </record>
        <record id="attr_troq_pegado" model="quality.attribute.template">
            <field name="name">Pegado correcto</field>
            <field name="process_type_id" ref="process_type_troquelado_plano"/>
            <field name="attribute_type">boolean</field>
            <field name="sequence">40</field>
            <field name="is_required" eval="True"/>
        </record>
        <record id="attr_troq_ranurado" model="quality.attribute.template">
            <field name="name">Ranurado</field>
            <field name="process_type_id" ref="process_type_troquelado_plano"/>
            <field name="attribute_type">boolean</field>
            <field name="sequence">50</field>
            <field name="is_required" eval="True"/>
        </record>
        <record id="attr_troq_troquelado" model="quality.attribute.template">
            <field name="name">Troquelado</field>
            <field name="process_type_id" ref="process_type_troquelado_plano"/>
            <field name="attribute_type">boolean</field>
            <field name="sequence">60</field>
            <field name="is_required" eval="True"/>
        </record>
        <record id="attr_troq_etiquetado" model="quality.attribute.template">
            <field name="name">Etiquetado</field>
            <field name="process_type_id" ref="process_type_troquelado_plano"/>
            <field name="attribute_type">boolean</field>
            <field name="sequence">70</field>
            <field name="is_required" eval="True"/>
        </record>
        <record id="attr_troq_emplayado" model="quality.attribute.template">
            <field name="name">Emplayado</field>
            <field name="process_type_id" ref="process_type_troquelado_plano"/>
            <field name="attribute_type">boolean</field>
            <field name="sequence">80</field>
            <field name="is_required" eval="True"/>
        </record>
        <record id="attr_troq_marcado" model="quality.attribute.template">
            <field name="name">Marcado correcto</field>
            <field name="process_type_id" ref="process_type_troquelado_plano"/>
            <field name="attribute_type">boolean</field>
            <field name="sequence">90</field>
            <field name="is_required" eval="True"/>
        </record>
        <record id="attr_troq_profundidad" model="quality.attribute.template">
            <field name="name">Profundidad</field>
            <field name="process_type_id" ref="process_type_troquelado_plano"/>
            <field name="attribute_type">boolean</field>
            <field name="sequence">100</field>
            <field name="is_required" eval="True"/>
        </record>

        <!-- ═══════════════ IMPRESIÓN ═══════════════ -->
        <record id="attr_imp_color" model="quality.attribute.template">
            <field name="name">Color/Tono</field>
            <field name="process_type_id" ref="process_type_impresion"/>
            <field name="attribute_type">boolean</field>
            <field name="sequence">10</field>
            <field name="is_required" eval="True"/>
        </record>
        <record id="attr_imp_registro" model="quality.attribute.template">
            <field name="name">Registro</field>
            <field name="process_type_id" ref="process_type_impresion"/>
            <field name="attribute_type">boolean</field>
            <field name="sequence">20</field>
            <field name="is_required" eval="True"/>
        </record>
        <record id="attr_imp_legibilidad" model="quality.attribute.template">
            <field name="name">Legibilidad</field>
            <field name="process_type_id" ref="process_type_impresion"/>
            <field name="attribute_type">boolean</field>
            <field name="sequence">30</field>
            <field name="is_required" eval="True"/>
        </record>
        <record id="attr_imp_uniformidad" model="quality.attribute.template">
            <field name="name">Uniformidad</field>
            <field name="process_type_id" ref="process_type_impresion"/>
            <field name="attribute_type">boolean</field>
            <field name="sequence">40</field>
            <field name="is_required" eval="True"/>
        </record>

        <!-- ═══════════════ ACABADO Y EMPAQUE ═══════════════ -->
        <record id="attr_aca_amarre" model="quality.attribute.template">
            <field name="name">Amarre de paquetes</field>
            <field name="process_type_id" ref="process_type_acabado"/>
            <field name="attribute_type">boolean</field>
            <field name="sequence">10</field>
            <field name="is_required" eval="True"/>
        </record>
        <record id="attr_aca_etiquetado" model="quality.attribute.template">
            <field name="name">Etiquetado</field>
            <field name="process_type_id" ref="process_type_acabado"/>
            <field name="attribute_type">boolean</field>
            <field name="sequence">20</field>
            <field name="is_required" eval="True"/>
        </record>
        <record id="attr_aca_emplayado" model="quality.attribute.template">
            <field name="name">Emplayado</field>
            <field name="process_type_id" ref="process_type_acabado"/>
            <field name="attribute_type">boolean</field>
            <field name="sequence">30</field>
            <field name="is_required" eval="True"/>
        </record>
        <record id="attr_aca_apariencia" model="quality.attribute.template">
            <field name="name">Apariencia general</field>
            <field name="process_type_id" ref="process_type_acabado"/>
            <field name="attribute_type">boolean</field>
            <field name="sequence">40</field>
            <field name="is_required" eval="True"/>
        </record>
        <record id="attr_aca_cantidad" model="quality.attribute.template">
            <field name="name">Cantidad por paquete</field>
            <field name="process_type_id" ref="process_type_acabado"/>
            <field name="attribute_type">boolean</field>
            <field name="sequence">50</field>
            <field name="is_required" eval="True"/>
        </record>

    </data>
</odoo>
"""


def fix_attribute_presets():
    step("[3] Atributos preconfigurados por proceso")
    created = write_file(
        "data/quality_attribute_preset_data.xml", ATTRIBUTE_PRESET_XML
    )
    # Agregarlo al manifest
    patch_file(
        "__manifest__.py",
        old='        "data/process_type_data.xml",\n        "data/cron_data.xml",',
        new='        "data/process_type_data.xml",\n        "data/quality_attribute_preset_data.xml",\n        "data/cron_data.xml",',
        marker_already="quality_attribute_preset_data.xml",
    )


# ─────────────────────────────────── FIX 4: Bloqueo troquelado_ids vacío ──
def fix_troquelado_required():
    step("[4] Bloqueo: troquelado_ids obligatorio si proceso es Troquelado")
    patch_file(
        "models/quality_inspection.py",
        old='''    def _check_measures_captured(self):
        """Bloqueo guardar si no se capturan Medidas y Propiedades (req. 5.1)."""
        for rec in self:
            checks = []
            if rec.show_largo and not rec.largo:
                checks.append("Largo")''',
        new='''    def _check_measures_captured(self):
        """Bloqueo guardar si no se capturan Medidas y Propiedades (req. 5.1)."""
        for rec in self:
            checks = []
            # Troquelado: obligatorio capturar al menos una línea (req. 5.7)
            if (rec.process_type_id.code == "troquelado_plano"
                    and not rec.troquelado_ids):
                raise UserError(_(
                    "Proceso Troquelado: debe capturar al menos una medida "
                    "en la pestaña Troquelado antes de liberar."
                ))
            # Sierras y Ranuradoras: obligatorio capturar al menos una línea
            if (rec.process_type_id.code == "sierras_ranuradoras"
                    and rec.show_ranurado and not rec.ranurado_ids):
                raise UserError(_(
                    "Proceso Sierras y Ranuradoras: capture al menos una "
                    "medida en la pestaña Ranurado antes de liberar."
                ))
            if rec.show_largo and not rec.largo:
                checks.append("Largo")''',
        marker_already='code == "troquelado_plano"',
    )


# ─────────────────────────────── FIX 5: Cliente auto-enlazado en Troquelado ──
def fix_partner_autolink():
    step("[5] Auto-enlazar cliente desde OP/Producto")
    patch_file(
        "models/quality_inspection.py",
        old='''    @api.onchange("process_type_id", "product_id")
    def _onchange_load_attribute_templates(self):''',
        new='''    @api.onchange("production_order_id")
    def _onchange_production_order(self):
        """Auto-enlazar cliente y producto desde la OP (req. 5.7)."""
        if self.production_order_id:
            mo = self.production_order_id
            if mo.product_id:
                self.product_id = mo.product_id
            # En MRP la OP no tiene partner directo, lo tomamos de la SO si existe
            origin_so = self.env["sale.order"].search([
                ("name", "=", mo.origin)], limit=1) if mo.origin else False
            if origin_so and origin_so.partner_id:
                self.partner_id = origin_so.partner_id

    @api.onchange("product_id")
    def _onchange_product_partner(self):
        """Si hay producto y aún no hay cliente, NO sobrescribir.
        Solo registrar que el cliente debe coincidir con la OP."""
        # Hook reservado para reglas adicionales por cliente.
        pass

    @api.onchange("process_type_id", "product_id")
    def _onchange_load_attribute_templates(self):''',
        marker_already="_onchange_production_order",
    )


# ──────────────────────────────────── FIX 6: show_alineacion en Octágono ──
def fix_octagono_alineacion():
    step("[6] Octágono — exponer campo Alineación")

    # 6.1 Agregar flag al modelo process_type
    patch_file(
        "models/quality_process_type.py",
        old="    show_engomado = fields.Boolean('Mostrar Engomado')",
        new="    show_engomado = fields.Boolean('Mostrar Engomado')\n    show_alineacion = fields.Boolean('Mostrar Alineación')",
        marker_already="show_alineacion",
    )

    # 6.2 Activarlo en el Octágono (data)
    patch_file(
        "data/process_type_data.xml",
        old='''            <field name="show_engomado" eval="True"/>
            <field name="show_corte_guillotina" eval="True"/>
            <field name="show_numero_corrida" eval="True"/>
        </record>

        <!-- 2. Guillotina -->''',
        new='''            <field name="show_engomado" eval="True"/>
            <field name="show_alineacion" eval="True"/>
            <field name="show_corte_guillotina" eval="True"/>
            <field name="show_numero_corrida" eval="True"/>
        </record>

        <!-- 2. Guillotina -->''',
        marker_already='show_alineacion" eval="True"/>\n            <field name="show_corte_guillotina"',
    )

    # 6.3 Related en quality_inspection
    patch_file(
        "models/quality_inspection.py",
        old='    show_engomado = fields.Boolean(related="process_type_id.show_engomado")',
        new='    show_engomado = fields.Boolean(related="process_type_id.show_engomado")\n    show_alineacion = fields.Boolean(related="process_type_id.show_alineacion")',
        marker_already='related="process_type_id.show_alineacion"',
    )

    # 6.4 Vista: hacer visible cuando aplique
    patch_file(
        "views/quality_inspection_views.xml",
        old='                    <field name="show_engomado" invisible="1"/>',
        new='                    <field name="show_engomado" invisible="1"/>\n                    <field name="show_alineacion" invisible="1"/>',
        marker_already='name="show_alineacion" invisible="1"',
    )

    # 6.5 oct_alineacion en pestaña Octágono
    patch_file(
        "views/quality_inspection_views.xml",
        old='''                                <group>
                                    <field name="oct_ancho"/>
                                    <field name="oct_alineacion" widget="radio"/>
                                    <field name="oct_pegado" widget="radio"/>
                                </group>''',
        new='''                                <group>
                                    <field name="oct_ancho"/>
                                    <field name="oct_alineacion" widget="radio"
                                           invisible="not show_alineacion"/>
                                    <field name="oct_pegado" widget="radio"/>
                                </group>''',
        marker_already='invisible="not show_alineacion"',
    )


# ───────────────────────────────── FIX 7: Wizard certificado — dedupe ──
def fix_certificate_wizard_dedupe():
    step("[7] Wizard certificado — dedupe automático de atributos")
    patch_file(
        "wizards/certificate_wizard.py",
        old='''        # Vincular atributos adicionales si se solicitó
        if self.include_all_attributes and insp.line_ids:
            cert.attribute_ids = [(6, 0, insp.line_ids.ids)]''',
        new='''        # Vincular atributos adicionales si se solicitó (con dedupe por nombre)
        if self.include_all_attributes and insp.line_ids:
            seen = set()
            unique_ids = []
            for line in insp.line_ids:
                key = (line.name or "").strip().lower()
                if key and key not in seen:
                    seen.add(key)
                    unique_ids.append(line.id)
            cert.attribute_ids = [(6, 0, unique_ids)]''',
        marker_already="seen = set()",
    )


# ──────────────────────────────── FIX 8: Help text en Folio y Código ──
def fix_folio_help():
    step("[8] Help text en Folio y Código")
    patch_file(
        "models/quality_inspection.py",
        old='    folio = fields.Char("Folio de Producción", required=True)\n    code = fields.Char("Código de Producto", required=True)',
        new='''    folio = fields.Char(
        "Folio de Producción", required=True,
        help="Formato: letras y/o números (ej. F-2026-001). "
             "Capture exactamente el folio impreso en el lote.")
    code = fields.Char(
        "Código de Producto", required=True,
        help="Código interno del producto (alfanumérico, sin espacios).")''',
        marker_already="Capture exactamente el folio",
    )


# ─────────────────────────────────────────────────────────────── main ──
def main():
    if not (MODULE_DIR / "__manifest__.py").exists():
        fail(
            "No se encontró __manifest__.py en este directorio.\n"
            f"   Coloca este script en la raíz de tu módulo "
            f"(actualmente está en: {MODULE_DIR})"
        )
        sys.exit(1)

    banner("APLICANDO CORRECCIONES CRÍTICAS — quality_management")
    print(f"Directorio: {MODULE_DIR}")

    backup()

    fix_8d_disciplines()
    fix_value_cumple_na()
    fix_attribute_presets()
    fix_troquelado_required()
    fix_partner_autolink()
    fix_octagono_alineacion()
    fix_certificate_wizard_dedupe()
    fix_folio_help()

    banner("LISTO")
    print(
        "\nSiguientes pasos:\n"
        "  1. Reinicia Odoo:        docker compose restart odoo\n"
        "  2. Actualiza el módulo:  -u quality_management\n"
        "     (o desde la UI: Apps → quality_management → Actualizar)\n"
        "  3. Verifica que los nuevos atributos aparezcan en Configuración →\n"
        "     Plantillas de Atributos (filtrando por proceso).\n\n"
        "Si algo sale mal, restaura el backup creado al inicio."
    )


if __name__ == "__main__":
    main()