#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
apply_hexagonos_quality_views.py
================================
Segunda parte: reescribe las vistas XML del módulo quality_management para
exponer todos los campos nuevos agregados por apply_hexagonos_quality_changes.py.

USO:
    python3 apply_hexagonos_quality_views.py /ruta/a/quality_management
"""

import shutil
import sys
from datetime import datetime
from pathlib import Path


def fatal(msg):
    print(f"❌ {msg}", file=sys.stderr)
    sys.exit(1)


def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  ✏  {path.relative_to(MODULE)}")


if len(sys.argv) < 2:
    fatal("Uso: python3 apply_hexagonos_quality_views.py /ruta/a/quality_management")

MODULE = Path(sys.argv[1]).resolve()
if not MODULE.exists() or not (MODULE / "__manifest__.py").exists():
    fatal(f"Módulo no encontrado en {MODULE}")

BACKUP = MODULE.parent / f"{MODULE.name}_views_backup_{datetime.now():%Y%m%d_%H%M%S}"
print(f"📦 Backup vistas: {BACKUP}")
(BACKUP / "views").mkdir(parents=True, exist_ok=True)
for f in (MODULE / "views").glob("*.xml"):
    shutil.copy2(f, BACKUP / "views" / f.name)
print(f"🔧 Reescribiendo vistas en {MODULE}\n")


# =============================================================================
# 1. Liberación de Muestras
# =============================================================================
write(MODULE / "views" / "quality_sample_release_views.xml", '''<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_quality_sample_release_list" model="ir.ui.view">
        <field name="name">quality.sample.release.list</field>
        <field name="model">quality.sample.release</field>
        <field name="arch" type="xml">
            <list decoration-success="state == 'aceptado'"
                  decoration-danger="state == 'rechazado'"
                  decoration-info="state == 'en_inspeccion'">
                <field name="name"/>
                <field name="sample_type"/>
                <field name="product_id"/>
                <field name="project_task_id"/>
                <field name="requested_by"/>
                <field name="inspector_id"/>
                <field name="date_requested"/>
                <field name="date_limit"/>
                <field name="state" widget="badge"
                       decoration-success="state == 'aceptado'"
                       decoration-danger="state == 'rechazado'"
                       decoration-info="state == 'en_inspeccion'"/>
            </list>
        </field>
    </record>

    <record id="view_quality_sample_release_form" model="ir.ui.view">
        <field name="name">quality.sample.release.form</field>
        <field name="model">quality.sample.release</field>
        <field name="arch" type="xml">
            <form string="Liberación de Muestra">
                <header>
                    <button name="action_register_cnc"
                            string="Registrar Transformación CNC"
                            type="object" class="btn-secondary"
                            invisible="sample_type != 'pt' or state != 'borrador' or cnc_date_realized"/>
                    <button name="action_submit_inspection"
                            string="Enviar a Inspección" type="object"
                            class="btn-primary"
                            invisible="state != 'borrador'"/>
                    <button name="action_accept" string="Liberar (Aceptado)"
                            type="object" class="btn-primary"
                            invisible="state != 'en_inspeccion'"
                            groups="quality_management.group_quality_inspector"/>
                    <button name="action_reject" string="Rechazar"
                            type="object" class="btn-danger"
                            invisible="state != 'en_inspeccion'"
                            groups="quality_management.group_quality_inspector"/>
                    <button name="action_print_sample_release" string="Imprimir"
                            type="object" class="btn-secondary" icon="fa-print"/>
                    <button name="action_reset_draft" string="Regresar a Borrador"
                            type="object"
                            invisible="state not in ('rechazado',)"
                            groups="quality_management.group_quality_manager"/>
                    <field name="state" widget="statusbar"
                           statusbar_visible="borrador,en_inspeccion,aceptado"/>
                </header>
                <sheet>
                    <div class="oe_title">
                        <h1><field name="name" readonly="1"/></h1>
                    </div>
                    <group>
                        <group string="Tipo y Datos">
                            <field name="sample_type" widget="radio"/>
                            <field name="project_task_id"/>
                            <field name="product_id"/>
                            <field name="requested_by"/>
                            <field name="inspector_id"/>
                        </group>
                        <group string="Fechas (automáticas)">
                            <field name="date_requested" readonly="1"/>
                            <field name="date_limit" readonly="1"/>
                            <field name="date_inspected" readonly="1"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Especificación PDF" name="spec">
                            <div class="alert alert-warning" role="alert"
                                 invisible="spec_pdf">
                                <i class="fa fa-exclamation-triangle"/>
                                La especificación PDF es <b>obligatoria</b>. Sin plano o dibujo no se puede inspeccionar.
                            </div>
                            <group>
                                <field name="spec_pdf" filename="spec_pdf_name"/>
                                <field name="spec_pdf_name" invisible="1"/>
                            </group>
                            <div invisible="not spec_pdf" class="o_quality_pdf_preview">
                                <field name="spec_pdf" widget="pdf_viewer" readonly="1"/>
                            </div>
                        </page>
                        <page string="Atributos de Inspección" name="attrs">
                            <field name="inspection_line_ids">
                                <list editable="bottom">
                                    <field name="sequence" widget="handle"/>
                                    <field name="name"/>
                                    <field name="attribute_type"/>
                                    <field name="value_float" invisible="attribute_type != 'float'"/>
                                    <field name="value_char" invisible="attribute_type not in ('char', 'selection')"/>
                                    <field name="value_cumple" invisible="attribute_type != 'boolean'"/>
                                    <field name="min_value" invisible="attribute_type != 'float'"/>
                                    <field name="max_value" invisible="attribute_type != 'float'"/>
                                    <field name="unit" placeholder="mm, cm, in, %..."/>
                                    <field name="result" widget="badge"
                                           decoration-success="result == 'cumple'"
                                           decoration-danger="result == 'no_cumple'"/>
                                </list>
                            </field>
                        </page>
                        <page string="Evidencia (Imágenes)" name="evidence">
                            <field name="evidence_ids" widget="many2many_binary"/>
                            <separator string="Vista Previa"/>
                            <field name="evidence_ids" widget="evidence_viewer" nolabel="1"/>
                        </page>
                        <page string="Transformación CNC"
                              invisible="sample_type != 'pt'" name="cnc">
                            <group>
                                <group>
                                    <field name="cnc_design_user_id" readonly="1"/>
                                    <field name="cnc_date_realized" readonly="1"/>
                                </group>
                            </group>
                            <field name="cnc_observations"
                                   placeholder="Observaciones de la transformación..."/>
                        </page>
                        <page string="Observaciones" name="notes">
                            <field name="notes"/>
                        </page>
                    </notebook>
                </sheet>
                <chatter/>
            </form>
        </field>
    </record>

    <record id="action_quality_sample_release" model="ir.actions.act_window">
        <field name="name">Liberación de Muestras</field>
        <field name="res_model">quality.sample.release</field>
        <field name="view_mode">list,form</field>
    </record>
</odoo>
''')

# =============================================================================
# 2. Liberación de Planos
# =============================================================================
write(MODULE / "views" / "quality_drawing_release_views.xml", '''<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_quality_drawing_release_list" model="ir.ui.view">
        <field name="name">quality.drawing.release.list</field>
        <field name="model">quality.drawing.release</field>
        <field name="arch" type="xml">
            <list decoration-success="state == 'aceptado_diseno'"
                  decoration-danger="state in ('rechazado','cerrada')"
                  decoration-info="state == 'en_revision'">
                <field name="name"/>
                <field name="partner_id"/>
                <field name="request_type"/>
                <field name="modification_count"/>
                <field name="sale_order_id" optional="show"/>
                <field name="requested_by"/>
                <field name="date_requested"/>
                <field name="date_release_expected" optional="show"/>
                <field name="state" widget="badge"/>
            </list>
        </field>
    </record>

    <record id="view_quality_drawing_release_form" model="ir.ui.view">
        <field name="name">quality.drawing.release.form</field>
        <field name="model">quality.drawing.release</field>
        <field name="arch" type="xml">
            <form string="Liberación de Plano">
                <header>
                    <button name="action_submit_review"
                            string="Enviar a Revisión Calidad"
                            type="object" class="btn-primary"
                            invisible="state not in ('borrador','rechazado')"/>
                    <button name="action_quality_accept"
                            string="✓ Calidad: Aceptar" type="object"
                            class="btn-primary"
                            invisible="state != 'en_revision'"
                            groups="quality_management.group_quality_inspector"/>
                    <button name="action_sales_accept"
                            string="✓ Ventas: Aceptar" type="object"
                            class="btn-primary"
                            invisible="state != 'aceptado_calidad'"
                            groups="sales_team.group_sale_salesman"/>
                    <button name="action_design_accept"
                            string="✓ Diseño: Aceptar (Final)" type="object"
                            class="btn-primary"
                            invisible="state != 'aceptado_ventas'"/>
                    <button name="action_reject" string="Rechazar"
                            type="object" class="btn-danger"
                            invisible="state != 'en_revision'"
                            groups="quality_management.group_quality_inspector"/>
                    <button name="action_print_drawing_release" string="Imprimir"
                            type="object" class="btn-secondary" icon="fa-print"/>
                    <button name="action_reset_draft" string="Regresar a Borrador"
                            type="object"
                            invisible="state != 'rechazado'"
                            groups="quality_management.group_quality_manager"/>
                    <field name="state" widget="statusbar"
                           statusbar_visible="borrador,en_revision,aceptado_calidad,aceptado_ventas,aceptado_diseno"/>
                </header>
                <sheet>
                    <div class="oe_title">
                        <h1><field name="name" readonly="1"/></h1>
                    </div>
                    <div class="alert alert-info" role="alert"
                         invisible="modification_count == 0">
                        <i class="fa fa-info-circle"/>
                        Modificación en curso: <b><field name="modification_count" nolabel="1" readonly="1"/> de 3</b>.
                        Si se excede el máximo, la liberación se cierra y debe iniciarse un nuevo ciclo.
                    </div>
                    <div class="alert alert-danger" role="alert"
                         invisible="state != 'cerrada'">
                        <i class="fa fa-ban"/>
                        <b>Liberación cerrada</b>: se excedió el máximo de 3 modificaciones.
                        Inicie un nuevo proceso de Alta/Actualización (continúe el consecutivo: 4, 5, 6...).
                    </div>
                    <group>
                        <group string="Cliente y Solicitud">
                            <field name="partner_id"/>
                            <field name="sale_order_id"/>
                            <field name="requested_by"/>
                            <field name="request_type" widget="radio"/>
                            <field name="drawing_path"
                                   placeholder="Ej. C:\\Users\\Calidad\\Nextcloud\\..."/>
                        </group>
                        <group string="Fechas (automáticas)">
                            <field name="date_requested" readonly="1"/>
                            <field name="date_release_expected" readonly="1"/>
                            <field name="date_released" readonly="1"/>
                            <field name="modification_count" readonly="1"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Requisitos de Fabricación" name="reqs">
                            <p class="text-muted">
                                <i class="fa fa-info-circle"/>
                                Captura de Ventas previa al envío a Calidad.
                            </p>
                            <group>
                                <group string="Sellos">
                                    <field name="req_sellos"/>
                                    <field name="req_sellos_date"
                                           invisible="not req_sellos"/>
                                </group>
                                <group string="Plantilla">
                                    <field name="req_plantilla"/>
                                    <field name="req_plantilla_date"
                                           invisible="not req_plantilla"/>
                                </group>
                                <group string="Troquel">
                                    <field name="req_troquel"/>
                                    <field name="req_troquel_date"
                                           invisible="not req_troquel"/>
                                </group>
                                <group string="Otro">
                                    <field name="req_otro"/>
                                    <field name="req_otro_desc"
                                           invisible="not req_otro"/>
                                    <field name="req_otro_date"
                                           invisible="not req_otro"/>
                                </group>
                            </group>
                        </page>
                        <page string="Plano (PDF)" name="drawing">
                            <div class="alert alert-warning" invisible="drawing_pdf">
                                <i class="fa fa-exclamation-triangle"/>
                                Sin plano cargado no se puede avanzar.
                            </div>
                            <group>
                                <field name="drawing_pdf" filename="drawing_pdf_name"/>
                                <field name="drawing_pdf_name" invisible="1"/>
                            </group>
                            <div invisible="not drawing_pdf" class="o_quality_pdf_preview">
                                <field name="drawing_pdf" widget="pdf_viewer" readonly="1"/>
                            </div>
                        </page>
                        <page string="Cotización/Dibujo (PDF)" name="quotation">
                            <div class="alert alert-warning" invisible="quotation_pdf">
                                <i class="fa fa-exclamation-triangle"/>
                                Sin cotización/dibujo cargado no se puede avanzar.
                            </div>
                            <group>
                                <field name="quotation_pdf" filename="quotation_pdf_name"/>
                                <field name="quotation_pdf_name" invisible="1"/>
                            </group>
                            <div invisible="not quotation_pdf" class="o_quality_pdf_preview">
                                <field name="quotation_pdf" widget="pdf_viewer" readonly="1"/>
                            </div>
                        </page>
                        <page string="Adjuntos Adicionales" name="attachs">
                            <field name="drawing_attachment_ids" widget="many2many_binary"/>
                        </page>
                        <page string="Modificaciones" name="mods">
                            <field name="modification_ids" readonly="1">
                                <list>
                                    <field name="sequence"/>
                                    <field name="date"/>
                                    <field name="requested_by"/>
                                    <field name="description"/>
                                </list>
                            </field>
                        </page>
                        <page string="Triple Check" name="triple">
                            <group>
                                <group string="Calidad">
                                    <field name="accepted_by_quality" readonly="1"/>
                                    <field name="accepted_by_quality_date" readonly="1"/>
                                </group>
                                <group string="Ventas">
                                    <field name="accepted_by_sales" readonly="1"/>
                                    <field name="accepted_by_sales_date" readonly="1"/>
                                </group>
                                <group string="Diseño">
                                    <field name="accepted_by_design" readonly="1"/>
                                    <field name="accepted_by_design_date" readonly="1"/>
                                </group>
                            </group>
                        </page>
                        <page string="Rechazo" invisible="state != 'rechazado'" name="reject">
                            <field name="rejection_reason"
                                   placeholder="Motivo de rechazo..."/>
                        </page>
                    </notebook>
                </sheet>
                <chatter/>
            </form>
        </field>
    </record>

    <record id="action_quality_drawing_release" model="ir.actions.act_window">
        <field name="name">Liberación de Planos</field>
        <field name="res_model">quality.drawing.release</field>
        <field name="view_mode">list,form</field>
    </record>
</odoo>
''')

# =============================================================================
# 3. Inspección
# =============================================================================
write(MODULE / "views" / "quality_inspection_views.xml", '''<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_quality_inspection_list" model="ir.ui.view">
        <field name="name">quality.inspection.list</field>
        <field name="model">quality.inspection</field>
        <field name="arch" type="xml">
            <list decoration-success="state == 'aceptado'"
                  decoration-danger="state in ('rechazado','retenido')"
                  decoration-info="state == 'en_proceso'">
                <field name="name"/>
                <field name="process_type_id"/>
                <field name="pp_pt"/>
                <field name="product_id"/>
                <field name="lot_id"/>
                <field name="partner_id"/>
                <field name="folio"/>
                <field name="shift"/>
                <field name="inspector_id" widget="many2one_avatar_user"/>
                <field name="date_inspection"/>
                <field name="state" widget="badge"
                       decoration-success="state == 'aceptado'"
                       decoration-danger="state in ('rechazado','retenido')"
                       decoration-info="state == 'en_proceso'"/>
            </list>
        </field>
    </record>

    <record id="view_quality_inspection_form" model="ir.ui.view">
        <field name="name">quality.inspection.form</field>
        <field name="model">quality.inspection</field>
        <field name="arch" type="xml">
            <form string="Inspección de Calidad">
                <header>
                    <button name="action_start" string="INICIAR INSPECCIÓN"
                            type="object" class="btn-primary"
                            invisible="state != 'borrador'"/>
                    <button name="action_accept" string="Aceptar (Liberar)"
                            type="object" class="btn-primary"
                            invisible="state != 'en_proceso'"
                            groups="quality_management.group_quality_inspector"/>
                    <button name="action_retain" string="Retener"
                            type="object" class="btn-warning"
                            invisible="state != 'en_proceso'"
                            groups="quality_management.group_quality_inspector"/>
                    <button name="action_reject" string="Rechazar"
                            type="object" class="btn-danger"
                            invisible="state != 'en_proceso'"
                            groups="quality_management.group_quality_inspector"/>
                    <button name="action_create_certificate" string="Crear Certificado"
                            type="object" class="btn-secondary"
                            invisible="state != 'aceptado'"
                            groups="quality_management.group_quality_manager"/>
                    <button name="action_print_inspection" string="Imprimir"
                            type="object" class="btn-secondary" icon="fa-print"/>
                    <button name="action_reset_draft" string="Regresar a Borrador"
                            type="object"
                            invisible="state not in ('rechazado','retenido')"
                            groups="quality_management.group_quality_manager"/>
                    <field name="state" widget="statusbar"
                           statusbar_visible="borrador,en_proceso,aceptado"/>
                </header>
                <sheet>
                    <div class="oe_button_box" name="button_box">
                        <button name="action_view_certificates" type="object"
                                class="oe_stat_button" icon="fa-certificate"
                                invisible="certificate_count == 0">
                            <field name="certificate_count" widget="statinfo"
                                   string="Certificados"/>
                        </button>
                    </div>
                    <div class="oe_title">
                        <h1><field name="name" readonly="1"/></h1>
                    </div>
                    <div class="alert alert-info" role="alert"
                         invisible="state != 'borrador'">
                        <i class="fa fa-info-circle"/>
                        <b>Captura bloqueada hasta presionar "INICIAR INSPECCIÓN".</b>
                    </div>
                    <field name="show_largo" invisible="1"/>
                    <field name="show_ancho" invisible="1"/>
                    <field name="show_espesor" invisible="1"/>
                    <field name="show_hexagono" invisible="1"/>
                    <field name="show_resistencia" invisible="1"/>
                    <field name="show_apariencia" invisible="1"/>
                    <field name="show_humedad" invisible="1"/>
                    <field name="show_pegado" invisible="1"/>
                    <field name="show_retiramiento" invisible="1"/>
                    <field name="show_calibracion" invisible="1"/>
                    <field name="show_engomado" invisible="1"/>
                    <field name="show_ranurado" invisible="1"/>
                    <field name="show_troquelado" invisible="1"/>
                    <field name="show_papel" invisible="1"/>
                    <field name="show_adhesivo" invisible="1"/>
                    <field name="show_tipo_hexagono" invisible="1"/>
                    <field name="show_corte_guillotina" invisible="1"/>
                    <field name="show_numero_corrida" invisible="1"/>
                    <field name="is_pp" invisible="1"/>
                    <field name="is_pt" invisible="1"/>

                    <group>
                        <group string="Datos Generales">
                            <field name="process_type_id"/>
                            <field name="pp_pt" widget="radio"
                                   readonly="state != 'borrador'"/>
                            <field name="product_id"
                                   options="{'no_create': True, 'no_create_edit': True, 'no_quick_create': True}"/>
                            <field name="production_order_id"
                                   options="{'no_create': True, 'no_create_edit': True, 'no_quick_create': True}"/>
                            <field name="lot_id"
                                   options="{'no_create': True, 'no_create_edit': True, 'no_quick_create': True}"
                                   domain="[('product_id', '=', product_id)]"/>
                            <field name="folio"/>
                            <field name="code"/>
                        </group>
                        <group string="Personal y Ubicación">
                            <field name="operator_id"
                                   options="{'no_create': True, 'no_create_edit': True}"/>
                            <field name="supervisor_id"
                                   options="{'no_create': True, 'no_create_edit': True}"/>
                            <field name="inspector_id"
                                   widget="many2one_avatar_user" readonly="1"/>
                            <field name="partner_id"
                                   context="{'show_vat': True, 'show_email': True}"
                                   options="{'no_create': True, 'no_create_edit': True}"/>
                            <field name="shift"/>
                            <field name="plant"/>
                            <field name="date_inspection" readonly="1"/>
                        </group>
                    </group>

                    <notebook>
                        <page string="Medidas y Propiedades"
                              invisible="state == 'borrador' or (not show_largo and not show_ancho and not show_espesor and not show_hexagono and not show_resistencia and not show_apariencia and not show_humedad and not show_pegado and not show_retiramiento and not show_calibracion and not show_engomado)"
                              name="medidas">
                            <group>
                                <group string="Medidas Dimensionales">
                                    <field name="largo" invisible="not show_largo"/>
                                    <field name="ancho" invisible="not show_ancho"/>
                                    <label for="espesor" string="Espesor"
                                           invisible="not show_espesor"/>
                                    <div class="o_row" invisible="not show_espesor">
                                        <field name="espesor"/>
                                        <field name="espesor_unit" nolabel="1"
                                               class="oe_inline"/>
                                    </div>
                                    <field name="hexagono" invisible="not show_hexagono"/>
                                </group>
                                <group string="Propiedades">
                                    <label for="resistencia"
                                           string="Resistencia (Lbf)"
                                           invisible="not show_resistencia"/>
                                    <div class="o_row" invisible="not show_resistencia">
                                        <field name="resistencia"
                                               readonly="resistencia_na"
                                               invisible="resistencia_na"/>
                                        <field name="resistencia_na"
                                               nolabel="1" class="oe_inline"/>
                                        <span class="ms-2 oe_inline"
                                              invisible="not resistencia_na">
                                            No Aplica
                                        </span>
                                        <label for="resistencia_na"
                                               string="No Aplica"
                                               class="ms-2 oe_inline"
                                               invisible="resistencia_na"/>
                                    </div>
                                    <field name="apariencia"
                                           invisible="not show_apariencia"
                                           widget="radio"/>
                                    <field name="humedad_pct"
                                           invisible="not show_humedad"/>
                                    <field name="pegado_result"
                                           invisible="not show_pegado"/>
                                    <field name="oct_retiramiento"
                                           invisible="not show_retiramiento"/>
                                    <field name="calibracion"
                                           invisible="not show_calibracion"/>
                                    <field name="engomado"
                                           invisible="not show_engomado"/>
                                </group>
                            </group>
                        </page>

                        <page string="Octágono (Extras)"
                              invisible="process_type_id and process_type_id.code != 'octagono'"
                              name="oct">
                            <group>
                                <group>
                                    <field name="oct_ancho"/>
                                    <field name="oct_alineacion" widget="radio"/>
                                    <field name="oct_pegado" widget="radio"/>
                                </group>
                            </group>
                        </page>

                        <page string="Guillotina (Extras)"
                              invisible="process_type_id and process_type_id.code != 'guillotina'"
                              name="guillot">
                            <group>
                                <group string="Retícula">
                                    <field name="reticula_extendida"/>
                                    <field name="reticula_vueltas"/>
                                    <field name="lote_reticula"/>
                                    <field name="gramaje_reticula"/>
                                </group>
                                <group string="Supervisión">
                                    <field name="sin_supervisor"/>
                                </group>
                            </group>
                        </page>

                        <page string="Ranurado"
                              invisible="not show_ranurado or state == 'borrador'"
                              name="ranurado">
                            <group>
                                <field name="ranurado_unit"
                                       string="Unidad predeterminada"/>
                            </group>
                            <field name="ranurado_ids"
                                   context="{'default_unidad': ranurado_unit}">
                                <list editable="bottom">
                                    <field name="sequence"/>
                                    <field name="medida"/>
                                    <field name="unidad"/>
                                    <field name="resultado" widget="badge"
                                           decoration-success="resultado == 'cumple'"
                                           decoration-danger="resultado == 'no_cumple'"/>
                                    <field name="notas"/>
                                </list>
                            </field>
                        </page>

                        <page string="Troquelado"
                              invisible="not show_troquelado or state == 'borrador'"
                              name="troquelado">
                            <field name="troquelado_ids">
                                <list editable="bottom">
                                    <field name="sequence"/>
                                    <field name="medida"/>
                                    <field name="resultado" widget="badge"
                                           decoration-success="resultado == 'cumple'"
                                           decoration-danger="resultado == 'no_cumple'"/>
                                    <field name="notas"/>
                                </list>
                            </field>
                        </page>

                        <page string="Datos de Producción"
                              invisible="state == 'borrador' or (not show_papel and not show_adhesivo and not show_tipo_hexagono and not show_numero_corrida and not show_corte_guillotina)"
                              name="prod">
                            <group>
                                <group string="Producción"
                                       invisible="not show_numero_corrida and not show_tipo_hexagono and not show_corte_guillotina">
                                    <field name="numero_corrida"
                                           invisible="not show_numero_corrida"/>
                                    <field name="tipo_hexagono"
                                           invisible="not show_tipo_hexagono"/>
                                    <field name="corte_guillotina"
                                           invisible="not show_corte_guillotina"
                                           widget="radio"/>
                                </group>
                                <group string="Papel" invisible="not show_papel">
                                    <field name="papel_ancho"/>
                                    <field name="papel_gramaje"/>
                                    <field name="papel_proveedor_id"
                                           options="{'no_create': True, 'no_create_edit': True}"/>
                                </group>
                            </group>
                            <group invisible="not show_adhesivo">
                                <group string="Adhesivo">
                                    <field name="adhesivo_lote1"/>
                                    <field name="adhesivo_lote2"/>
                                </group>
                            </group>
                        </page>

                        <page string="Atributos Adicionales"
                              invisible="state == 'borrador'" name="attrs">
                            <p class="text-muted">
                                <i class="fa fa-info-circle"/>
                                CUMPLE / NO CUMPLE / N/A — sin duplicados con
                                Medidas y Propiedades.
                            </p>
                            <field name="line_ids">
                                <list editable="bottom">
                                    <field name="sequence" widget="handle"/>
                                    <field name="name"/>
                                    <field name="attribute_type"/>
                                    <field name="value_float"
                                           invisible="attribute_type != 'float'"/>
                                    <field name="value_char"
                                           invisible="attribute_type not in ('char','selection')"/>
                                    <field name="value_cumple"
                                           string="Cumple/NC/N/A"
                                           invisible="attribute_type != 'boolean'"
                                           widget="badge"
                                           decoration-success="value_cumple == 'cumple'"
                                           decoration-danger="value_cumple == 'no_cumple'"/>
                                    <field name="min_value"
                                           invisible="attribute_type != 'float'"/>
                                    <field name="max_value"
                                           invisible="attribute_type != 'float'"/>
                                    <field name="unit"/>
                                    <field name="result" widget="badge"
                                           decoration-success="result == 'cumple'"
                                           decoration-danger="result == 'no_cumple'"/>
                                    <field name="notes"/>
                                </list>
                            </field>
                        </page>

                        <page string="Evidencia (Imágenes)" name="evimg"
                              invisible="state == 'borrador'">
                            <p class="text-muted">
                                <i class="fa fa-info-circle"/>
                                Hasta 10 imágenes.
                            </p>
                            <field name="evidence_image_ids" widget="many2many_binary"/>
                            <separator string="Vista Previa"/>
                            <field name="evidence_image_ids"
                                   widget="evidence_viewer" nolabel="1"/>
                        </page>

                        <page string="Evidencia PDF" name="evpdf"
                              invisible="state == 'borrador'">
                            <group>
                                <field name="evidence_pdf"
                                       filename="evidence_pdf_name"/>
                                <field name="evidence_pdf_name" invisible="1"/>
                            </group>
                            <div invisible="not evidence_pdf"
                                 class="o_quality_pdf_preview">
                                <field name="evidence_pdf" widget="pdf_viewer" readonly="1"/>
                            </div>
                        </page>

                        <page string="Observaciones" name="notes">
                            <field name="notes"/>
                        </page>
                    </notebook>
                </sheet>
                <chatter/>
            </form>
        </field>
    </record>

    <record id="view_quality_inspection_search" model="ir.ui.view">
        <field name="name">quality.inspection.search</field>
        <field name="model">quality.inspection</field>
        <field name="arch" type="xml">
            <search string="Inspecciones">
                <field name="name"/>
                <field name="product_id"/>
                <field name="lot_id"/>
                <field name="partner_id"/>
                <field name="folio"/>
                <field name="inspector_id"/>
                <field name="process_type_id"/>
                <filter string="Hoy" name="today"
                        domain="[('date_inspection','&gt;=', datetime.datetime.combine(context_today(), datetime.time(0,0,0))),
                                 ('date_inspection','&lt;=', datetime.datetime.combine(context_today(), datetime.time(23,59,59)))]"/>
                <separator/>
                <filter string="PP" name="pp" domain="[('pp_pt','=','pp')]"/>
                <filter string="PT" name="pt" domain="[('pp_pt','=','pt')]"/>
                <separator/>
                <filter string="Aceptadas" name="accepted" domain="[('state','=','aceptado')]"/>
                <filter string="Retenidas" name="retained" domain="[('state','=','retenido')]"/>
                <filter string="Rechazadas" name="rejected" domain="[('state','=','rechazado')]"/>
                <group expand="0" string="Agrupar por">
                    <filter string="Tipo de Proceso" name="group_type"
                            context="{'group_by': 'process_type_id'}"/>
                    <filter string="PP/PT" name="group_pppt"
                            context="{'group_by': 'pp_pt'}"/>
                    <filter string="Turno" name="group_shift"
                            context="{'group_by': 'shift'}"/>
                    <filter string="Planta" name="group_plant"
                            context="{'group_by': 'plant'}"/>
                    <filter string="Inspector" name="group_inspector"
                            context="{'group_by': 'inspector_id'}"/>
                    <filter string="Estado" name="group_state"
                            context="{'group_by': 'state'}"/>
                </group>
            </search>
        </field>
    </record>

    <record id="view_quality_inspection_pivot" model="ir.ui.view">
        <field name="name">quality.inspection.pivot</field>
        <field name="model">quality.inspection</field>
        <field name="arch" type="xml">
            <pivot string="Análisis de Inspecciones">
                <field name="process_type_id" type="row"/>
                <field name="state" type="col"/>
            </pivot>
        </field>
    </record>

    <record id="action_quality_inspection" model="ir.actions.act_window">
        <field name="name">Inspecciones</field>
        <field name="res_model">quality.inspection</field>
        <field name="view_mode">list,form,pivot</field>
        <field name="context">{'search_default_today': 1}</field>
    </record>
</odoo>
''')

# =============================================================================
# 4. Acciones Correctivas / 8D
# =============================================================================
write(MODULE / "views" / "quality_corrective_action_views.xml", '''<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_quality_corrective_action_tree" model="ir.ui.view">
        <field name="name">quality.corrective.action.tree</field>
        <field name="model">quality.corrective.action</field>
        <field name="arch" type="xml">
            <list decoration-success="state == 'cerrada'"
                  decoration-danger="action_overdue_count > 0"
                  decoration-muted="state == 'no_procede'">
                <field name="name"/>
                <field name="origin_type"/>
                <field name="defect_type" optional="show"/>
                <field name="responsible_id"/>
                <field name="date_opened"/>
                <field name="date_closed" optional="show"/>
                <field name="action_count"/>
                <field name="action_completed_count"/>
                <field name="action_overdue_count"
                       decoration-danger="action_overdue_count > 0"/>
                <field name="progress" widget="progressbar"/>
                <field name="state" widget="badge"/>
            </list>
        </field>
    </record>

    <record id="view_quality_action_line_form" model="ir.ui.view">
        <field name="name">quality.action.line.form</field>
        <field name="model">quality.action.line</field>
        <field name="arch" type="xml">
            <form string="Detalle de Acción">
                <group>
                    <group>
                        <field name="description"/>
                        <field name="responsible_id"/>
                        <field name="state" widget="badge"/>
                    </group>
                    <group>
                        <field name="date_due"/>
                        <field name="date_completed"/>
                        <field name="delay_days"/>
                    </group>
                </group>
                <group string="Adjuntar Evidencia">
                    <field name="evidence_ids" widget="many2many_binary" nolabel="1"/>
                </group>
                <separator string="Vista Previa de Evidencia"/>
                <field name="evidence_ids" widget="evidence_viewer" nolabel="1"/>
                <group>
                    <field name="notes"/>
                </group>
            </form>
        </field>
    </record>

    <record id="view_quality_corrective_action_form" model="ir.ui.view">
        <field name="name">quality.corrective.action.form</field>
        <field name="model">quality.corrective.action</field>
        <field name="arch" type="xml">
            <form string="Acción Correctiva / 8D">
                <header>
                    <button name="action_evaluate_quality"
                            string="Enviar a Evaluación Calidad"
                            type="object" class="btn-primary"
                            invisible="state != 'borrador'"/>
                    <button name="action_quality_evaluated"
                            string="Calidad Evaluó - Continuar a 8D"
                            type="object" class="btn-primary"
                            invisible="state != 'evaluacion_calidad'"
                            groups="quality_management.group_quality_manager"/>
                    <button name="action_in_progress" string="En Proceso"
                            type="object"
                            invisible="state != 'abierta'"/>
                    <button name="action_close" string="Cerrar"
                            type="object" class="btn-primary"
                            invisible="state not in ('abierta','en_proceso')"
                            groups="quality_management.group_quality_manager"/>
                    <button name="action_no_proceed" string="No Procede"
                            type="object" class="btn-secondary"
                            invisible="state in ('cerrada','no_procede')"
                            groups="quality_management.group_quality_manager"/>
                    <button name="action_reopen" string="Reabrir"
                            type="object"
                            invisible="state not in ('cerrada','no_procede')"
                            groups="quality_management.group_quality_manager"/>
                    <button name="action_print_8d" string="Imprimir 8D"
                            type="object" class="btn-secondary" icon="fa-print"/>
                    <field name="state" widget="statusbar"
                           statusbar_visible="borrador,evaluacion_calidad,abierta,en_proceso,cerrada"/>
                </header>
                <sheet>
                    <div class="oe_title">
                        <h1><field name="name" readonly="1"/></h1>
                    </div>
                    <group>
                        <group string="Origen e Identificación">
                            <field name="origin_type"/>
                            <field name="origin_inspection_id"
                                   invisible="origin_type != 'inspeccion'"/>
                            <field name="origin_return_id"
                                   invisible="origin_type not in ('devolucion','reclamacion')"/>
                            <field name="defect_type"/>
                            <field name="defect_other_desc"
                                   invisible="defect_type != 'otro'"
                                   required="defect_type == 'otro'"/>
                            <field name="responsible_id"/>
                        </group>
                        <group string="Fechas y Avance">
                            <field name="date_opened"/>
                            <field name="date_closed" readonly="1"/>
                            <field name="quality_evaluated_by" readonly="1"/>
                            <field name="quality_evaluated_date" readonly="1"/>
                            <field name="progress" widget="progressbar"/>
                        </group>
                    </group>
                    <separator string="D1 - Descripción del Incumplimiento"/>
                    <field name="origin_description"/>
                    <notebook>
                        <page string="D2 - Equipo de Trabajo" name="team">
                            <p class="text-muted">
                                <i class="fa fa-info-circle"/>
                                Miembros que recibirán notificaciones de avance.
                            </p>
                            <field name="work_team_ids">
                                <list editable="bottom">
                                    <field name="user_id"/>
                                    <field name="role"/>
                                    <field name="notify_progress"/>
                                </list>
                            </field>
                        </page>
                        <page string="D4 - 5 Por qué" name="why">
                            <field name="why_ids">
                                <list editable="bottom">
                                    <field name="sequence"/>
                                    <field name="question"/>
                                    <field name="answer"/>
                                </list>
                            </field>
                        </page>
                        <page string="D5 - Ishikawa (Causa-Efecto)" name="ishikawa">
                            <field name="ishikawa_ids">
                                <list editable="bottom">
                                    <field name="category"/>
                                    <field name="cause"/>
                                    <field name="is_root_cause"/>
                                </list>
                            </field>
                        </page>
                        <page string="D6 - Acciones" name="actions">
                            <field name="action_line_ids">
                                <list editable="bottom">
                                    <field name="description"/>
                                    <field name="responsible_id"/>
                                    <field name="date_due"/>
                                    <field name="date_completed"/>
                                    <field name="evidence_ids" widget="many2many_binary"/>
                                    <field name="delay_days"
                                           decoration-danger="delay_days > 0"/>
                                    <field name="state" widget="badge"
                                           decoration-success="state == 'completada'"
                                           decoration-danger="state == 'vencida'"
                                           decoration-info="state == 'en_proceso'"/>
                                </list>
                            </field>
                            <div class="text-muted mt-2">
                                <i class="fa fa-info-circle"/>
                                Para ver vista previa de evidencia, abra cada
                                acción en formulario.
                            </div>
                        </page>
                        <page string="No Procede"
                              invisible="state != 'no_procede'" name="no_proc">
                            <field name="no_procede_reason"
                                   placeholder="Motivo por el que no procede la acción correctiva..."/>
                        </page>
                    </notebook>
                </sheet>
                <chatter/>
            </form>
        </field>
    </record>

    <record id="view_quality_corrective_action_search" model="ir.ui.view">
        <field name="name">quality.corrective.action.search</field>
        <field name="model">quality.corrective.action</field>
        <field name="arch" type="xml">
            <search string="Acciones Correctivas">
                <field name="name"/>
                <field name="responsible_id"/>
                <filter string="En Evaluación Calidad" name="eval"
                        domain="[('state','=','evaluacion_calidad')]"/>
                <filter string="Abiertas" name="open"
                        domain="[('state','in',('abierta','en_proceso'))]"/>
                <filter string="Con Acciones Vencidas" name="overdue"
                        domain="[('action_line_ids.state','=','vencida')]"/>
                <filter string="Cerradas" name="closed"
                        domain="[('state','=','cerrada')]"/>
                <group expand="0" string="Agrupar por">
                    <filter string="Tipo de Origen" name="group_origin"
                            context="{'group_by': 'origin_type'}"/>
                    <filter string="Tipo de Defecto" name="group_defect"
                            context="{'group_by': 'defect_type'}"/>
                    <filter string="Responsable" name="group_resp"
                            context="{'group_by': 'responsible_id'}"/>
                    <filter string="Estado" name="group_state"
                            context="{'group_by': 'state'}"/>
                </group>
            </search>
        </field>
    </record>

    <record id="action_quality_corrective_action" model="ir.actions.act_window">
        <field name="name">Acciones Correctivas / 8D</field>
        <field name="res_model">quality.corrective.action</field>
        <field name="view_mode">list,form</field>
        <field name="context">{'search_default_open': 1}</field>
    </record>
</odoo>
''')

# =============================================================================
# 5. Devoluciones de Cliente
# =============================================================================
write(MODULE / "views" / "quality_customer_return_views.xml", '''<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_quality_customer_return_list" model="ir.ui.view">
        <field name="name">quality.customer.return.list</field>
        <field name="model">quality.customer.return</field>
        <field name="arch" type="xml">
            <list decoration-success="state == 'cerrada'"
                  decoration-danger="state == 'no_procede'"
                  decoration-info="state in ('evaluacion_ventas','evaluacion_calidad')">
                <field name="name"/>
                <field name="partner_id"/>
                <field name="defect_type"/>
                <field name="defect_pieces"/>
                <field name="production_date"/>
                <field name="days_since_production"/>
                <field name="date_received"/>
                <field name="corrective_action_id" optional="show"/>
                <field name="state" widget="badge"/>
            </list>
        </field>
    </record>

    <record id="view_quality_customer_return_form" model="ir.ui.view">
        <field name="name">quality.customer.return.form</field>
        <field name="model">quality.customer.return</field>
        <field name="arch" type="xml">
            <form string="Devolución de Cliente">
                <header>
                    <button name="action_submit_sales"
                            string="Registrar / Evaluar"
                            type="object" class="btn-primary"
                            invisible="state != 'borrador'"/>
                    <button name="action_authorize_commercial"
                            string="Autorizar Comercialmente"
                            type="object" class="btn-warning"
                            invisible="state != 'no_procede' or not sales_manager_justification"
                            groups="sales_team.group_sale_manager"/>
                    <button name="action_submit_quality"
                            string="Enviar a Calidad" type="object"
                            class="btn-primary"
                            invisible="state != 'evaluacion_ventas'"/>
                    <button name="action_generate_8d" string="Generar 8D"
                            type="object" class="btn-primary"
                            invisible="state != 'evaluacion_calidad'"
                            groups="quality_management.group_quality_manager"/>
                    <button name="action_no_proceed" string="No Procede"
                            type="object" class="btn-secondary"
                            invisible="state not in ('evaluacion_ventas','evaluacion_calidad')"
                            groups="quality_management.group_quality_manager"/>
                    <button name="action_close" string="Cerrar"
                            type="object" class="btn-primary"
                            invisible="state != 'en_8d'"
                            groups="quality_management.group_quality_manager"/>
                    <button name="action_print_customer_return" string="Imprimir"
                            type="object" class="btn-secondary" icon="fa-print"/>
                    <field name="state" widget="statusbar"
                           statusbar_visible="borrador,evaluacion_ventas,evaluacion_calidad,en_8d,cerrada"/>
                </header>
                <sheet>
                    <div class="oe_title">
                        <h1><field name="name" readonly="1"/></h1>
                    </div>
                    <div class="alert alert-warning" role="alert"
                         invisible="is_within_period">
                        <strong>⚠️ Fuera de periodo:</strong>
                        <field name="days_since_production" nolabel="1" readonly="1"/> días
                        desde producción (>30). Esta devolución NO procede,
                        salvo justificación comercial del Gerente de Ventas.
                    </div>
                    <div class="alert alert-danger" role="alert"
                         invisible="not pallet_alert_15">
                        <i class="fa fa-clock-o"/>
                        <strong>Alerta:</strong> el retorno de tarimas se programó
                        a más de 15 días hábiles desde la recepción.
                    </div>
                    <group>
                        <group string="Datos del Cliente">
                            <field name="partner_id"/>
                            <field name="sale_order_id"/>
                            <field name="date_received"/>
                            <field name="production_date"/>
                            <field name="delivery_date"/>
                            <field name="days_since_production" readonly="1"/>
                            <field name="is_within_period" invisible="1"/>
                            <field name="pallet_alert_15" invisible="1"/>
                        </group>
                        <group string="Detalle del Defecto">
                            <field name="defect_type"/>
                            <field name="defect_other_desc"
                                   invisible="defect_type != 'otro'"
                                   required="defect_type == 'otro'"/>
                            <field name="defect_pieces"/>
                            <field name="affects_functionality"/>
                        </group>
                    </group>
                    <separator string="Motivo de la Devolución"/>
                    <field name="return_reason"/>
                    <notebook>
                        <page string="Evidencia Fotográfica" name="evi">
                            <field name="evidence_ids" widget="many2many_binary"/>
                            <separator string="Vista Previa"/>
                            <field name="evidence_ids" widget="evidence_viewer"
                                   nolabel="1"/>
                        </page>
                        <page string="Reporte de Evidencia (PDF)" name="evpdf">
                            <group>
                                <field name="evidence_pdf"
                                       filename="evidence_pdf_name"/>
                                <field name="evidence_pdf_name" invisible="1"/>
                            </group>
                            <div invisible="not evidence_pdf"
                                 class="o_quality_pdf_preview">
                                <field name="evidence_pdf" widget="pdf_viewer" readonly="1"/>
                            </div>
                        </page>
                        <page string="Formato de Reclamación (PDF)" name="claim">
                            <div class="alert alert-warning" invisible="claim_format_pdf">
                                <i class="fa fa-exclamation-triangle"/>
                                Formato obligatorio para registrar la devolución.
                            </div>
                            <group>
                                <field name="claim_format_pdf"
                                       filename="claim_format_pdf_name"/>
                                <field name="claim_format_pdf_name" invisible="1"/>
                            </group>
                            <div invisible="not claim_format_pdf"
                                 class="o_quality_pdf_preview">
                                <field name="claim_format_pdf" widget="pdf_viewer" readonly="1"/>
                            </div>
                        </page>
                        <page string="Tarimas" name="pallets">
                            <group>
                                <field name="pallets_returned"/>
                                <field name="pallet_return_date"
                                       invisible="not pallets_returned"/>
                            </group>
                        </page>
                        <page string="Autorización Comercial"
                              invisible="is_within_period and not sales_manager_id"
                              name="commercial">
                            <p class="text-muted">
                                <i class="fa fa-info-circle"/>
                                Aplica cuando comercialmente se decide proceder
                                a pesar del bloqueo por >30 días.
                            </p>
                            <group>
                                <field name="sales_manager_id" readonly="1"/>
                            </group>
                            <field name="sales_manager_justification"
                                   placeholder="Motivos por los cuales se realizará la reposición..."/>
                        </page>
                        <page string="8D" invisible="not corrective_action_id"
                              name="eightd">
                            <group>
                                <field name="corrective_action_id"/>
                            </group>
                        </page>
                    </notebook>
                </sheet>
                <chatter/>
            </form>
        </field>
    </record>

    <record id="view_quality_customer_return_search" model="ir.ui.view">
        <field name="name">quality.customer.return.search</field>
        <field name="model">quality.customer.return</field>
        <field name="arch" type="xml">
            <search string="Devoluciones">
                <field name="name"/>
                <field name="partner_id"/>
                <filter string="Abiertas" name="open"
                        domain="[('state','not in',('cerrada','no_procede'))]"/>
                <filter string="En 8D" name="in_8d"
                        domain="[('state','=','en_8d')]"/>
                <filter string="Fuera de periodo" name="out"
                        domain="[('is_within_period','=',False)]"/>
                <group expand="0" string="Agrupar por">
                    <filter string="Cliente" name="group_partner"
                            context="{'group_by': 'partner_id'}"/>
                    <filter string="Tipo de Defecto" name="group_defect"
                            context="{'group_by': 'defect_type'}"/>
                    <filter string="Estado" name="group_state"
                            context="{'group_by': 'state'}"/>
                </group>
            </search>
        </field>
    </record>

    <record id="action_quality_customer_return" model="ir.actions.act_window">
        <field name="name">Devoluciones de Clientes</field>
        <field name="res_model">quality.customer.return</field>
        <field name="view_mode">list,form</field>
        <field name="context">{'search_default_open': 1}</field>
    </record>
</odoo>
''')

# =============================================================================
# 6. Documentos del Cliente
# =============================================================================
write(MODULE / "views" / "quality_customer_document_views.xml", '''<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_quality_customer_document_list" model="ir.ui.view">
        <field name="name">quality.customer.document.list</field>
        <field name="model">quality.customer.document</field>
        <field name="arch" type="xml">
            <list decoration-success="state == 'enviado'"
                  decoration-info="state == 'en_proceso'">
                <field name="name"/>
                <field name="partner_id"/>
                <field name="document_type"/>
                <field name="document_type_other" optional="show"/>
                <field name="requires_dimensions"/>
                <field name="requested_by"/>
                <field name="responsible_id"/>
                <field name="date_requested"/>
                <field name="date_due"/>
                <field name="state" widget="badge"/>
            </list>
        </field>
    </record>

    <record id="view_quality_customer_document_form" model="ir.ui.view">
        <field name="name">quality.customer.document.form</field>
        <field name="model">quality.customer.document</field>
        <field name="arch" type="xml">
            <form string="Documento de Cliente">
                <header>
                    <button name="action_start" string="Iniciar"
                            type="object" class="btn-primary"
                            invisible="state != 'borrador'"/>
                    <button name="action_complete" string="Completar"
                            type="object" class="btn-primary"
                            invisible="state != 'en_proceso'"
                            groups="quality_management.group_quality_inspector"/>
                    <button name="action_send" string="Marcar como Enviado"
                            type="object"
                            invisible="state != 'completado'"/>
                    <button name="action_print_customer_document"
                            string="Imprimir" type="object"
                            class="btn-secondary" icon="fa-print"/>
                    <field name="state" widget="statusbar"
                           statusbar_visible="borrador,en_proceso,completado,enviado"/>
                </header>
                <sheet>
                    <div class="oe_title">
                        <h1><field name="name" readonly="1"/></h1>
                    </div>
                    <group>
                        <group string="Cliente y Documento">
                            <field name="partner_id"/>
                            <field name="document_type"/>
                            <field name="document_type_other"
                                   invisible="document_type != 'otro'"
                                   required="document_type == 'otro'"
                                   placeholder="Especifique el tipo de documento..."/>
                            <field name="requires_dimensions"/>
                            <field name="has_client_format" widget="radio"/>
                        </group>
                        <group string="Responsables y Fechas">
                            <field name="requested_by"/>
                            <field name="responsible_id"/>
                            <field name="date_requested" readonly="1"/>
                            <field name="date_due" readonly="1"/>
                            <field name="date_completed" readonly="1"/>
                        </group>
                    </group>
                    <separator string="Descripción de la Solicitud"/>
                    <div class="alert alert-warning" role="alert"
                         invisible="description">
                        <i class="fa fa-exclamation-triangle"/>
                        La descripción es obligatoria para avanzar.
                    </div>
                    <field name="description"
                           placeholder="Detalle de lo que solicita el cliente..."/>
                    <notebook>
                        <page string="Documento Principal (PDF)" name="pdf">
                            <group>
                                <field name="main_pdf" filename="main_pdf_name"/>
                                <field name="main_pdf_name" invisible="1"/>
                            </group>
                            <div invisible="not main_pdf"
                                 class="o_quality_pdf_preview">
                                <field name="main_pdf" widget="pdf_viewer" readonly="1"/>
                            </div>
                        </page>
                        <page string="Documento Principal (Imagen)" name="img">
                            <p class="text-muted">
                                <i class="fa fa-info-circle"/>
                                Use esta pestaña cuando el insumo sea correo o
                                solicitud del cliente como imagen (no obligatorio PDF).
                            </p>
                            <group>
                                <field name="main_image" widget="image"
                                       options="{'size': [400, 400]}"/>
                                <field name="main_image_name" invisible="1"/>
                            </group>
                        </page>
                        <page string="Formato del Cliente"
                              invisible="has_client_format != 'si'"
                              name="cli_fmt">
                            <field name="client_format_ids" widget="many2many_binary"/>
                        </page>
                        <page string="Documentos Generados / Cargados" name="results">
                            <field name="result_document_ids" widget="many2many_binary"/>
                        </page>
                    </notebook>
                </sheet>
                <chatter/>
            </form>
        </field>
    </record>

    <record id="action_quality_customer_document" model="ir.actions.act_window">
        <field name="name">Documentos de Cliente</field>
        <field name="res_model">quality.customer.document</field>
        <field name="view_mode">list,form</field>
    </record>
</odoo>
''')

# =============================================================================
# 7. Certificados (versión depurada)
# =============================================================================
write(MODULE / "views" / "quality_certificate_views.xml", '''<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_quality_certificate_list" model="ir.ui.view">
        <field name="name">quality.certificate.list</field>
        <field name="model">quality.certificate</field>
        <field name="arch" type="xml">
            <list decoration-success="state == 'enviado'"
                  decoration-info="state == 'generado'">
                <field name="name"/>
                <field name="inspection_id"/>
                <field name="partner_id"/>
                <field name="product_id"/>
                <field name="process_type_id"/>
                <field name="folio" optional="show"/>
                <field name="lot_id" optional="show"/>
                <field name="date_generated"/>
                <field name="certified_by"/>
                <field name="state" widget="badge"
                       decoration-success="state == 'enviado'"
                       decoration-info="state == 'generado'"/>
            </list>
        </field>
    </record>

    <record id="view_quality_certificate_form" model="ir.ui.view">
        <field name="name">quality.certificate.form</field>
        <field name="model">quality.certificate</field>
        <field name="arch" type="xml">
            <form string="Certificado de Calidad">
                <header>
                    <button name="action_generate" string="Generar Certificado"
                            type="object" class="btn-primary"
                            invisible="state != 'borrador'"/>
                    <button name="action_print_certificate" string="Imprimir PDF"
                            type="object" class="btn-secondary" icon="fa-print"
                            invisible="state == 'borrador'"/>
                    <button name="action_send_email" string="Enviar por Correo"
                            type="object" class="btn-secondary"
                            invisible="state == 'borrador'"/>
                    <button name="action_mark_sent"
                            string="Marcar como Enviado"
                            type="object"
                            invisible="state != 'generado'"/>
                    <field name="state" widget="statusbar"
                           statusbar_visible="borrador,generado,enviado"/>
                </header>
                <sheet>
                    <div class="oe_title">
                        <h1><field name="name" readonly="1"/></h1>
                    </div>
                    <group>
                        <group>
                            <field name="inspection_id"/>
                            <field name="partner_id"/>
                            <field name="product_id" readonly="1"/>
                            <field name="process_type_id" readonly="1"/>
                        </group>
                        <group>
                            <field name="folio" readonly="1"/>
                            <field name="lot_id" readonly="1"/>
                            <field name="date_generated"/>
                            <field name="certified_by"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Valores Certificados" name="vals">
                            <p class="text-muted">
                                <i class="fa fa-info-circle"/>
                                No se permiten valores en cero ni atributos repetidos.
                            </p>
                            <group>
                                <group>
                                    <field name="certified_largo"
                                           invisible="certified_largo == 0"/>
                                    <field name="certified_ancho"
                                           invisible="certified_ancho == 0"/>
                                    <field name="certified_espesor"
                                           invisible="certified_espesor == 0"/>
                                    <field name="certified_hexagono"
                                           invisible="certified_hexagono == 0"/>
                                    <field name="certified_resistencia"
                                           invisible="certified_resistencia == 0"/>
                                </group>
                                <group>
                                    <field name="certified_apariencia"
                                           invisible="not certified_apariencia"/>
                                    <field name="certified_humedad"
                                           invisible="certified_humedad == 0"/>
                                    <field name="certified_pegado"
                                           invisible="not certified_pegado"/>
                                    <field name="certified_retiramiento"
                                           invisible="certified_retiramiento == 0"/>
                                    <field name="certified_calibracion"
                                           invisible="certified_calibracion == 0"/>
                                    <field name="certified_engomado"
                                           invisible="not certified_engomado"/>
                                </group>
                            </group>
                        </page>
                        <page string="Atributos Adicionales (solo CUMPLE)"
                              name="attrs">
                            <p class="text-muted">
                                <i class="fa fa-info-circle"/>
                                Solo deben aparecer atributos que CUMPLEN.
                            </p>
                            <field name="attribute_ids"
                                   domain="[('result','=','cumple')]">
                                <list>
                                    <field name="name"/>
                                    <field name="attribute_type"/>
                                    <field name="value_float"
                                           invisible="attribute_type != 'float'"/>
                                    <field name="value_char"
                                           invisible="attribute_type not in ('char','selection')"/>
                                    <field name="value_cumple"
                                           invisible="attribute_type != 'boolean'"/>
                                    <field name="result" widget="badge"/>
                                </list>
                            </field>
                        </page>
                        <page string="PDF Generado" invisible="not report_pdf"
                              name="pdf">
                            <group>
                                <field name="report_pdf"
                                       filename="report_pdf_name"/>
                                <field name="report_pdf_name" invisible="1"/>
                            </group>
                            <div class="o_quality_pdf_preview">
                                <field name="report_pdf" widget="pdf_viewer" readonly="1"/>
                            </div>
                        </page>
                    </notebook>
                </sheet>
                <chatter/>
            </form>
        </field>
    </record>

    <record id="action_quality_certificate" model="ir.actions.act_window">
        <field name="name">Certificados de Calidad</field>
        <field name="res_model">quality.certificate</field>
        <field name="view_mode">list,form</field>
    </record>
</odoo>
''')

# =============================================================================
# Cierre
# =============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Vistas reescritas. Próximos pasos:

 1. Reinicia Odoo con upgrade:
        odoo-bin -d <db> -u quality_management --stop-after-init

 2. Verifica:
    • Liberación de Muestras: tipo MP/PT, fechas bloqueadas, evidencia,
      flujo CNC para opción PT.
    • Liberación de Planos: requisitos sellos/plantilla/troquel/otro,
      contador de modificaciones, triple check, doble PDF obligatorio.
    • Inspecciones: PP/PT widget radio, fechas bloqueadas, alertas en 0,
      pestañas Octágono/Guillotina extras según tipo, evidencia 10 imgs.
    • 8D: tipo Reclamación, defecto OTRO con descripción, equipo de trabajo,
      5 Por qué, Ishikawa, motivo No Procede.
    • Devoluciones: justificación comercial Gerente Ventas, formato
      reclamación obligatorio, alerta tarimas >15 días.
    • Documentos Cliente: tipos limpios, OTRO con descripción libre,
      imagen + PDF, formato cliente Sí/No.
    • Certificados: filtro automático solo CUMPLE en atributos adicionales.

 3. Backup en: """ + str(BACKUP) + """

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")