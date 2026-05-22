## ./__init__.py
```py
from . import models
from . import wizards
```

## ./__manifest__.py
```py
# -*- coding: utf-8 -*-
{
    "name": "Gestión de Calidad - Hexágonos Mexicanos",
    # FOLIO-QM-ODOO18-070: Acabado y Empaque queda limitado a atributos adicionales Cumple/No Cumple.
    # FOLIO-QM-ODOO18-071: Impresión queda limitado a atributos adicionales Cumple/No Cumple.
    # FOLIO-QM-ODOO18-072: Laminadora y Remanejo quedan como procesos separados.
    # FOLIO-QM-ODOO18-073: El historial detallado se unifica en el chatter inicial; se elimina pestaña duplicada.
    # FOLIO-QM-ODOO18-074: Se refuerza el enlace secuencial Octágono -> Guillotina -> Pegado -> Laminadora -> Remanejo -> Troquelado Plano.
    # FOLIO-QM-ODOO18-075: Octágono se endurece con campos obligatorios, sin espesor/retiramiento, precisión de calibración y certificados.
    "version": "18.0.3.7.0",
    "category": "Manufacturing/Quality",
    "summary": "Gestión integral de calidad - Hexágonos (req. Feb-26)",
    "author": "Alphaqueb Consulting SAS",
    "website": "https://alphaqueb.com",
    "license": "LGPL-3",
    "depends": [
        "base",
        "sales_team",
        "web",
        "mail",
        "project",
        "mrp",
        "sale",
        "stock",
        "product",
        "contacts",
        "hr",
    ],
    "data": [
        "security/quality_groups.xml",
        "security/ir.model.access.csv",
        "security/quality_rules.xml",
        "security/quality_strict_acl.xml",
        "data/sequence_data.xml",
        "data/process_type_data.xml",
        "data/quality_attribute_preset_data.xml",
        "data/quality_hardening_data.xml",
        "data/quality_routes_data.xml",
        "data/cron_data.xml",
        "wizards/certificate_wizard_views.xml",
        "views/quality_process_type_views.xml",
        "views/quality_attribute_template_views.xml",
        "views/quality_sample_release_views.xml",
        "views/quality_drawing_release_views.xml",
        "views/quality_inspection_views.xml",
        "views/quality_certificate_views.xml",
        "views/quality_hardening_views.xml",
        "views/quality_corrective_action_views.xml",
        "views/quality_customer_return_views.xml",
        "views/quality_customer_document_views.xml",
        "views/quality_dashboard_views.xml",
        "views/quality_troquel_views.xml",
        "views/res_company_views.xml",
        "views/product_views.xml",
        "views/project_task_quality_views.xml",
        "views/quality_process_route_views.xml",
        "views/quality_retention_views.xml",
        "views/quality_change_history_views.xml",
        "views/quality_troquel_validation_views.xml",
        "views/quality_certificate_email_views.xml",
        "views/quality_inherited_views.xml",
        "views/quality_menus.xml",
        "reports/report_quality_certificate.xml",
        "reports/report_8d.xml",
        "reports/report_8d_extended.xml",
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
}```

## ./data/cron_data.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        <record id="cron_check_overdue_actions" model="ir.cron">
            <field name="name">Calidad: Verificar acciones vencidas</field>
            <field name="model_id" ref="model_quality_corrective_action"/>
            <field name="state">code</field>
            <field name="code">model._cron_check_overdue_actions()</field>
            <field name="interval_number">1</field>
            <field name="interval_type">days</field>
            <field name="active">True</field>
        </record>
    </data>
</odoo>
```

## ./data/process_type_data.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
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
            <field name="show_alineacion" eval="True"/>
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

        <!-- 4. Laminadora -->
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

        <!-- 5. Remanejo -->
        <record id="process_type_remanejo" model="quality.process.type">
            <field name="name">Remanejo</field>
            <field name="code">remanejo</field>
            <field name="sequence">50</field>
            <!-- FOLIO-QM-ODOO18-072: Remanejo se separa de Laminadora como proceso independiente. -->
            <field name="show_largo" eval="True"/>
            <field name="show_ancho" eval="True"/>
            <field name="show_espesor" eval="True"/>
            <field name="show_hexagono" eval="True"/>
            <field name="show_resistencia" eval="True"/>
            <field name="show_apariencia" eval="True"/>
            <field name="show_humedad" eval="True"/>
        </record>

        <!-- 6. Sierras y Ranuradoras -->
        <record id="process_type_sierras_ranuradoras" model="quality.process.type">
            <field name="name">Sierras y Ranuradoras</field>
            <field name="code">sierras_ranuradoras</field>
            <field name="sequence">55</field>
            <field name="show_largo" eval="True"/>
            <field name="show_ancho" eval="True"/>
            <field name="show_espesor" eval="True"/>
            <field name="show_apariencia" eval="True"/>
            <field name="show_ranurado" eval="True"/>
        </record>

        <!-- 7. Troquelado Plano -->
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

        <!-- 8. Impresión -->
        <record id="process_type_impresion" model="quality.process.type">
            <field name="name">Impresión</field>
            <field name="code">impresion</field>
            <field name="sequence">70</field>
            <field name="show_apariencia" eval="True"/>
        </record>

        <!-- 9. Esquinera -->
        <record id="process_type_esquinera" model="quality.process.type">
            <field name="name">Esquinera</field>
            <field name="code">esquinera</field>
            <field name="sequence">75</field>
            <!-- FOLIO-QM-ODOO18-068: proceso solicitado por Calidad/Producción para Planta 2. -->
            <field name="show_largo" eval="True"/>
            <field name="show_ancho" eval="True"/>
            <field name="show_espesor" eval="True"/>
            <field name="show_apariencia" eval="True"/>
            <field name="show_pegado" eval="True"/>
            <field name="show_numero_corrida" eval="True"/>
        </record>

        <!-- 10. Acabado y Empaque -->
        <record id="process_type_acabado" model="quality.process.type">
            <field name="name">Acabado y Empaque</field>
            <field name="code">acabado_empaque</field>
            <field name="sequence">80</field>
            <field name="show_apariencia" eval="True"/>
        </record>
    </data>
</odoo>```

## ./data/quality_attribute_preset_data.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
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

                <!-- ═══════════════ ESQUINERA ═══════════════ -->
        <record id="attr_esquinera_medidas" model="quality.attribute.template">
            <field name="name">Medidas correctas</field>
            <field name="process_type_id" ref="process_type_esquinera"/>
            <field name="attribute_type">boolean</field>
            <field name="sequence">10</field>
            <field name="is_required" eval="True"/>
        </record>
        <record id="attr_esquinera_escuadra" model="quality.attribute.template">
            <field name="name">Escuadra / Esquinado correcto</field>
            <field name="process_type_id" ref="process_type_esquinera"/>
            <field name="attribute_type">boolean</field>
            <field name="sequence">20</field>
            <field name="is_required" eval="True"/>
        </record>
        <record id="attr_esquinera_pegado" model="quality.attribute.template">
            <field name="name">Pegado correcto</field>
            <field name="process_type_id" ref="process_type_esquinera"/>
            <field name="attribute_type">boolean</field>
            <field name="sequence">30</field>
            <field name="is_required" eval="True"/>
        </record>
        <record id="attr_esquinera_apariencia" model="quality.attribute.template">
            <field name="name">Apariencia general</field>
            <field name="process_type_id" ref="process_type_esquinera"/>
            <field name="attribute_type">boolean</field>
            <field name="sequence">40</field>
            <field name="is_required" eval="True"/>
        </record>
        <record id="attr_esquinera_etiquetado" model="quality.attribute.template">
            <field name="name">Etiquetado</field>
            <field name="process_type_id" ref="process_type_esquinera"/>
            <field name="attribute_type">boolean</field>
            <field name="sequence">50</field>
            <field name="is_required" eval="True"/>
        </record>

    </data>
</odoo>
```

## ./data/quality_hardening_data.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="0">

        <record id="process_type_octagono" model="quality.process.type">
            <!-- FOLIO-QM-ODOO18-075:
                 Octágono debe capturar Ancho, Hexágono, Número de Corrida,
                 Papel, Adhesivo, Calibración, Engomado, Alineación y Corte de Guillotina.
                 No aplica Espesor ni Retiramiento en este proceso. -->
            <field name="name">Octágono</field>
            <field name="code">octagono</field>
            <field name="sequence">10</field>
            <field name="capture_mode">full</field>
            <field name="require_measures" eval="True"/>
            <field name="require_additional_attributes" eval="True"/>
            <field name="zero_value_blocking" eval="True"/>

            <field name="show_largo" eval="False"/>
            <field name="show_ancho" eval="True"/>
            <field name="show_espesor" eval="False"/>
            <field name="show_hexagono" eval="True"/>
            <field name="show_resistencia" eval="False"/>
            <field name="show_apariencia" eval="False"/>
            <field name="show_humedad" eval="False"/>
            <field name="show_pegado" eval="False"/>
            <field name="show_retiramiento" eval="False"/>
            <field name="show_calibracion" eval="True"/>
            <field name="show_engomado" eval="True"/>
            <field name="show_alineacion" eval="True"/>
            <field name="show_ranurado" eval="False"/>
            <field name="show_troquelado" eval="False"/>
            <field name="show_papel" eval="True"/>
            <field name="show_adhesivo" eval="True"/>
            <field name="show_tipo_hexagono" eval="False"/>
            <field name="show_corte_guillotina" eval="True"/>
            <field name="show_numero_corrida" eval="True"/>
        </record>

        <record id="process_type_guillotina" model="quality.process.type">
            <field name="name">Guillotina</field>
            <field name="code">guillotina</field>
            <field name="sequence">20</field>
            <field name="capture_mode">full</field>
            <field name="require_measures" eval="True"/>
            <field name="require_additional_attributes" eval="True"/>
            <field name="zero_value_blocking" eval="True"/>
        </record>

        <record id="process_type_pegado" model="quality.process.type">
            <field name="name">Pegado</field>
            <field name="code">pegado</field>
            <field name="sequence">30</field>
            <field name="capture_mode">full</field>
            <field name="require_measures" eval="True"/>
            <field name="require_additional_attributes" eval="True"/>
            <field name="zero_value_blocking" eval="True"/>
        </record>

        <record id="process_type_laminadora" model="quality.process.type">
            <field name="name">Laminadora</field>
            <field name="code">laminadora</field>
            <field name="sequence">40</field>
            <!-- FOLIO-QM-ODOO18-072: Laminadora queda separada de Remanejo. -->
            <field name="capture_mode">full</field>
            <field name="require_measures" eval="True"/>
            <field name="require_additional_attributes" eval="True"/>
            <field name="zero_value_blocking" eval="True"/>
            <field name="show_largo" eval="True"/>
            <field name="show_ancho" eval="True"/>
            <field name="show_espesor" eval="True"/>
            <field name="show_hexagono" eval="True"/>
            <field name="show_resistencia" eval="True"/>
            <field name="show_apariencia" eval="True"/>
            <field name="show_humedad" eval="True"/>
        </record>

        <record id="process_type_remanejo" model="quality.process.type">
            <field name="name">Remanejo</field>
            <field name="code">remanejo</field>
            <field name="sequence">50</field>
            <!-- FOLIO-QM-ODOO18-072: nuevo proceso independiente dentro del flujo estándar. -->
            <field name="capture_mode">full</field>
            <field name="require_measures" eval="True"/>
            <field name="require_additional_attributes" eval="True"/>
            <field name="zero_value_blocking" eval="True"/>
            <field name="show_largo" eval="True"/>
            <field name="show_ancho" eval="True"/>
            <field name="show_espesor" eval="True"/>
            <field name="show_hexagono" eval="True"/>
            <field name="show_resistencia" eval="True"/>
            <field name="show_apariencia" eval="True"/>
            <field name="show_humedad" eval="True"/>
        </record>

        <record id="process_type_sierras_ranuradoras" model="quality.process.type">
            <field name="name">Sierras y Ranuradoras</field>
            <field name="code">sierras_ranuradoras</field>
            <field name="sequence">55</field>
            <field name="capture_mode">full</field>
            <field name="require_measures" eval="True"/>
            <field name="require_additional_attributes" eval="True"/>
            <field name="zero_value_blocking" eval="True"/>
        </record>

        <record id="process_type_troquelado_plano" model="quality.process.type">
            <field name="name">Troquelado Plano</field>
            <field name="code">troquelado_plano</field>
            <field name="sequence">60</field>
            <field name="capture_mode">full</field>
            <field name="require_measures" eval="True"/>
            <field name="require_additional_attributes" eval="True"/>
            <field name="zero_value_blocking" eval="True"/>
        </record>

        <record id="process_type_impresion" model="quality.process.type">
            <field name="name">Impresión</field>
            <field name="code">impresion</field>
            <!-- FOLIO-QM-ODOO18-071: Impresión solo captura atributos adicionales Cumple/No Cumple; no permite OK/NO OK/N/A, selección ni numéricos. -->
            <field name="capture_mode">additional_only</field>
            <field name="require_measures" eval="False"/>
            <field name="require_additional_attributes" eval="True"/>
            <field name="zero_value_blocking" eval="True"/>

            <field name="show_largo" eval="False"/>
            <field name="show_ancho" eval="False"/>
            <field name="show_espesor" eval="False"/>
            <field name="show_hexagono" eval="False"/>
            <field name="show_resistencia" eval="False"/>
            <field name="show_apariencia" eval="False"/>
            <field name="show_humedad" eval="False"/>
            <field name="show_pegado" eval="False"/>
            <field name="show_retiramiento" eval="False"/>
            <field name="show_calibracion" eval="False"/>
            <field name="show_engomado" eval="False"/>
            <field name="show_alineacion" eval="False"/>
            <field name="show_ranurado" eval="False"/>
            <field name="show_troquelado" eval="False"/>
            <field name="show_papel" eval="False"/>
            <field name="show_adhesivo" eval="False"/>
            <field name="show_tipo_hexagono" eval="False"/>
            <field name="show_corte_guillotina" eval="False"/>
            <field name="show_numero_corrida" eval="False"/>
        </record>

        <record id="process_type_esquinera" model="quality.process.type">
            <field name="name">Esquinera</field>
            <field name="code">esquinera</field>
            <!-- FOLIO-QM-ODOO18-068: endurecimiento del proceso Esquinera sin hacerlo parte de la secuencia obligatoria global. -->
            <field name="capture_mode">full</field>
            <field name="require_measures" eval="True"/>
            <field name="require_additional_attributes" eval="True"/>
            <field name="zero_value_blocking" eval="True"/>
            <field name="show_largo" eval="True"/>
            <field name="show_ancho" eval="True"/>
            <field name="show_espesor" eval="True"/>
            <field name="show_apariencia" eval="True"/>
            <field name="show_pegado" eval="True"/>
            <field name="show_numero_corrida" eval="True"/>
        </record>

        <record id="process_type_acabado" model="quality.process.type">
            <field name="name">Acabado y Empaque</field>
            <field name="code">acabado_empaque</field>
            <!-- FOLIO-QM-ODOO18-070: Acabado y Empaque solo captura atributos Cumple/No Cumple; no medidas numéricas. -->
            <field name="capture_mode">additional_only</field>
            <field name="require_measures" eval="False"/>
            <field name="require_additional_attributes" eval="True"/>
            <field name="zero_value_blocking" eval="True"/>

            <field name="show_largo" eval="False"/>
            <field name="show_ancho" eval="False"/>
            <field name="show_espesor" eval="False"/>
            <field name="show_hexagono" eval="False"/>
            <field name="show_resistencia" eval="False"/>
            <field name="show_apariencia" eval="False"/>
            <field name="show_humedad" eval="False"/>
            <field name="show_pegado" eval="False"/>
            <field name="show_retiramiento" eval="False"/>
            <field name="show_calibracion" eval="False"/>
            <field name="show_engomado" eval="False"/>
            <field name="show_alineacion" eval="False"/>
            <field name="show_ranurado" eval="False"/>
            <field name="show_troquelado" eval="False"/>
            <field name="show_papel" eval="False"/>
            <field name="show_adhesivo" eval="False"/>
            <field name="show_tipo_hexagono" eval="False"/>
            <field name="show_corte_guillotina" eval="False"/>
            <field name="show_numero_corrida" eval="False"/>
        </record>

        <!-- FOLIO-QM-ODOO18-071: atributos de Impresión quedan forzados como booleanos Cumple/No Cumple. -->
        <record id="attr_imp_color" model="quality.attribute.template">
            <field name="attribute_type">boolean</field>
            <field name="capture_zone">additional</field>
            <field name="result_mode">cumple</field>
            <field name="allow_zero" eval="False"/>
        </record>

        <record id="attr_imp_registro" model="quality.attribute.template">
            <field name="attribute_type">boolean</field>
            <field name="capture_zone">additional</field>
            <field name="result_mode">cumple</field>
            <field name="allow_zero" eval="False"/>
        </record>

        <record id="attr_imp_legibilidad" model="quality.attribute.template">
            <field name="attribute_type">boolean</field>
            <field name="capture_zone">additional</field>
            <field name="result_mode">cumple</field>
            <field name="allow_zero" eval="False"/>
        </record>

        <record id="attr_imp_uniformidad" model="quality.attribute.template">
            <field name="attribute_type">boolean</field>
            <field name="capture_zone">additional</field>
            <field name="result_mode">cumple</field>
            <field name="allow_zero" eval="False"/>
        </record>

        <!-- FOLIO-QM-ODOO18-070: atributos de Acabado y Empaque quedan como booleanos Cumple/No Cumple. -->
        <record id="attr_aca_amarre" model="quality.attribute.template">
            <field name="attribute_type">boolean</field>
            <field name="capture_zone">additional</field>
            <field name="result_mode">cumple</field>
            <field name="allow_zero" eval="False"/>
        </record>

        <record id="attr_aca_etiquetado" model="quality.attribute.template">
            <field name="attribute_type">boolean</field>
            <field name="capture_zone">additional</field>
            <field name="result_mode">cumple</field>
            <field name="allow_zero" eval="False"/>
        </record>

        <record id="attr_aca_emplayado" model="quality.attribute.template">
            <field name="attribute_type">boolean</field>
            <field name="capture_zone">additional</field>
            <field name="result_mode">cumple</field>
            <field name="allow_zero" eval="False"/>
        </record>

        <record id="attr_aca_apariencia" model="quality.attribute.template">
            <field name="attribute_type">boolean</field>
            <field name="capture_zone">additional</field>
            <field name="result_mode">cumple</field>
            <field name="allow_zero" eval="False"/>
        </record>

        <record id="attr_aca_cantidad" model="quality.attribute.template">
            <field name="attribute_type">boolean</field>
            <field name="capture_zone">additional</field>
            <field name="result_mode">cumple</field>
            <field name="allow_zero" eval="False"/>
        </record>

    </data>
</odoo>```

## ./data/quality_routes_data.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="0">
        <record id="seq_quality_troquel_validation" model="ir.sequence">
            <field name="name">Validación de Troquel</field>
            <field name="code">quality.troquel.validation</field>
            <field name="prefix">TVAL-</field>
            <field name="padding">4</field>
        </record>

        <record id="seq_quality_troquel_repair" model="ir.sequence">
            <field name="name">Reparación de Troquel</field>
            <field name="code">quality.troquel.repair</field>
            <field name="prefix">TREP-</field>
            <field name="padding">4</field>
        </record>

        <!-- FOLIO-QM-ODOO18-074: ruta estándar corregida según flujo solicitado. -->
        <record id="quality_route_estandar" model="quality.process.route">
            <field name="name">Ruta Estándar Hexágonos</field>
            <field name="sequence">10</field>
            <field name="active" eval="True"/>
        </record>

        <record id="quality_route_estandar_l1" model="quality.process.route.line">
            <field name="route_id" ref="quality_route_estandar"/>
            <field name="sequence">10</field>
            <field name="process_type_id" ref="process_type_octagono"/>
            <field name="is_optional" eval="False"/>
        </record>

        <record id="quality_route_estandar_l2" model="quality.process.route.line">
            <field name="route_id" ref="quality_route_estandar"/>
            <field name="sequence">20</field>
            <field name="process_type_id" ref="process_type_guillotina"/>
            <field name="is_optional" eval="False"/>
        </record>

        <record id="quality_route_estandar_l3" model="quality.process.route.line">
            <field name="route_id" ref="quality_route_estandar"/>
            <field name="sequence">30</field>
            <field name="process_type_id" ref="process_type_pegado"/>
            <field name="is_optional" eval="False"/>
        </record>

        <record id="quality_route_estandar_l4" model="quality.process.route.line">
            <field name="route_id" ref="quality_route_estandar"/>
            <field name="sequence">40</field>
            <field name="process_type_id" ref="process_type_laminadora"/>
            <field name="is_optional" eval="False"/>
        </record>

        <record id="quality_route_estandar_l5" model="quality.process.route.line">
            <field name="route_id" ref="quality_route_estandar"/>
            <field name="sequence">50</field>
            <field name="process_type_id" ref="process_type_remanejo"/>
            <field name="is_optional" eval="False"/>
        </record>

        <record id="quality_route_estandar_l6" model="quality.process.route.line">
            <field name="route_id" ref="quality_route_estandar"/>
            <field name="sequence">60</field>
            <field name="process_type_id" ref="process_type_troquelado_plano"/>
            <field name="is_optional" eval="False"/>
        </record>

        <!-- Se conserva el proceso existente, pero ya no se usa como paso obligatorio entre Laminadora y Troquelado. -->
        <record id="quality_route_estandar_l7" model="quality.process.route.line">
            <field name="route_id" ref="quality_route_estandar"/>
            <field name="sequence">70</field>
            <field name="process_type_id" ref="process_type_sierras_ranuradoras"/>
            <field name="is_optional" eval="True"/>
            <field name="notes">Proceso conservado como opcional para no romper configuraciones previas.</field>
        </record>
    </data>
</odoo>```

## ./data/sequence_data.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        <record id="seq_quality_sample_release" model="ir.sequence">
            <field name="name">Liberación de Muestras</field>
            <field name="code">quality.sample.release</field>
            <field name="prefix">QSR-</field>
            <field name="padding">4</field>
        </record>

        <record id="seq_quality_drawing_release" model="ir.sequence">
            <field name="name">Liberación de Planos</field>
            <field name="code">quality.drawing.release</field>
            <field name="prefix">QDR-</field>
            <field name="padding">4</field>
        </record>

        <record id="seq_quality_inspection" model="ir.sequence">
            <field name="name">Inspección de Calidad</field>
            <field name="code">quality.inspection</field>
            <field name="prefix">QI-</field>
            <field name="padding">4</field>
        </record>

        <record id="seq_quality_certificate" model="ir.sequence">
            <field name="name">Certificado de Calidad</field>
            <field name="code">quality.certificate</field>
            <field name="prefix">QC-</field>
            <field name="padding">4</field>
        </record>

        <record id="seq_quality_corrective_action" model="ir.sequence">
            <field name="name">Acción Correctiva</field>
            <field name="code">quality.corrective.action</field>
            <field name="prefix">QCA-</field>
            <field name="padding">4</field>
        </record>

        <record id="seq_quality_customer_return" model="ir.sequence">
            <field name="name">Devolución de Cliente</field>
            <field name="code">quality.customer.return</field>
            <field name="prefix">QCR-</field>
            <field name="padding">4</field>
        </record>

        <record id="seq_quality_customer_document" model="ir.sequence">
            <field name="name">Documento de Cliente</field>
            <field name="code">quality.customer.document</field>
            <field name="prefix">QCD-</field>
            <field name="padding">4</field>
        </record>

        <!-- Email template para certificados -->
        <record id="email_template_quality_certificate" model="mail.template">
            <field name="name">Calidad: Envío de Certificado</field>
            <field name="model_id" ref="model_quality_certificate"/>
            <field name="subject">Certificado de Calidad {{ object.name }}</field>
            <field name="email_from">{{ (object.company_id.email or user.email) }}</field>
            <field name="email_to">{{ object.partner_id.email }}</field>
            <field name="body_html"><![CDATA[
<p>Estimado/a {{ object.partner_id.name }},</p>
<p>Adjuntamos el certificado de calidad <strong>{{ object.name }}</strong>
correspondiente al producto <strong>{{ object.product_id.name }}</strong>.</p>
<p>Folio de producción: {{ object.folio or '' }}<br/>
Lote: {{ object.lot_id.name or '' }}<br/>
Fecha: {{ object.date_generated }}</p>
<p>Saludos cordiales,<br/>
{{ object.certified_by.name }}<br/>
Departamento de Calidad<br/>
{{ object.company_id.name }}</p>
]]></field>
        </record>
    </data>
</odoo>
```

## ./models/__init__.py
```py
from . import quality_process_type
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
from . import quality_hardening
from . import project_task_quality
from . import quality_process_route
from . import quality_retention_flow
from . import quality_change_history
from . import quality_certificate_email
from . import quality_corrective_extra
from . import quality_customer_document_extra
from . import quality_troquel_validation
from . import quality_security_enforcement```

## ./models/product_template.py
```py
from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    quality_attribute_template_ids = fields.One2many(
        'quality.attribute.template', 'product_tmpl_id',
        string='Plantillas de Atributos de Calidad'
    )
    quality_attribute_count = fields.Integer(
        compute='_compute_quality_attribute_count',
        string='Atributos de Calidad'
    )

    @api.depends('quality_attribute_template_ids')
    def _compute_quality_attribute_count(self):
        for rec in self:
            rec.quality_attribute_count = len(rec.quality_attribute_template_ids)

    def action_view_quality_attributes(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Plantillas de Atributos'),
            'res_model': 'quality.attribute.template',
            'view_mode': 'list,form',
            'domain': [('product_tmpl_id', '=', self.id)],
            'context': {'default_product_tmpl_id': self.id},
        }```

## ./models/project_task_quality.py
```py
# -*- coding: utf-8 -*-
"""
Integración con project.task — bloqueos al mover tarjetas en Kanban.
Cubre los requerimientos de Muestras & Prototipos y Altas & Actualizaciones
de Planos que nacen desde Proyectos.
"""
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProjectTaskQuality(models.Model):
    _inherit = "project.task"

    quality_sample_release_id = fields.Many2one(
        "quality.sample.release", "Liberación de Muestra",
        help="Vinculación con la liberación de muestra de Calidad.")
    quality_drawing_release_id = fields.Many2one(
        "quality.drawing.release", "Liberación de Plano")

    quality_required_for_progress = fields.Boolean(
        "Requiere Liberación de Calidad",
        help="Si está activo, no se puede mover la tarjeta a etapas avanzadas "
             "sin liberación aprobada de Calidad.")
    quality_block_reason = fields.Char(
        "Motivo de Bloqueo de Etapa",
        compute="_compute_quality_block_reason")

    @api.depends("quality_sample_release_id.state",
                 "quality_drawing_release_id.state",
                 "quality_required_for_progress")
    def _compute_quality_block_reason(self):
        for task in self:
            reasons = []
            if task.quality_required_for_progress:
                if (task.quality_sample_release_id
                        and task.quality_sample_release_id.state != "aceptado"):
                    reasons.append(_("Muestra no liberada por Calidad"))
                if (task.quality_drawing_release_id
                        and task.quality_drawing_release_id.state != "aceptado_diseno"):
                    reasons.append(_("Plano no liberado (Calidad/Ventas/Diseño)"))
            task.quality_block_reason = "; ".join(reasons) if reasons else False

    def _quality_validate_stage_move(self, new_stage_id):
        """Llamada desde write() cuando cambia stage_id."""
        for task in self:
            if not task.quality_required_for_progress:
                continue

            new_stage = self.env["project.task.type"].browse(new_stage_id)
            # Permite regresar a etapas anteriores; bloquea solo avance.
            if task.stage_id and new_stage.sequence <= task.stage_id.sequence:
                continue

            sample = task.quality_sample_release_id
            drawing = task.quality_drawing_release_id

            if sample:
                if not sample.spec_pdf:
                    raise UserError(_(
                        "No se puede avanzar la tarea '%s': la muestra '%s' "
                        "no tiene Especificación PDF cargada."
                    ) % (task.name, sample.name))
                if not sample.inspection_line_ids:
                    raise UserError(_(
                        "No se puede avanzar la tarea '%s': la muestra '%s' "
                        "no tiene atributos de inspección capturados."
                    ) % (task.name, sample.name))
                if sample.state != "aceptado":
                    raise UserError(_(
                        "No se puede avanzar la tarea '%s': la muestra '%s' "
                        "está en estado '%s' (debe estar Aceptada)."
                    ) % (task.name, sample.name,
                         dict(sample._fields["state"].selection).get(sample.state)))

            if drawing:
                if not drawing.drawing_pdf or not drawing.quotation_pdf:
                    raise UserError(_(
                        "No se puede avanzar la tarea '%s': el plano '%s' "
                        "requiere AMBOS documentos (Plano + Cotización/Dibujo)."
                    ) % (task.name, drawing.name))
                if drawing.state != "aceptado_diseno":
                    raise UserError(_(
                        "No se puede avanzar la tarea '%s': el plano '%s' "
                        "no ha completado el triple-check (Calidad/Ventas/Diseño). "
                        "Estado actual: '%s'."
                    ) % (task.name, drawing.name,
                         dict(drawing._fields["state"].selection).get(drawing.state)))

    def write(self, vals):
        if "stage_id" in vals and vals["stage_id"]:
            self._quality_validate_stage_move(vals["stage_id"])
        return super().write(vals)


class QualitySampleReleaseTask(models.Model):
    _inherit = "quality.sample.release"

    project_task_ids = fields.One2many(
        "project.task", "quality_sample_release_id",
        string="Tareas Vinculadas")


class QualityDrawingReleaseTask(models.Model):
    _inherit = "quality.drawing.release"

    project_task_ids = fields.One2many(
        "project.task", "quality_drawing_release_id",
        string="Tareas Vinculadas")
```

## ./models/quality_5why.py
```py
# -*- coding: utf-8 -*-
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
```

## ./models/quality_action_line.py
```py
# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class QualityActionLine(models.Model):
    _name = "quality.action.line"
    _description = "Línea de Acción Correctiva"
    _order = "date_due, id"

    corrective_id = fields.Many2one(
        "quality.corrective.action",
        required=True,
        ondelete="cascade",
    )
    description = fields.Text("Descripción de la Acción", required=True)
    responsible_id = fields.Many2one("res.users", "Responsable", required=True)
    date_due = fields.Date("Fecha de Cumplimiento", required=True)
    date_completed = fields.Date("Fecha de Cumplimiento Real")
    evidence_ids = fields.Many2many(
        "ir.attachment",
        "quality_action_evidence_rel",
        "action_line_id",
        "attachment_id",
        string="Evidencia",
    )

    # FOLIO-QM-ODOO18-005: se elimina el compute de state porque no asignaba valor
    # en todas las rutas y podía romper la carga del registro; el avance por evidencia
    # se controla ahora en create/write y en las acciones explícitas.
    state = fields.Selection(
        [
            ("pendiente", "Pendiente"),
            ("en_proceso", "En Proceso"),
            ("completada", "Completada"),
            ("vencida", "Vencida"),
        ],
        default="pendiente",
        required=True,
        readonly=False,
    )

    delay_days = fields.Integer(compute="_compute_delay_days", store=True)
    notes = fields.Text()

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec, vals in zip(records, vals_list):
            # FOLIO-QM-ODOO18-006: si la acción nace con evidencia, debe iniciar en proceso.
            if vals.get("evidence_ids") and rec.state == "pendiente":
                rec.state = "en_proceso"
        return records

    def write(self, vals):
        res = super().write(vals)
        if "evidence_ids" in vals:
            for rec in self.filtered(lambda line: line.evidence_ids and line.state == "pendiente"):
                # FOLIO-QM-ODOO18-006: al adjuntar evidencia se refleja avance sin depender de compute.
                rec.state = "en_proceso"
        return res

    @api.depends("date_due", "state")
    def _compute_delay_days(self):
        today = fields.Date.today()
        for line in self:
            if line.date_due and line.state in ("pendiente", "en_proceso", "vencida"):
                line.delay_days = max(0, (today - line.date_due).days)
            else:
                line.delay_days = 0

    def action_complete(self):
        for rec in self:
            if not rec.evidence_ids:
                raise UserError(_("No se puede completar la acción sin adjuntar evidencia."))
            rec.state = "completada"
            rec.date_completed = fields.Date.today()

    def action_reopen(self):
        for rec in self:
            rec.state = "en_proceso"
            rec.date_completed = False```

## ./models/quality_attribute_template.py
```py
from odoo import models, fields


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
    )```

## ./models/quality_certificate_email.py
```py
# -*- coding: utf-8 -*-
"""
Certificados:
- Adjuntar PDF generado al correo automáticamente.
- Registrar bitácora de envíos.
- Marcar fecha de envío real.
"""
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64


class QualityCertificateEmail(models.Model):
    _inherit = "quality.certificate"

    date_sent = fields.Datetime("Fecha de Envío Real", readonly=True, copy=False)
    sent_by = fields.Many2one("res.users", "Enviado por", readonly=True, copy=False)
    email_log_ids = fields.One2many(
        "quality.certificate.email.log", "certificate_id",
        string="Bitácora de Envíos")

    def _generate_certificate_attachment(self):
        self.ensure_one()
        report = self.env.ref(
            "quality_management.action_report_quality_certificate")
        pdf_content, _content_type = report._render_qweb_pdf(
            "quality_management.report_quality_certificate_document",
            res_ids=[self.id])
        filename = "Certificado_%s.pdf" % (self.name or "").replace("/", "-")
        attachment = self.env["ir.attachment"].create({
            "name": filename,
            "type": "binary",
            "datas": base64.b64encode(pdf_content),
            "res_model": "quality.certificate",
            "res_id": self.id,
            "mimetype": "application/pdf",
        })
        # Guardar también en report_pdf
        self.write({
            "report_pdf": base64.b64encode(pdf_content),
            "report_pdf_name": filename,
        })
        return attachment

    def action_send_email(self):
        """Override: adjunta PDF generado y precarga template."""
        self.ensure_one()
        if self.state == "borrador":
            raise UserError(_(
                "Genere primero el certificado antes de enviarlo."))

        attachment = self._generate_certificate_attachment()
        template = self.env.ref(
            "quality_management.email_template_quality_certificate",
            raise_if_not_found=False)
        compose = self.env.ref("mail.email_compose_message_wizard_form")
        ctx = {
            "default_model": "quality.certificate",
            "default_res_ids": self.ids,
            "default_template_id": template.id if template else False,
            "default_composition_mode": "comment",
            "default_attachment_ids": [(6, 0, [attachment.id])],
            "mark_so_as_sent": True,
            "force_email": True,
        }
        return {
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(compose.id, "form")],
            "target": "new",
            "context": ctx,
        }

    def action_mark_sent(self):
        for rec in self:
            rec.state = "enviado"
            rec.date_sent = fields.Datetime.now()
            rec.sent_by = self.env.user
            self.env["quality.certificate.email.log"].create({
                "certificate_id": rec.id,
                "user_id": self.env.user.id,
                "recipient_email": rec.partner_id.email or "",
                "notes": _("Marcado como enviado manualmente."),
            })

    def message_post(self, **kwargs):
        """Detectar envíos vía mail.compose para registrar bitácora y fecha."""
        msg = super().message_post(**kwargs)
        try:
            if (kwargs.get("subtype_xmlid") == "mail.mt_comment"
                    and kwargs.get("partner_ids")
                    and self.state in ("generado", "enviado")):
                if not self.date_sent:
                    self.write({
                        "date_sent": fields.Datetime.now(),
                        "sent_by": self.env.user.id,
                        "state": "enviado",
                    })
                self.env["quality.certificate.email.log"].create({
                    "certificate_id": self.id,
                    "user_id": self.env.user.id,
                    "recipient_email": self.partner_id.email or "",
                    "message_id": msg.id if msg else False,
                    "notes": _("Envío registrado vía mensajería."),
                })
        except Exception:
            # Nunca romper el envío por la bitácora
            pass
        return msg


class QualityCertificateEmailLog(models.Model):
    _name = "quality.certificate.email.log"
    _description = "Bitácora de Envío de Certificados"
    _order = "date desc, id desc"

    certificate_id = fields.Many2one(
        "quality.certificate", required=True, ondelete="cascade", index=True)
    date = fields.Datetime(default=fields.Datetime.now, readonly=True)
    user_id = fields.Many2one("res.users", "Enviado por")
    recipient_email = fields.Char("Destinatario")
    message_id = fields.Many2one("mail.message", "Mensaje", ondelete="set null")
    notes = fields.Text("Notas")
```

## ./models/quality_certificate.py
```py
# -*- coding: utf-8 -*-
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
```

## ./models/quality_change_history.py
```py
# -*- coding: utf-8 -*-
"""
Historial campo a campo en inspecciones y líneas.

FOLIO-QM-ODOO18-073:
- Se conserva el modelo técnico de historial.
- Ya no se muestra una pestaña duplicada al usuario.
- Cada movimiento se publica también en el chatter inicial de la inspección,
  que queda como única sección visible de movimientos.
"""
from collections import defaultdict

from markupsafe import Markup, escape

from odoo import models, fields, api, _


TRACKED_INSPECTION_FIELDS = [
    "largo", "ancho", "espesor", "hexagono", "resistencia", "resistencia_na",
    "apariencia", "humedad_pct", "pegado_result", "oct_retiramiento",
    "calibracion", "engomado", "oct_ancho", "oct_espesor", "oct_hexagono",
    "oct_hexagono_tipo", "oct_alineacion", "oct_pegado",
    "reticula_extendida", "reticula_vueltas", "lote_reticula",
    "gramaje_reticula", "numero_corrida", "tipo_hexagono",
    "corte_guillotina", "papel_ancho", "papel_gramaje", "papel_proveedor_id",
    "adhesivo_lote1", "adhesivo_lote2", "state", "retention_state",
]

TRACKED_LINE_FIELDS = [
    "value_float", "value_char", "value_cumple", "value_ok",
    "min_value", "max_value", "result", "notes",
]


class QualityInspectionHistory(models.Model):
    _name = "quality.inspection.history"
    _description = "Historial de Cambios — Inspección"
    _order = "change_date desc, id desc"
    _rec_name = "field_name"

    inspection_id = fields.Many2one(
        "quality.inspection", "Inspección", ondelete="cascade", index=True)
    line_id = fields.Many2one(
        "quality.inspection.line", "Línea", ondelete="cascade", index=True)
    field_name = fields.Char("Campo", required=True)
    field_label = fields.Char("Etiqueta del Campo")
    old_value = fields.Char("Valor Anterior")
    new_value = fields.Char("Valor Nuevo")
    changed_by = fields.Many2one(
        "res.users", "Cambiado por",
        default=lambda s: s.env.user, readonly=True)
    change_date = fields.Datetime(
        default=fields.Datetime.now, readonly=True)
    reason = fields.Char("Motivo (opcional)")
    inspection_state_at_change = fields.Char("Estado al momento del cambio")


def _format_value(record, field_name):
    if field_name not in record._fields:
        return ""

    val = record[field_name]
    field = record._fields[field_name]

    if val is False or val is None:
        return ""

    if field.type == "many2one":
        return val.display_name or ""

    if field.type == "selection":
        return dict(field.selection).get(val, str(val))

    if field.type == "boolean":
        return _("Sí") if val else _("No")

    return str(val)


def _safe_display(value):
    value = value if value not in (False, None, "") else "—"
    return escape(str(value))


def _post_quality_history_to_chatter(inspection, changes):
    """
    Publica cambios detallados en el chatter inicial.
    changes: list(dict(label, old, new, state))
    """
    if not inspection or not changes:
        return

    if inspection.env.context.get("skip_quality_history_chatter"):
        return

    items = []
    for change in changes:
        items.append(
            "<li>"
            "<b>%s</b>: "
            "<span style='color:#6b7280;'>%s</span> "
            "<span style='color:#9ca3af;'>→</span> "
            "<span>%s</span>"
            "<br/><small style='color:#6b7280;'>Estado: %s</small>"
            "</li>"
            % (
                _safe_display(change.get("label")),
                _safe_display(change.get("old")),
                _safe_display(change.get("new")),
                _safe_display(change.get("state")),
            )
        )

    body = Markup(
        "<p><b>%s</b></p><ul>%s</ul>"
        % (
            escape(_("Movimiento registrado en captura de calidad")),
            "".join(items),
        )
    )

    inspection.message_post(
        body=body,
        subtype_xmlid="mail.mt_comment",
    )


class QualityInspectionTracked(models.Model):
    _inherit = "quality.inspection"

    history_ids = fields.One2many(
        "quality.inspection.history", "inspection_id",
        string="Historial de Cambios")
    history_count = fields.Integer(compute="_compute_history_count")

    def _compute_history_count(self):
        for rec in self:
            rec.history_count = len(rec.history_ids)

    def write(self, vals):
        History = self.env["quality.inspection.history"]
        snapshots = {}
        tracked_keys = [k for k in vals.keys() if k in TRACKED_INSPECTION_FIELDS]

        if tracked_keys:
            for rec in self:
                snapshots[rec.id] = {
                    k: _format_value(rec, k) for k in tracked_keys
                }

        res = super().write(vals)

        if tracked_keys:
            for rec in self:
                old = snapshots.get(rec.id, {})
                changes_for_chatter = []

                for fname in tracked_keys:
                    new_val = _format_value(rec, fname)
                    old_val = old.get(fname, "")

                    if old_val == new_val:
                        continue

                    label = rec._fields[fname].string or fname
                    History.create({
                        "inspection_id": rec.id,
                        "field_name": fname,
                        "field_label": label,
                        "old_value": old_val,
                        "new_value": new_val,
                        "inspection_state_at_change": rec.state,
                    })
                    changes_for_chatter.append({
                        "label": label,
                        "old": old_val,
                        "new": new_val,
                        "state": rec.state,
                    })

                _post_quality_history_to_chatter(rec, changes_for_chatter)

        return res


class QualityInspectionLineTracked(models.Model):
    _inherit = "quality.inspection.line"

    def write(self, vals):
        History = self.env["quality.inspection.history"]
        snapshots = {}
        tracked_keys = [k for k in vals.keys() if k in TRACKED_LINE_FIELDS]

        if tracked_keys:
            for line in self:
                snapshots[line.id] = {
                    k: _format_value(line, k) for k in tracked_keys
                }

        res = super().write(vals)

        if tracked_keys:
            changes_by_inspection = defaultdict(list)

            for line in self:
                if not line.inspection_id:
                    continue

                old = snapshots.get(line.id, {})
                for fname in tracked_keys:
                    new_val = _format_value(line, fname)
                    old_val = old.get(fname, "")

                    if old_val == new_val:
                        continue

                    label = line._fields[fname].string or fname
                    full_label = "%s — %s" % (line.name or "", label)

                    History.create({
                        "inspection_id": line.inspection_id.id,
                        "line_id": line.id,
                        "field_name": "%s.%s" % (line.name or "Atributo", fname),
                        "field_label": full_label,
                        "old_value": old_val,
                        "new_value": new_val,
                        "inspection_state_at_change": line.inspection_id.state,
                    })

                    changes_by_inspection[line.inspection_id.id].append({
                        "label": full_label,
                        "old": old_val,
                        "new": new_val,
                        "state": line.inspection_id.state,
                    })

            Inspection = self.env["quality.inspection"]
            for inspection_id, changes in changes_by_inspection.items():
                _post_quality_history_to_chatter(
                    Inspection.browse(inspection_id),
                    changes,
                )

        return res```

## ./models/quality_corrective_action.py
```py
# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class QualityCorrectiveAction(models.Model):
    _name = "quality.corrective.action"
    _description = "Acción Correctiva/Preventiva (8D)"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_opened desc, id desc"

    name = fields.Char(
        "Referencia",
        required=True,
        readonly=True,
        default="Nuevo",
        copy=False,
    )

    origin_type = fields.Selection(
        [
            ("inspeccion", "Inspección"),
            ("auditoria_interna", "Auditoría Interna"),
            ("auditoria_externa", "Auditoría Externa"),
            ("devolucion", "Devolución"),
            ("reclamacion", "Reclamación"),
            ("otro", "Otro"),
        ],
        required=True,
        tracking=True,
    )

    defect_type = fields.Selection(
        [
            ("dimensional", "Dimensional"),
            ("apariencia", "Apariencia"),
            ("funcional", "Funcional"),
            ("afecta_funcionalidad", "Afecta Funcionalidad"),
            ("empaque", "Empaque"),
            ("otro", "Otro"),
        ],
        string="Tipo de Defecto",
    )
    defect_other_desc = fields.Char(
        "Descripción de Defecto (Otro)",
        help="Aplica cuando Tipo de Defecto = OTRO",
    )

    origin_description = fields.Text("Descripción del Incumplimiento", required=True)
    origin_inspection_id = fields.Many2one("quality.inspection")
    origin_return_id = fields.Many2one("quality.customer.return")

    responsible_id = fields.Many2one(
        "res.users",
        "Responsable General",
        required=True,
        tracking=True,
    )

    work_team_ids = fields.One2many(
        "quality.work.team",
        "corrective_id",
        string="Equipo de Trabajo",
    )
    action_line_ids = fields.One2many(
        "quality.action.line",
        "corrective_id",
        string="Acciones Específicas",
    )

    containment_actions = fields.Text(
        "D3 - Acciones de Contención",
        help="Acciones inmediatas para contener el problema y proteger al cliente.",
    )
    containment_date = fields.Date("Fecha de Contención")
    containment_responsible_id = fields.Many2one("res.users", "Responsable Contención")

    prevention_actions = fields.Text(
        "D7 - Acciones Preventivas Sistémicas",
        help="Cambios al sistema para evitar recurrencia.",
    )
    prevention_implemented_date = fields.Date("Fecha de Implementación de Prevención")
    prevention_responsible_id = fields.Many2one("res.users", "Responsable Prevención")

    team_recognition = fields.Text("D8 - Reconocimiento al Equipo")
    d8_closing_date = fields.Date("Fecha de Cierre D8")

    why_ids = fields.One2many("quality.5why", "corrective_id", string="5 Por qué")
    ishikawa_ids = fields.One2many(
        "quality.ishikawa",
        "corrective_id",
        string="Diagrama de Ishikawa",
    )

    state = fields.Selection(
        [
            ("borrador", "Borrador"),
            ("evaluacion_calidad", "Evaluación Calidad"),
            ("abierta", "Abierta"),
            ("en_proceso", "En Proceso"),
            ("cerrada", "Cerrada"),
            ("no_procede", "No Procede"),
        ],
        default="borrador",
        required=True,
        tracking=True,
        copy=False,
    )

    no_procede_reason = fields.Text("Motivo No Procede")
    quality_evaluated_by = fields.Many2one("res.users", "Calidad Evaluó", readonly=True)
    quality_evaluated_date = fields.Datetime(readonly=True)

    date_opened = fields.Date(
        "Fecha de Apertura",
        required=True,
        default=fields.Date.context_today,
    )
    date_closed = fields.Date(
        "Fecha de Cierre",
        tracking=True,
        compute="_compute_date_closed",
        store=True,
        readonly=False,
    )

    action_count = fields.Integer(compute="_compute_action_stats")
    action_completed_count = fields.Integer(compute="_compute_action_stats")
    action_overdue_count = fields.Integer(compute="_compute_action_stats")
    progress = fields.Float(compute="_compute_action_stats")

    company_id = fields.Many2one(
        "res.company",
        "Compañía",
        default=lambda s: s.env.company,
    )

    @api.depends("action_line_ids", "action_line_ids.state", "action_line_ids.evidence_ids")
    def _compute_action_stats(self):
        for rec in self:
            lines = rec.action_line_ids
            rec.action_count = len(lines)
            rec.action_completed_count = len(lines.filtered(lambda l: l.state == "completada"))
            rec.action_overdue_count = len(lines.filtered(lambda l: l.state == "vencida"))
            rec.progress = (
                rec.action_completed_count / rec.action_count * 100
                if rec.action_count
                else 0.0
            )

    @api.depends("state", "action_line_ids.date_due", "action_line_ids.state")
    def _compute_date_closed(self):
        """Fecha cierre = fecha más lejana de las acciones."""
        for rec in self:
            # FOLIO-QM-ODOO18-007: todo compute debe asignar valor a cada registro.
            if rec.state == "cerrada":
                dates = [d for d in rec.action_line_ids.mapped("date_due") if d]
                rec.date_closed = max(dates) if dates else (rec.date_closed or fields.Date.today())
            elif rec.state == "no_procede":
                rec.date_closed = rec.date_closed or fields.Date.today()
            else:
                rec.date_closed = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Nuevo") == "Nuevo":
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "quality.corrective.action"
                ) or "Nuevo"
        return super().create(vals_list)

    @api.constrains("defect_type", "defect_other_desc")
    def _check_other_desc(self):
        for rec in self:
            if rec.defect_type == "otro" and not rec.defect_other_desc:
                raise UserError(_("Cuando el tipo de defecto es OTRO, debe describir el defecto."))

    def _check_pestañas_completas(self):
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
                raise UserError(_("No se puede cerrar. Complete: %s") % ", ".join(faltantes))

    def action_evaluate_quality(self):
        for rec in self:
            rec.state = "evaluacion_calidad"
            rec.message_post(
                body=_("Enviado a Evaluación de Calidad."),
                subtype_xmlid="mail.mt_comment",
            )

    def action_quality_evaluated(self):
        for rec in self:
            if rec.state != "evaluacion_calidad":
                raise UserError(
                    _("Solo se puede marcar como evaluada cuando está en estado 'Evaluación Calidad'.")
                )
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
        for rec in self:
            if not rec.quality_evaluated_by:
                raise UserError(_("Debe completar primero la 'Evaluación Calidad' antes de continuar al 8D."))
            rec.state = "abierta"

    def action_in_progress(self):
        for rec in self:
            rec.state = "en_proceso"

    def action_close(self):
        for rec in self:
            rec._check_pestañas_completas()
            pending = rec.action_line_ids.filtered(lambda l: l.state != "completada")
            if pending:
                raise UserError(_("No se puede cerrar: %d acción(es) sin completar.") % len(pending))
            rec.state = "cerrada"

    def action_no_proceed(self):
        for rec in self:
            if not rec.no_procede_reason:
                raise UserError(_("Capture el motivo por el que no procede la acción."))
            rec.state = "no_procede"

    def action_reopen(self):
        for rec in self:
            rec.state = "en_proceso"
            rec.date_closed = False

    def action_print_8d(self):
        return self.env.ref("quality_management.action_report_8d").report_action(self)

    @api.model
    def _cron_check_overdue_actions(self):
        today = fields.Date.today()
        overdue = self.env["quality.action.line"].search(
            [
                ("state", "in", ("pendiente", "en_proceso")),
                ("date_due", "<", today),
            ]
        )
        for line in overdue:
            line.state = "vencida"
            line.delay_days = (today - line.date_due).days
            partners = []
            for member in line.corrective_id.work_team_ids.filtered("notify_progress"):
                if member.user_id.partner_id:
                    partners.append(member.user_id.partner_id.id)
            line.corrective_id.message_post(
                body=_("Acción vencida (%d días): %s — Responsable: %s")
                % (line.delay_days, line.description[:80], line.responsible_id.name),
                partner_ids=list(set(partners)),
                subtype_xmlid="mail.mt_comment",
            )```

## ./models/quality_corrective_extra.py
```py
# -*- coding: utf-8 -*-
"""
Mejoras a 8D / acciones correctivas:
- Si origen = devolución/reclamación → responsable inicial = Ventas.
- Retorno de tarimas en días hábiles (lunes-viernes).
- Bloqueos finales más estrictos al cerrar.
"""
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import timedelta


def _business_days_between(d1, d2):
    """Días hábiles entre dos fechas (lunes=0 .. viernes=4)."""
    if not d1 or not d2:
        return 0
    if d2 < d1:
        d1, d2 = d2, d1
    days = 0
    cur = d1
    while cur <= d2:
        if cur.weekday() < 5:
            days += 1
        cur += timedelta(days=1)
    return days


class QualityCorrectiveActionExtra(models.Model):
    _inherit = "quality.corrective.action"

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            if rec.origin_type in ("devolucion", "reclamacion") and rec.origin_return_id:
                # Si hay vendedor en la SO original, asignarlo
                so = rec.origin_return_id.sale_order_id
                if so and so.user_id and rec.responsible_id != so.user_id:
                    rec.responsible_id = so.user_id
                    rec.message_post(
                        body=_("Responsable inicial reasignado a Ventas: %s")
                        % so.user_id.name,
                        subtype_xmlid="mail.mt_comment")
        return records


class QualityCustomerReturnExtra(models.Model):
    _inherit = "quality.customer.return"

    pallet_return_business_days = fields.Integer(
        "Días Hábiles para Retorno de Tarimas",
        compute="_compute_pallet_return_business_days", store=True)
    pallet_alert_15_business = fields.Boolean(
        "Alerta: >15 días hábiles",
        compute="_compute_pallet_return_business_days", store=True)

    @api.depends("pallet_return_date", "date_received", "pallets_returned")
    def _compute_pallet_return_business_days(self):
        for rec in self:
            if (rec.pallets_returned and rec.pallet_return_date
                    and rec.date_received):
                d = _business_days_between(rec.date_received, rec.pallet_return_date)
                rec.pallet_return_business_days = d
                rec.pallet_alert_15_business = d > 15
            else:
                rec.pallet_return_business_days = 0
                rec.pallet_alert_15_business = False

    def write(self, vals):
        """Bloquear guardado si falta formato de reclamación cuando ya no es borrador."""
        for rec in self:
            target_state = vals.get("state", rec.state)
            if target_state not in ("borrador", "no_procede"):
                claim_pdf = vals.get("claim_format_pdf", rec.claim_format_pdf)
                if not claim_pdf:
                    raise UserError(_(
                        "No se puede guardar la devolución '%s' sin el "
                        "Formato de Reclamación (PDF)."
                    ) % (rec.name or "Nueva"))
        return super().write(vals)
```

## ./models/quality_customer_document_extra.py
```py
# -*- coding: utf-8 -*-
"""
Bloqueos adicionales para Documentos de Cliente:
- write() bloqueado si no hay descripción ni documento cargado y se intenta
  avanzar de borrador.
- Fecha de entrega real al pasar a 'enviado'.
- Actividades automáticas para Calidad al crear.
- Notificación a Ventas al completar.
"""
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import timedelta


class QualityCustomerDocumentExtra(models.Model):
    _inherit = "quality.customer.document"

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for rec in records:
            if rec.responsible_id:
                rec.activity_schedule(
                    "mail.mail_activity_data_todo",
                    date_deadline=rec.date_due or (
                        fields.Date.today() + timedelta(days=5)),
                    summary=_("Atender solicitud de documento: %s") % rec.name,
                    user_id=rec.responsible_id.id)
        return records

    def write(self, vals):
        """Bloquea avance sin descripción ni documento."""
        for rec in self:
            target_state = vals.get("state", rec.state)
            if target_state in ("en_proceso", "completado", "enviado"):
                desc = vals.get("description", rec.description)
                if not desc or not (desc or "").strip():
                    raise UserError(_(
                        "No se puede avanzar el documento '%s' sin descripción."
                    ) % (rec.name or "Nuevo"))
                has_doc = (
                    vals.get("main_pdf", rec.main_pdf)
                    or vals.get("main_image", rec.main_image)
                    or rec.result_document_ids
                    or rec.client_format_ids)
                if not has_doc:
                    raise UserError(_(
                        "No se puede avanzar '%s' sin al menos un documento "
                        "cargado (PDF, imagen o adjunto)."
                    ) % (rec.name or "Nuevo"))
        return super().write(vals)

    def action_complete(self):
        res = super().action_complete()
        for rec in self:
            # Notificar a Ventas (solicitante)
            if rec.requested_by and rec.requested_by.partner_id:
                rec.message_post(
                    body=_("📄 Documento listo para envío al cliente."),
                    partner_ids=[rec.requested_by.partner_id.id],
                    subtype_xmlid="mail.mt_comment")
        return res

    def action_send(self):
        res = super().action_send()
        for rec in self:
            # Fecha de entrega real
            if not rec.date_completed:
                rec.date_completed = fields.Date.today()
        return res
```

## ./models/quality_customer_document.py
```py
# -*- coding: utf-8 -*-
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
```

## ./models/quality_customer_return.py
```py
# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


def _business_days_between(date_start, date_end):
    """Cuenta días hábiles lunes-viernes entre dos fechas, incluyendo extremos."""
    if not date_start or not date_end:
        return 0
    if date_end < date_start:
        date_start, date_end = date_end, date_start

    days = 0
    current = date_start
    while current <= date_end:
        if current.weekday() < 5:
            days += 1
        current += timedelta(days=1)
    return days


class QualityCustomerReturn(models.Model):
    _name = "quality.customer.return"
    _description = "Devolución de Cliente"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_received desc, id desc"

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
        "Orden de Venta Original",
        tracking=True,
    )
    defect_type = fields.Selection(
        [
            ("dimensional", "Dimensional"),
            ("apariencia", "Apariencia"),
            ("funcional", "Funcional"),
            ("empaque", "Empaque"),
            ("otro", "Otro"),
        ],
        required=True,
        tracking=True,
    )
    defect_other_desc = fields.Char("Descripción Defecto Otro")
    defect_pieces = fields.Integer("Piezas con Defecto", required=True)
    return_reason = fields.Text("Motivo de la Devolución", required=True)
    production_date = fields.Date("Fecha de Producción", required=True)
    delivery_date = fields.Date("Fecha de Entrega Producción/Fabricación")

    evidence_ids = fields.Many2many(
        "ir.attachment",
        "quality_return_evidence_rel",
        "return_id",
        "attachment_id",
        string="Evidencia Fotográfica",
        required=True,
    )

    evidence_pdf = fields.Binary("Reporte de Evidencia (PDF)", attachment=True)
    evidence_pdf_name = fields.Char()

    pallets_returned = fields.Boolean("Se Regresan Tarimas")
    pallet_return_date = fields.Date("Fecha Retorno de Tarimas")

    claim_format_pdf = fields.Binary(
        "Formato de Reclamación (PDF)",
        attachment=True,
        required=False,
    )
    claim_format_pdf_name = fields.Char()

    affects_functionality = fields.Boolean(
        "Afecta Funcionalidad",
        tracking=True,
    )
    corrective_action_id = fields.Many2one(
        "quality.corrective.action",
        "8D Generado",
        readonly=True,
        tracking=True,
    )

    sales_manager_justification = fields.Text(
        "Motivo Comercial - Gerente de Ventas",
        help=(
            "Cuando comercialmente se decide proceder con devolución/reposición "
            "pese al bloqueo (>30 días)."
        ),
    )
    sales_manager_id = fields.Many2one(
        "res.users",
        "Gerente de Ventas Autorizó",
    )

    state = fields.Selection(
        [
            ("borrador", "Borrador"),
            ("evaluacion_ventas", "Evaluación Ventas"),
            ("evaluacion_calidad", "Evaluación Calidad"),
            ("en_8d", "En 8D"),
            ("cerrada", "Cerrada"),
            ("no_procede", "No Procede"),
        ],
        default="borrador",
        required=True,
        tracking=True,
        copy=False,
    )

    date_received = fields.Date(
        "Fecha de Recepción",
        required=True,
        default=fields.Date.context_today,
    )
    days_since_production = fields.Integer(
        compute="_compute_days_since_production",
        store=True,
    )
    is_within_period = fields.Boolean(
        compute="_compute_days_since_production",
        store=True,
    )

    pallet_alert_15 = fields.Boolean(
        "Alerta: Retorno >15 días hábiles",
        compute="_compute_pallet_alert_15",
        store=True,
    )

    company_id = fields.Many2one(
        "res.company",
        "Compañía",
        default=lambda s: s.env.company,
    )

    @api.depends("production_date", "date_received")
    def _compute_days_since_production(self):
        for rec in self:
            if rec.production_date and rec.date_received:
                delta = (rec.date_received - rec.production_date).days
                rec.days_since_production = delta
                # FOLIO-QM-ODOO18-012: el periodo válido es hasta 30 días inclusive;
                # solo debe bloquear cuando excede 30 días.
                rec.is_within_period = delta <= 30
            else:
                rec.days_since_production = 0
                rec.is_within_period = True

    @api.depends("pallet_return_date", "date_received", "pallets_returned")
    def _compute_pallet_alert_15(self):
        for rec in self:
            if rec.pallets_returned and rec.pallet_return_date and rec.date_received:
                # FOLIO-QM-ODOO18-013: el aviso de tarimas debe calcularse en días hábiles,
                # no en días calendario, porque la vista y el requerimiento hablan de hábiles.
                business_days = _business_days_between(
                    rec.date_received,
                    rec.pallet_return_date,
                )
                rec.pallet_alert_15 = business_days > 15
            else:
                rec.pallet_alert_15 = False

    @api.constrains("defect_type", "defect_other_desc")
    def _check_other(self):
        for rec in self:
            if rec.defect_type == "otro" and not rec.defect_other_desc:
                raise UserError(_("Tipo de defecto OTRO requiere descripción."))

    @api.constrains("defect_pieces")
    def _check_defect_pieces(self):
        for rec in self:
            # FOLIO-QM-ODOO18-014: se bloquean devoluciones con cantidad inválida.
            if rec.defect_pieces <= 0:
                raise UserError(_("Las piezas con defecto deben ser mayores a cero."))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Nuevo") == "Nuevo":
                vals["name"] = (
                    self.env["ir.sequence"].next_by_code("quality.customer.return")
                    or "Nuevo"
                )
        return super().create(vals_list)

    def _check_required_attachments(self):
        for rec in self:
            if not rec.evidence_ids:
                raise UserError(_("Debe adjuntar evidencia fotográfica."))
            if not rec.claim_format_pdf:
                raise UserError(_("Debe adjuntar el Formato de Reclamación (PDF)."))

    def action_submit_sales(self):
        for rec in self:
            rec._check_required_attachments()

            if not rec.is_within_period and not rec.sales_manager_justification:
                rec.state = "no_procede"
                rec.message_post(
                    body=_(
                        "Devolución NO PROCEDE: %d días desde producción (>30). "
                        "Capture el motivo comercial del Gerente de Ventas si desea proceder."
                    )
                    % rec.days_since_production,
                    subtype_xmlid="mail.mt_comment",
                )
                continue

            rec.state = "evaluacion_ventas"

    def action_authorize_commercial(self):
        """Permite continuar pese a >30 días si Gerente de Ventas lo justifica."""
        for rec in self:
            if not rec.sales_manager_justification:
                raise UserError(_("Capture el motivo comercial del Gerente de Ventas."))

            rec.sales_manager_id = self.env.user
            rec.state = "evaluacion_ventas"
            rec.message_post(
                body=_("Autorización comercial por %s. Motivo: %s")
                % (self.env.user.name, rec.sales_manager_justification),
                subtype_xmlid="mail.mt_comment",
            )

    def action_submit_quality(self):
        for rec in self:
            rec.state = "evaluacion_calidad"

            users = self.env.ref(
                "quality_management.group_quality_manager",
                raise_if_not_found=False,
            )
            manager_users = users.users if users else self.env["res.users"]

            for user in manager_users:
                rec.activity_schedule(
                    "mail.mail_activity_data_todo",
                    date_deadline=fields.Date.today() + timedelta(days=3),
                    summary=_("Evaluar devolución: %s") % rec.name,
                    user_id=user.id,
                )

            if rec.pallets_returned:
                rec.message_post(
                    body=_(
                        "Tarimas retornadas. Logística/Producción: "
                        "evaluar físicamente de inmediato."
                    ),
                    subtype_xmlid="mail.mt_comment",
                )

            if rec.pallet_alert_15:
                rec.message_post(
                    body=_(
                        "Alerta: el retorno de tarimas se programó a más de "
                        "15 días hábiles desde recepción."
                    ),
                    subtype_xmlid="mail.mt_comment",
                )

    def action_generate_8d(self):
        for rec in self:
            corrective = self.env["quality.corrective.action"].create(
                {
                    "origin_type": "devolucion",
                    "defect_type": rec.defect_type,
                    "defect_other_desc": rec.defect_other_desc,
                    "origin_description": _(
                        "Devolución de cliente: %s\n"
                        "Tipo de defecto: %s\n"
                        "Piezas: %d\n"
                        "Motivo: %s"
                    )
                    % (
                        rec.partner_id.name,
                        dict(rec._fields["defect_type"].selection).get(
                            rec.defect_type,
                            "",
                        ),
                        rec.defect_pieces,
                        rec.return_reason,
                    ),
                    "origin_return_id": rec.id,
                    "responsible_id": self.env.user.id,
                }
            )
            rec.corrective_action_id = corrective.id
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
        ).report_action(self)```

## ./models/quality_drawing_modification.py
```py
# -*- coding: utf-8 -*-
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
```

## ./models/quality_drawing_release.py
```py
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
    accepted_by_quality_date = fields.Datetime(readonly=True)
    accepted_by_sales = fields.Many2one(
        "res.users",
        "Ventas Aceptó",
        readonly=True,
    )
    accepted_by_sales_date = fields.Datetime(readonly=True)
    accepted_by_design = fields.Many2one(
        "res.users",
        "Diseño Aceptó",
        readonly=True,
    )
    accepted_by_design_date = fields.Datetime(readonly=True)

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
        ).report_action(self)```

## ./models/quality_hardening.py
```py
# -*- coding: utf-8 -*-
import re
import unicodedata
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


# FOLIO-QM-ODOO18-074:
# Secuencia obligatoria solicitada para impedir saltos de flujo.
PROCESS_SEQUENCE = [
    "octagono",
    "guillotina",
    "pegado",
    "laminadora",
    "remanejo",
    "troquelado_plano",
]

# FOLIO-QM-ODOO18-072 / 074:
# Alias exactos que no se pueden capturar como atributos adicionales
# cuando el proceso ya los captura en Medidas y Propiedades.
RESERVED_MEASURE_FIELD_ALIASES = {
    "largo": ("Largo", ("show_largo",)),
    "largo_mm": ("Largo", ("show_largo",)),
    "ancho": ("Ancho", ("show_ancho",)),
    "ancho_mm": ("Ancho", ("show_ancho",)),
    "espesor": ("Espesor", ("show_espesor",)),
    "espesor_mm": ("Espesor", ("show_espesor",)),
    "espesor_in": ("Espesor", ("show_espesor",)),
    "hexagono": ("Hexágono", ("show_hexagono", "show_tipo_hexagono")),
    "hexagono_tipo": ("Hexágono", ("show_hexagono", "show_tipo_hexagono")),
    "tipo_hexagono": ("Tipo de Hexágono", ("show_hexagono", "show_tipo_hexagono")),
    "tipo_de_hexagono": ("Tipo de Hexágono", ("show_hexagono", "show_tipo_hexagono")),
    "resistencia": ("Resistencia", ("show_resistencia",)),
    "resistencia_lbf": ("Resistencia", ("show_resistencia",)),
    "apariencia": ("Apariencia", ("show_apariencia",)),
    "humedad": ("Humedad", ("show_humedad",)),
    "humedad_pct": ("Humedad", ("show_humedad",)),
    "porcentaje_humedad": ("Humedad", ("show_humedad",)),
    "pegado": ("Resultado de Pegado", ("show_pegado",)),
    "resultado_pegado": ("Resultado de Pegado", ("show_pegado",)),
    "resultado_de_pegado": ("Resultado de Pegado", ("show_pegado",)),
    "retiramiento": ("Retiramiento", ("show_retiramiento",)),
    "restiramiento": ("Retiramiento", ("show_retiramiento",)),
    "reticula": ("Retícula", ("show_retiramiento",)),
    "reticula_extendida": ("Retícula Extendida", ("show_retiramiento",)),
    "calibracion": ("Calibración", ("show_calibracion",)),
    "engomado": ("Engomado", ("show_engomado",)),
    "alineacion": ("Alineación", ("show_alineacion",)),
}

# Compatibilidad con código anterior.
RESERVED_MEASURE_ATTRS = set(RESERVED_MEASURE_FIELD_ALIASES)

# FOLIO-QM-ODOO18-070 / FOLIO-QM-ODOO18-071:
# Procesos que solo aceptan atributos adicionales binarios Cumple/No Cumple.
# No permiten N/A, OK/NO OK/N/A, atributos de selección ni atributos numéricos.
STRICT_BINARY_RESULT_PROCESS_CODES = {
    "acabado_empaque",
    "impresion",
}

# FOLIO-QM-ODOO18-075:
# En Octágono estos conceptos son campos nativos obligatorios o no aplican
# en el proceso; no deben duplicarse como atributos adicionales.
OCTAGONO_RESERVED_FIELD_ALIASES = {
    "ancho": "Ancho",
    "ancho_mm": "Ancho",
    "hexagono": "Hexágono",
    "hexagono_tipo": "Hexágono",
    "tipo_hexagono": "Hexágono",
    "tipo_de_hexagono": "Hexágono",
    "numero_corrida": "Número de Corrida",
    "numero_de_corrida": "Número de Corrida",
    "corrida": "Número de Corrida",
    "papel": "Papel",
    "ancho_papel": "Ancho de Papel",
    "papel_ancho": "Ancho de Papel",
    "gramaje": "Gramaje de Papel",
    "gramaje_papel": "Gramaje de Papel",
    "papel_gramaje": "Gramaje de Papel",
    "proveedor": "Proveedor de Papel",
    "proveedor_papel": "Proveedor de Papel",
    "proveedor_de_rollos": "Proveedor de Rollos",
    "adhesivo": "Adhesivo",
    "lote_1": "Lote 1 Adhesivo",
    "lote1": "Lote 1 Adhesivo",
    "adhesivo_lote1": "Lote 1 Adhesivo",
    "lote_2": "Lote 2 Adhesivo",
    "lote2": "Lote 2 Adhesivo",
    "adhesivo_lote2": "Lote 2 Adhesivo",
    "calibracion": "Calibración",
    "engomado": "Engomado",
    "alineacion": "Alineación",
    "corte_guillotina": "Corte de Guillotina",
    "corte_de_guillotina": "Corte de Guillotina",
    "retiramiento": "Retiramiento no aplica en Octágono",
    "restiramiento": "Retiramiento no aplica en Octágono",
    "reticula": "Retiramiento no aplica en Octágono",
    "reticula_extendida": "Retiramiento no aplica en Octágono",
    "espesor": "Espesor no aplica en Octágono",
    "espesor_mm": "Espesor no aplica en Octágono",
    "espesor_in": "Espesor no aplica en Octágono",
}


def _slug(value):
    value = value or ""
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    value = re.sub(r"[^a-zA-Z0-9]+", "_", value.lower()).strip("_")
    return value


def _reserved_measure_label_for_inspection(inspection, normalized_key):
    if not inspection or not normalized_key:
        return False

    # FOLIO-QM-ODOO18-075:
    # Octágono tiene una matriz fija de captura. Estos conceptos no deben
    # aparecer como atributos adicionales, aunque la configuración legacy
    # del proceso aún no haya sido actualizada en la base.
    if inspection.process_code == "octagono":
        oct_label = OCTAGONO_RESERVED_FIELD_ALIASES.get(normalized_key)
        if oct_label:
            return oct_label

    alias = RESERVED_MEASURE_FIELD_ALIASES.get(normalized_key)
    if not alias:
        return False

    label, flag_names = alias
    if any(getattr(inspection, flag_name, False) for flag_name in flag_names):
        return label

    return False


class QualityProcessTypeHardening(models.Model):
    _inherit = "quality.process.type"

    capture_mode = fields.Selection(
        [
            ("full", "Medidas + Propiedades + Atributos"),
            ("additional_only", "Solo Atributos Adicionales"),
        ],
        default="full",
        required=True,
    )
    require_measures = fields.Boolean(
        "Requerir Medidas/Propiedades para liberar",
        default=True,
    )
    require_additional_attributes = fields.Boolean(
        "Requerir Atributos Adicionales para liberar",
        default=True,
    )
    zero_value_blocking = fields.Boolean(
        "Bloquear valores numéricos en cero",
        default=True,
    )


class QualityAttributeTemplateHardening(models.Model):
    _inherit = "quality.attribute.template"

    # FOLIO-QM-ODOO18-075: soporta rangos finos como 0.0010 en plantillas numéricas.
    min_value = fields.Float("Valor Mínimo", digits=(16, 4))
    max_value = fields.Float("Valor Máximo", digits=(16, 4))

    normalized_name = fields.Char(
        "Nombre Normalizado",
        compute="_compute_normalized_name",
        store=True,
        index=True,
    )
    capture_zone = fields.Selection(
        [
            ("additional", "Atributos Adicionales"),
            ("measures", "Medidas y Propiedades"),
            ("ranurado", "Ranurado"),
            ("troquelado", "Troquelado"),
            ("production", "Datos de Producción"),
        ],
        default="additional",
        required=True,
    )
    result_mode = fields.Selection(
        [
            ("cumple", "Cumple / No Cumple / N/A"),
            ("ok", "OK / NO OK / N/A"),
        ],
        default="cumple",
        required=True,
    )
    allow_zero = fields.Boolean("Permitir valor cero", default=False)

    @api.depends("name")
    def _compute_normalized_name(self):
        for rec in self:
            rec.normalized_name = _slug(rec.name)

    def _target_process_is_strict_binary(self, vals=None):
        self.ensure_one()
        vals = vals or {}

        if "process_type_id" in vals:
            process = (
                self.env["quality.process.type"].browse(vals["process_type_id"])
                if vals.get("process_type_id")
                else False
            )
        else:
            process = self.process_type_id

        return bool(process and process.code in STRICT_BINARY_RESULT_PROCESS_CODES)

    def _normalize_template_vals_for_strict_binary(self, vals):
        vals = dict(vals or {})
        vals.update({
            "attribute_type": "boolean",
            "capture_zone": "additional",
            "result_mode": "cumple",
            "allow_zero": False,
            "min_value": 0.0,
            "max_value": 0.0,
            "unit": False,
            "selection_options": False,
        })
        return vals

    @api.onchange("process_type_id", "attribute_type", "result_mode")
    def _onchange_strict_binary_template(self):
        for rec in self:
            if rec.process_type_id and rec.process_type_id.code in STRICT_BINARY_RESULT_PROCESS_CODES:
                # FOLIO-QM-ODOO18-071: Impresión y Acabado no permiten configurar OK/NO OK/N/A, selección ni numéricos.
                rec.attribute_type = "boolean"
                rec.capture_zone = "additional"
                rec.result_mode = "cumple"
                rec.allow_zero = False
                rec.min_value = 0.0
                rec.max_value = 0.0
                rec.unit = False
                rec.selection_options = False

    @api.model_create_multi
    def create(self, vals_list):
        clean_vals_list = []
        Process = self.env["quality.process.type"]

        for vals in vals_list:
            vals = dict(vals or {})
            process = (
                Process.browse(vals["process_type_id"])
                if vals.get("process_type_id")
                else False
            )
            if process and process.code in STRICT_BINARY_RESULT_PROCESS_CODES:
                vals = self._normalize_template_vals_for_strict_binary(vals)
            clean_vals_list.append(vals)

        return super().create(clean_vals_list)

    def write(self, vals):
        vals = dict(vals or {})
        if not vals:
            return super().write(vals)

        strict_records = self.filtered(lambda rec: rec._target_process_is_strict_binary(vals))
        other_records = self - strict_records

        result = True
        if other_records:
            result = super(QualityAttributeTemplateHardening, other_records).write(vals) and result

        if strict_records:
            strict_vals = self._normalize_template_vals_for_strict_binary(vals)
            result = super(QualityAttributeTemplateHardening, strict_records).write(strict_vals) and result

        return result


class QualityInspectionLineHardening(models.Model):
    _inherit = "quality.inspection.line"

    # FOLIO-QM-ODOO18-075:
    # Permite capturas finas como 0.0010 en calibración sin que la lista
    # editable ni los reportes redondeen visualmente a cero.
    value_float = fields.Float("Valor Numérico", digits=(16, 4))
    min_value = fields.Float("Mínimo", digits=(16, 4))
    max_value = fields.Float("Máximo", digits=(16, 4))

    normalized_name = fields.Char(
        "Nombre Normalizado",
        compute="_compute_normalized_name",
        store=True,
        index=True,
    )
    capture_zone = fields.Selection(
        [
            ("additional", "Atributos Adicionales"),
            ("measures", "Medidas y Propiedades"),
            ("ranurado", "Ranurado"),
            ("troquelado", "Troquelado"),
            ("production", "Datos de Producción"),
        ],
        default="additional",
        required=True,
    )
    result_mode = fields.Selection(
        [
            ("cumple", "Cumple / No Cumple / N/A"),
            ("ok", "OK / NO OK / N/A"),
        ],
        default="cumple",
        required=True,
    )

    # FOLIO-QM-ODOO18-018: se extiende el campo existente con N/A sin redefinirlo
    # por completo, evitando conflictos de upgrade en Odoo 18.
    value_cumple = fields.Selection(
        selection_add=[("na", "N/A")],
        ondelete={"na": "set default"},
        default="na",
    )
    value_ok = fields.Selection(
        [
            ("ok", "OK"),
            ("no_ok", "NO OK"),
            ("na", "N/A"),
        ],
        string="OK/NO OK/N/A",
        default="na",
    )
    result = fields.Selection(
        selection_add=[
            ("ok", "OK"),
            ("no_ok", "NO OK"),
        ],
        ondelete={
            "ok": "set default",
            "no_ok": "set default",
        },
    )
    allow_zero = fields.Boolean("Permitir cero")

    # FOLIO-QM-ODOO18-070 / FOLIO-QM-ODOO18-071:
    # Permite que vistas, validaciones y reportes identifiquen líneas pertenecientes
    # a procesos estrictamente Cumple/No Cumple.
    process_code = fields.Char(
        related="inspection_id.process_code",
        store=True,
        readonly=True,
    )
    strict_binary_result = fields.Boolean(
        compute="_compute_strict_binary_result",
        store=False,
    )

    def init(self):
        """
        FOLIO-QM-ODOO18-071:
        Normaliza líneas existentes de Impresión y Acabado/Empaque durante upgrade.
        Esto corrige capturas previas donde las líneas quedaron como OK/NO OK/N/A,
        numéricas o con Resultado = N/A.
        """
        super().init()
        cr = self.env.cr

        cr.execute("""
            SELECT EXISTS (
                SELECT 1
                  FROM information_schema.tables
                 WHERE table_name = 'quality_inspection_line'
            )
        """)
        line_table_exists = cr.fetchone()[0]

        cr.execute("""
            SELECT EXISTS (
                SELECT 1
                  FROM information_schema.tables
                 WHERE table_name = 'quality_inspection'
            )
        """)
        inspection_table_exists = cr.fetchone()[0]

        if not line_table_exists or not inspection_table_exists:
            return

        cr.execute("""
            SELECT column_name
              FROM information_schema.columns
             WHERE table_name = 'quality_inspection_line'
        """)
        line_columns = {row[0] for row in cr.fetchall()}

        required_line_columns = {
            "inspection_id",
            "attribute_type",
            "capture_zone",
            "result_mode",
            "value_float",
            "value_char",
            "value_cumple",
            "value_ok",
            "result",
            "min_value",
            "max_value",
            "unit",
            "allow_zero",
        }
        if not required_line_columns.issubset(line_columns):
            return

        cr.execute("""
            SELECT column_name
              FROM information_schema.columns
             WHERE table_name = 'quality_inspection'
        """)
        inspection_columns = {row[0] for row in cr.fetchall()}

        if "process_code" not in inspection_columns:
            return

        cr.execute("""
            UPDATE quality_inspection_line AS line
               SET attribute_type = 'boolean',
                   capture_zone = 'additional',
                   result_mode = 'cumple',
                   value_float = 0,
                   value_char = NULL,
                   value_ok = NULL,
                   min_value = 0,
                   max_value = 0,
                   unit = NULL,
                   allow_zero = FALSE,
                   value_cumple = CASE
                       WHEN line.value_cumple IN ('cumple', 'no_cumple') THEN line.value_cumple
                       WHEN line.result IN ('cumple', 'no_cumple') THEN line.result
                       ELSE NULL
                   END,
                   result = CASE
                       WHEN line.value_cumple IN ('cumple', 'no_cumple') THEN line.value_cumple
                       WHEN line.result IN ('cumple', 'no_cumple') THEN line.result
                       ELSE NULL
                   END
              FROM quality_inspection AS inspection
             WHERE line.inspection_id = inspection.id
               AND inspection.process_code IN ('acabado_empaque', 'impresion')
        """)

    @api.depends("inspection_id.process_code")
    def _compute_strict_binary_result(self):
        for line in self:
            line.strict_binary_result = (
                line.inspection_id.process_code in STRICT_BINARY_RESULT_PROCESS_CODES
                if line.inspection_id
                else False
            )

    def _is_strict_binary_result_line(self):
        self.ensure_one()
        return bool(
            self.inspection_id
            and self.inspection_id.process_code in STRICT_BINARY_RESULT_PROCESS_CODES
        )

    def _strict_binary_process_display_name(self):
        self.ensure_one()
        if self.inspection_id and self.inspection_id.process_type_id:
            return self.inspection_id.process_type_id.display_name
        return _("Este proceso")

    def _normalize_vals_for_strict_binary_line(self, vals, reset_missing=False):
        vals = dict(vals or {})

        vals.update({
            "attribute_type": "boolean",
            "capture_zone": "additional",
            "result_mode": "cumple",
            "value_ok": False,
            "value_float": 0.0,
            "value_char": False,
            "min_value": 0.0,
            "max_value": 0.0,
            "unit": False,
            "allow_zero": False,
        })

        if reset_missing or "value_cumple" in vals:
            if vals.get("value_cumple") not in ("cumple", "no_cumple"):
                vals["value_cumple"] = False

        if reset_missing or "result" in vals:
            if vals.get("result") not in ("cumple", "no_cumple"):
                vals["result"] = False

        if vals.get("value_cumple") in ("cumple", "no_cumple"):
            vals["result"] = vals["value_cumple"]
        elif vals.get("result") in ("cumple", "no_cumple"):
            vals["value_cumple"] = vals["result"]

        return vals

    def _clear_strict_na_values_hardening(self):
        for line in self:
            if not line._is_strict_binary_result_line():
                continue

            vals = {}
            if line.attribute_type != "boolean":
                vals["attribute_type"] = "boolean"
            if line.capture_zone != "additional":
                vals["capture_zone"] = "additional"
            if line.result_mode != "cumple":
                vals["result_mode"] = "cumple"
            if line.value_ok:
                vals["value_ok"] = False
            if line.value_float:
                vals["value_float"] = 0.0
            if line.value_char:
                vals["value_char"] = False
            if line.min_value:
                vals["min_value"] = 0.0
            if line.max_value:
                vals["max_value"] = 0.0
            if line.unit:
                vals["unit"] = False
            if line.allow_zero:
                vals["allow_zero"] = False

            if line.value_cumple == "na":
                vals["value_cumple"] = False
            if line.result == "na":
                vals["result"] = False

            if line.value_cumple in ("cumple", "no_cumple") and line.result != line.value_cumple:
                vals["result"] = line.value_cumple
            elif line.result in ("cumple", "no_cumple") and line.value_cumple != line.result:
                vals["value_cumple"] = line.result

            if vals:
                line.with_context(skip_strict_binary_cleanup=True).write(vals)

    @api.depends("name")
    def _compute_normalized_name(self):
        for line in self:
            line.normalized_name = _slug(line.name)

    @api.model_create_multi
    def create(self, vals_list):
        clean_vals_list = []
        Inspection = self.env["quality.inspection"]

        for vals in vals_list:
            vals = dict(vals or {})
            inspection = (
                Inspection.browse(vals["inspection_id"])
                if vals.get("inspection_id")
                else False
            )
            if inspection and inspection.process_code in STRICT_BINARY_RESULT_PROCESS_CODES:
                vals = self._normalize_vals_for_strict_binary_line(vals, reset_missing=True)
            clean_vals_list.append(vals)

        records = super().create(clean_vals_list)
        records._clear_strict_na_values_hardening()
        return records

    def write(self, vals):
        vals = dict(vals or {})
        if not vals:
            return super().write(vals)

        if not self.env.context.get("skip_strict_binary_cleanup"):
            writes_na = any(
                vals.get(field_name) == "na"
                for field_name in ("value_cumple", "value_ok", "result")
            )
            if writes_na:
                for line in self:
                    if line._is_strict_binary_result_line():
                        raise ValidationError(_(
                            "%s no permite N/A. Seleccione únicamente Cumple o No Cumple."
                        ) % line._strict_binary_process_display_name())

        strict_lines = self.filtered(lambda line: line._is_strict_binary_result_line())
        other_lines = self - strict_lines

        res = True
        if other_lines:
            res = super(QualityInspectionLineHardening, other_lines).write(vals) and res

        if strict_lines:
            strict_vals = self._normalize_vals_for_strict_binary_line(vals, reset_missing=False)
            res = super(QualityInspectionLineHardening, strict_lines).write(strict_vals) and res

        if not self.env.context.get("skip_strict_binary_cleanup"):
            self._clear_strict_na_values_hardening()

        return res

    @api.onchange("attribute_template_id")
    def _onchange_template_hardening(self):
        for line in self:
            template = line.attribute_template_id
            if not template:
                continue

            line.name = template.name
            line.attribute_type = template.attribute_type
            line.capture_zone = template.capture_zone
            line.result_mode = template.result_mode
            line.min_value = template.min_value
            line.max_value = template.max_value
            line.unit = template.unit
            line.allow_zero = template.allow_zero

            if line._is_strict_binary_result_line():
                # FOLIO-QM-ODOO18-071: Impresión y Acabado se fuerzan a Cumple/No Cumple.
                line.attribute_type = "boolean"
                line.capture_zone = "additional"
                line.result_mode = "cumple"
                line.value_ok = False
                line.value_float = 0.0
                line.value_char = False
                line.min_value = 0.0
                line.max_value = 0.0
                line.unit = False
                line.allow_zero = False
                if line.value_cumple == "na":
                    line.value_cumple = False
                if line.result == "na":
                    line.result = False

    @api.onchange("attribute_type", "result_mode")
    def _onchange_strict_binary_attribute_config(self):
        for line in self:
            if not line._is_strict_binary_result_line():
                continue

            warning = False
            if line.attribute_type != "boolean" or line.result_mode != "cumple":
                warning = True

            line.attribute_type = "boolean"
            line.capture_zone = "additional"
            line.result_mode = "cumple"
            line.value_ok = False
            line.value_float = 0.0
            line.value_char = False
            line.min_value = 0.0
            line.max_value = 0.0
            line.unit = False
            line.allow_zero = False
            if line.value_cumple == "na":
                line.value_cumple = False
            if line.result == "na":
                line.result = False

            if warning:
                return {
                    "warning": {
                        "title": _("Configuración no permitida"),
                        "message": _(
                            "%s solo permite atributos adicionales de tipo Cumple/No Cumple."
                        ) % line._strict_binary_process_display_name(),
                    }
                }

    @api.onchange("value_float", "min_value", "max_value", "attribute_type")
    def _onchange_evaluate_result_hardening(self):
        for line in self:
            if line._is_strict_binary_result_line():
                if line.attribute_type != "boolean":
                    line.attribute_type = "boolean"
                    line.capture_zone = "additional"
                    line.result_mode = "cumple"
                    line.value_float = 0.0
                    line.min_value = 0.0
                    line.max_value = 0.0
                    line.unit = False
                    line.result = line.value_cumple if line.value_cumple in ("cumple", "no_cumple") else False
                continue

            if line.attribute_type != "float":
                continue

            if not line.value_float and not line.allow_zero:
                line.result = "na"
                continue

            if line.min_value and line.value_float < line.min_value:
                line.result = "no_cumple"
            elif line.max_value and line.value_float > line.max_value:
                line.result = "no_cumple"
            else:
                line.result = "cumple"

    @api.onchange("value_cumple", "attribute_type", "result_mode")
    def _onchange_value_cumple_hardening(self):
        for line in self:
            if line.attribute_type == "boolean" and line.result_mode == "cumple":
                if line._is_strict_binary_result_line():
                    if line.value_cumple == "na":
                        line.value_cumple = False
                        line.result = False
                        return {
                            "warning": {
                                "title": _("Valor no permitido"),
                                "message": _(
                                    "%s no permite N/A. Seleccione Cumple o No Cumple."
                                ) % line._strict_binary_process_display_name(),
                            }
                        }
                    line.result = line.value_cumple or False
                else:
                    line.result = line.value_cumple or "na"

    @api.onchange("value_ok", "attribute_type", "result_mode")
    def _onchange_value_ok_hardening(self):
        for line in self:
            if line._is_strict_binary_result_line():
                if line.value_ok:
                    line.value_ok = False
                    line.result_mode = "cumple"
                    line.attribute_type = "boolean"
                    return {
                        "warning": {
                            "title": _("Modo no permitido"),
                            "message": _(
                                "%s no permite OK/NO OK/N/A. Use únicamente Cumple o No Cumple."
                            ) % line._strict_binary_process_display_name(),
                        }
                    }
                continue

            if line.attribute_type == "boolean" and line.result_mode == "ok":
                line.result = line.value_ok or "na"

    @api.constrains(
        "inspection_id",
        "sample_release_id",
        "normalized_name",
        "capture_zone",
    )
    def _check_duplicate_attribute_hardening(self):
        for line in self:
            if not line.normalized_name:
                continue

            domain = [
                ("id", "!=", line.id),
                ("normalized_name", "=", line.normalized_name),
                ("capture_zone", "=", line.capture_zone),
            ]

            if line.inspection_id:
                domain.append(("inspection_id", "=", line.inspection_id.id))
            elif line.sample_release_id:
                domain.append(("sample_release_id", "=", line.sample_release_id.id))
            else:
                continue

            if self.search_count(domain):
                raise ValidationError(
                    _("Atributo duplicado: '%s'. No se permite repetir atributos.")
                    % line.name
                )

    @api.constrains("name", "normalized_name", "capture_zone", "inspection_id")
    def _check_reserved_measure_attribute_line_hardening(self):
        """
        FOLIO-QM-ODOO18-072:
        Evita capturar en Atributos Adicionales conceptos que ya existen
        en Medidas y Propiedades del proceso actual.
        """
        for line in self:
            if not line.inspection_id or line.capture_zone != "additional":
                continue

            key = line.normalized_name or _slug(line.name)
            duplicated_label = _reserved_measure_label_for_inspection(
                line.inspection_id,
                key,
            )
            if duplicated_label:
                raise ValidationError(_(
                    "No puede capturar '%s' como Atributo Adicional porque "
                    "ya existe como campo nativo del proceso o no aplica en este proceso."
                ) % duplicated_label)

    @api.constrains("attribute_type", "result_mode", "capture_zone", "inspection_id")
    def _check_strict_binary_attribute_config(self):
        for line in self:
            if not line._is_strict_binary_result_line():
                continue

            if (
                line.attribute_type != "boolean"
                or line.result_mode != "cumple"
                or line.capture_zone != "additional"
            ):
                raise ValidationError(_(
                    "%s solo permite atributos adicionales de tipo Cumple/No Cumple."
                ) % line._strict_binary_process_display_name())

    @api.constrains("value_float", "attribute_type", "allow_zero", "result")
    def _check_zero_numeric_hardening(self):
        for line in self:
            if line._is_strict_binary_result_line():
                continue

            parent_state = (
                line.inspection_id.state
                if line.inspection_id
                else line.sample_release_id.state
                if line.sample_release_id
                else False
            )
            if parent_state in ("borrador", False):
                continue

            if (
                line.attribute_type == "float"
                and not line.allow_zero
                and not line.value_float
                and line.result != "na"
            ):
                raise ValidationError(
                    _(
                        "El atributo numérico '%s' no puede quedar en cero. "
                        "Capture el valor real o marque N/A."
                    )
                    % line.name
                )


class QualityInspectionRanuradoHardening(models.Model):
    _inherit = "quality.inspection.ranurado"

    concepto = fields.Char("Concepto", default="Largo")
    unidad = fields.Selection(
        selection_add=[("cm", "cm")],
        ondelete={"cm": "set default"},
    )
    resultado = fields.Selection(
        selection_add=[("na", "N/A")],
        ondelete={"na": "set default"},
    )

    @api.constrains("medida", "resultado")
    def _check_medida_gt_zero(self):
        for rec in self:
            if rec.resultado != "na" and rec.medida <= 0:
                raise ValidationError(
                    _("La medida debe ser mayor a cero o marcarse como N/A.")
                )


class QualityInspectionTroqueladoHardening(models.Model):
    _inherit = "quality.inspection.troquelado"

    unidad = fields.Selection(
        [
            ("mm", "mm"),
            ("cm", "cm"),
            ("in", "in"),
        ],
        default="mm",
        required=True,
    )
    resultado = fields.Selection(
        selection_add=[("na", "N/A")],
        ondelete={"na": "set default"},
    )

    @api.constrains("medida", "resultado")
    def _check_medida_gt_zero(self):
        for rec in self:
            if rec.resultado != "na" and rec.medida <= 0:
                raise ValidationError(
                    _("La medida de troquelado debe ser mayor a cero o marcarse como N/A.")
                )


class QualityInspectionHardening(models.Model):
    _inherit = "quality.inspection"

    # FOLIO-QM-ODOO18-075:
    # Leyendas se trasladan a la vista para evitar los íconos de interrogación
    # que no aportaban acción al usuario final.
    folio = fields.Char("Folio de Producción", required=True, help="")
    code = fields.Char("Código de Producto", required=True, help="")

    # FOLIO-QM-ODOO18-072 / 075:
    # Espesor no aplica en Octágono; se conserva para otros procesos.
    espesor = fields.Float("Espesor", digits=(16, 2))
    oct_espesor = fields.Float("Espesor Octágono (mm)", digits=(16, 2))

    # FOLIO-QM-ODOO18-075:
    # Octágono requiere precisión visual y de persistencia en calibración.
    ancho = fields.Float("Ancho (mm)", digits=(16, 2))
    oct_ancho = fields.Float("Ancho Octágono (mm)", digits=(16, 2))
    calibracion = fields.Float("Calibración", digits=(16, 4))
    papel_ancho = fields.Float("Ancho del Papel", digits=(16, 2))
    papel_gramaje = fields.Float("Gramaje del Papel", digits=(16, 2))
    oct_retiramiento = fields.Float("Retiramiento (cm) - Legacy", digits=(16, 2))
    reticula_extendida = fields.Float("Retiramiento / Retícula Extendida (cm)", digits=(16, 2))

    # FOLIO-QM-ODOO18-019: se evita redeclarar campos base con otro tipo
    # en hardening; solo se agregan campos nuevos o relacionados.
    capture_mode = fields.Selection(
        related="process_type_id.capture_mode",
        store=True,
        readonly=True,
    )
    date_started = fields.Datetime("Fecha de Inicio", readonly=True)
    date_closed = fields.Datetime("Fecha de Cierre", readonly=True)

    # FOLIO-QM-ODOO18-074: campos informativos para bloquear/habilitar captura por flujo.
    previous_process_type_id = fields.Many2one(
        "quality.process.type",
        string="Proceso Previo Requerido",
        compute="_compute_process_gate_hardening",
        store=False,
    )
    previous_process_inspection_id = fields.Many2one(
        "quality.inspection",
        string="Inspección Previa Liberada",
        compute="_compute_process_gate_hardening",
        store=False,
    )
    process_gate_open = fields.Boolean(
        "Ruta Habilitada",
        compute="_compute_process_gate_hardening",
        store=False,
    )
    process_gate_message = fields.Char(
        "Mensaje de Bloqueo de Ruta",
        compute="_compute_process_gate_hardening",
        store=False,
    )

    def _normalize_inspection_vals_hardening(self, vals):
        vals = dict(vals or {})
        if "espesor" in vals and vals.get("espesor") not in (False, None, ""):
            vals["espesor"] = round(float(vals["espesor"]), 2)
        if "calibracion" in vals and vals.get("calibracion") not in (False, None, ""):
            vals["calibracion"] = round(float(vals["calibracion"]), 4)
        return vals

    @api.model_create_multi
    def create(self, vals_list):
        clean_vals_list = [
            self._normalize_inspection_vals_hardening(vals)
            for vals in vals_list
        ]
        records = super().create(clean_vals_list)
        records._cleanup_octagono_not_applicable_hardening()
        return records

    def write(self, vals):
        vals = self._normalize_inspection_vals_hardening(vals)
        res = super().write(vals)
        if not self.env.context.get("skip_octagono_cleanup"):
            self._cleanup_octagono_not_applicable_hardening()
        return res

    def _cleanup_octagono_not_applicable_hardening(self):
        """
        FOLIO-QM-ODOO18-075:
        Octágono no debe conservar Espesor ni Retiramiento. Si quedaron valores
        legacy por capturas previas o por una configuración antigua, se limpian.
        """
        for rec in self.filtered(lambda item: item.process_code == "octagono"):
            vals = {}
            if rec.espesor:
                vals["espesor"] = 0.0
            if getattr(rec, "oct_espesor", 0.0):
                vals["oct_espesor"] = 0.0
            if getattr(rec, "oct_retiramiento", 0.0):
                vals["oct_retiramiento"] = 0.0
            if getattr(rec, "reticula_extendida", 0.0):
                vals["reticula_extendida"] = 0.0
            if vals:
                super(QualityInspectionHardening, rec.with_context(skip_octagono_cleanup=True)).write(vals)

    @api.onchange("espesor")
    def _onchange_round_espesor_hardening(self):
        for rec in self:
            if rec.espesor not in (False, None):
                rec.espesor = round(rec.espesor, 2)

    @api.onchange("calibracion")
    def _onchange_round_calibracion_hardening(self):
        for rec in self:
            if rec.calibracion not in (False, None):
                rec.calibracion = round(rec.calibracion, 4)

    @api.onchange("process_type_id")
    def _onchange_process_type_octagono_hardening(self):
        for rec in self:
            if rec.process_type_id and rec.process_type_id.code == "octagono":
                # FOLIO-QM-ODOO18-075: Espesor y Retiramiento no aplican en Octágono.
                rec.espesor = 0.0
                rec.oct_espesor = 0.0
                rec.oct_retiramiento = 0.0
                rec.reticula_extendida = 0.0

    @api.onchange("product_id")
    def _onchange_product_code_hardening(self):
        for rec in self:
            if rec.product_id and rec.product_id.default_code:
                rec.code = rec.product_id.default_code

    @api.depends(
        "process_type_id",
        "production_order_id",
        "lot_id",
        "folio",
        "product_id",
    )
    def _compute_process_gate_hardening(self):
        Process = self.env["quality.process.type"].sudo()
        for rec in self:
            previous_code = rec._get_previous_process_code_hardening()
            rec.previous_process_type_id = False
            rec.previous_process_inspection_id = False
            rec.process_gate_open = True
            rec.process_gate_message = False

            if not previous_code:
                continue

            previous_process = Process.search([
                ("code", "=", previous_code),
                "|",
                ("company_id", "=", rec.company_id.id),
                ("company_id", "=", False),
            ], limit=1)
            rec.previous_process_type_id = previous_process

            previous_inspection = rec._find_previous_inspection_hardening(previous_code)
            if previous_inspection:
                rec.previous_process_inspection_id = previous_inspection
                rec.process_gate_open = True
                continue

            rec.process_gate_open = False
            rec.process_gate_message = rec._build_previous_process_block_message_hardening(previous_code)

    @api.constrains("sin_supervisor", "supervisor_id")
    def _check_supervisor_or_no_supervisor(self):
        for rec in self:
            if not rec.sin_supervisor and not rec.supervisor_id:
                raise ValidationError(
                    _("Seleccione un supervisor o marque 'Sin Supervisor'.")
                )

    @api.onchange("sin_supervisor")
    def _onchange_sin_supervisor(self):
        if self.sin_supervisor:
            self.supervisor_id = False

    @api.onchange("production_order_id")
    def _onchange_production_order(self):
        # FOLIO-QM-ODOO18-020 / 075:
        # Se consolida el enlace OP -> Producto/Lote/Cliente/Código para que
        # Octágono no dependa de seleccionar productos al azar.
        if not self.production_order_id:
            return

        production = self.production_order_id
        if production.product_id:
            self.product_id = production.product_id
            self.code = production.product_id.default_code or self.code

        if not self.folio and production.name:
            self.folio = production.name

        if getattr(production, "lot_producing_id", False):
            self.lot_id = production.lot_producing_id

        sale_order = (
            self.env["sale.order"].search([("name", "=", production.origin)], limit=1)
            if production.origin
            else False
        )
        if sale_order and sale_order.partner_id:
            self.partner_id = sale_order.partner_id

    @api.onchange("process_type_id", "product_id")
    def _onchange_load_attribute_templates(self):
        # FOLIO-QM-ODOO18-070 / FOLIO-QM-ODOO18-071:
        # Acabado y Empaque e Impresión solo cargan atributos booleanos Cumple/No Cumple
        # y nunca inicializan líneas con N/A.
        if not self.process_type_id and not self.product_id:
            return

        process_code = self.process_type_id.code or self.process_code
        strict_binary = process_code in STRICT_BINARY_RESULT_PROCESS_CODES

        templates = self.env["quality.attribute.template"]
        if self.process_type_id:
            templates |= self.process_type_id.attribute_template_ids.filtered(
                lambda template: not template.product_tmpl_id and template.active
            )

        if self.product_id and self.product_id.product_tmpl_id:
            templates |= self.env["quality.attribute.template"].search(
                [
                    ("product_tmpl_id", "=", self.product_id.product_tmpl_id.id),
                    ("active", "=", True),
                ]
            )

        if strict_binary:
            templates = templates.filtered(lambda template: template.attribute_type == "boolean")

        if not templates:
            return

        lines = [(5, 0, 0)]
        seen = set()
        for template in templates.sorted(lambda item: (item.sequence, item.id)):
            key = template.normalized_name or _slug(template.name)
            if not key or key in seen:
                continue

            seen.add(key)

            if strict_binary:
                value_cumple = False
                value_ok = False
                result = False
                attribute_type = "boolean"
                result_mode = "cumple"
                capture_zone = "additional"
                min_value = 0.0
                max_value = 0.0
                unit = False
                allow_zero = False
            else:
                value_cumple = "na"
                value_ok = "na"
                result = "na"
                attribute_type = template.attribute_type
                result_mode = template.result_mode
                capture_zone = template.capture_zone
                min_value = template.min_value
                max_value = template.max_value
                unit = template.unit
                allow_zero = template.allow_zero

            lines.append(
                (
                    0,
                    0,
                    {
                        "attribute_template_id": template.id,
                        "name": template.name,
                        "attribute_type": attribute_type,
                        "capture_zone": capture_zone,
                        "result_mode": result_mode,
                        "min_value": min_value,
                        "max_value": max_value,
                        "unit": unit,
                        "allow_zero": allow_zero,
                        "sequence": template.sequence,
                        "value_cumple": value_cumple,
                        "value_ok": value_ok,
                        "result": result,
                    },
                )
            )

        self.line_ids = lines

    def _get_previous_process_code_hardening(self):
        self.ensure_one()
        code = self.process_code
        if code not in PROCESS_SEQUENCE:
            return False

        index = PROCESS_SEQUENCE.index(code)
        if index <= 0:
            return False

        return PROCESS_SEQUENCE[index - 1]

    def _get_process_context_domains_hardening(self):
        self.ensure_one()
        domains = []

        if self.production_order_id:
            domains.append((
                [("production_order_id", "=", self.production_order_id.id)],
                _("orden de producción %s") % self.production_order_id.display_name,
            ))

        if self.lot_id:
            domains.append((
                [("lot_id", "=", self.lot_id.id)],
                _("lote %s") % (self.lot_id.display_name or "—"),
            ))

        if self.folio and self.product_id:
            domains.append((
                [
                    ("folio", "=", self.folio),
                    ("product_id", "=", self.product_id.id),
                ],
                _("folio %s y producto %s") % (
                    self.folio,
                    self.product_id.display_name,
                ),
            ))

        return domains

    def _find_previous_inspection_hardening(self, previous_code, states=("aceptado",)):
        self.ensure_one()
        Inspection = self.env["quality.inspection"].sudo()

        base_domain = [
            ("id", "!=", self.id),
            ("process_code", "=", previous_code),
            ("state", "in", list(states)),
        ]

        for context_domain, _context_label in self._get_process_context_domains_hardening():
            found = Inspection.search(
                base_domain + context_domain,
                order="date_inspection desc, id desc",
                limit=1,
            )
            if found:
                return found

        return Inspection.browse()

    def _build_previous_process_block_message_hardening(self, previous_code):
        self.ensure_one()

        Process = self.env["quality.process.type"].sudo()
        previous_process = Process.search([
            ("code", "=", previous_code),
            "|",
            ("company_id", "=", self.company_id.id),
            ("company_id", "=", False),
        ], limit=1)

        previous_name = previous_process.display_name or previous_code.replace("_", " ").title()
        current_name = self.process_type_id.display_name or self.process_code or _("este proceso")

        blocking_previous = self._find_previous_inspection_hardening(
            previous_code,
            states=("borrador", "en_proceso", "retenido", "rechazado"),
        )

        if blocking_previous:
            state_label = dict(blocking_previous._fields["state"].selection).get(
                blocking_previous.state,
                blocking_previous.state,
            )
            if blocking_previous.state in ("retenido", "rechazado"):
                return _(
                    "Secuencia bloqueada: el proceso previo '%s' existe como %s "
                    "pero está en estado '%s'. No se permite movimiento ni captura "
                    "hasta que Producción marque la corrección como hecha y Calidad "
                    "lo libere."
                ) % (
                    previous_name,
                    blocking_previous.name,
                    state_label,
                )

            return _(
                "Secuencia bloqueada: el proceso previo '%s' existe como %s, "
                "pero aún no está liberado. Debe quedar Aceptado/Liberado antes "
                "de iniciar o liberar '%s'."
            ) % (
                previous_name,
                blocking_previous.name,
                current_name,
            )

        context_labels = [
            label for _domain, label in self._get_process_context_domains_hardening()
        ]
        context_text = ", ".join(context_labels) if context_labels else _("la misma orden/lote/folio")

        return _(
            "Secuencia bloqueada: antes de iniciar o liberar '%s' debe existir "
            "una inspección aceptada/liberada del proceso previo '%s' para %s."
        ) % (
            current_name,
            previous_name,
            context_text,
        )

    def _check_previous_process_hardening(self):
        for rec in self:
            previous_code = rec._get_previous_process_code_hardening()
            if not previous_code:
                continue

            previous_inspection = rec._find_previous_inspection_hardening(previous_code)
            if not previous_inspection:
                raise UserError(rec._build_previous_process_block_message_hardening(previous_code))

        return True

    def _check_reserved_duplicate_attributes_hardening(self):
        for rec in self:
            duplicates = []
            for line in rec.line_ids.filtered(lambda item: item.capture_zone == "additional"):
                key = line.normalized_name or _slug(line.name)
                duplicated_label = _reserved_measure_label_for_inspection(rec, key)
                if duplicated_label:
                    duplicates.append(duplicated_label)

            if duplicates:
                raise UserError(
                    _(
                        "Estos atributos no deben capturarse como adicionales porque "
                        "ya pertenecen al formulario del proceso o no aplican aquí: %s"
                    )
                    % ", ".join(sorted(set(duplicates)))
                )

    def _check_required_additional_attributes_hardening(self):
        for rec in self:
            if not rec.process_type_id.require_additional_attributes:
                continue

            required_lines = rec.line_ids.filtered(
                lambda line: line.attribute_template_id.is_required
                if line.attribute_template_id
                else True
            )
            if not required_lines:
                raise UserError(_("Debe capturar los atributos adicionales del proceso."))

            strict_binary = rec.process_code in STRICT_BINARY_RESULT_PROCESS_CODES

            if strict_binary:
                invalid_type = required_lines.filtered(
                    lambda line: (
                        line.attribute_type != "boolean"
                        or line.result_mode != "cumple"
                        or line.capture_zone != "additional"
                    )
                )
                if invalid_type:
                    raise UserError(_(
                        "%s solo permite atributos adicionales de tipo Cumple/No Cumple. Revise: %s"
                    ) % (
                        rec.process_type_id.display_name,
                        ", ".join(invalid_type.mapped("name")),
                    ))

                for line in required_lines:
                    if line.value_cumple in ("cumple", "no_cumple") and line.result != line.value_cumple:
                        line.result = line.value_cumple

                missing_binary = required_lines.filtered(
                    lambda line: (
                        line.value_cumple not in ("cumple", "no_cumple")
                        or line.result not in ("cumple", "no_cumple")
                    )
                )
                if missing_binary:
                    raise UserError(_(
                        "%s no permite N/A ni resultados vacíos. Seleccione Cumple o No Cumple en: %s"
                    ) % (
                        rec.process_type_id.display_name,
                        ", ".join(missing_binary.mapped("name")),
                    ))

                continue

            missing_result = required_lines.filtered(
                lambda line: not line.result
            )
            if missing_result:
                raise UserError(
                    _("Hay atributos adicionales sin dictamen: %s")
                    % ", ".join(missing_result.mapped("name"))
                )

            numeric_zero = required_lines.filtered(
                lambda line: (
                    line.attribute_type == "float"
                    and not line.allow_zero
                    and not line.value_float
                    and line.result != "na"
                )
            )
            if numeric_zero:
                raise UserError(
                    _("Se detectan atributos numéricos con valor igual a cero. Rectifique: %s")
                    % ", ".join(numeric_zero.mapped("name"))
                )

    def _check_measures_captured_hardening(self):
        for rec in self:
            # FOLIO-QM-ODOO18-070 / FOLIO-QM-ODOO18-071:
            # Procesos solo adicionales no deben validar medidas, aunque la base conserve banderas show_* antiguas.
            if rec.capture_mode == "additional_only" or rec.process_code in STRICT_BINARY_RESULT_PROCESS_CODES:
                continue

            if not rec.process_type_id.require_measures:
                continue

            # FOLIO-QM-ODOO18-075:
            # Octágono se valida por su matriz propia, sin Espesor ni Retiramiento.
            if rec.process_code == "octagono":
                missing = []

                if not (rec.ancho or getattr(rec, "oct_ancho", 0.0)):
                    missing.append("Ancho")
                if not (
                    rec.hexagono
                    or getattr(rec, "oct_hexagono_tipo", False)
                    or getattr(rec, "oct_hexagono", False)
                    or rec.tipo_hexagono
                ):
                    missing.append("Hexágono")
                if not rec.numero_corrida:
                    missing.append("Número de Corrida")
                if not rec.papel_ancho:
                    missing.append("Ancho de Papel")
                if not rec.papel_gramaje:
                    missing.append("Gramaje de Papel")
                if not rec.papel_proveedor_id:
                    missing.append("Proveedor de Rollos")
                if not rec.adhesivo_lote1:
                    missing.append("Lote 1 Adhesivo")
                if not rec.adhesivo_lote2:
                    missing.append("Lote 2 Adhesivo")
                if not rec.calibracion:
                    missing.append("Calibración")
                if not rec.engomado:
                    missing.append("Engomado")
                if not rec.oct_alineacion:
                    missing.append("Alineación")
                if rec.corte_guillotina not in ("si", "no"):
                    missing.append("Corte de Guillotina (Sí/No)")

                if missing:
                    raise UserError(
                        _("Capture la información obligatoria de Octágono antes de liberar. Faltan: %s")
                        % ", ".join(missing)
                    )
                continue

            missing = []

            if rec.show_largo and not rec.largo:
                missing.append("Largo")
            if rec.show_ancho and not (rec.ancho or getattr(rec, "oct_ancho", 0.0)):
                missing.append("Ancho")
            if rec.show_espesor and not (rec.espesor or getattr(rec, "oct_espesor", 0.0)):
                missing.append("Espesor")
            if rec.show_hexagono and not (
                rec.hexagono
                or getattr(rec, "tipo_hexagono", False)
                or getattr(rec, "oct_hexagono_tipo", False)
                or getattr(rec, "oct_hexagono", False)
            ):
                missing.append("Hexágono")
            if rec.show_resistencia and not rec.resistencia_na and not rec.resistencia:
                missing.append("Resistencia")
            if rec.show_apariencia and not rec.apariencia:
                missing.append("Apariencia")
            if rec.show_humedad and not rec.humedad_pct:
                missing.append("Humedad")
            if rec.show_pegado and not rec.pegado_result:
                missing.append("Resultado de Pegado")
            if rec.show_retiramiento and not (
                getattr(rec, "oct_retiramiento", 0.0)
                or getattr(rec, "reticula_extendida", 0.0)
            ):
                missing.append("Retícula Extendida / Restiramiento")
            if rec.show_calibracion and not rec.calibracion:
                missing.append("Calibración")
            if rec.show_engomado and not rec.engomado:
                missing.append("Engomado")
            if rec.show_alineacion and not rec.oct_alineacion:
                missing.append("Alineación")
            if rec.show_numero_corrida and not rec.numero_corrida:
                missing.append("Número de Corrida")
            if rec.show_tipo_hexagono and not rec.tipo_hexagono:
                missing.append("Tipo de Hexágono")

            if rec.show_papel:
                if not rec.papel_ancho:
                    missing.append("Ancho de Papel")
                if not rec.papel_gramaje:
                    missing.append("Gramaje de Papel")
                if not rec.papel_proveedor_id:
                    missing.append("Proveedor de Papel")

            if rec.show_adhesivo and not (rec.adhesivo_lote1 or rec.adhesivo_lote2):
                missing.append("Lote de Adhesivo")

            if rec.show_corte_guillotina and not rec.corte_guillotina:
                missing.append("Corte en Guillotina")

            if rec.process_code == "troquelado_plano" and not rec.troquelado_ids:
                missing.append("Pestaña Troquelado")

            if (
                rec.process_code == "sierras_ranuradoras"
                and rec.show_ranurado
                and not rec.ranurado_ids
            ):
                missing.append("Pestaña Ranurado / Corte Sierra")

            if missing:
                raise UserError(
                    _("Capture la información obligatoria antes de liberar. Faltan: %s")
                    % ", ".join(missing)
                )

    def _full_quality_validation_hardening(self):
        for rec in self:
            if rec.state != "en_proceso":
                raise UserError(_("Debe presionar 'INICIAR INSPECCIÓN' antes de liberar."))

            rec._check_reserved_duplicate_attributes_hardening()
            rec._check_measures_captured_hardening()
            rec._check_required_additional_attributes_hardening()
            rec._check_previous_process_hardening()

    def _sync_strict_binary_lines_hardening(self):
        for rec in self.filtered(lambda item: item.process_code in STRICT_BINARY_RESULT_PROCESS_CODES):
            for line in rec.line_ids:
                vals = {}

                if line.attribute_type != "boolean":
                    vals["attribute_type"] = "boolean"
                if line.capture_zone != "additional":
                    vals["capture_zone"] = "additional"
                if line.result_mode != "cumple":
                    vals["result_mode"] = "cumple"
                if line.value_ok:
                    vals["value_ok"] = False
                if line.value_float:
                    vals["value_float"] = 0.0
                if line.value_char:
                    vals["value_char"] = False
                if line.min_value:
                    vals["min_value"] = 0.0
                if line.max_value:
                    vals["max_value"] = 0.0
                if line.unit:
                    vals["unit"] = False
                if line.allow_zero:
                    vals["allow_zero"] = False

                if line.value_cumple == "na":
                    vals["value_cumple"] = False
                if line.value_ok == "na":
                    vals["value_ok"] = False
                if line.result == "na":
                    vals["result"] = False

                if line.value_cumple in ("cumple", "no_cumple") and line.result != line.value_cumple:
                    vals["result"] = line.value_cumple
                elif line.result in ("cumple", "no_cumple") and line.value_cumple != line.result:
                    vals["value_cumple"] = line.result

                if vals:
                    line.write(vals)

    def action_start(self):
        for rec in self:
            # FOLIO-QM-ODOO18-074: no se permite iniciar captura si el proceso previo no está liberado.
            rec._check_previous_process_hardening()
            rec.date_started = fields.Datetime.now()
            rec.state = "en_proceso"
            rec._sync_strict_binary_lines_hardening()
            rec.message_post(
                body=_("Inspección iniciada."),
                subtype_xmlid="mail.mt_comment",
            )

    def action_accept(self):
        for rec in self:
            rec._full_quality_validation_hardening()
            rec.state = "aceptado"
            rec.date_closed = fields.Datetime.now()
            rec.message_post(
                body=_("Inspección ACEPTADA/LIBERADA por %s.") % self.env.user.name,
                subtype_xmlid="mail.mt_comment",
            )

    def _get_supervisor_user_hardening(self):
        self.ensure_one()
        if self.supervisor_id and self.supervisor_id.user_id:
            return self.supervisor_id.user_id
        return False

    def action_retain(self):
        for rec in self:
            if rec.state != "en_proceso":
                raise UserError(_("Solo se puede retener una inspección en proceso."))

            rec._check_reserved_duplicate_attributes_hardening()
            rec.state = "retenido"

            supervisor_user = rec._get_supervisor_user_hardening()
            partner_ids = []

            if supervisor_user and supervisor_user.partner_id:
                partner_ids = [supervisor_user.partner_id.id]
                rec.message_subscribe(partner_ids=partner_ids)
                rec.activity_schedule(
                    "mail.mail_activity_data_todo",
                    date_deadline=fields.Date.today() + timedelta(days=1),
                    summary=_("Producto retenido en Calidad: %s") % rec.name,
                    user_id=supervisor_user.id,
                )

            rec.message_post(
                body=_(
                    "Producto RETENIDO por %s. Supervisor en turno: %s. "
                    "Cuando Producción marque HECHO, Calidad debe validar nuevamente."
                )
                % (
                    self.env.user.name,
                    rec.supervisor_id.name if rec.supervisor_id else "Sin supervisor",
                ),
                partner_ids=partner_ids,
                subtype_xmlid="mail.mt_comment",
            )

    def action_reject(self):
        for rec in self:
            if rec.state != "en_proceso":
                raise UserError(_("Solo se puede rechazar una inspección en proceso."))
            rec.state = "rechazado"
            rec.date_closed = fields.Datetime.now()
            rec.message_post(
                body=_("Inspección RECHAZADA por %s.") % self.env.user.name,
                subtype_xmlid="mail.mt_comment",
            )


class QualityCertificateHardening(models.Model):
    _inherit = "quality.certificate"

    certified_hexagono_label = fields.Char("Hexágono")
    certified_retiramiento = fields.Float("Retiramiento", digits=(16, 2))
    certified_calibracion = fields.Float("Calibración", digits=(16, 4))

    @api.constrains("inspection_id")
    def _check_inspection_accepted_hardening(self):
        for rec in self:
            if rec.inspection_id and rec.inspection_id.state != "aceptado":
                raise ValidationError(_("Solo se puede certificar una inspección aceptada."))

    @api.constrains("attribute_ids")
    def _check_attribute_dedup_and_source_hardening(self):
        for rec in self:
            names = []
            for line in rec.attribute_ids:
                if line.inspection_id != rec.inspection_id:
                    raise ValidationError(
                        _("El certificado solo puede contener atributos de la inspección fuente.")
                    )

                key = line.normalized_name or _slug(line.name)
                if key:
                    names.append(key)

                if line.attribute_type == "float" and not line.allow_zero and not line.value_float:
                    raise ValidationError(
                        _("No se puede certificar el atributo '%s' con valor 0.")
                        % line.name
                    )

                if line.result not in ("cumple", "ok"):
                    raise ValidationError(
                        _("Solo se pueden certificar atributos con resultado Cumple/OK.")
                    )

            if len(names) != len(set(names)):
                raise ValidationError(_("Hay atributos repetidos en el certificado."))

    def action_generate(self):
        for rec in self:
            if rec.inspection_id.state != "aceptado":
                raise UserError(_("Solo se puede generar certificado desde inspección aceptada."))
            rec.state = "generado"


class QualityActionLineHardening(models.Model):
    _inherit = "quality.action.line"

    def write(self, vals):
        res = super().write(vals)
        if "evidence_ids" in vals:
            for line in self:
                if line.evidence_ids and line.state == "pendiente":
                    line.state = "en_proceso"
        return res

    def action_complete(self):
        for rec in self:
            if not rec.evidence_ids:
                raise UserError(_("No se puede completar la acción sin adjuntar evidencia."))
            rec.state = "completada"
            rec.date_completed = fields.Date.today()


class QualityCustomerDocumentHardening(models.Model):
    _inherit = "quality.customer.document"

    def action_send(self):
        for rec in self:
            has_doc = (
                rec.main_pdf
                or rec.main_image
                or rec.result_document_ids
                or rec.client_format_ids
            )
            if not has_doc:
                raise UserError(
                    _("No puede marcar como enviado si no existe documento cargado.")
                )
            rec.state = "enviado"```

## ./models/quality_inherited_models.py
```py
from odoo import models, fields, api, _


class ResPartnerQuality(models.Model):
    _inherit = 'res.partner'

    quality_certificate_ids = fields.One2many(
        'quality.certificate', 'partner_id', string='Certificados de Calidad'
    )
    quality_certificate_count = fields.Integer(
        compute='_compute_quality_certificate_count', string='Certificados'
    )
    quality_return_ids = fields.One2many(
        'quality.customer.return', 'partner_id', string='Devoluciones de Calidad'
    )
    quality_return_count = fields.Integer(
        compute='_compute_quality_return_count', string='Devoluciones'
    )
    quality_document_ids = fields.One2many(
        'quality.customer.document', 'partner_id', string='Documentos de Calidad'
    )
    quality_document_count = fields.Integer(
        compute='_compute_quality_document_count', string='Docs. Calidad'
    )
    quality_inspection_ids = fields.One2many(
        'quality.inspection', 'partner_id', string='Inspecciones de Calidad'
    )
    quality_inspection_count = fields.Integer(
        compute='_compute_quality_inspection_count', string='Inspecciones'
    )

    @api.depends('quality_certificate_ids')
    def _compute_quality_certificate_count(self):
        data = self.env['quality.certificate']._read_group(
            [('partner_id', 'in', self.ids)],
            ['partner_id'], ['__count'],
        )
        mapped = {partner.id: count for partner, count in data}
        for rec in self:
            rec.quality_certificate_count = mapped.get(rec.id, 0)

    @api.depends('quality_return_ids')
    def _compute_quality_return_count(self):
        data = self.env['quality.customer.return']._read_group(
            [('partner_id', 'in', self.ids)],
            ['partner_id'], ['__count'],
        )
        mapped = {partner.id: count for partner, count in data}
        for rec in self:
            rec.quality_return_count = mapped.get(rec.id, 0)

    @api.depends('quality_document_ids')
    def _compute_quality_document_count(self):
        data = self.env['quality.customer.document']._read_group(
            [('partner_id', 'in', self.ids)],
            ['partner_id'], ['__count'],
        )
        mapped = {partner.id: count for partner, count in data}
        for rec in self:
            rec.quality_document_count = mapped.get(rec.id, 0)

    @api.depends('quality_inspection_ids')
    def _compute_quality_inspection_count(self):
        data = self.env['quality.inspection']._read_group(
            [('partner_id', 'in', self.ids)],
            ['partner_id'], ['__count'],
        )
        mapped = {partner.id: count for partner, count in data}
        for rec in self:
            rec.quality_inspection_count = mapped.get(rec.id, 0)

    @api.depends('name', 'vat', 'email', 'city', 'ref', 'parent_id')
    @api.depends_context('show_vat', 'show_email')
    def _compute_display_name(self):
        """Diferenciar clientes con mismo nombre en el dropdown de calidad."""
        show_vat = self.env.context.get('show_vat')
        show_email = self.env.context.get('show_email')
        if not (show_vat or show_email):
            return super()._compute_display_name()
        # Detectar duplicados por nombre
        names = [p.name for p in self if p.name]
        duplicates = set()
        if names:
            groups = self.env['res.partner']._read_group(
                [('name', 'in', names)],
                ['name'], ['__count'],
            )
            duplicates = {name for name, count in groups if count > 1}
        for partner in self:
            base = partner.name or ''
            if partner.parent_id:
                base = f"{partner.parent_id.name}, {base}"
            # Solo agrega identificador si hay homónimos
            if partner.name in duplicates:
                extras = []
                if show_vat and partner.vat:
                    extras.append(partner.vat)
                elif partner.ref:
                    extras.append(partner.ref)
                elif partner.city:
                    extras.append(partner.city)
                elif show_email and partner.email:
                    extras.append(partner.email)
                if extras:
                    base = f"{base} ({' · '.join(extras)})"
            partner.display_name = base or _('Sin nombre')

    def action_view_quality_certificates(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Certificados de Calidad'),
            'res_model': 'quality.certificate',
            'view_mode': 'list,form',
            'domain': [('partner_id', '=', self.id)],
            'context': {'default_partner_id': self.id},
        }

    def action_view_quality_returns(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Devoluciones'),
            'res_model': 'quality.customer.return',
            'view_mode': 'list,form',
            'domain': [('partner_id', '=', self.id)],
            'context': {'default_partner_id': self.id},
        }

    def action_view_quality_documents(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Documentos de Calidad'),
            'res_model': 'quality.customer.document',
            'view_mode': 'list,form',
            'domain': [('partner_id', '=', self.id)],
            'context': {'default_partner_id': self.id},
        }

    def action_view_quality_inspections(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Inspecciones de Calidad'),
            'res_model': 'quality.inspection',
            'view_mode': 'list,form',
            'domain': [('partner_id', '=', self.id)],
            'context': {'default_partner_id': self.id},
        }


class SaleOrderQuality(models.Model):
    _inherit = 'sale.order'

    quality_drawing_ids = fields.One2many(
        'quality.drawing.release', 'sale_order_id',
        string='Liberaciones de Plano'
    )
    quality_drawing_count = fields.Integer(
        compute='_compute_quality_drawing_count', string='Planos'
    )
    quality_return_ids = fields.One2many(
        'quality.customer.return', 'sale_order_id',
        string='Devoluciones'
    )
    quality_return_count = fields.Integer(
        compute='_compute_quality_return_count', string='Devoluciones'
    )

    @api.depends('quality_drawing_ids')
    def _compute_quality_drawing_count(self):
        data = self.env['quality.drawing.release']._read_group(
            [('sale_order_id', 'in', self.ids)],
            ['sale_order_id'], ['__count'],
        )
        mapped = {so.id: count for so, count in data}
        for rec in self:
            rec.quality_drawing_count = mapped.get(rec.id, 0)

    @api.depends('quality_return_ids')
    def _compute_quality_return_count(self):
        data = self.env['quality.customer.return']._read_group(
            [('sale_order_id', 'in', self.ids)],
            ['sale_order_id'], ['__count'],
        )
        mapped = {so.id: count for so, count in data}
        for rec in self:
            rec.quality_return_count = mapped.get(rec.id, 0)

    def action_view_quality_drawings(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Planos de Calidad'),
            'res_model': 'quality.drawing.release',
            'view_mode': 'list,form',
            'domain': [('sale_order_id', '=', self.id)],
            'context': {
                'default_sale_order_id': self.id,
                'default_partner_id': self.partner_id.id,
            },
        }

    def action_view_quality_returns(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Devoluciones'),
            'res_model': 'quality.customer.return',
            'view_mode': 'list,form',
            'domain': [('sale_order_id', '=', self.id)],
            'context': {
                'default_sale_order_id': self.id,
                'default_partner_id': self.partner_id.id,
            },
        }


class MrpProductionQuality(models.Model):
    _inherit = 'mrp.production'

    quality_inspection_ids = fields.One2many(
        'quality.inspection', 'production_order_id',
        string='Inspecciones de Calidad'
    )
    quality_inspection_count = fields.Integer(
        compute='_compute_quality_inspection_count', string='Inspecciones'
    )

    @api.depends('quality_inspection_ids')
    def _compute_quality_inspection_count(self):
        data = self.env['quality.inspection']._read_group(
            [('production_order_id', 'in', self.ids)],
            ['production_order_id'], ['__count'],
        )
        mapped = {mo.id: count for mo, count in data}
        for rec in self:
            rec.quality_inspection_count = mapped.get(rec.id, 0)

    def action_view_quality_inspections(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Inspecciones de Calidad'),
            'res_model': 'quality.inspection',
            'view_mode': 'list,form',
            'domain': [('production_order_id', '=', self.id)],
            'context': {'default_production_order_id': self.id},
        }```

## ./models/quality_inspection_line.py
```py
from odoo import models, fields, api


class QualityInspectionLine(models.Model):
    _name = 'quality.inspection.line'
    _description = 'Línea de Inspección'
    _order = 'sequence, id'

    inspection_id = fields.Many2one(
        'quality.inspection', 'Inspección', ondelete='cascade'
    )
    sample_release_id = fields.Many2one(
        'quality.sample.release', 'Liberación de Muestra', ondelete='cascade'
    )
    attribute_template_id = fields.Many2one(
        'quality.attribute.template', 'Atributo'
    )
    sequence = fields.Integer('Secuencia', default=10)
    name = fields.Char('Nombre del Atributo', required=True)
    attribute_type = fields.Selection([
        ('float', 'Numérico'),
        ('selection', 'Selección'),
        ('boolean', 'Cumple/No Cumple'),
        ('char', 'Texto'),
    ], string='Tipo de Dato', default='float')
    value_float = fields.Float('Valor Numérico')
    value_char = fields.Char('Valor Texto')
    value_boolean = fields.Boolean('Valor Sí/No')  # legacy
    value_cumple = fields.Selection([
        ('cumple', 'Cumple'),
        ('no_cumple', 'No Cumple'),
    ], string='Valor Cumple/No Cumple')
    value_selection = fields.Char('Valor Selección')
    min_value = fields.Float('Mínimo')
    max_value = fields.Float('Máximo')
    unit = fields.Char('Unidad')
    result = fields.Selection([
        ('cumple', 'Cumple'),
        ('no_cumple', 'No Cumple'),
        ('na', 'N/A'),
    ], string='Resultado', default='na')
    notes = fields.Char('Notas')

    @api.onchange('value_float', 'min_value', 'max_value', 'attribute_type')
    def _onchange_evaluate_result(self):
        for line in self:
            if line.attribute_type == 'float' and (line.min_value or line.max_value):
                if line.min_value and line.value_float < line.min_value:
                    line.result = 'no_cumple'
                elif line.max_value and line.value_float > line.max_value:
                    line.result = 'no_cumple'
                elif line.value_float:
                    line.result = 'cumple'

    @api.onchange('value_cumple', 'attribute_type')
    def _onchange_value_cumple(self):
        for line in self:
            if line.attribute_type == 'boolean' and line.value_cumple:
                line.result = line.value_cumple```

## ./models/quality_inspection_ranurado.py
```py
from odoo import models, fields


class QualityInspectionRanurado(models.Model):
    _name = 'quality.inspection.ranurado'
    _description = 'Captura de Ranurado'
    _order = 'sequence, id'

    inspection_id = fields.Many2one(
        'quality.inspection', 'Inspección',
        required=True, ondelete='cascade'
    )
    sequence = fields.Integer('N°', default=1)
    medida = fields.Float('Medida', required=True)
    unidad = fields.Selection([
        ('mm', 'mm'),
        ('in', 'in'),
    ], string='Unidad', default='mm', required=True)
    resultado = fields.Selection([
        ('cumple', 'Cumple'),
        ('no_cumple', 'No Cumple'),
    ], string='Resultado', default='cumple')
    notas = fields.Char('Notas')```

## ./models/quality_inspection_troquelado.py
```py
from odoo import models, fields


class QualityInspectionTroquelado(models.Model):
    _name = 'quality.inspection.troquelado'
    _description = 'Captura de Troquelado'
    _order = 'sequence, id'

    inspection_id = fields.Many2one(
        'quality.inspection', 'Inspección',
        required=True, ondelete='cascade'
    )
    sequence = fields.Integer('N°', default=1)
    medida = fields.Float('Medida (mm)', required=True)
    resultado = fields.Selection([
        ('cumple', 'Cumple'),
        ('no_cumple', 'No Cumple'),
    ], string='Resultado', default='cumple')
    notas = fields.Char('Notas')
```

## ./models/quality_inspection.py
```py
# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


PROCESS_SEQUENCE = [
    "octagono",
    "guillotina",
    "pegado",
    "laminadora",
    "sierras_ranuradoras",
    "troquelado_plano",
]

OCT_HEXAGONO_SELECTION = [
    ("tipo_1", "Tipo 1"),
    ("tipo_2", "Tipo 2"),
    ("tipo_3", "Tipo 3"),
    ("tipo_4", "Tipo 4"),
]

OCT_HEXAGONO_VALUES = {value for value, _label in OCT_HEXAGONO_SELECTION}


class QualityInspection(models.Model):
    _name = "quality.inspection"
    _description = "Inspección de PP/PT"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_inspection desc, id desc"

    # FOLIO-QM-ODOO18-022: se define process_code en el archivo base para que
    # vistas heredadas, rutas y reportes puedan depender de un campo estable.
    process_code = fields.Char(
        related="process_type_id.code",
        store=True,
        readonly=True,
        index=True,
    )

    name = fields.Char(
        "Referencia",
        required=True,
        readonly=True,
        default="Nuevo",
        copy=False,
    )

    process_type_id = fields.Many2one(
        "quality.process.type",
        "Tipo de Proceso",
        required=True,
        tracking=True,
    )
    inspection_type = fields.Selection(
        [
            ("laminadora_remanejo", "Laminadora y Remanejo"),
            ("octagono", "Octágono"),
            ("guillotina_pegado", "Guillotina y Pegado"),
        ],
        compute="_compute_inspection_type",
        store=True,
    )

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
    show_alineacion = fields.Boolean(related="process_type_id.show_alineacion")
    show_ranurado = fields.Boolean(related="process_type_id.show_ranurado")
    show_troquelado = fields.Boolean(related="process_type_id.show_troquelado")
    show_papel = fields.Boolean(related="process_type_id.show_papel")
    show_adhesivo = fields.Boolean(related="process_type_id.show_adhesivo")
    show_tipo_hexagono = fields.Boolean(related="process_type_id.show_tipo_hexagono")
    show_corte_guillotina = fields.Boolean(related="process_type_id.show_corte_guillotina")
    show_numero_corrida = fields.Boolean(related="process_type_id.show_numero_corrida")

    production_order_id = fields.Many2one(
        "mrp.production",
        "Orden de Producción",
        tracking=True,
        required=True,
    )
    lot_id = fields.Many2one(
        "stock.lot",
        "Lote de Fabricación",
        tracking=True,
        required=True,
    )
    product_id = fields.Many2one(
        "product.product",
        "Producto",
        required=True,
        tracking=True,
    )
    operator_id = fields.Many2one(
        "hr.employee",
        "Operador",
        required=True,
    )
    # FOLIO-QM-ODOO18-023: supervisor deja de ser required a nivel ORM para permitir
    # la opción formal "Sin Supervisor"; el bloqueo real queda en constraint hardening.
    supervisor_id = fields.Many2one(
        "hr.employee",
        "Supervisor",
    )
    partner_id = fields.Many2one(
        "res.partner",
        "Cliente",
        required=True,
        tracking=True,
    )
    folio = fields.Char(
        "Folio de Producción",
        required=True,
        help="Formato: letras y/o números. Capture exactamente el folio impreso en el lote.",
    )
    code = fields.Char(
        "Código de Producto",
        required=True,
        help="Código interno del producto.",
    )
    shift = fields.Selection(
        [
            ("turno_1", "Turno 1"),
            ("turno_2", "Turno 2"),
            ("turno_3", "Turno 3"),
        ],
        required=True,
    )
    plant = fields.Selection(
        [
            ("planta_1", "Planta 1"),
            ("planta_2", "Planta 2"),
            ("planta_3", "Planta 3"),
            ("planta_6", "Planta 6"),
            ("planta_7", "Planta 7"),
        ],
        required=True,
    )
    inspector_id = fields.Many2one(
        "res.users",
        "Inspector de Calidad",
        required=True,
        default=lambda s: s.env.user,
        tracking=True,
    )

    date_inspection = fields.Datetime(
        "Fecha y Hora de Inspección",
        required=True,
        readonly=True,
        default=fields.Datetime.now,
    )

    state = fields.Selection(
        [
            ("borrador", "Borrador"),
            ("en_proceso", "En Proceso"),
            ("aceptado", "Aceptado"),
            ("retenido", "Retenido"),
            ("rechazado", "Rechazado"),
        ],
        default="borrador",
        required=True,
        tracking=True,
        copy=False,
    )

    pp_pt = fields.Selection(
        [
            ("pp", "Producto en Proceso (PP)"),
            ("pt", "Producto Terminado (PT)"),
        ],
        string="PP / PT",
        required=True,
        default="pp",
        tracking=True,
    )
    is_pp = fields.Boolean(compute="_compute_is_pp_pt")
    is_pt = fields.Boolean(compute="_compute_is_pp_pt")

    line_ids = fields.One2many(
        "quality.inspection.line",
        "inspection_id",
        string="Atributos Capturados",
    )

    largo = fields.Float("Largo (mm)")
    ancho = fields.Float("Ancho (mm)")
    espesor = fields.Float("Espesor")
    espesor_unit = fields.Selection(
        [
            ("in", "Pulgadas (in)"),
            ("mm", "Milímetros (mm)"),
        ],
        default="in",
    )
    espesor_label = fields.Char(compute="_compute_espesor_label")

    hexagono = fields.Selection(
        OCT_HEXAGONO_SELECTION,
        string="Hexágono",
    )

    resistencia = fields.Float("Resistencia (Lbf)")
    resistencia_na = fields.Boolean("Resistencia No Aplica")
    apariencia = fields.Selection(
        [
            ("cumple", "Cumple"),
            ("no_cumple", "No Cumple"),
            ("na", "N/A"),
        ]
    )
    humedad_pct = fields.Float("% Humedad")
    ranurado_unit = fields.Selection(
        [
            ("mm", "Milímetros (mm)"),
            ("in", "Pulgadas (in)"),
        ],
        default="mm",
    )
    ranurado_ids = fields.One2many(
        "quality.inspection.ranurado",
        "inspection_id",
        string="Ranurado",
    )
    troquelado_ids = fields.One2many(
        "quality.inspection.troquelado",
        "inspection_id",
        string="Troquelado",
    )
    pegado_result = fields.Selection(
        [
            ("cumple", "Cumple"),
            ("no_cumple", "No Cumple"),
            ("na", "N/A"),
        ],
        string="Resultado de Pegado",
    )

    oct_ancho = fields.Float("Ancho Octágono (mm)")
    oct_espesor = fields.Float("Espesor Octágono (mm)")

    # FOLIO-QM-ODOO18-061: se conserva oct_hexagono como Selection legacy para no romper
    # upgrades donde Odoo ya creó ir.model.fields.selection para este campo.
    # No debe volver a cambiarse a Float dentro de este mismo upgrade.
    oct_hexagono = fields.Selection(
        OCT_HEXAGONO_SELECTION,
        string="Hexágono Octágono Legacy",
        copy=False,
        help=(
            "Campo legacy conservado para compatibilidad de actualización. "
            "El campo definitivo para nuevas capturas es 'Tipo de Hexágono Octágono'."
        ),
    )

    # FOLIO-QM-ODOO18-062: nuevo campo definitivo para capturar el tipo de hexágono
    # de Octágono sin reutilizar/modificar la columna histórica oct_hexagono.
    oct_hexagono_tipo = fields.Selection(
        OCT_HEXAGONO_SELECTION,
        string="Tipo de Hexágono Octágono",
        tracking=True,
        copy=False,
    )

    oct_retiramiento = fields.Float("Retiramiento (cm)")
    oct_alineacion = fields.Selection(
        [
            ("cumple", "Cumple"),
            ("no_cumple", "No Cumple"),
            ("na", "N/A"),
        ],
        string="Alineación",
    )
    oct_pegado = fields.Selection(
        [
            ("cumple", "Cumple"),
            ("no_cumple", "No Cumple"),
            ("na", "N/A"),
        ],
        string="Pegado Octágono",
    )

    numero_corrida = fields.Char("Número de Corrida")
    papel_ancho = fields.Float("Ancho del Papel")
    papel_gramaje = fields.Float("Gramaje del Papel")
    papel_proveedor_id = fields.Many2one(
        "res.partner",
        "Proveedor del Papel",
        domain=[("supplier_rank", ">", 0)],
    )
    adhesivo_lote1 = fields.Char("Lote 1 Adhesivo")
    adhesivo_lote2 = fields.Char("Lote 2 Adhesivo")
    tipo_hexagono = fields.Selection(
        OCT_HEXAGONO_SELECTION,
        string="Tipo de Hexágono",
    )
    calibracion = fields.Float("Calibración", digits=(16, 6))
    engomado = fields.Selection(
        [
            ("cumple", "Cumple"),
            ("no_cumple", "No Cumple"),
            ("na", "N/A"),
        ]
    )
    corte_guillotina = fields.Selection(
        [
            ("si", "Sí"),
            ("no", "No"),
            ("na", "N/A"),
        ],
        string="Corte en Guillotina",
    )

    reticula_extendida = fields.Float("Retícula Extendida (cm)")
    reticula_vueltas = fields.Integer("Cantidad de Vueltas")
    lote_reticula = fields.Char("Lote de Retícula")
    gramaje_reticula = fields.Float("Gramaje de Retícula")
    sin_supervisor = fields.Boolean("Sin Supervisor")

    evidence_pdf = fields.Binary("Evidencia (PDF)", attachment=True)
    evidence_pdf_name = fields.Char()
    evidence_image_ids = fields.Many2many(
        "ir.attachment",
        "quality_inspection_evidence_rel",
        "inspection_id",
        "attachment_id",
        string="Evidencia (Imágenes)",
        help="Hasta 10 imágenes",
    )

    notes = fields.Html("Observaciones")
    certificate_ids = fields.One2many(
        "quality.certificate",
        "inspection_id",
        string="Certificados",
    )
    certificate_count = fields.Integer(compute="_compute_certificate_count")
    company_id = fields.Many2one(
        "res.company",
        "Compañía",
        default=lambda s: s.env.company,
    )

    def init(self):
        """
        FOLIO-QM-ODOO18-063:
        Migración defensiva para bases donde oct_hexagono ya recibió valores de selección.
        Copia esos valores al campo nuevo oct_hexagono_tipo sin eliminar ni transformar
        la columna legacy durante el upgrade.
        """
        super().init()
        cr = self.env.cr

        cr.execute(
            """
            SELECT EXISTS (
                SELECT 1
                  FROM information_schema.tables
                 WHERE table_name = 'quality_inspection'
            )
            """
        )
        table_exists = cr.fetchone()[0]
        if not table_exists:
            return

        cr.execute(
            """
            SELECT column_name
              FROM information_schema.columns
             WHERE table_name = 'quality_inspection'
               AND column_name IN ('oct_hexagono', 'oct_hexagono_tipo')
            """
        )
        existing_columns = {row[0] for row in cr.fetchall()}
        if not {"oct_hexagono", "oct_hexagono_tipo"}.issubset(existing_columns):
            return

        cr.execute(
            """
            UPDATE quality_inspection
               SET oct_hexagono_tipo = oct_hexagono::text
             WHERE oct_hexagono_tipo IS NULL
               AND oct_hexagono IS NOT NULL
               AND oct_hexagono::text IN ('tipo_1', 'tipo_2', 'tipo_3', 'tipo_4')
            """
        )

    @staticmethod
    def _sync_oct_hexagono_values(vals):
        """
        FOLIO-QM-ODOO18-064:
        Mantiene sincronizados el campo legacy y el campo nuevo durante el periodo
        de transición. Las nuevas capturas deben terminar en oct_hexagono_tipo.
        """
        vals = dict(vals)

        if "oct_hexagono" in vals and "oct_hexagono_tipo" not in vals:
            vals["oct_hexagono_tipo"] = vals.get("oct_hexagono")

        if "oct_hexagono_tipo" in vals and "oct_hexagono" not in vals:
            vals["oct_hexagono"] = vals.get("oct_hexagono_tipo")

        return vals

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
            rec.espesor_label = "Espesor (mm)" if rec.espesor_unit == "mm" else "Espesor (in)"

    @api.depends("pp_pt")
    def _compute_is_pp_pt(self):
        for rec in self:
            rec.is_pp = rec.pp_pt == "pp"
            rec.is_pt = rec.pp_pt == "pt"

    @api.constrains("evidence_image_ids")
    def _check_image_count(self):
        for rec in self:
            if len(rec.evidence_image_ids) > 10:
                raise ValidationError(_("Máximo 10 imágenes de evidencia por inspección."))

    @api.onchange("oct_hexagono")
    def _onchange_oct_hexagono_legacy(self):
        # FOLIO-QM-ODOO18-065: si alguna vista antigua todavía escribe en el campo legacy,
        # se migra inmediatamente al campo nuevo.
        for rec in self:
            if rec.oct_hexagono and not rec.oct_hexagono_tipo:
                rec.oct_hexagono_tipo = rec.oct_hexagono

    @api.onchange("oct_hexagono_tipo")
    def _onchange_oct_hexagono_tipo(self):
        # FOLIO-QM-ODOO18-066: mantiene compatibilidad con reportes o lógica antigua
        # que todavía consulten oct_hexagono.
        for rec in self:
            if rec.oct_hexagono_tipo:
                rec.oct_hexagono = rec.oct_hexagono_tipo

    @api.onchange("resistencia_na")
    def _onchange_resistencia_na(self):
        if self.resistencia_na:
            self.resistencia = 0.0

    @api.onchange(
        "largo",
        "ancho",
        "espesor",
        "humedad_pct",
        "resistencia",
        "calibracion",
    )
    def _onchange_alert_zero(self):
        zeros = []
        if self.show_largo and self.largo == 0:
            zeros.append("Largo")
        if self.show_ancho and self.ancho == 0:
            zeros.append("Ancho")
        if self.show_espesor and self.espesor == 0:
            zeros.append("Espesor")
        if self.show_humedad and self.humedad_pct == 0:
            zeros.append("Humedad")
        if self.show_resistencia and not self.resistencia_na and self.resistencia == 0:
            zeros.append("Resistencia")
        if zeros:
            return {
                "warning": {
                    "title": _("Valores en cero"),
                    "message": _("Atención: %s en 0. Verifique la captura.")
                    % ", ".join(zeros),
                }
            }
        return {}

    @api.onchange("production_order_id")
    def _onchange_production_order(self):
        if self.production_order_id:
            production = self.production_order_id
            if production.product_id:
                self.product_id = production.product_id

            sale_order = (
                self.env["sale.order"].search([("name", "=", production.origin)], limit=1)
                if production.origin
                else False
            )
            if sale_order and sale_order.partner_id:
                self.partner_id = sale_order.partner_id

    @api.onchange("product_id")
    def _onchange_product_partner(self):
        pass

    @api.onchange("process_type_id", "product_id")
    def _onchange_load_attribute_templates(self):
        if not self.process_type_id and not self.product_id:
            return

        templates = self.env["quality.attribute.template"]
        if self.process_type_id:
            templates |= self.process_type_id.attribute_template_ids.filtered(
                lambda template: not template.product_tmpl_id and template.active
            )

        if self.product_id and self.product_id.product_tmpl_id:
            templates |= self.env["quality.attribute.template"].search(
                [
                    ("product_tmpl_id", "=", self.product_id.product_tmpl_id.id),
                    ("active", "=", True),
                ]
            )

        if templates:
            lines = [(5, 0, 0)]
            seen_names = set()
            for template in templates.sorted(lambda item: (item.sequence, item.id)):
                key = (template.name or "").strip().lower()
                if key in seen_names:
                    continue
                seen_names.add(key)
                lines.append(
                    (
                        0,
                        0,
                        {
                            "attribute_template_id": template.id,
                            "name": template.name,
                            "attribute_type": template.attribute_type,
                            "min_value": template.min_value,
                            "max_value": template.max_value,
                            "unit": template.unit,
                            "sequence": template.sequence,
                        },
                    )
                )
            self.line_ids = lines

    @api.model_create_multi
    def create(self, vals_list):
        clean_vals_list = []
        for vals in vals_list:
            vals = self._sync_oct_hexagono_values(vals)
            if vals.get("name", "Nuevo") == "Nuevo":
                vals["name"] = (
                    self.env["ir.sequence"].next_by_code("quality.inspection")
                    or "Nuevo"
                )
            clean_vals_list.append(vals)
        return super().create(clean_vals_list)

    def write(self, vals):
        vals = self._sync_oct_hexagono_values(vals)
        return super().write(vals)

    def _check_previous_process(self):
        for rec in self:
            code = rec.process_type_id.code
            if code not in PROCESS_SEQUENCE:
                continue

            index = PROCESS_SEQUENCE.index(code)
            if index == 0:
                continue

            previous = PROCESS_SEQUENCE[index - 1]
            previous_inspection = self.search(
                [
                    ("lot_id", "=", rec.lot_id.id),
                    ("process_type_id.code", "=", previous),
                    ("state", "=", "aceptado"),
                ],
                limit=1,
            )
            if not previous_inspection:
                raise UserError(
                    _(
                        "Secuencia bloqueada: para liberar este proceso primero "
                        "debe estar liberado el proceso previo (%s) para el lote %s."
                    )
                    % (
                        previous.replace("_", " ").title(),
                        rec.lot_id.name or "—",
                    )
                )

    def _check_measures_captured(self):
        for rec in self:
            checks = []
            if rec.process_type_id.code == "troquelado_plano" and not rec.troquelado_ids:
                raise UserError(
                    _(
                        "Proceso Troquelado: debe capturar al menos una medida "
                        "en la pestaña Troquelado antes de liberar."
                    )
                )
            if (
                rec.process_type_id.code == "sierras_ranuradoras"
                and rec.show_ranurado
                and not rec.ranurado_ids
            ):
                raise UserError(
                    _(
                        "Proceso Sierras y Ranuradoras: capture al menos una "
                        "medida en la pestaña Ranurado antes de liberar."
                    )
                )
            if rec.show_largo and not rec.largo:
                checks.append("Largo")
            if rec.show_ancho and not (rec.ancho or rec.oct_ancho):
                checks.append("Ancho")
            if rec.show_espesor and not (rec.espesor or rec.oct_espesor):
                checks.append("Espesor")

            # FOLIO-QM-ODOO18-067: la validación acepta el campo nuevo
            # oct_hexagono_tipo y conserva compatibilidad con oct_hexagono legacy.
            if rec.show_hexagono and not (
                rec.hexagono
                or rec.tipo_hexagono
                or rec.oct_hexagono_tipo
                or rec.oct_hexagono
            ):
                checks.append("Hexágono")

            if rec.show_resistencia and not rec.resistencia_na and not rec.resistencia:
                checks.append("Resistencia")
            if rec.show_apariencia and not rec.apariencia:
                checks.append("Apariencia")
            if rec.show_humedad and not rec.humedad_pct:
                checks.append("Humedad")

            if checks:
                raise UserError(
                    _(
                        "Capture Medidas y Propiedades antes de cerrar la inspección. "
                        "Faltan: %s"
                    )
                    % ", ".join(checks)
                )

    def action_start(self):
        for rec in self:
            rec.state = "en_proceso"
            rec.message_post(
                body=_("Inspección iniciada."),
                subtype_xmlid="mail.mt_comment",
            )

    def action_accept(self):
        for rec in self:
            if rec.state != "en_proceso":
                raise UserError(_("Debe presionar 'INICIAR INSPECCION' antes de liberar."))
            rec._check_measures_captured()
            rec._check_previous_process()
            rec.state = "aceptado"
            rec.message_post(
                body=_("Inspección ACEPTADA por %s") % self.env.user.name,
                subtype_xmlid="mail.mt_comment",
            )

    def action_retain(self):
        for rec in self:
            rec.state = "retenido"
            partners = []
            if (
                rec.supervisor_id
                and rec.supervisor_id.user_id
                and rec.supervisor_id.user_id.partner_id
            ):
                partner_id = rec.supervisor_id.user_id.partner_id.id
                partners.append(partner_id)
                # FOLIO-QM-ODOO18-025: se usa el argumento explícito partner_ids
                # para evitar ambigüedad en message_subscribe.
                rec.message_subscribe(partner_ids=[partner_id])

            rec.message_post(
                body=_(
                    "Producto RETENIDO por %s. Lote: %s. "
                    "Notificando al supervisor en turno: %s."
                )
                % (
                    self.env.user.name,
                    rec.lot_id.name or "N/A",
                    rec.supervisor_id.name or "—",
                ),
                partner_ids=partners,
                subtype_xmlid="mail.mt_comment",
            )

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
        # FOLIO-QM-ODOO18-060: los grupos en vistas no son seguridad real;
        # se agrega validación backend para evitar RPC manual no autorizado.
        if not self.env.user.has_group("quality_management.group_quality_manager"):
            raise UserError(_("Solo Responsable de Calidad puede regresar inspecciones a borrador."))
        for rec in self:
            rec.state = "borrador"

    def action_create_certificate(self):
        self.ensure_one()
        if self.state != "aceptado":
            raise UserError(_("Solo se pueden crear certificados de inspecciones aceptadas."))
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
        ).report_action(self)```

## ./models/quality_ishikawa.py
```py
# -*- coding: utf-8 -*-
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
```

## ./models/quality_process_route.py
```py
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

        return True```

## ./models/quality_process_type.py
```py
from odoo import models, fields


class QualityProcessType(models.Model):
    _name = 'quality.process.type'
    _description = 'Tipo de Proceso de Calidad'
    _order = 'sequence, id'

    name = fields.Char('Nombre del Proceso', required=True)
    code = fields.Char(
        'Código Interno', required=True,
        help='Código único. Ej: laminadora_remanejo, octagono, corte_laser'
    )
    sequence = fields.Integer('Secuencia', default=10)
    active = fields.Boolean('Activo', default=True)
    description = fields.Text('Descripción')
    # Configuración de campos visibles
    show_largo = fields.Boolean('Mostrar Largo')
    show_ancho = fields.Boolean('Mostrar Ancho')
    show_espesor = fields.Boolean('Mostrar Espesor')
    show_hexagono = fields.Boolean('Mostrar Hexágono')
    show_resistencia = fields.Boolean('Mostrar Resistencia')
    show_apariencia = fields.Boolean('Mostrar Apariencia')
    show_humedad = fields.Boolean('Mostrar % Humedad')
    show_pegado = fields.Boolean('Mostrar Pegado')
    show_retiramiento = fields.Boolean('Mostrar Retiramiento')
    show_calibracion = fields.Boolean('Mostrar Calibración')
    show_engomado = fields.Boolean('Mostrar Engomado')
    show_alineacion = fields.Boolean('Mostrar Alineación')
    show_ranurado = fields.Boolean('Mostrar Ranurado')
    show_troquelado = fields.Boolean('Mostrar Troquelado')
    show_papel = fields.Boolean('Mostrar Datos de Papel')
    show_adhesivo = fields.Boolean('Mostrar Datos de Adhesivo')
    show_tipo_hexagono = fields.Boolean('Mostrar Tipo de Hexágono')
    show_corte_guillotina = fields.Boolean('Mostrar Corte en Guillotina')
    show_numero_corrida = fields.Boolean('Mostrar Número de Corrida')
    # Plantillas de atributos
    attribute_template_ids = fields.One2many(
        'quality.attribute.template', 'process_type_id',
        string='Plantillas de Atributos'
    )
    company_id = fields.Many2one(
        'res.company', 'Compañía',
        default=lambda self: self.env.company
    )

    _sql_constraints = [
        ('code_company_unique', 'unique(code, company_id)',
         'El código del proceso debe ser único por compañía.'),
    ]
```

## ./models/quality_retention_flow.py
```py
# -*- coding: utf-8 -*-
"""
Ciclo completo: Retenido → Corrección por Producción → Hecho → Reinspección.
Se monta sobre el state existente sin modificarlo, usando un sub-estado.
"""
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import timedelta


class QualityInspectionRetention(models.Model):
    _inherit = "quality.inspection"

    retention_state = fields.Selection([
        ("none", "Sin retención"),
        ("retenido", "Retenido — esperando corrección"),
        ("en_correccion", "En corrección por Producción"),
        ("correccion_hecha", "Corrección hecha — pendiente reinspección"),
        ("reinspeccion", "Reinspección en curso"),
        ("liberado_post_retencion", "Liberado tras reinspección"),
        ("rechazado_post_retencion", "Rechazado tras reinspección"),
    ], default="none", required=True, tracking=True, copy=False,
       string="Sub-estado de Retención")

    retention_log_ids = fields.One2many(
        "quality.inspection.retention.log", "inspection_id",
        string="Bitácora de Retención")
    retention_correction_notes = fields.Html(
        "Notas de Corrección (Producción)")
    retention_correction_done_by = fields.Many2one(
        "res.users", "Producción marcó hecho", readonly=True)
    retention_correction_done_date = fields.Datetime(
        "Fecha Hecho", readonly=True)

    def _log_retention(self, msg):
        for rec in self:
            self.env["quality.inspection.retention.log"].create({
                "inspection_id": rec.id,
                "user_id": self.env.user.id,
                "description": msg,
                "retention_state_after": rec.retention_state,
            })

    # ---- Override: cuando se retiene, marcar sub-estado --------------------
    def action_retain(self):
        res = super().action_retain()
        for rec in self:
            rec.retention_state = "retenido"
            rec._log_retention(_("Producto retenido por Calidad."))
        return res

    # ---- Producción acepta corregir ----------------------------------------
    def action_accept_correction(self):
        for rec in self:
            if rec.state != "retenido" or rec.retention_state not in (
                    "retenido", "en_correccion"):
                raise UserError(_(
                    "Solo se puede aceptar corrección desde una inspección retenida."))
            rec.retention_state = "en_correccion"
            rec._log_retention(_("Producción acepta corregir el producto."))

    # ---- Producción / Supervisor marca corrección como hecha ---------------
    def action_correction_done(self):
        for rec in self:
            if rec.retention_state not in ("retenido", "en_correccion"):
                raise UserError(_(
                    "La inspección no está en estado de corrección."))
            rec.retention_state = "correccion_hecha"
            rec.retention_correction_done_by = self.env.user
            rec.retention_correction_done_date = fields.Datetime.now()
            rec._log_retention(
                _("Supervisor/Producción marca corrección como HECHA."))

            # Avisar a Calidad
            inspector = rec.inspector_id
            if inspector:
                rec.activity_schedule(
                    "mail.mail_activity_data_todo",
                    date_deadline=fields.Date.today() + timedelta(days=1),
                    summary=_("Reinspeccionar producto: %s") % rec.name,
                    user_id=inspector.id)
            partners = []
            if inspector and inspector.partner_id:
                partners.append(inspector.partner_id.id)
            rec.message_post(
                body=_("✋ Producción marcó corrección hecha. Calidad debe REINSPECCIONAR."),
                partner_ids=partners,
                subtype_xmlid="mail.mt_comment")

    # ---- Calidad inicia reinspección ---------------------------------------
    def action_start_reinspection(self):
        for rec in self:
            if rec.retention_state != "correccion_hecha":
                raise UserError(_(
                    "No hay corrección pendiente de reinspección."))
            rec.retention_state = "reinspeccion"
            rec.state = "en_proceso"  # reabrir captura
            rec._log_retention(_("Calidad inicia reinspección."))

    # ---- Calidad acepta tras reinspección ----------------------------------
    def action_accept_after_retention(self):
        for rec in self:
            if rec.retention_state != "reinspeccion":
                raise UserError(_(
                    "Debe iniciar la reinspección primero."))
            rec._full_quality_validation_hardening()
            rec.state = "aceptado"
            rec.retention_state = "liberado_post_retencion"
            rec._log_retention(_("Aceptado tras reinspección."))

    # ---- Calidad rechaza tras reinspección ---------------------------------
    def action_reject_after_retention(self):
        for rec in self:
            if rec.retention_state != "reinspeccion":
                raise UserError(_(
                    "Debe iniciar la reinspección primero."))
            rec.state = "rechazado"
            rec.retention_state = "rechazado_post_retencion"
            rec._log_retention(_("Rechazado tras reinspección."))


class QualityInspectionRetentionLog(models.Model):
    _name = "quality.inspection.retention.log"
    _description = "Bitácora de Retención"
    _order = "date desc, id desc"

    inspection_id = fields.Many2one(
        "quality.inspection", required=True, ondelete="cascade", index=True)
    date = fields.Datetime(default=fields.Datetime.now, readonly=True)
    user_id = fields.Many2one("res.users", "Usuario")
    description = fields.Text("Descripción", required=True)
    retention_state_after = fields.Char("Sub-estado tras evento")
```

## ./models/quality_sample_release.py
```py
# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class QualitySampleRelease(models.Model):
    _name = "quality.sample.release"
    _description = "Liberación de Muestras"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_requested desc, id desc"

    name = fields.Char(
        "Referencia",
        required=True,
        readonly=True,
        default="Nuevo",
        copy=False,
    )

    sample_type = fields.Selection(
        [
            ("mp", "Opción 1: MP - Sale de Laminadora"),
            ("pt", "Opción 2: PT - Pasa por Taller CNC / Transformación"),
        ],
        string="Tipo de Muestra",
        required=True,
        default="mp",
        tracking=True,
    )

    project_task_id = fields.Many2one(
        "project.task",
        "Tarea de Proyecto",
        required=True,
        tracking=True,
    )
    product_id = fields.Many2one(
        "product.product",
        "Producto/Muestra",
        required=True,
        tracking=True,
    )
    requested_by = fields.Many2one(
        "res.users",
        "Solicitante (Diseño)",
        required=True,
        default=lambda s: s.env.user,
        tracking=True,
    )
    inspector_id = fields.Many2one(
        "res.users",
        "Inspector de Calidad",
        tracking=True,
    )

    date_requested = fields.Datetime(
        "Fecha de Solicitud",
        required=True,
        readonly=True,
        copy=False,
        default=fields.Datetime.now,
    )
    date_limit = fields.Datetime(
        "Fecha Límite de Inspección",
        compute="_compute_date_limit",
        store=True,
        readonly=True,
        copy=False,
        help="Solicitud + 48 horas",
    )
    date_inspected = fields.Datetime(
        "Fecha de Inspección",
        readonly=True,
        copy=False,
        tracking=True,
    )

    state = fields.Selection(
        [
            ("borrador", "Borrador"),
            ("en_inspeccion", "En Inspección"),
            ("aceptado", "Aceptado"),
            ("rechazado", "Rechazado"),
        ],
        default="borrador",
        required=True,
        tracking=True,
        copy=False,
    )

    inspection_line_ids = fields.One2many(
        "quality.inspection.line",
        "sample_release_id",
        string="Atributos Inspeccionados",
    )

    spec_pdf = fields.Binary("Especificación (PDF)", attachment=True)
    spec_pdf_name = fields.Char("Nombre Especificación")

    evidence_ids = fields.Many2many(
        "ir.attachment",
        "quality_sample_evidence_rel",
        "sample_id",
        "attachment_id",
        string="Evidencia",
    )

    cnc_design_user_id = fields.Many2one("res.users", "Personal de Diseño")
    cnc_date_realized = fields.Datetime("Fecha de Realización CNC", readonly=True)
    cnc_observations = fields.Html("Observaciones CNC")

    notes = fields.Html("Observaciones")
    company_id = fields.Many2one(
        "res.company",
        "Compañía",
        default=lambda s: s.env.company,
    )

    @api.depends("date_requested")
    def _compute_date_limit(self):
        for rec in self:
            rec.date_limit = (
                rec.date_requested + timedelta(hours=48)
                if rec.date_requested
                else False
            )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Nuevo") == "Nuevo":
                vals["name"] = (
                    self.env["ir.sequence"].next_by_code("quality.sample.release")
                    or "Nuevo"
                )
        return super().create(vals_list)

    def _check_attributes_valid(self):
        for rec in self:
            if not rec.inspection_line_ids:
                raise UserError(
                    _("Debe capturar al menos un atributo de inspección antes de avanzar.")
                )

            # FOLIO-QM-ODOO18-027: se respeta N/A y allow_zero; antes todo float en 0
            # bloqueaba incluso cuando el atributo no aplicaba.
            zero_lines = rec.inspection_line_ids.filtered(
                lambda line: (
                    line.attribute_type == "float"
                    and not getattr(line, "allow_zero", False)
                    and not line.value_float
                    and line.result != "na"
                )
            )
            if zero_lines:
                raise UserError(
                    _("Hay atributos con valor 0 que deben capturarse: %s")
                    % ", ".join(zero_lines.mapped("name"))
                )

    def _check_spec_pdf(self):
        for rec in self:
            if not rec.spec_pdf:
                raise UserError(
                    _(
                        "La Especificación PDF es obligatoria. "
                        "Sin plano o dibujo no se puede inspeccionar."
                    )
                )

    def _check_pt_workflow(self):
        for rec in self:
            if rec.sample_type == "pt" and not rec.cnc_date_realized:
                raise UserError(
                    _(
                        "Esta muestra PT requiere captura previa en Transformación "
                        "(Taller CNC) antes de mover a Inspección de Calidad."
                    )
                )

    def action_register_cnc(self):
        for rec in self:
            if rec.sample_type != "pt":
                raise UserError(_("Solo aplica a muestras PT."))

            rec._check_attributes_valid()
            rec.cnc_date_realized = fields.Datetime.now()
            rec.cnc_design_user_id = self.env.user
            rec.message_post(
                body=_("CNC: transformación registrada por %s") % self.env.user.name,
                subtype_xmlid="mail.mt_comment",
            )

    def action_submit_inspection(self):
        for rec in self:
            rec._check_spec_pdf()
            rec._check_pt_workflow()
            rec._check_attributes_valid()
            rec.state = "en_inspeccion"

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
                    summary=_("Inspección de muestra: %s") % rec.name,
                    user_id=user.id,
                )

    def action_accept(self):
        for rec in self:
            rec._check_attributes_valid()
            failing = rec.inspection_line_ids.filtered(
                lambda line: line.result in ("no_cumple", "no_ok")
            )
            if failing:
                raise UserError(
                    _("No se puede liberar: hay %d atributo(s) que no cumplen.")
                    % len(failing)
                )

            rec.state = "aceptado"
            rec.date_inspected = fields.Datetime.now()
            rec.activity_feedback(
                ["mail.mail_activity_data_todo"],
                feedback=_("Muestra aceptada"),
            )
            rec.message_post(
                body=_("Muestra ACEPTADA y liberada por %s") % self.env.user.name,
                subtype_xmlid="mail.mt_comment",
            )

    def action_reject(self):
        for rec in self:
            rec.state = "rechazado"
            rec.date_inspected = fields.Datetime.now()
            rec.activity_feedback(
                ["mail.mail_activity_data_todo"],
                feedback=_("Muestra rechazada"),
            )

            partner_ids = []
            if rec.requested_by.partner_id:
                partner_ids.append(rec.requested_by.partner_id.id)
                rec.message_subscribe(partner_ids=partner_ids)

            rec.message_post(
                body=_("Muestra RECHAZADA por %s. Notificando a la solicitante: %s")
                % (self.env.user.name, rec.requested_by.name),
                partner_ids=partner_ids,
                subtype_xmlid="mail.mt_comment",
            )

    def action_reset_draft(self):
        for rec in self:
            rec.state = "borrador"

    def action_print_sample_release(self):
        return self.env.ref(
            "quality_management.action_report_sample_release"
        ).report_action(self)```

## ./models/quality_security_enforcement.py
```py
# -*- coding: utf-8 -*-
from odoo import api, models, _
from odoo.exceptions import AccessError


class MrpProductionQualitySecurity(models.Model):
    _inherit = "mrp.production"

    @api.model_create_multi
    def create(self, vals_list):
        # FOLIO-QM-ODOO18-029: las reglas ir.rule no niegan create/write;
        # se agrega enforcement explícito para que inspectores no creen OP.
        if (
            self.env.user.has_group("quality_management.group_quality_inspector")
            and not self.env.user.has_group("quality_management.group_quality_manager")
        ):
            raise AccessError(_("Un inspector de Calidad no puede crear órdenes de producción."))
        return super().create(vals_list)

    def write(self, vals):
        if (
            self.env.user.has_group("quality_management.group_quality_inspector")
            and not self.env.user.has_group("quality_management.group_quality_manager")
        ):
            raise AccessError(_("Un inspector de Calidad no puede modificar órdenes de producción."))
        return super().write(vals)

    def unlink(self):
        if (
            self.env.user.has_group("quality_management.group_quality_inspector")
            and not self.env.user.has_group("quality_management.group_quality_manager")
        ):
            raise AccessError(_("Un inspector de Calidad no puede eliminar órdenes de producción."))
        return super().unlink()


class StockLotQualitySecurity(models.Model):
    _inherit = "stock.lot"

    @api.model_create_multi
    def create(self, vals_list):
        # FOLIO-QM-ODOO18-029: las reglas ir.rule no niegan create/write;
        # se agrega enforcement explícito para que inspectores no creen lotes.
        if (
            self.env.user.has_group("quality_management.group_quality_inspector")
            and not self.env.user.has_group("quality_management.group_quality_manager")
        ):
            raise AccessError(_("Un inspector de Calidad no puede crear lotes."))
        return super().create(vals_list)

    def write(self, vals):
        if (
            self.env.user.has_group("quality_management.group_quality_inspector")
            and not self.env.user.has_group("quality_management.group_quality_manager")
        ):
            raise AccessError(_("Un inspector de Calidad no puede modificar lotes."))
        return super().write(vals)

    def unlink(self):
        if (
            self.env.user.has_group("quality_management.group_quality_inspector")
            and not self.env.user.has_group("quality_management.group_quality_manager")
        ):
            raise AccessError(_("Un inspector de Calidad no puede eliminar lotes."))
        return super().unlink()```

## ./models/quality_troquel_validation.py
```py
# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class QualityTroquelValidation(models.Model):
    _name = "quality.troquel.validation"
    _description = "Validación de Troquel"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date desc, id desc"

    name = fields.Char("Referencia", default="Nueva", readonly=True, copy=False)
    troquel_id = fields.Many2one(
        "quality.troquel",
        required=True,
        ondelete="cascade",
        tracking=True,
        index=True,
    )
    date = fields.Datetime(default=fields.Datetime.now, required=True)
    convoked_quality = fields.Boolean("Calidad Convocada")
    convoked_production = fields.Boolean("Producción Convocada")

    quality_user_id = fields.Many2one("res.users", "Calidad")
    production_user_id = fields.Many2one("res.users", "Producción")
    design_user_id = fields.Many2one("res.users", "Diseño")

    line_ids = fields.One2many(
        "quality.troquel.validation.line",
        "validation_id",
        string="Mediciones / Pruebas",
    )

    dimensional_ok = fields.Boolean(
        "Dimensional OK",
        compute="_compute_results",
        store=True,
    )
    functional_ok = fields.Boolean(
        "Funcional OK",
        compute="_compute_results",
        store=True,
    )
    overall_ok = fields.Boolean(
        "Resultado Global",
        compute="_compute_results",
        store=True,
    )

    state = fields.Selection(
        [
            ("borrador", "Borrador"),
            ("en_validacion", "En Validación"),
            ("aprobado", "Aprobado"),
            ("rechazado", "Rechazado"),
        ],
        default="borrador",
        required=True,
        tracking=True,
    )
    notes = fields.Text("Observaciones")

    @api.depends("line_ids.result", "line_ids.test_type")
    def _compute_results(self):
        for rec in self:
            dimensional_lines = rec.line_ids.filtered(
                lambda line: line.test_type == "dimensional"
            )
            functional_lines = rec.line_ids.filtered(
                lambda line: line.test_type == "funcional"
            )
            rec.dimensional_ok = bool(dimensional_lines) and all(
                line.result == "cumple" for line in dimensional_lines
            )
            rec.functional_ok = bool(functional_lines) and all(
                line.result == "cumple" for line in functional_lines
            )
            rec.overall_ok = rec.dimensional_ok and rec.functional_ok

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Nueva") == "Nueva":
                # FOLIO-QM-ODOO18-028: la secuencia ya contiene prefijo TVAL-;
                # no debe anteponerse nuevamente para evitar TVAL-TVAL-0001.
                vals["name"] = (
                    self.env["ir.sequence"].next_by_code("quality.troquel.validation")
                    or "Nueva"
                )
        return super().create(vals_list)

    def action_start(self):
        for rec in self:
            rec.state = "en_validacion"

    def action_approve(self):
        for rec in self:
            if not rec.dimensional_ok or not rec.functional_ok:
                raise UserError(
                    _(
                        "No se puede aprobar: faltan pruebas dimensionales "
                        "o funcionales OK."
                    )
                )
            rec.state = "aprobado"
            rec.troquel_id.action_activate()

    def action_reject(self):
        for rec in self:
            rec.state = "rechazado"
            rec.troquel_id.message_post(
                body=_("Validación rechazada (%s).") % rec.name,
                subtype_xmlid="mail.mt_comment",
            )


class QualityTroquelValidationLine(models.Model):
    _name = "quality.troquel.validation.line"
    _description = "Línea de Validación de Troquel"
    _order = "sequence, id"

    validation_id = fields.Many2one(
        "quality.troquel.validation",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(default=10)
    test_type = fields.Selection(
        [
            ("dimensional", "Dimensional"),
            ("funcional", "Funcional"),
        ],
        required=True,
        default="dimensional",
    )
    name = fields.Char("Concepto / Punto de Medición", required=True)
    expected = fields.Char("Valor Esperado / Especificación")
    measured = fields.Char("Valor Medido / Observado")
    tolerance = fields.Char("Tolerancia")
    result = fields.Selection(
        [
            ("cumple", "Cumple"),
            ("no_cumple", "No Cumple"),
            ("na", "N/A"),
        ],
        default="na",
        required=True,
    )
    notes = fields.Char("Notas")


class QualityTroquelRepair(models.Model):
    _name = "quality.troquel.repair"
    _description = "Reparación de Troquel"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_started desc, id desc"

    name = fields.Char(default="Nueva", readonly=True, copy=False)
    troquel_id = fields.Many2one(
        "quality.troquel",
        required=True,
        ondelete="cascade",
        index=True,
    )
    repair_type = fields.Selection(
        [
            ("interna", "Interna"),
            ("proveedor", "Proveedor Externo"),
        ],
        required=True,
        default="interna",
    )
    proveedor_id = fields.Many2one(
        "res.partner",
        "Proveedor",
        domain=[("supplier_rank", ">", 0)],
    )
    date_started = fields.Datetime(
        "Inicio Reparación",
        default=fields.Datetime.now,
        required=True,
    )
    date_finished = fields.Datetime("Fin Reparación")
    days_estimated = fields.Integer("Días Estimados Fuera")
    description = fields.Text("Desglose de Reparación", required=True)
    cost = fields.Monetary("Costo")
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda s: s.env.company.currency_id,
    )
    state = fields.Selection(
        [
            ("en_curso", "En Curso"),
            ("finalizada", "Finalizada"),
            ("rechazada", "Rechazada"),
        ],
        default="en_curso",
        required=True,
        tracking=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Nueva") == "Nueva":
                # FOLIO-QM-ODOO18-028: la secuencia ya contiene prefijo TREP-;
                # no debe anteponerse nuevamente para evitar TREP-TREP-0001.
                vals["name"] = (
                    self.env["ir.sequence"].next_by_code("quality.troquel.repair")
                    or "Nueva"
                )
        return super().create(vals_list)

    def action_finish(self):
        for rec in self:
            rec.state = "finalizada"
            rec.date_finished = fields.Datetime.now()
            rec.troquel_id.message_post(
                body=_("Reparación %s finalizada.") % rec.name,
                subtype_xmlid="mail.mt_comment",
            )
            # FOLIO-QM-ODOO18-029: al finalizar reparación, el troquel vuelve
            # a validación para no quedar activo sin revisión dimensional/funcional.
            if rec.troquel_id.state in ("reparacion_interna", "reparacion_proveedor", "danado"):
                rec.troquel_id.state = "validacion"


class QualityTroquelExtended(models.Model):
    _inherit = "quality.troquel"

    validation_ids = fields.One2many(
        "quality.troquel.validation",
        "troquel_id",
        string="Validaciones",
    )
    validation_count = fields.Integer(compute="_compute_counts")
    repair_ids = fields.One2many(
        "quality.troquel.repair",
        "troquel_id",
        string="Reparaciones",
    )
    repair_count = fields.Integer(compute="_compute_counts")
    pieces_produced = fields.Integer(
        "Piezas Producidas Acumuladas",
        help="Conteo manual de piezas troqueladas para programar revisión.",
    )
    needs_review = fields.Boolean(
        "Requiere Revisión",
        compute="_compute_needs_review",
        store=True,
    )

    @api.depends("validation_ids", "repair_ids")
    def _compute_counts(self):
        for rec in self:
            rec.validation_count = len(rec.validation_ids)
            rec.repair_count = len(rec.repair_ids)

    @api.depends("pieces_produced", "pieces_per_review")
    def _compute_needs_review(self):
        for rec in self:
            rec.needs_review = bool(
                rec.pieces_per_review
                and rec.pieces_produced >= rec.pieces_per_review
            )

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
        }```

## ./models/quality_troquel.py
```py
# -*- coding: utf-8 -*-
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
```

## ./models/quality_work_team.py
```py
# -*- coding: utf-8 -*-
from odoo import models, fields


class QualityWorkTeam(models.Model):
    _name = "quality.work.team"
    _description = "Equipo de Trabajo (8D)"

    corrective_id = fields.Many2one("quality.corrective.action", required=True,
                                    ondelete="cascade", index=True)
    user_id = fields.Many2one("res.users", "Miembro", required=True)
    role = fields.Char("Rol en el Equipo")
    notify_progress = fields.Boolean("Notificar Avances", default=True)
```

## ./models/res_company.py
```py
from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    quality_stamp = fields.Binary(
        'Sello de Calidad',
        help='Imagen del sello de la empresa que aparece en los certificados de calidad.'
    )```

## ./reports/report_8d_extended.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <template id="report_8d_document_extended"
              inherit_id="quality_management.report_8d_document">
        <xpath expr="//h4[contains(., 'D6 - Plan de Acciones')]" position="before">
            <h4>D4 - 5 Por qué</h4>
            <table class="table table-bordered table-sm" style="margin-bottom: 15px;">
                <thead>
                    <tr class="table-active">
                        <th style="width: 10%;">N°</th>
                        <th style="width: 35%;">Pregunta</th>
                        <th>Respuesta</th>
                    </tr>
                </thead>
                <tbody>
                    <tr t-foreach="doc.why_ids" t-as="why">
                        <td><span t-field="why.sequence"/></td>
                        <td><span t-field="why.question"/></td>
                        <td><span t-field="why.answer"/></td>
                    </tr>
                </tbody>
            </table>

            <h4>D5 - Análisis Causa-Efecto (Ishikawa)</h4>
            <table class="table table-bordered table-sm" style="margin-bottom: 15px;">
                <thead>
                    <tr class="table-active">
                        <th style="width: 25%;">Categoría</th>
                        <th>Causa</th>
                        <th style="width: 15%;" class="text-center">Causa Raíz</th>
                    </tr>
                </thead>
                <tbody>
                    <tr t-foreach="doc.ishikawa_ids" t-as="ish">
                        <td><span t-field="ish.category"/></td>
                        <td><span t-field="ish.cause"/></td>
                        <td class="text-center">
                            <t t-if="ish.is_root_cause">
                                <strong style="color:#c00;">★ RAÍZ</strong>
                            </t>
                        </td>
                    </tr>
                </tbody>
            </table>

            <h4>D2 - Equipo de Trabajo</h4>
            <table class="table table-bordered table-sm" style="margin-bottom: 15px;">
                <thead>
                    <tr class="table-active">
                        <th>Miembro</th>
                        <th>Rol</th>
                        <th class="text-center">Notifica</th>
                    </tr>
                </thead>
                <tbody>
                    <tr t-foreach="doc.work_team_ids" t-as="m">
                        <td><span t-field="m.user_id.name"/></td>
                        <td><span t-field="m.role"/></td>
                        <td class="text-center">
                            <t t-if="m.notify_progress">Sí</t>
                            <t t-else="">No</t>
                        </td>
                    </tr>
                </tbody>
            </table>
        </xpath>
    </template>
</odoo>
```

## ./reports/report_8d.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="action_report_8d" model="ir.actions.report">
        <field name="name">Reporte 8D</field>
        <field name="model">quality.corrective.action</field>
        <field name="report_type">qweb-pdf</field>
        <field name="report_name">quality_management.report_8d_document</field>
        <field name="report_file">quality_management.report_8d_document</field>
        <field name="binding_model_id" ref="model_quality_corrective_action"/>
        <field name="binding_type">report</field>
    </record>

    <template id="report_8d_document">
        <t t-call="web.html_container">
            <t t-foreach="docs" t-as="doc">
                <t t-call="web.external_layout">
                    <div class="page">
                        <div class="text-center" style="margin-bottom: 20px;">
                            <h2>REPORTE 8D</h2>
                            <h3>ACCIÓN CORRECTIVA / PREVENTIVA</h3>
                            <h4 t-field="doc.name"/>
                        </div>

                        <table class="table table-bordered" style="margin-bottom: 20px;">
                            <tbody>
                                <tr>
                                    <td class="fw-bold" style="width: 30%;">Referencia:</td>
                                    <td><span t-field="doc.name"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Tipo de Origen:</td>
                                    <td><span t-field="doc.origin_type"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Fecha de Apertura:</td>
                                    <td><span t-field="doc.date_opened"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Responsable General:</td>
                                    <td><span t-field="doc.responsible_id.name"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Estado:</td>
                                    <td><span t-field="doc.state"/></td>
                                </tr>
                                <tr t-if="doc.date_closed">
                                    <td class="fw-bold">Fecha de Cierre:</td>
                                    <td><span t-field="doc.date_closed"/></td>
                                </tr>
                                <tr t-if="doc.origin_return_id">
                                    <td class="fw-bold">Devolución:</td>
                                    <td><span t-field="doc.origin_return_id.name"/></td>
                                </tr>
                                <tr t-if="doc.origin_inspection_id">
                                    <td class="fw-bold">Inspección:</td>
                                    <td><span t-field="doc.origin_inspection_id.name"/></td>
                                </tr>
                            </tbody>
                        </table>

                        <h4>D1 - Descripción del Problema</h4>
                        <div style="border: 1px solid #dee2e6; padding: 10px; margin-bottom: 15px; min-height: 60px;">
                            <span t-field="doc.origin_description"/>
                        </div>

                        <t t-if="doc.origin_return_id">
                            <h4>D2 - Datos de la Reclamación</h4>
                            <table class="table table-bordered table-sm" style="margin-bottom: 15px;">
                                <tbody>
                                    <tr>
                                        <td class="fw-bold" style="width: 30%;">Cliente:</td>
                                        <td><span t-field="doc.origin_return_id.partner_id.name"/></td>
                                    </tr>
                                    <tr>
                                        <td class="fw-bold">Tipo de Defecto:</td>
                                        <td><span t-field="doc.origin_return_id.defect_type"/></td>
                                    </tr>
                                    <tr>
                                        <td class="fw-bold">Piezas Afectadas:</td>
                                        <td><span t-field="doc.origin_return_id.defect_pieces"/></td>
                                    </tr>
                                    <tr>
                                        <td class="fw-bold">Afecta Funcionalidad:</td>
                                        <td><span t-field="doc.origin_return_id.affects_functionality"/></td>
                                    </tr>
                                </tbody>
                            </table>
                        </t>

                        <h4>D3 - Contención</h4>
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

                        <h4>D6 - Plan de Acciones</h4>
                        <table class="table table-bordered table-sm">
                            <thead>
                                <tr class="table-active">
                                    <th style="width: 5%;">#</th>
                                    <th style="width: 35%;">Acción</th>
                                    <th>Responsable</th>
                                    <th>Fecha Límite</th>
                                    <th>Fecha Real</th>
                                    <th>Atraso</th>
                                    <th>Estado</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr t-foreach="doc.action_line_ids" t-as="line">
                                    <td><t t-esc="line_index + 1"/></td>
                                    <td><span t-field="line.description"/></td>
                                    <td><span t-field="line.responsible_id.name"/></td>
                                    <td><span t-field="line.date_due"/></td>
                                    <td><span t-field="line.date_completed"/></td>
                                    <td>
                                        <t t-if="line.delay_days > 0">
                                            <span t-field="line.delay_days"/> días
                                        </t>
                                    </td>
                                    <td><span t-field="line.state"/></td>
                                </tr>
                            </tbody>
                        </table>

                        <h4>D7 - Acciones Preventivas Sistémicas</h4>
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
                        </div>
                    </div>
                </t>
            </t>
        </t>
    </template>
</odoo>
```

## ./reports/report_customer_document.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="action_report_customer_document" model="ir.actions.report">
        <field name="name">Ficha de Documento de Cliente</field>
        <field name="model">quality.customer.document</field>
        <field name="report_type">qweb-pdf</field>
        <field name="report_name">quality_management.report_customer_document_doc</field>
        <field name="report_file">quality_management.report_customer_document_doc</field>
        <field name="binding_model_id" ref="model_quality_customer_document"/>
        <field name="binding_type">report</field>
    </record>

    <template id="report_customer_document_doc">
        <t t-call="web.html_container">
            <t t-foreach="docs" t-as="doc">
                <t t-call="web.external_layout">
                    <div class="page">
                        <div class="text-center" style="margin-bottom: 20px;">
                            <h2>FICHA DE DOCUMENTO SOLICITADO POR CLIENTE</h2>
                            <h4 t-field="doc.name"/>
                        </div>

                        <div class="text-center" style="margin-bottom: 15px;">
                            <t t-if="doc.state == 'enviado'">
                                <span style="background-color: #28a745; color: white; padding: 5px 20px; border-radius: 4px; font-size: 14px; font-weight: bold;">ENVIADO</span>
                            </t>
                            <t t-if="doc.state == 'completado'">
                                <span style="background-color: #17a2b8; color: white; padding: 5px 20px; border-radius: 4px; font-size: 14px; font-weight: bold;">COMPLETADO</span>
                            </t>
                            <t t-if="doc.state == 'en_proceso'">
                                <span style="background-color: #ffc107; color: #333; padding: 5px 20px; border-radius: 4px; font-size: 14px; font-weight: bold;">EN PROCESO</span>
                            </t>
                        </div>

                        <table class="table table-bordered" style="margin-bottom: 20px;">
                            <tbody>
                                <tr>
                                    <td class="fw-bold" style="width: 30%;">Referencia:</td>
                                    <td><span t-field="doc.name"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Cliente Solicitante:</td>
                                    <td><span t-field="doc.partner_id.name"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Tipo de Documento:</td>
                                    <td><span t-field="doc.document_type"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Implica Mediciones:</td>
                                    <td>
                                        <span t-if="doc.requires_dimensions">Sí</span>
                                        <span t-if="not doc.requires_dimensions">No</span>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Solicitante (Ventas):</td>
                                    <td><span t-field="doc.requested_by.name"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Responsable (Calidad):</td>
                                    <td><span t-field="doc.responsible_id.name"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Fecha de Solicitud:</td>
                                    <td><span t-field="doc.date_requested"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Fecha Límite:</td>
                                    <td><span t-field="doc.date_due"/></td>
                                </tr>
                                <tr t-if="doc.date_completed">
                                    <td class="fw-bold">Fecha de Entrega Real:</td>
                                    <td><span t-field="doc.date_completed"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Estado:</td>
                                    <td><span t-field="doc.state"/></td>
                                </tr>
                            </tbody>
                        </table>

                        <t t-if="doc.description">
                            <h4>Descripción Adicional</h4>
                            <div style="border: 1px solid #dee2e6; padding: 10px; margin-bottom: 15px; min-height: 40px;">
                                <span t-field="doc.description"/>
                            </div>
                        </t>

                        <!-- Tiempos de respuesta -->
                        <t t-if="doc.date_completed and doc.date_requested">
                            <h4>Tiempo de Respuesta</h4>
                            <table class="table table-bordered table-sm" style="margin-bottom: 15px;">
                                <tbody>
                                    <tr>
                                        <td class="fw-bold" style="width: 30%;">Días hábiles estimados:</td>
                                        <td>
                                            <t t-if="doc.requires_dimensions">7 días</t>
                                            <t t-if="not doc.requires_dimensions">5 días</t>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td class="fw-bold">Días reales:</td>
                                        <td><t t-esc="(doc.date_completed - doc.date_requested).days"/> días</td>
                                    </tr>
                                </tbody>
                            </table>
                        </t>

                        <div style="margin-top: 50px;">
                            <div class="row">
                                <div class="col-4 text-center">
                                    <p>____________________________</p>
                                    <p class="fw-bold"><span t-field="doc.requested_by.name"/></p>
                                    <p>Solicitante (Ventas)</p>
                                </div>
                                <div class="col-4 text-center">
                                    <p>____________________________</p>
                                    <p class="fw-bold"><span t-field="doc.responsible_id.name"/></p>
                                    <p>Responsable (Calidad)</p>
                                </div>
                                <div class="col-4 text-center">
                                    <p>____________________________</p>
                                    <p>Vo. Bo. Gerencia</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </t>
            </t>
        </t>
    </template>
</odoo>
```

## ./reports/report_customer_return.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="action_report_customer_return" model="ir.actions.report">
        <field name="name">Reporte de Devolución</field>
        <field name="model">quality.customer.return</field>
        <field name="report_type">qweb-pdf</field>
        <field name="report_name">quality_management.report_customer_return_document</field>
        <field name="report_file">quality_management.report_customer_return_document</field>
        <field name="binding_model_id" ref="model_quality_customer_return"/>
        <field name="binding_type">report</field>
    </record>

    <template id="report_customer_return_document">
        <t t-call="web.html_container">
            <t t-foreach="docs" t-as="doc">
                <t t-call="web.external_layout">
                    <div class="page">
                        <div class="text-center" style="margin-bottom: 20px;">
                            <h2>REPORTE DE DEVOLUCIÓN DE CLIENTE</h2>
                            <h4 t-field="doc.name"/>
                        </div>

                        <div class="text-center" style="margin-bottom: 15px;">
                            <t t-if="doc.state == 'cerrada'">
                                <span style="background-color: #28a745; color: white; padding: 5px 20px; border-radius: 4px; font-size: 14px; font-weight: bold;">CERRADA</span>
                            </t>
                            <t t-if="doc.state == 'no_procede'">
                                <span style="background-color: #dc3545; color: white; padding: 5px 20px; border-radius: 4px; font-size: 14px; font-weight: bold;">NO PROCEDE</span>
                            </t>
                            <t t-if="doc.state == 'en_8d'">
                                <span style="background-color: #ffc107; color: #333; padding: 5px 20px; border-radius: 4px; font-size: 14px; font-weight: bold;">EN PROCESO 8D</span>
                            </t>
                            <t t-if="doc.state in ('evaluacion_ventas', 'evaluacion_calidad')">
                                <span style="background-color: #17a2b8; color: white; padding: 5px 20px; border-radius: 4px; font-size: 14px; font-weight: bold;">EN EVALUACIÓN</span>
                            </t>
                        </div>

                        <table class="table table-bordered" style="margin-bottom: 20px;">
                            <tbody>
                                <tr>
                                    <td class="fw-bold" style="width: 30%;">Referencia:</td>
                                    <td><span t-field="doc.name"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Cliente:</td>
                                    <td><span t-field="doc.partner_id.name"/></td>
                                </tr>
                                <tr t-if="doc.sale_order_id">
                                    <td class="fw-bold">Orden de Venta:</td>
                                    <td><span t-field="doc.sale_order_id.name"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Fecha de Recepción:</td>
                                    <td><span t-field="doc.date_received"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Fecha de Producción:</td>
                                    <td><span t-field="doc.production_date"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Días desde Producción:</td>
                                    <td>
                                        <span t-field="doc.days_since_production"/> días
                                        <t t-if="not doc.is_within_period">
                                            <span style="color: red; font-weight: bold;"> (FUERA DE PERIODO)</span>
                                        </t>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Estado:</td>
                                    <td><span t-field="doc.state"/></td>
                                </tr>
                            </tbody>
                        </table>

                        <h4>Detalle del Defecto</h4>
                        <table class="table table-bordered table-sm" style="margin-bottom: 15px;">
                            <tbody>
                                <tr>
                                    <td class="fw-bold" style="width: 30%;">Tipo de Defecto:</td>
                                    <td><span t-field="doc.defect_type"/></td>
                                </tr>
                                <tr t-if="doc.defect_type == 'otro' and doc.defect_other_desc">
                                    <td class="fw-bold">Descripción Otro:</td>
                                    <td><span t-field="doc.defect_other_desc"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Piezas con Defecto:</td>
                                    <td><span t-field="doc.defect_pieces"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Afecta Funcionalidad:</td>
                                    <td>
                                        <span t-if="doc.affects_functionality" style="color: red; font-weight: bold;">SÍ</span>
                                        <span t-if="not doc.affects_functionality">No</span>
                                    </td>
                                </tr>
                            </tbody>
                        </table>

                        <h4>Motivo de la Devolución</h4>
                        <div style="border: 1px solid #dee2e6; padding: 10px; margin-bottom: 15px; min-height: 60px;">
                            <span t-field="doc.return_reason"/>
                        </div>

                        <t t-if="doc.pallets_returned">
                            <h4>Tarimas</h4>
                            <table class="table table-bordered table-sm" style="margin-bottom: 15px;">
                                <tbody>
                                    <tr>
                                        <td class="fw-bold" style="width: 30%;">Se Regresan Tarimas:</td>
                                        <td>Sí</td>
                                    </tr>
                                    <tr t-if="doc.pallet_return_date">
                                        <td class="fw-bold">Fecha Retorno:</td>
                                        <td><span t-field="doc.pallet_return_date"/></td>
                                    </tr>
                                    <tr t-if="doc.pallet_alert_15">
                                        <td class="fw-bold">Alerta:</td>
                                        <!-- FOLIO-QM-ODOO18-053: el reporte refleja la regla de más de 15 días hábiles para tarimas. -->
                                        <td><strong style="color:red;">Retorno mayor a 15 días hábiles desde recepción.</strong></td>
                                    </tr>
                                </tbody>
                            </table>
                        </t>

                        <t t-if="doc.sales_manager_justification">
                            <h4>Autorización Comercial</h4>
                            <table class="table table-bordered table-sm" style="margin-bottom: 15px;">
                                <tbody>
                                    <tr>
                                        <td class="fw-bold" style="width: 30%;">Gerente autorizó:</td>
                                        <td><span t-field="doc.sales_manager_id.name"/></td>
                                    </tr>
                                    <tr>
                                        <td class="fw-bold">Motivo:</td>
                                        <td><span t-field="doc.sales_manager_justification"/></td>
                                    </tr>
                                </tbody>
                            </table>
                        </t>

                        <t t-if="doc.corrective_action_id">
                            <h4>Acción Correctiva (8D)</h4>
                            <table class="table table-bordered table-sm" style="margin-bottom: 15px;">
                                <tbody>
                                    <tr>
                                        <td class="fw-bold" style="width: 30%;">Referencia 8D:</td>
                                        <td><span t-field="doc.corrective_action_id.name"/></td>
                                    </tr>
                                    <tr>
                                        <td class="fw-bold">Estado 8D:</td>
                                        <td><span t-field="doc.corrective_action_id.state"/></td>
                                    </tr>
                                </tbody>
                            </table>
                        </t>

                        <div style="margin-top: 40px;">
                            <div class="row">
                                <div class="col-4 text-center">
                                    <p>____________________________</p>
                                    <p>Ventas</p>
                                </div>
                                <div class="col-4 text-center">
                                    <p>____________________________</p>
                                    <p>Calidad</p>
                                </div>
                                <div class="col-4 text-center">
                                    <p>____________________________</p>
                                    <p>Producción</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </t>
            </t>
        </t>
    </template>
</odoo>```

## ./reports/report_drawing_release.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="action_report_drawing_release" model="ir.actions.report">
        <field name="name">Liberación de Plano</field>
        <field name="model">quality.drawing.release</field>
        <field name="report_type">qweb-pdf</field>
        <field name="report_name">quality_management.report_drawing_release_document</field>
        <field name="report_file">quality_management.report_drawing_release_document</field>
        <field name="binding_model_id" ref="model_quality_drawing_release"/>
        <field name="binding_type">report</field>
    </record>

    <template id="report_drawing_release_document">
        <t t-call="web.html_container">
            <t t-foreach="docs" t-as="doc">
                <t t-call="web.external_layout">
                    <div class="page">
                        <div class="text-center" style="margin-bottom: 20px;">
                            <h2>LIBERACIÓN DE PLANO</h2>
                            <h4 t-field="doc.name"/>
                        </div>

                        <!-- FOLIO-QM-ODOO18-052: se usa el estado real final del flujo triple-check. -->
                        <t t-if="doc.state == 'aceptado_diseno'">
                            <div class="text-center" style="margin-bottom: 15px;">
                                <span style="background-color: #28a745; color: white; padding: 5px 20px; border-radius: 4px; font-size: 16px; font-weight: bold;">
                                    PLANO LIBERADO
                                </span>
                            </div>
                        </t>

                        <t t-if="doc.state == 'rechazado'">
                            <div class="text-center" style="margin-bottom: 15px;">
                                <span style="background-color: #dc3545; color: white; padding: 5px 20px; border-radius: 4px; font-size: 16px; font-weight: bold;">
                                    PLANO RECHAZADO
                                </span>
                            </div>
                        </t>

                        <table class="table table-bordered" style="margin-bottom: 20px;">
                            <tbody>
                                <tr>
                                    <td class="fw-bold" style="width: 30%;">Referencia:</td>
                                    <td><span t-field="doc.name"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Cliente:</td>
                                    <td><span t-field="doc.partner_id.name"/></td>
                                </tr>
                                <tr t-if="doc.sale_order_id">
                                    <td class="fw-bold">Orden de Venta:</td>
                                    <td><span t-field="doc.sale_order_id.name"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Solicitante (Ventas):</td>
                                    <td><span t-field="doc.requested_by.name"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Inspector de Calidad:</td>
                                    <td><span t-field="doc.inspector_id.name"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Fecha de Solicitud:</td>
                                    <td><span t-field="doc.date_requested"/></td>
                                </tr>
                                <tr t-if="doc.date_release_expected">
                                    <td class="fw-bold">Fecha Esperada:</td>
                                    <td><span t-field="doc.date_release_expected"/></td>
                                </tr>
                                <tr t-if="doc.date_released">
                                    <td class="fw-bold">Fecha de Liberación:</td>
                                    <td><span t-field="doc.date_released"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Estado:</td>
                                    <td><span t-field="doc.state"/></td>
                                </tr>
                            </tbody>
                        </table>

                        <t t-if="doc.rejection_reason">
                            <h4>Motivo de Rechazo</h4>
                            <div style="border: 2px solid #dc3545; padding: 10px; margin-bottom: 15px; min-height: 40px; background-color: #fff5f5;">
                                <span t-field="doc.rejection_reason"/>
                            </div>
                        </t>

                        <h4>Triple Check</h4>
                        <table class="table table-bordered table-sm" style="margin-bottom: 20px;">
                            <tbody>
                                <tr>
                                    <td class="fw-bold" style="width: 30%;">Calidad:</td>
                                    <td>
                                        <span t-if="doc.accepted_by_quality">
                                            <span t-field="doc.accepted_by_quality.name"/> —
                                            <span t-field="doc.accepted_by_quality_date"/>
                                        </span>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Ventas:</td>
                                    <td>
                                        <span t-if="doc.accepted_by_sales">
                                            <span t-field="doc.accepted_by_sales.name"/> —
                                            <span t-field="doc.accepted_by_sales_date"/>
                                        </span>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Diseño:</td>
                                    <td>
                                        <span t-if="doc.accepted_by_design">
                                            <span t-field="doc.accepted_by_design.name"/> —
                                            <span t-field="doc.accepted_by_design_date"/>
                                        </span>
                                    </td>
                                </tr>
                            </tbody>
                        </table>

                        <div style="margin-top: 50px;">
                            <div class="row">
                                <div class="col-4 text-center">
                                    <p>____________________________</p>
                                    <p class="fw-bold"><span t-field="doc.requested_by.name"/></p>
                                    <p>Solicitante (Ventas)</p>
                                </div>
                                <div class="col-4 text-center">
                                    <p>____________________________</p>
                                    <p class="fw-bold"><span t-field="doc.inspector_id.name"/></p>
                                    <p>Inspector de Calidad</p>
                                </div>
                                <div class="col-4 text-center">
                                    <p>____________________________</p>
                                    <p>Vo. Bo. Gerencia</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </t>
            </t>
        </t>
    </template>
</odoo>```

## ./reports/report_inspection_summary.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="action_report_inspection_summary" model="ir.actions.report">
        <field name="name">Resumen de Inspección</field>
        <field name="model">quality.inspection</field>
        <field name="report_type">qweb-pdf</field>
        <field name="report_name">quality_management.report_inspection_summary_document</field>
        <field name="report_file">quality_management.report_inspection_summary_document</field>
        <field name="binding_model_id" ref="model_quality_inspection"/>
        <field name="binding_type">report</field>
    </record>

    <template id="report_inspection_summary_document">
        <t t-call="web.html_container">
            <t t-foreach="docs" t-as="doc">
                <t t-call="web.external_layout">
                    <div class="page">
                        <div class="text-center" style="margin-bottom: 20px;">
                            <h2>RESUMEN DE INSPECCIÓN</h2>
                            <h4 t-field="doc.name"/>
                        </div>

                        <table class="table table-bordered" style="margin-bottom: 20px;">
                            <tbody>
                                <tr>
                                    <td class="fw-bold" style="width: 25%;">Tipo de Proceso:</td>
                                    <td><span t-field="doc.process_type_id.name"/></td>
                                    <td class="fw-bold" style="width: 25%;">Estado:</td>
                                    <td><span t-field="doc.state"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Producto:</td>
                                    <td><span t-field="doc.product_id.name"/></td>
                                    <td class="fw-bold">Código:</td>
                                    <td><span t-field="doc.code"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Cliente:</td>
                                    <td><span t-field="doc.partner_id.name"/></td>
                                    <td class="fw-bold">Folio:</td>
                                    <td><span t-field="doc.folio"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Operador:</td>
                                    <td><span t-field="doc.operator_id.name"/></td>
                                    <td class="fw-bold">Supervisor:</td>
                                    <td>
                                        <t t-if="doc.sin_supervisor">Sin supervisor</t>
                                        <t t-else=""><span t-field="doc.supervisor_id.name"/></t>
                                    </td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Inspector:</td>
                                    <td><span t-field="doc.inspector_id.name"/></td>
                                    <td class="fw-bold">Turno:</td>
                                    <td><span t-field="doc.shift"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Planta:</td>
                                    <td><span t-field="doc.plant"/></td>
                                    <td class="fw-bold">Fecha:</td>
                                    <td><span t-field="doc.date_inspection" t-options='{"widget": "date"}'/></td>
                                </tr>
                                <tr t-if="doc.lot_id">
                                    <td class="fw-bold">Lote:</td>
                                    <td><span t-field="doc.lot_id.name"/></td>
                                    <td class="fw-bold">O. Producción:</td>
                                    <td><span t-field="doc.production_order_id.name"/></td>
                                </tr>
                            </tbody>
                        </table>

                        <!-- FOLIO-QM-ODOO18-075: reporte dedicado de Octágono, sin Espesor ni Retiramiento. -->
                        <t t-if="doc.process_code == 'octagono'">
                            <h4>Medidas y Producción - Octágono</h4>
                            <table class="table table-bordered table-sm">
                                <tbody>
                                    <tr>
                                        <td class="fw-bold" style="width: 25%;">Ancho (mm):</td>
                                        <td class="text-center">
                                            <t t-if="doc.ancho">
                                                <span t-field="doc.ancho"/>
                                            </t>
                                            <t t-elif="doc.oct_ancho">
                                                <span t-field="doc.oct_ancho"/>
                                            </t>
                                        </td>
                                        <td class="fw-bold" style="width: 25%;">Hexágono:</td>
                                        <td class="text-center">
                                            <t t-if="doc.hexagono">
                                                <span t-field="doc.hexagono"/>
                                            </t>
                                            <t t-elif="doc.oct_hexagono_tipo">
                                                <span t-field="doc.oct_hexagono_tipo"/>
                                            </t>
                                            <t t-elif="doc.oct_hexagono">
                                                <span t-field="doc.oct_hexagono"/>
                                            </t>
                                            <t t-elif="doc.tipo_hexagono">
                                                <span t-field="doc.tipo_hexagono"/>
                                            </t>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td class="fw-bold">Número de Corrida:</td>
                                        <td><span t-field="doc.numero_corrida"/></td>
                                        <td class="fw-bold">Calibración:</td>
                                        <td class="text-center">
                                            <t t-if="doc.calibracion">
                                                <span t-esc="'%.4f' % doc.calibracion"/>
                                            </t>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td class="fw-bold">Engomado:</td>
                                        <td class="text-center"><span t-field="doc.engomado"/></td>
                                        <td class="fw-bold">Alineación:</td>
                                        <td class="text-center"><span t-field="doc.oct_alineacion"/></td>
                                    </tr>
                                    <tr>
                                        <td class="fw-bold">Corte de Guillotina:</td>
                                        <td class="text-center"><span t-field="doc.corte_guillotina"/></td>
                                        <td class="fw-bold">Espesor / Retiramiento:</td>
                                        <td class="text-center">No aplica en Octágono</td>
                                    </tr>
                                </tbody>
                            </table>

                            <h5>Materiales - Octágono</h5>
                            <table class="table table-bordered table-sm">
                                <tbody>
                                    <tr>
                                        <td class="fw-bold" style="width: 25%;">Papel - Ancho:</td>
                                        <td class="text-center"><span t-field="doc.papel_ancho"/></td>
                                        <td class="fw-bold" style="width: 25%;">Papel - Gramaje:</td>
                                        <td class="text-center"><span t-field="doc.papel_gramaje"/></td>
                                    </tr>
                                    <tr>
                                        <td class="fw-bold">Proveedor de Rollos:</td>
                                        <td colspan="3"><span t-field="doc.papel_proveedor_id.name"/></td>
                                    </tr>
                                    <tr>
                                        <td class="fw-bold">Adhesivo Lote 1:</td>
                                        <td><span t-field="doc.adhesivo_lote1"/></td>
                                        <td class="fw-bold">Adhesivo Lote 2:</td>
                                        <td><span t-field="doc.adhesivo_lote2"/></td>
                                    </tr>
                                </tbody>
                            </table>
                        </t>

                        <t t-if="doc.capture_mode != 'additional_only' and doc.process_code not in ('acabado_empaque', 'octagono') and (doc.show_largo or doc.show_ancho or doc.show_espesor or doc.show_hexagono or doc.show_resistencia or doc.show_apariencia or doc.show_humedad or doc.show_pegado or doc.show_retiramiento or doc.show_calibracion or doc.show_engomado)">
                            <h4>Medidas - <span t-field="doc.process_type_id.name"/></h4>
                            <table class="table table-bordered table-sm">
                                <thead>
                                    <tr class="table-active">
                                        <th t-if="doc.show_largo">Largo (mm)</th>
                                        <th t-if="doc.show_ancho">Ancho (mm)</th>
                                        <th t-if="doc.show_espesor">Espesor (<t t-esc="doc.espesor_unit or 'in'"/>)</th>
                                        <th t-if="doc.show_hexagono">Hexágono</th>
                                        <th t-if="doc.show_resistencia">Resistencia (Lbf)</th>
                                        <th t-if="doc.show_apariencia">Apariencia</th>
                                        <th t-if="doc.show_humedad">% Humedad</th>
                                        <th t-if="doc.show_pegado">Pegado</th>
                                        <th t-if="doc.show_retiramiento">Retiramiento (cm)</th>
                                        <th t-if="doc.show_calibracion">Calibración</th>
                                        <th t-if="doc.show_engomado">Engomado</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td t-if="doc.show_largo" class="text-center"><span t-field="doc.largo"/></td>
                                        <td t-if="doc.show_ancho" class="text-center"><span t-esc="doc.ancho or doc.oct_ancho"/></td>
                                        <td t-if="doc.show_espesor" class="text-center"><span t-esc="doc.espesor or doc.oct_espesor"/></td>
                                        <td t-if="doc.show_hexagono" class="text-center">
                                            <span t-esc="doc.hexagono or doc.oct_hexagono or doc.tipo_hexagono or ''"/>
                                        </td>
                                        <td t-if="doc.show_resistencia" class="text-center">
                                            <t t-if="doc.resistencia_na">N/A</t>
                                            <t t-else=""><span t-field="doc.resistencia"/></t>
                                        </td>
                                        <td t-if="doc.show_apariencia" class="text-center"><span t-field="doc.apariencia"/></td>
                                        <td t-if="doc.show_humedad" class="text-center"><span t-field="doc.humedad_pct"/>%</td>
                                        <td t-if="doc.show_pegado" class="text-center"><span t-esc="doc.pegado_result or doc.oct_pegado or ''"/></td>
                                        <td t-if="doc.show_retiramiento" class="text-center">
                                            <t t-if="doc.reticula_extendida">
                                                <span t-field="doc.reticula_extendida"/>
                                            </t>
                                            <t t-else="">
                                                <span t-field="doc.oct_retiramiento"/>
                                            </t>
                                        </td>
                                        <td t-if="doc.show_calibracion" class="text-center">
                                            <t t-if="doc.calibracion">
                                                <span t-esc="'%.4f' % doc.calibracion"/>
                                            </t>
                                        </td>
                                        <td t-if="doc.show_engomado" class="text-center"><span t-field="doc.engomado"/></td>
                                    </tr>
                                </tbody>
                            </table>
                        </t>

                        <t t-if="doc.process_code != 'octagono' and (doc.show_numero_corrida or doc.show_papel or doc.show_adhesivo)">
                            <h4>Datos de Producción</h4>
                            <table class="table table-bordered table-sm">
                                <tbody>
                                    <tr t-if="doc.show_numero_corrida">
                                        <td class="fw-bold" style="width: 30%;">Número de Corrida:</td>
                                        <td><span t-field="doc.numero_corrida"/></td>
                                    </tr>
                                    <tr t-if="doc.show_tipo_hexagono">
                                        <td class="fw-bold">Tipo de Hexágono:</td>
                                        <td><span t-field="doc.tipo_hexagono"/></td>
                                    </tr>
                                    <tr t-if="doc.show_papel">
                                        <td class="fw-bold">Papel (Ancho / Gramaje):</td>
                                        <td><span t-field="doc.papel_ancho"/> / <span t-field="doc.papel_gramaje"/></td>
                                    </tr>
                                    <tr t-if="doc.show_papel and doc.papel_proveedor_id">
                                        <td class="fw-bold">Proveedor del Papel:</td>
                                        <td><span t-field="doc.papel_proveedor_id.name"/></td>
                                    </tr>
                                    <tr t-if="doc.show_adhesivo">
                                        <td class="fw-bold">Lotes Adhesivo:</td>
                                        <td><span t-field="doc.adhesivo_lote1"/> / <span t-field="doc.adhesivo_lote2"/></td>
                                    </tr>
                                    <tr t-if="doc.show_corte_guillotina">
                                        <td class="fw-bold">Corte en Guillotina:</td>
                                        <td><span t-field="doc.corte_guillotina"/></td>
                                    </tr>
                                </tbody>
                            </table>
                        </t>

                        <t t-if="doc.ranurado_ids">
                            <h5>Ranurado</h5>
                            <table class="table table-bordered table-sm">
                                <thead>
                                    <tr class="table-active">
                                        <th>N°</th>
                                        <th>Medida</th>
                                        <th>Unidad</th>
                                        <th>Resultado</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr t-foreach="doc.ranurado_ids" t-as="r">
                                        <td><span t-field="r.sequence"/></td>
                                        <td class="text-center"><span t-field="r.medida"/></td>
                                        <td class="text-center"><span t-field="r.unidad"/></td>
                                        <td class="text-center"><span t-field="r.resultado"/></td>
                                    </tr>
                                </tbody>
                            </table>
                        </t>

                        <t t-if="doc.troquelado_ids">
                            <h5>Troquelado</h5>
                            <table class="table table-bordered table-sm">
                                <thead>
                                    <tr class="table-active">
                                        <th>N°</th>
                                        <th>Medida</th>
                                        <th>Unidad</th>
                                        <th>Resultado</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr t-foreach="doc.troquelado_ids" t-as="t_line">
                                        <td><span t-field="t_line.sequence"/></td>
                                        <td class="text-center"><span t-field="t_line.medida"/></td>
                                        <td class="text-center"><span t-field="t_line.unidad"/></td>
                                        <td class="text-center"><span t-field="t_line.resultado"/></td>
                                    </tr>
                                </tbody>
                            </table>
                        </t>

                        <t t-if="doc.line_ids">
                            <h5>Atributos Adicionales</h5>
                            <table class="table table-bordered table-sm">
                                <thead>
                                    <tr class="table-active">
                                        <th>Atributo</th>
                                        <th>Valor</th>
                                        <th>Rango</th>
                                        <th>Resultado</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr t-foreach="doc.line_ids" t-as="attr">
                                        <td><span t-field="attr.name"/></td>
                                        <td class="text-center">
                                            <t t-if="doc.process_code == 'acabado_empaque'">
                                                <t t-if="attr.value_cumple == 'cumple' or (not attr.value_cumple and attr.result == 'cumple')">Cumple</t>
                                                <t t-elif="attr.value_cumple == 'no_cumple' or (not attr.value_cumple and attr.result == 'no_cumple')">No Cumple</t>
                                            </t>
                                            <t t-else="">
                                                <span t-if="attr.attribute_type == 'float'" t-field="attr.value_float"/>
                                                <span t-if="attr.attribute_type in ('char', 'selection')" t-field="attr.value_char"/>
                                                <!-- FOLIO-QM-ODOO18-045: el resumen impreso soporta Cumple/NC y OK/NO OK. -->
                                                <span t-if="attr.attribute_type == 'boolean' and attr.result_mode == 'cumple'" t-field="attr.value_cumple"/>
                                                <span t-if="attr.attribute_type == 'boolean' and attr.result_mode == 'ok'" t-field="attr.value_ok"/>
                                            </t>
                                        </td>
                                        <td class="text-center">
                                            <t t-if="doc.process_code != 'acabado_empaque' and (attr.min_value or attr.max_value)">
                                                <span t-field="attr.min_value"/> - <span t-field="attr.max_value"/> <span t-field="attr.unit"/>
                                            </t>
                                        </td>
                                        <td class="text-center">
                                            <t t-if="doc.process_code == 'acabado_empaque'">
                                                <t t-if="attr.result == 'cumple' or attr.value_cumple == 'cumple'">Cumple</t>
                                                <t t-elif="attr.result == 'no_cumple' or attr.value_cumple == 'no_cumple'">No Cumple</t>
                                            </t>
                                            <t t-else="">
                                                <span t-field="attr.result"/>
                                            </t>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </t>

                        <div style="margin-top: 30px;">
                            <div class="row">
                                <div class="col-6 text-center">
                                    <p>____________________________</p>
                                    <p class="fw-bold"><span t-field="doc.inspector_id.name"/></p>
                                    <p>Inspector de Calidad</p>
                                </div>
                                <div class="col-6 text-center">
                                    <p>____________________________</p>
                                    <p class="fw-bold" t-if="doc.supervisor_id">
                                        <span t-field="doc.supervisor_id.name"/>
                                    </p>
                                    <p>Supervisor</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </t>
            </t>
        </t>
    </template>
</odoo>```

## ./reports/report_quality_certificate.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="action_report_quality_certificate" model="ir.actions.report">
        <field name="name">Certificado de Calidad</field>
        <field name="model">quality.certificate</field>
        <field name="report_type">qweb-pdf</field>
        <field name="report_name">quality_management.report_quality_certificate_document</field>
        <field name="report_file">quality_management.report_quality_certificate_document</field>
        <field name="binding_model_id" ref="model_quality_certificate"/>
        <field name="binding_type">report</field>
    </record>

    <template id="report_quality_certificate_document">
        <t t-call="web.html_container">
            <t t-foreach="docs" t-as="doc">
                <t t-call="web.external_layout">
                    <div class="page">
                        <div class="text-center" style="margin-bottom: 20px;">
                            <h2>CERTIFICADO DE CALIDAD</h2>
                            <h4 t-field="doc.name"/>
                        </div>

                        <table class="table table-bordered" style="margin-bottom: 20px;">
                            <tbody>
                                <tr>
                                    <td class="fw-bold" style="width: 30%;">Cliente:</td>
                                    <td><span t-field="doc.partner_id.name"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Producto:</td>
                                    <td><span t-field="doc.product_id.name"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Tipo de Proceso:</td>
                                    <td><span t-field="doc.process_type_id.name"/></td>
                                </tr>
                                <tr t-if="doc.folio">
                                    <td class="fw-bold">Folio de Producción:</td>
                                    <td><span t-field="doc.folio"/></td>
                                </tr>
                                <tr t-if="doc.lot_id">
                                    <td class="fw-bold">Lote:</td>
                                    <td><span t-field="doc.lot_id.name"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Fecha de Inspección:</td>
                                    <td><span t-field="doc.inspection_id.date_inspection" t-options='{"widget": "date"}'/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Fecha de Certificación:</td>
                                    <td><span t-field="doc.date_generated"/></td>
                                </tr>
                            </tbody>
                        </table>

                        <h4 class="text-center" style="margin-bottom: 15px;">Resultados de Inspección</h4>
                        <table class="table table-bordered table-sm">
                            <thead>
                                <tr class="table-active">
                                    <th>Atributo</th>
                                    <th class="text-center">Valor</th>
                                    <th class="text-center">Unidad</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr t-if="doc.certified_largo">
                                    <td>Largo</td>
                                    <td class="text-center"><span t-field="doc.certified_largo"/></td>
                                    <td class="text-center">mm</td>
                                </tr>
                                <tr t-if="doc.certified_ancho">
                                    <td>Ancho</td>
                                    <td class="text-center"><span t-field="doc.certified_ancho"/></td>
                                    <td class="text-center">mm</td>
                                </tr>
                                <tr t-if="doc.certified_espesor">
                                    <td>Espesor</td>
                                    <td class="text-center"><span t-field="doc.certified_espesor"/></td>
                                    <td class="text-center">
                                        <span t-esc="doc.inspection_id.espesor_unit or 'in'"/>
                                    </td>
                                </tr>
                                <tr t-if="doc.certified_hexagono_label or doc.certified_hexagono">
                                    <td>Hexágono</td>
                                    <td class="text-center">
                                        <t t-if="doc.certified_hexagono_label">
                                            <span t-field="doc.certified_hexagono_label"/>
                                        </t>
                                        <t t-else="">
                                            <span t-field="doc.certified_hexagono"/>
                                        </t>
                                    </td>
                                    <td class="text-center">-</td>
                                </tr>
                                <tr t-if="doc.certified_resistencia">
                                    <td>Resistencia</td>
                                    <td class="text-center"><span t-field="doc.certified_resistencia"/></td>
                                    <td class="text-center">Lbf</td>
                                </tr>
                                <tr t-if="doc.certified_apariencia">
                                    <td>Apariencia</td>
                                    <td class="text-center"><span t-field="doc.certified_apariencia"/></td>
                                    <td class="text-center">-</td>
                                </tr>
                                <tr t-if="doc.certified_humedad">
                                    <td>Humedad</td>
                                    <td class="text-center"><span t-field="doc.certified_humedad"/>%</td>
                                    <td class="text-center">%</td>
                                </tr>
                                <tr t-if="doc.certified_pegado">
                                    <td>Pegado</td>
                                    <td class="text-center"><span t-field="doc.certified_pegado"/></td>
                                    <td class="text-center">-</td>
                                </tr>
                                <tr t-if="doc.certified_retiramiento">
                                    <td>Retiramiento</td>
                                    <td class="text-center"><span t-field="doc.certified_retiramiento"/></td>
                                    <td class="text-center">cm</td>
                                </tr>
                                <tr t-if="doc.certified_calibracion">
                                    <td>Calibración</td>
                                    <!-- FOLIO-QM-ODOO18-075: preservar capturas como 0.0010. -->
                                    <td class="text-center"><span t-esc="'%.4f' % doc.certified_calibracion"/></td>
                                    <td class="text-center">-</td>
                                </tr>
                                <tr t-if="doc.certified_engomado">
                                    <td>Engomado</td>
                                    <td class="text-center"><span t-field="doc.certified_engomado"/></td>
                                    <td class="text-center">-</td>
                                </tr>
                            </tbody>
                        </table>

                        <t t-if="doc.attribute_ids">
                            <h5 style="margin-top: 15px;">Atributos Adicionales</h5>
                            <table class="table table-bordered table-sm">
                                <thead>
                                    <tr class="table-active">
                                        <th>Atributo</th>
                                        <th class="text-center">Valor</th>
                                        <th class="text-center">Resultado</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr t-foreach="doc.attribute_ids" t-as="attr">
                                        <td><span t-field="attr.name"/></td>
                                        <td class="text-center">
                                            <span t-if="attr.attribute_type == 'float'" t-field="attr.value_float"/>
                                            <span t-if="attr.attribute_type in ('char', 'selection')" t-field="attr.value_char"/>
                                            <!-- FOLIO-QM-ODOO18-042: el PDF del certificado muestra correctamente Cumple/NC o OK/NO OK según result_mode. -->
                                            <span t-if="attr.attribute_type == 'boolean' and attr.result_mode == 'cumple'" t-field="attr.value_cumple"/>
                                            <span t-if="attr.attribute_type == 'boolean' and attr.result_mode == 'ok'" t-field="attr.value_ok"/>
                                        </td>
                                        <td class="text-center"><span t-field="attr.result"/></td>
                                    </tr>
                                </tbody>
                            </table>
                        </t>

                        <div style="margin-top: 60px;">
                            <div class="row">
                                <div class="col-6 text-center">
                                    <p>____________________________</p>
                                    <p class="fw-bold"><span t-field="doc.certified_by.name"/></p>
                                    <p>Responsable de Calidad</p>
                                </div>
                                <div class="col-6 text-center">
                                    <t t-if="doc.company_id.quality_stamp">
                                        <!-- FOLIO-QM-ODOO18-043: image_data_uri evita errores por decode/bytes en binarios de Odoo 18. -->
                                        <img t-att-src="image_data_uri(doc.company_id.quality_stamp)"
                                             style="max-height: 120px; max-width: 200px;"
                                             alt="Sello de la Empresa"/>
                                    </t>
                                    <t t-else="">
                                        <div style="height: 120px; border: 1px dashed #ccc; display: flex; align-items: center; justify-content: center;">
                                            <span class="text-muted">Sello de la Empresa</span>
                                        </div>
                                    </t>
                                    <p class="fw-bold mt-2">Sello de la Empresa</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </t>
            </t>
        </t>
    </template>
</odoo>```

## ./reports/report_sample_release.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="action_report_sample_release" model="ir.actions.report">
        <field name="name">Liberación de Muestra</field>
        <field name="model">quality.sample.release</field>
        <field name="report_type">qweb-pdf</field>
        <field name="report_name">quality_management.report_sample_release_document</field>
        <field name="report_file">quality_management.report_sample_release_document</field>
        <field name="binding_model_id" ref="model_quality_sample_release"/>
        <field name="binding_type">report</field>
    </record>

    <template id="report_sample_release_document">
        <t t-call="web.html_container">
            <t t-foreach="docs" t-as="doc">
                <t t-call="web.external_layout">
                    <div class="page">
                        <div class="text-center" style="margin-bottom: 20px;">
                            <h2>LIBERACIÓN DE MUESTRA</h2>
                            <h4 t-field="doc.name"/>
                        </div>

                        <t t-if="doc.state == 'aceptado'">
                            <div class="text-center" style="margin-bottom: 15px;">
                                <span style="background-color: #28a745; color: white; padding: 5px 20px; border-radius: 4px; font-size: 16px; font-weight: bold;">
                                    MUESTRA LIBERADA
                                </span>
                            </div>
                        </t>
                        <t t-if="doc.state == 'rechazado'">
                            <div class="text-center" style="margin-bottom: 15px;">
                                <span style="background-color: #dc3545; color: white; padding: 5px 20px; border-radius: 4px; font-size: 16px; font-weight: bold;">
                                    MUESTRA RECHAZADA
                                </span>
                            </div>
                        </t>

                        <table class="table table-bordered" style="margin-bottom: 20px;">
                            <tbody>
                                <tr>
                                    <td class="fw-bold" style="width: 30%;">Referencia:</td>
                                    <td><span t-field="doc.name"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Producto/Muestra:</td>
                                    <td><span t-field="doc.product_id.name"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Tarea de Proyecto:</td>
                                    <td><span t-field="doc.project_task_id.name"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Solicitante (Diseño):</td>
                                    <td><span t-field="doc.requested_by.name"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Inspector de Calidad:</td>
                                    <td><span t-field="doc.inspector_id.name"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Fecha de Solicitud:</td>
                                    <td><span t-field="doc.date_requested"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Fecha de Inspección:</td>
                                    <td><span t-field="doc.date_inspected"/></td>
                                </tr>
                                <tr>
                                    <td class="fw-bold">Estado:</td>
                                    <td><span t-field="doc.state"/></td>
                                </tr>
                            </tbody>
                        </table>

                        <t t-if="doc.inspection_line_ids">
                            <h4>Resultados de Inspección</h4>
                            <table class="table table-bordered table-sm">
                                <thead>
                                    <tr class="table-active">
                                        <th>#</th>
                                        <th>Atributo</th>
                                        <th class="text-center">Valor</th>
                                        <th class="text-center">Rango</th>
                                        <th class="text-center">Unidad</th>
                                        <th class="text-center">Resultado</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr t-foreach="doc.inspection_line_ids" t-as="line">
                                        <td><t t-esc="line_index + 1"/></td>
                                        <td><span t-field="line.name"/></td>
                                        <td class="text-center">
                                            <span t-if="line.attribute_type == 'float'" t-field="line.value_float"/>
                                            <span t-if="line.attribute_type in ('char', 'selection')" t-field="line.value_char"/>
                                            <!-- FOLIO-QM-ODOO18-044: se deja de usar value_boolean legacy y se muestran los modos reales. -->
                                            <span t-if="line.attribute_type == 'boolean' and line.result_mode == 'cumple'" t-field="line.value_cumple"/>
                                            <span t-if="line.attribute_type == 'boolean' and line.result_mode == 'ok'" t-field="line.value_ok"/>
                                        </td>
                                        <td class="text-center">
                                            <t t-if="line.min_value or line.max_value">
                                                <span t-field="line.min_value"/> - <span t-field="line.max_value"/>
                                            </t>
                                        </td>
                                        <td class="text-center"><span t-field="line.unit"/></td>
                                        <td class="text-center">
                                            <span t-if="line.result in ('cumple','ok')" style="color: green; font-weight: bold;">
                                                <span t-field="line.result"/>
                                            </span>
                                            <span t-if="line.result in ('no_cumple','no_ok')" style="color: red; font-weight: bold;">
                                                <span t-field="line.result"/>
                                            </span>
                                            <span t-if="line.result == 'na'">N/A</span>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </t>

                        <t t-if="doc.notes">
                            <h4>Observaciones</h4>
                            <div style="border: 1px solid #dee2e6; padding: 10px; min-height: 40px;">
                                <span t-field="doc.notes"/>
                            </div>
                        </t>

                        <div style="margin-top: 50px;">
                            <div class="row">
                                <div class="col-4 text-center">
                                    <p>____________________________</p>
                                    <p class="fw-bold"><span t-field="doc.requested_by.name"/></p>
                                    <p>Solicitante</p>
                                </div>
                                <div class="col-4 text-center">
                                    <p>____________________________</p>
                                    <p class="fw-bold"><span t-field="doc.inspector_id.name"/></p>
                                    <p>Inspector de Calidad</p>
                                </div>
                                <div class="col-4 text-center">
                                    <p>____________________________</p>
                                    <p>Vo. Bo. Gerencia</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </t>
            </t>
        </t>
    </template>
</odoo>```

## ./security/quality_groups.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <record id="module_category_quality" model="ir.module.category">
            <field name="name">Calidad</field>
            <field name="sequence">50</field>
        </record>

        <!-- NUEVO: Usuario básico de Calidad (solo productos/clientes) -->
        <record id="group_quality_user" model="res.groups">
            <field name="name">Usuario de Calidad (Productos y Clientes)</field>
            <field name="category_id" ref="module_category_quality"/>
            <field name="implied_ids" eval="[
                (4, ref('base.group_user')),
                (4, ref('product.group_product_variant')),
            ]"/>
            <field name="comment">Puede crear/editar productos y clientes para uso en Calidad. No puede crear inspecciones ni liberaciones.</field>
        </record>

        <record id="group_quality_design" model="res.groups">
            <field name="name">Diseño / Ingeniería de Calidad</field>
            <field name="category_id" ref="module_category_quality"/>
            <field name="implied_ids" eval="[
                (4, ref('base.group_user')),
                (4, ref('project.group_project_user')),
            ]"/>
            <field name="comment">Puede registrar transformaciones CNC y realizar la aprobación final de Diseño en liberaciones de planos.</field>
        </record>

        <record id="group_quality_inspector" model="res.groups">
            <field name="name">Inspector de Calidad</field>
            <field name="category_id" ref="module_category_quality"/>
            <field name="implied_ids" eval="[(4, ref('group_quality_user'))]"/>
            <field name="comment">Captura de datos e inspecciones de calidad</field>
        </record>

        <record id="group_quality_manager" model="res.groups">
            <field name="name">Responsable de Calidad</field>
            <field name="category_id" ref="module_category_quality"/>
            <field name="implied_ids" eval="[(4, ref('group_quality_inspector'))]"/>
            <field name="comment">Aprobaciones, certificados, acciones correctivas</field>
        </record>

        <record id="group_quality_admin" model="res.groups">
            <field name="name">Administrador de Calidad</field>
            <field name="category_id" ref="module_category_quality"/>
            <field name="implied_ids" eval="[(4, ref('group_quality_manager'))]"/>
            <field name="comment">Configuración de plantillas, tipos de proceso y atributos</field>
        </record>
    </data>
</odoo>```

## ./security/quality_rules.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <!-- FOLIO-QM-ODOO18-030: se normalizan referencias de grupos con namespace del módulo. -->
        <record id="rule_inspection_inspector_own" model="ir.rule">
            <field name="name">Inspector: solo sus inspecciones</field>
            <field name="model_id" ref="model_quality_inspection"/>
            <field name="domain_force">[('inspector_id', '=', user.id)]</field>
            <field name="groups" eval="[(4, ref('quality_management.group_quality_inspector'))]"/>
        </record>

        <record id="rule_inspection_manager_all" model="ir.rule">
            <field name="name">Manager: todas las inspecciones</field>
            <field name="model_id" ref="model_quality_inspection"/>
            <field name="domain_force">[(1, '=', 1)]</field>
            <field name="groups" eval="[(4, ref('quality_management.group_quality_manager'))]"/>
        </record>

        <record id="rule_sample_release_sale" model="ir.rule">
            <field name="name">Ventas: solo sus solicitudes de muestra</field>
            <field name="model_id" ref="model_quality_sample_release"/>
            <field name="domain_force">['|', ('requested_by', '=', user.id), ('state', 'in', ['aceptado', 'rechazado'])]</field>
            <field name="groups" eval="[(4, ref('sales_team.group_sale_salesman'))]"/>
        </record>

        <record id="rule_sample_release_design" model="ir.rule">
            <field name="name">Diseño: solo sus solicitudes de muestra</field>
            <field name="model_id" ref="model_quality_sample_release"/>
            <!-- FOLIO-QM-ODOO18-055: limita el nuevo grupo de Diseño a sus propias muestras. -->
            <field name="domain_force">[('requested_by', '=', user.id)]</field>
            <field name="groups" eval="[(4, ref('quality_management.group_quality_design'))]"/>
        </record>

        <record id="rule_inspection_line_design_sample" model="ir.rule">
            <field name="name">Diseño: atributos solo de sus muestras</field>
            <field name="model_id" ref="model_quality_inspection_line"/>
            <!-- FOLIO-QM-ODOO18-055: evita lectura global de líneas de inspección por el grupo Diseño. -->
            <field name="domain_force">[('sample_release_id.requested_by', '=', user.id)]</field>
            <field name="groups" eval="[(4, ref('quality_management.group_quality_design'))]"/>
        </record>

        <record id="rule_drawing_release_sale" model="ir.rule">
            <field name="name">Ventas: solo sus solicitudes de plano</field>
            <field name="model_id" ref="model_quality_drawing_release"/>
            <!-- FOLIO-QM-ODOO18-031: el estado 'aceptado' no existe en quality.drawing.release; se usan estados reales del flujo triple-check. -->
            <field name="domain_force">['|', ('requested_by', '=', user.id), ('state', 'in', ['aceptado_calidad', 'aceptado_ventas', 'aceptado_diseno', 'rechazado'])]</field>
            <field name="groups" eval="[(4, ref('sales_team.group_sale_salesman'))]"/>
        </record>

        <record id="rule_drawing_release_design" model="ir.rule">
            <field name="name">Diseño: planos pendientes o aprobados por Diseño</field>
            <field name="model_id" ref="model_quality_drawing_release"/>
            <!-- FOLIO-QM-ODOO18-055: el nuevo grupo de Diseño solo ve planos en etapa de Diseño o ya cerrados por Diseño. -->
            <field name="domain_force">['|', ('state', 'in', ['aceptado_ventas', 'aceptado_diseno']), ('accepted_by_design', '=', user.id)]</field>
            <field name="groups" eval="[(4, ref('quality_management.group_quality_design'))]"/>
        </record>

        <record id="rule_customer_return_sale" model="ir.rule">
            <field name="name">Ventas: devoluciones propias o de sus órdenes</field>
            <field name="model_id" ref="model_quality_customer_return"/>
            <!-- FOLIO-QM-ODOO18-054: la regla anterior permitía a cualquier vendedor ver todas las devoluciones. -->
            <field name="domain_force">['|', ('create_uid', '=', user.id), ('sale_order_id.user_id', '=', user.id)]</field>
            <field name="groups" eval="[(4, ref('sales_team.group_sale_salesman'))]"/>
        </record>

        <record id="rule_customer_return_manager_all" model="ir.rule">
            <field name="name">Calidad: todas las devoluciones de cliente</field>
            <field name="model_id" ref="model_quality_customer_return"/>
            <field name="domain_force">[(1, '=', 1)]</field>
            <field name="groups" eval="[(4, ref('quality_management.group_quality_manager'))]"/>
        </record>

        <record id="rule_customer_document_sale" model="ir.rule">
            <field name="name">Ventas: documentos solicitados por el usuario</field>
            <field name="model_id" ref="model_quality_customer_document"/>
            <!-- FOLIO-QM-ODOO18-055: se evita que Ventas vea documentos de otros solicitantes. -->
            <field name="domain_force">[('requested_by', '=', user.id)]</field>
            <field name="groups" eval="[(4, ref('sales_team.group_sale_salesman'))]"/>
        </record>

        <record id="rule_customer_document_manager_all" model="ir.rule">
            <field name="name">Calidad: todos los documentos de cliente</field>
            <field name="model_id" ref="model_quality_customer_document"/>
            <field name="domain_force">[(1, '=', 1)]</field>
            <field name="groups" eval="[(4, ref('quality_management.group_quality_manager'))]"/>
        </record>

        <record id="rule_sample_release_manager" model="ir.rule">
            <field name="name">Manager: todas las liberaciones de muestra</field>
            <field name="model_id" ref="model_quality_sample_release"/>
            <field name="domain_force">[(1, '=', 1)]</field>
            <field name="groups" eval="[(4, ref('quality_management.group_quality_manager'))]"/>
        </record>

        <record id="rule_drawing_release_manager" model="ir.rule">
            <field name="name">Manager: todas las liberaciones de plano</field>
            <field name="model_id" ref="model_quality_drawing_release"/>
            <field name="domain_force">[(1, '=', 1)]</field>
            <field name="groups" eval="[(4, ref('quality_management.group_quality_manager'))]"/>
        </record>

        <record id="rule_corrective_action_manager" model="ir.rule">
            <field name="name">Manager: todas las acciones correctivas</field>
            <field name="model_id" ref="model_quality_corrective_action"/>
            <field name="domain_force">[(1, '=', 1)]</field>
            <field name="groups" eval="[(4, ref('quality_management.group_quality_manager'))]"/>
        </record>
    </data>
</odoo>```

## ./security/quality_strict_acl.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="0">
        <!-- Inspector NO debe crear órdenes de producción ni lotes -->
        <record id="rule_inspector_no_create_mrp" model="ir.rule">
            <field name="name">Inspector: solo lectura de órdenes de producción</field>
            <field name="model_id" ref="mrp.model_mrp_production"/>
            <field name="domain_force">[(1,'=',1)]</field>
            <field name="groups" eval="[(4, ref('quality_management.group_quality_inspector'))]"/>
            <field name="perm_read" eval="True"/>
            <field name="perm_write" eval="False"/>
            <field name="perm_create" eval="False"/>
            <field name="perm_unlink" eval="False"/>
        </record>
        <record id="rule_inspector_no_create_lot" model="ir.rule">
            <field name="name">Inspector: solo lectura de lotes</field>
            <field name="model_id" ref="stock.model_stock_lot"/>
            <field name="domain_force">[(1,'=',1)]</field>
            <field name="groups" eval="[(4, ref('quality_management.group_quality_inspector'))]"/>
            <field name="perm_read" eval="True"/>
            <field name="perm_write" eval="False"/>
            <field name="perm_create" eval="False"/>
            <field name="perm_unlink" eval="False"/>
        </record>
    </data>
</odoo>
```

## ./static/src/js/evidence_viewer_widget.js
```js
/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, onWillUpdateProps } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

const IMAGE_EXTS = ["jpg", "jpeg", "png", "gif", "webp", "bmp", "svg"];
const VIDEO_EXTS = ["mp4", "webm", "ogg", "mov", "avi", "mkv"];
const PDF_EXTS = ["pdf"];

function getFileExtension(filename) {
    if (!filename) return "";
    return (filename.split(".").pop() || "").toLowerCase();
}

function getFileType(filename) {
    const ext = getFileExtension(filename);
    if (IMAGE_EXTS.includes(ext)) return "image";
    if (VIDEO_EXTS.includes(ext)) return "video";
    if (PDF_EXTS.includes(ext)) return "pdf";
    return "other";
}

export class EvidenceViewerWidget extends Component {
    static template = "quality_management.EvidenceViewerWidget";
    static props = { ...standardFieldProps };

    setup() {
        this.orm = useService("orm");
        this.state = useState({
            attachments: [],
            loading: true,
            lightbox: null,  // { type, url, name }
        });
        this._loadAttachments();
        onWillUpdateProps(() => this._loadAttachments());
    }

    get recordIds() {
        const val = this.props.record.data[this.props.name];
        if (!val) return [];
        if (val.records) return val.records.map((r) => r.resId);
        if (val.currentIds) return val.currentIds;
        return [];
    }

    async _loadAttachments() {
        this.state.loading = true;
        const ids = this.recordIds;
        if (!ids.length) {
            this.state.attachments = [];
            this.state.loading = false;
            return;
        }
        try {
            const attachments = await this.orm.read("ir.attachment", ids, [
                "name", "mimetype", "datas", "type", "url",
            ]);
            this.state.attachments = attachments.map((att) => {
                const fileType = getFileType(att.name);
                let src = "";
                if (att.type === "url" && att.url) {
                    src = att.url;
                } else if (att.datas) {
                    const mime = att.mimetype || "application/octet-stream";
                    src = `data:${mime};base64,${att.datas}`;
                } else {
                    src = `/web/content/${att.id}?download=false`;
                }
                return {
                    id: att.id,
                    name: att.name,
                    mimetype: att.mimetype,
                    fileType,
                    src,
                    downloadUrl: `/web/content/${att.id}?download=true`,
                };
            });
        } catch (e) {
            console.error("EvidenceViewer: error loading attachments", e);
            this.state.attachments = [];
        }
        this.state.loading = false;
    }

    openLightbox(att) {
        if (att.fileType === "image" || att.fileType === "video" || att.fileType === "pdf") {
            this.state.lightbox = att;
        }
    }

    closeLightbox() {
        this.state.lightbox = null;
    }

    onLightboxBackdrop(ev) {
        if (ev.target === ev.currentTarget) {
            this.closeLightbox();
        }
    }
}

EvidenceViewerWidget.template = "quality_management.EvidenceViewerWidget";

registry.category("fields").add("evidence_viewer", {
    component: EvidenceViewerWidget,
    supportedTypes: ["many2many"],
});```

## ./static/src/xml/evidence_viewer_widget.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<templates xml:space="preserve">

    <t t-name="quality_management.EvidenceViewerWidget">
        <div class="o_evidence_viewer">
            <!-- Loading -->
            <div t-if="state.loading" class="text-muted p-2">
                <i class="fa fa-spinner fa-spin"/> Cargando evidencias...
            </div>

            <!-- Empty -->
            <div t-if="!state.loading and !state.attachments.length" class="text-muted p-2">
                <i class="fa fa-image"/> Sin evidencias adjuntas
            </div>

            <!-- Grid -->
            <div t-if="!state.loading and state.attachments.length" class="o_evidence_grid">
                <t t-foreach="state.attachments" t-as="att" t-key="att.id">
                    <!-- IMAGE -->
                    <div t-if="att.fileType === 'image'" class="o_evidence_item o_evidence_image"
                         t-on-click="() => this.openLightbox(att)">
                        <img t-att-src="att.src" t-att-alt="att.name" loading="lazy"/>
                        <div class="o_evidence_overlay">
                            <span class="o_evidence_name" t-esc="att.name"/>
                            <i class="fa fa-search-plus"/>
                        </div>
                    </div>

                    <!-- VIDEO -->
                    <div t-if="att.fileType === 'video'" class="o_evidence_item o_evidence_video">
                        <video controls="controls" preload="metadata" t-att-src="att.src">
                            Tu navegador no soporta video.
                        </video>
                        <div class="o_evidence_caption">
                            <i class="fa fa-video-camera"/>
                            <span t-esc="att.name"/>
                        </div>
                    </div>

                    <!-- PDF -->
                    <div t-if="att.fileType === 'pdf'" class="o_evidence_item o_evidence_pdf"
                         t-on-click="() => this.openLightbox(att)">
                        <iframe t-att-src="'/web/content/' + att.id + '?download=false#toolbar=0'"
                                class="o_evidence_pdf_thumb"/>
                        <div class="o_evidence_overlay">
                            <span class="o_evidence_name" t-esc="att.name"/>
                            <i class="fa fa-file-pdf-o"/>
                        </div>
                    </div>

                    <!-- OTHER -->
                    <div t-if="att.fileType === 'other'" class="o_evidence_item o_evidence_other">
                        <a t-att-href="att.downloadUrl" target="_blank" class="o_evidence_download_link">
                            <i class="fa fa-file-o fa-3x"/>
                            <div class="o_evidence_name" t-esc="att.name"/>
                        </a>
                    </div>
                </t>
            </div>

            <!-- Lightbox -->
            <div t-if="state.lightbox" class="o_evidence_lightbox" t-on-click="onLightboxBackdrop">
                <div class="o_evidence_lightbox_content">
                    <button class="o_evidence_lightbox_close" t-on-click="closeLightbox">
                        <i class="fa fa-times"/>
                    </button>
                    <div class="o_evidence_lightbox_title" t-esc="state.lightbox.name"/>

                    <img t-if="state.lightbox.fileType === 'image'"
                         t-att-src="state.lightbox.src"
                         t-att-alt="state.lightbox.name"
                         class="o_evidence_lightbox_img"/>

                    <video t-if="state.lightbox.fileType === 'video'"
                           controls="controls" autoplay="autoplay"
                           t-att-src="state.lightbox.src"
                           class="o_evidence_lightbox_video"/>

                    <iframe t-if="state.lightbox.fileType === 'pdf'"
                            t-att-src="'/web/content/' + state.lightbox.id + '?download=false'"
                            class="o_evidence_lightbox_pdf"/>

                    <a t-att-href="state.lightbox.downloadUrl" target="_blank"
                       class="btn btn-sm btn-outline-light mt-2">
                        <i class="fa fa-download"/> Descargar
                    </a>
                </div>
            </div>
        </div>
    </t>

</templates>```

## ./views/product_views.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_product_template_form_quality" model="ir.ui.view">
        <field name="name">product.template.form.quality</field>
        <field name="model">product.template</field>
        <field name="inherit_id" ref="product.product_template_form_view"/>
        <field name="arch" type="xml">
            <xpath expr="//div[@name='button_box']" position="inside">
                <button name="action_view_quality_attributes"
                        type="object"
                        class="oe_stat_button"
                        icon="fa-sliders"
                        groups="quality_management.group_quality_manager">
                    <field name="quality_attribute_count" widget="statinfo"
                           string="Atributos Calidad"/>
                </button>
            </xpath>
            <xpath expr="//notebook" position="inside">
                <page string="Calidad" name="quality"
                      groups="quality_management.group_quality_manager">
                    <field name="quality_attribute_template_ids"
                           context="{'default_product_tmpl_id': id}">
                        <list editable="bottom">
                            <field name="sequence" widget="handle"/>
                            <field name="name"/>
                            <field name="attribute_type"/>
                            <field name="selection_options" invisible="attribute_type != 'selection'"/>
                            <field name="min_value" invisible="attribute_type != 'float'"/>
                            <field name="max_value" invisible="attribute_type != 'float'"/>
                            <field name="unit"/>
                            <field name="is_required"/>
                        </list>
                    </field>
                    <div class="text-muted mt-2">
                        <i class="fa fa-info-circle"/>
                        Estos atributos se cargarán automáticamente al crear una inspección
                        para este producto, adicionales a los del tipo de proceso.
                    </div>
                </page>
            </xpath>
        </field>
    </record>
</odoo>```

## ./views/project_task_quality_views.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_task_form_quality" model="ir.ui.view">
        <field name="name">project.task.form.quality</field>
        <field name="model">project.task</field>
        <field name="inherit_id" ref="project.view_task_form2"/>
        <field name="arch" type="xml">
            <xpath expr="//notebook" position="inside">
                <page string="Calidad" name="quality">
                    <group>
                        <group>
                            <field name="quality_required_for_progress"/>
                            <field name="quality_sample_release_id"
                                   options="{'no_create': True}"/>
                            <field name="quality_drawing_release_id"
                                   options="{'no_create': True}"/>
                        </group>
                        <group>
                            <field name="quality_block_reason" readonly="1"
                                   invisible="not quality_block_reason"/>
                        </group>
                    </group>
                    <div class="alert alert-warning" role="alert"
                         invisible="not quality_block_reason">
                        <i class="fa fa-exclamation-triangle"/>
                        <strong>Bloqueo:</strong>
                        <field name="quality_block_reason" nolabel="1" readonly="1"/>
                    </div>
                </page>
            </xpath>
        </field>
    </record>
</odoo>
```

## ./views/quality_attribute_template_views.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_quality_attribute_template_list" model="ir.ui.view">
        <field name="name">quality.attribute.template.list</field>
        <field name="model">quality.attribute.template</field>
        <field name="arch" type="xml">
            <list editable="bottom">
                <field name="sequence" widget="handle"/>
                <field name="name"/>
                <field name="product_tmpl_id" optional="show"/>
                <field name="process_type_id" optional="show"/>
                <field name="attribute_type"/>
                <field name="selection_options" invisible="attribute_type != 'selection'"/>
                <field name="min_value" invisible="attribute_type != 'float'"/>
                <field name="max_value" invisible="attribute_type != 'float'"/>
                <field name="unit"/>
                <field name="is_required"/>
            </list>
        </field>
    </record>

    <record id="view_quality_attribute_template_form" model="ir.ui.view">
        <field name="name">quality.attribute.template.form</field>
        <field name="model">quality.attribute.template</field>
        <field name="arch" type="xml">
            <form string="Plantilla de Atributo">
                <sheet>
                    <group>
                        <group string="Identificación">
                            <field name="name"/>
                            <field name="product_tmpl_id"
                                   options="{'no_create': True, 'no_create_edit': True, 'no_quick_create': True}"/>
                            <field name="process_type_id"/>
                            <field name="is_required"/>
                            <field name="active"/>
                        </group>
                        <group string="Configuración del Valor">
                            <field name="attribute_type"/>
                            <field name="unit"/>
                            <field name="min_value" invisible="attribute_type != 'float'"/>
                            <field name="max_value" invisible="attribute_type != 'float'"/>
                            <field name="selection_options" invisible="attribute_type != 'selection'"/>
                        </group>
                    </group>
                    <div class="alert alert-info" role="alert" invisible="product_tmpl_id or process_type_id">
                        <i class="fa fa-info-circle"/>
                        Esta plantilla aplicará de forma general. Asígnala a un
                        <strong>Producto</strong> o a un <strong>Tipo de Proceso</strong>
                        para que se cargue automáticamente en las inspecciones correspondientes.
                    </div>
                </sheet>
            </form>
        </field>
    </record>

    <record id="view_quality_attribute_template_search" model="ir.ui.view">
        <field name="name">quality.attribute.template.search</field>
        <field name="model">quality.attribute.template</field>
        <field name="arch" type="xml">
            <search>
                <field name="name"/>
                <field name="product_tmpl_id"/>
                <field name="process_type_id"/>
                <filter string="Por Producto" name="has_product"
                        domain="[('product_tmpl_id', '!=', False)]"/>
                <filter string="Por Proceso" name="has_process"
                        domain="[('process_type_id', '!=', False)]"/>
                <filter string="Generales" name="general"
                        domain="[('product_tmpl_id', '=', False), ('process_type_id', '=', False)]"/>
                <separator/>
                <filter string="Activas" name="active" domain="[('active', '=', True)]"/>
                <filter string="Archivadas" name="inactive" domain="[('active', '=', False)]"/>
                <group expand="0" string="Agrupar por">
                    <filter string="Producto" name="group_product" context="{'group_by': 'product_tmpl_id'}"/>
                    <filter string="Tipo de Proceso" name="group_process" context="{'group_by': 'process_type_id'}"/>
                    <filter string="Tipo de Dato" name="group_type" context="{'group_by': 'attribute_type'}"/>
                </group>
            </search>
        </field>
    </record>

    <record id="action_quality_attribute_template" model="ir.actions.act_window">
        <field name="name">Plantillas de Atributos</field>
        <field name="res_model">quality.attribute.template</field>
        <field name="view_mode">list,form</field>
        <field name="search_view_id" ref="view_quality_attribute_template_search"/>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Crear una plantilla de atributo de calidad
            </p>
            <p>Configure atributos por producto o por tipo de proceso.</p>
        </field>
    </record>
</odoo>```

## ./views/quality_certificate_email_views.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_quality_certificate_form_email" model="ir.ui.view">
        <field name="name">quality.certificate.form.email</field>
        <field name="model">quality.certificate</field>
        <field name="inherit_id" ref="quality_management.view_quality_certificate_form"/>
        <field name="arch" type="xml">
            <xpath expr="//notebook" position="inside">
                <page string="Bitácora de Envíos" name="emails">
                    <group>
                        <field name="date_sent" readonly="1"/>
                        <field name="sent_by" readonly="1"/>
                    </group>
                    <field name="email_log_ids" readonly="1">
                        <list>
                            <field name="date"/>
                            <field name="user_id"/>
                            <field name="recipient_email"/>
                            <field name="notes"/>
                        </list>
                    </field>
                </page>
            </xpath>
        </field>
    </record>
</odoo>
```

## ./views/quality_certificate_views.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
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
                        <page string="Atributos Adicionales (solo CUMPLE/OK)" name="attrs">
                            <p class="text-muted">
                                <i class="fa fa-info-circle"/>
                                <!-- FOLIO-QM-ODOO18-037: el certificado acepta resultados Cumple y OK, no solo Cumple. -->
                                Solo deben aparecer atributos con resultado CUMPLE u OK.
                            </p>
                            <field name="attribute_ids"
                                   domain="[('result','in',['cumple','ok'])]">
                                <list>
                                    <field name="name"/>
                                    <field name="attribute_type"/>
                                    <field name="result_mode"/>
                                    <field name="value_float"
                                           invisible="attribute_type != 'float'"/>
                                    <field name="value_char"
                                           invisible="attribute_type not in ('char','selection')"/>
                                    <field name="value_cumple"
                                           invisible="attribute_type != 'boolean' or result_mode != 'cumple'"/>
                                    <field name="value_ok"
                                           invisible="attribute_type != 'boolean' or result_mode != 'ok'"/>
                                    <field name="result" widget="badge"
                                           decoration-success="result in ('cumple','ok')"
                                           decoration-danger="result in ('no_cumple','no_ok')"/>
                                </list>
                            </field>
                        </page>
                        <page string="PDF Generado" invisible="not report_pdf" name="pdf">
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
</odoo>```

## ./views/quality_change_history_views.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_quality_inspection_history_list" model="ir.ui.view">
        <field name="name">quality.inspection.history.list</field>
        <field name="model">quality.inspection.history</field>
        <field name="arch" type="xml">
            <list>
                <field name="change_date"/>
                <field name="changed_by"/>
                <field name="field_label"/>
                <field name="old_value"/>
                <field name="new_value"/>
                <field name="inspection_state_at_change"/>
            </list>
        </field>
    </record>

    <record id="view_quality_inspection_form_history" model="ir.ui.view">
        <field name="name">quality.inspection.form.history</field>
        <field name="model">quality.inspection</field>
        <field name="inherit_id" ref="quality_management.view_quality_inspection_form"/>
        <field name="arch" type="xml">
            <!--
                FOLIO-QM-ODOO18-073:
                Ya no se agrega pestaña "Historial de Cambios".
                Los movimientos detallados se publican en el chatter inicial.
                Se deja history_count como campo técnico invisible.
            -->
            <xpath expr="//field[@name='process_code']" position="after">
                <field name="history_count" invisible="1"/>
            </xpath>
        </field>
    </record>
</odoo>```

## ./views/quality_corrective_action_views.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
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
                        <!-- FOLIO-QM-ODOO18-039: el motivo No Procede debe capturarse antes de presionar el botón. -->
                        <page string="No Procede" invisible="state == 'cerrada'" name="no_proc">
                            <div class="alert alert-warning" role="alert"
                                 invisible="no_procede_reason">
                                <i class="fa fa-exclamation-triangle"/>
                                Si la acción no procede, capture aquí el motivo antes de presionar <b>No Procede</b>.
                            </div>
                            <field name="no_procede_reason"
                                   placeholder="Motivo por el que no procede la acción correctiva..."/>
                        </page>

                        <page string="D3 - Contención" name="containment">
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
                                Para ver vista previa de evidencia, abra cada acción en formulario.
                            </div>
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
</odoo>```

## ./views/quality_customer_document_views.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
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
```

## ./views/quality_customer_return_views.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
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

                    <field name="is_within_period" invisible="1"/>
                    <field name="pallet_alert_15" invisible="1"/>

                    <div class="alert alert-warning" role="alert"
                         invisible="is_within_period">
                        <strong>Fuera de periodo:</strong>
                        <field name="days_since_production" nolabel="1" readonly="1"/> días
                        desde producción (&gt;30). Esta devolución no procede,
                        salvo justificación comercial del Gerente de Ventas.
                    </div>

                    <div class="alert alert-danger" role="alert"
                         invisible="not pallet_alert_15">
                        <i class="fa fa-clock-o"/>
                        <!-- FOLIO-QM-ODOO18-047: se aclara que la alerta de tarimas opera sobre días hábiles. -->
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
                                Aplica cuando comercialmente se decide proceder a pesar del bloqueo por &gt;30 días.
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
</odoo>```

## ./views/quality_dashboard_views.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_quality_inspection_graph" model="ir.ui.view">
        <field name="name">quality.inspection.graph</field>
        <field name="model">quality.inspection</field>
        <field name="arch" type="xml">
            <graph string="Inspecciones por Estado" type="bar">
                <field name="process_type_id"/>
                <field name="state" type="col"/>
            </graph>
        </field>
    </record>

    <record id="view_quality_corrective_action_graph" model="ir.ui.view">
        <field name="name">quality.corrective.action.graph</field>
        <field name="model">quality.corrective.action</field>
        <field name="arch" type="xml">
            <graph string="Acciones Correctivas" type="pie">
                <field name="state"/>
            </graph>
        </field>
    </record>
</odoo>
```

## ./views/quality_drawing_release_views.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
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
                        Modificación en curso:
                        <b><field name="modification_count" nolabel="1" readonly="1"/> de 3</b>.
                        Si se excede el máximo, la liberación se cierra y debe iniciarse un nuevo ciclo.
                    </div>
                    <div class="alert alert-danger" role="alert"
                         invisible="state != 'cerrada'">
                        <i class="fa fa-ban"/>
                        <b>Liberación cerrada</b>: se excedió el máximo de 3 modificaciones.
                        Inicie un nuevo proceso de Alta/Actualización.
                    </div>
                    <group>
                        <group string="Cliente y Solicitud">
                            <field name="partner_id"/>
                            <field name="sale_order_id"/>
                            <field name="requested_by"/>
                            <field name="request_type" widget="radio"/>
                            <field name="drawing_path"
                                   placeholder="Ej. C:\Users\Calidad\Nextcloud\..."/>
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
                        <!-- FOLIO-QM-ODOO18-038: el motivo de rechazo debe capturarse antes de presionar Rechazar. -->
                        <page string="Rechazo"
                              invisible="state not in ('en_revision','rechazado')"
                              name="reject">
                            <div class="alert alert-warning" role="alert"
                                 invisible="rejection_reason">
                                <i class="fa fa-exclamation-triangle"/>
                                Capture el motivo antes de presionar <b>Rechazar</b>.
                            </div>
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
</odoo>```

## ./views/quality_hardening_views.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>

    <record id="view_quality_process_type_form_hardening" model="ir.ui.view">
        <field name="name">quality.process.type.form.hardening</field>
        <field name="model">quality.process.type</field>
        <field name="inherit_id" ref="quality_management.view_quality_process_type_form"/>
        <field name="arch" type="xml">
            <!-- FOLIO-QM-ODOO18-032: se agregan controles de endurecimiento del proceso en configuración. -->
            <xpath expr="//field[@name='active']" position="after">
                <field name="capture_mode"/>
                <field name="require_measures"/>
                <field name="require_additional_attributes"/>
                <field name="zero_value_blocking"/>
            </xpath>
        </field>
    </record>

    <record id="view_quality_attribute_template_form_hardening" model="ir.ui.view">
        <field name="name">quality.attribute.template.form.hardening</field>
        <field name="model">quality.attribute.template</field>
        <field name="inherit_id" ref="quality_management.view_quality_attribute_template_form"/>
        <field name="arch" type="xml">
            <!-- FOLIO-QM-ODOO18-033: se agregan zona de captura, modo de resultado y permiso de cero por plantilla. -->
            <xpath expr="//field[@name='attribute_type']" position="after">
                <field name="capture_zone"/>
                <field name="result_mode" invisible="attribute_type != 'boolean'"/>
                <field name="allow_zero" invisible="attribute_type != 'float'"/>
                <field name="normalized_name" readonly="1"/>
            </xpath>
        </field>
    </record>

    <record id="view_quality_inspection_form_hardening" model="ir.ui.view">
        <field name="name">quality.inspection.form.hardening</field>
        <field name="model">quality.inspection</field>
        <field name="inherit_id" ref="quality_management.view_quality_inspection_form"/>
        <field name="arch" type="xml">
            <!-- FOLIO-QM-ODOO18-034: se permite declarar inspección sin supervisor sin romper required ORM. -->
            <xpath expr="//field[@name='supervisor_id']" position="before">
                <field name="sin_supervisor"/>
            </xpath>

            <xpath expr="//field[@name='supervisor_id']" position="attributes">
                <attribute name="invisible">sin_supervisor</attribute>
                <attribute name="required">not sin_supervisor</attribute>
            </xpath>

            <!-- FOLIO-QM-ODOO18-035: se agregan fechas operativas de inicio/cierre sin duplicar process_code/capture_mode. -->
            <xpath expr="//field[@name='date_inspection']" position="after">
                <field name="date_started" readonly="1"/>
                <field name="date_closed" readonly="1"/>
            </xpath>
        </field>
    </record>

    <record id="view_quality_certificate_form_hardening" model="ir.ui.view">
        <field name="name">quality.certificate.form.hardening</field>
        <field name="model">quality.certificate</field>
        <field name="inherit_id" ref="quality_management.view_quality_certificate_form"/>
        <field name="arch" type="xml">
            <!-- FOLIO-QM-ODOO18-036: se muestra la etiqueta textual del hexágono cuando proviene de selección. -->
            <xpath expr="//field[@name='certified_hexagono']" position="after">
                <field name="certified_hexagono_label" invisible="not certified_hexagono_label"/>
            </xpath>
        </field>
    </record>

</odoo>```

## ./views/quality_inherited_views.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>

    <!-- ═══════════════════════════════════════════ -->
    <!--  res.partner – Smart Buttons de Calidad     -->
    <!-- ═══════════════════════════════════════════ -->
    <record id="view_partner_form_quality_buttons" model="ir.ui.view">
        <field name="name">res.partner.form.quality.buttons</field>
        <field name="model">res.partner</field>
        <field name="inherit_id" ref="base.view_partner_form"/>
        <field name="arch" type="xml">
            <xpath expr="//div[@name='button_box']" position="inside">
                <button name="action_view_quality_certificates" type="object"
                        class="oe_stat_button" icon="fa-certificate">
                    <field name="quality_certificate_count" widget="statinfo"
                           string="Certificados"/>
                </button>
                <button name="action_view_quality_returns" type="object"
                        class="oe_stat_button" icon="fa-undo">
                    <field name="quality_return_count" widget="statinfo"
                           string="Devoluciones"/>
                </button>
                <button name="action_view_quality_documents" type="object"
                        class="oe_stat_button" icon="fa-file-text-o">
                    <field name="quality_document_count" widget="statinfo"
                           string="Docs. Calidad"/>
                </button>
                <button name="action_view_quality_inspections" type="object"
                        class="oe_stat_button" icon="fa-check-square-o">
                    <field name="quality_inspection_count" widget="statinfo"
                           string="Inspecciones"/>
                </button>
            </xpath>
        </field>
    </record>

    <!-- ═══════════════════════════════════════════ -->
    <!--  sale.order – Smart Buttons de Calidad      -->
    <!-- ═══════════════════════════════════════════ -->
    <record id="view_sale_order_form_quality_buttons" model="ir.ui.view">
        <field name="name">sale.order.form.quality.buttons</field>
        <field name="model">sale.order</field>
        <field name="inherit_id" ref="sale.view_order_form"/>
        <field name="arch" type="xml">
            <xpath expr="//div[@name='button_box']" position="inside">
                <button name="action_view_quality_drawings" type="object"
                        class="oe_stat_button" icon="fa-pencil-square-o">
                    <field name="quality_drawing_count" widget="statinfo"
                           string="Planos"/>
                </button>
                <button name="action_view_quality_returns" type="object"
                        class="oe_stat_button" icon="fa-undo">
                    <field name="quality_return_count" widget="statinfo"
                           string="Devoluciones"/>
                </button>
            </xpath>
        </field>
    </record>

    <!-- ═══════════════════════════════════════════ -->
    <!--  mrp.production – Smart Buttons de Calidad  -->
    <!-- ═══════════════════════════════════════════ -->
    <record id="view_mrp_production_form_quality_buttons" model="ir.ui.view">
        <field name="name">mrp.production.form.quality.buttons</field>
        <field name="model">mrp.production</field>
        <field name="inherit_id" ref="mrp.mrp_production_form_view"/>
        <field name="arch" type="xml">
            <xpath expr="//div[@name='button_box']" position="inside">
                <button name="action_view_quality_inspections" type="object"
                        class="oe_stat_button" icon="fa-check-square-o">
                    <field name="quality_inspection_count" widget="statinfo"
                           string="Inspecciones"/>
                </button>
            </xpath>
        </field>
    </record>

</odoo>```

## ./views/quality_inspection_views.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
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
                            invisible="state != 'borrador' or not process_gate_open"/>
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

                    <!-- FOLIO-QM-ODOO18-075: leyenda visible para Octágono; evita depender de íconos de ayuda. -->
                    <div class="alert alert-info" role="alert"
                         invisible="process_code != 'octagono'">
                        <i class="fa fa-info-circle"/>
                        <b>Octágono:</b>
                        seleccione primero la Orden de Producción. El sistema toma de ahí
                        Producto, Lote, Código y Cliente cuando existan. El Folio de Producción
                        debe coincidir con el folio físico/documental del lote. En este proceso
                        <b>no aplica Espesor ni Retiramiento</b>; Retiramiento se captura en Guillotina
                        en centímetros. Hexágono se captura como Tipo 1, 2, 3 o 4 según el catálogo
                        interno vigente de Calidad.
                    </div>

                    <div class="alert alert-warning" role="alert"
                         invisible="process_gate_open or state != 'borrador'">
                        <i class="fa fa-lock"/>
                        <strong>Flujo de proceso bloqueado:</strong>
                        <field name="process_gate_message" nolabel="1" readonly="1"/>
                    </div>

                    <!-- FOLIO-QM-ODOO18-040: campos técnicos necesarios para expresiones de Odoo 18. -->
                    <field name="process_code" invisible="1"/>
                    <field name="history_count" invisible="1"/>
                    <field name="capture_mode" invisible="1"/>
                    <field name="process_gate_open" invisible="1"/>
                    <field name="process_gate_message" invisible="1"/>
                    <field name="previous_process_type_id" invisible="1"/>
                    <field name="previous_process_inspection_id" invisible="1"/>
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
                    <field name="show_alineacion" invisible="1"/>
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
                            <field name="process_type_id" readonly="state != 'borrador'"/>
                            <field name="pp_pt" widget="radio"
                                   readonly="state != 'borrador'"/>
                            <field name="production_order_id"
                                   readonly="state != 'borrador'"
                                   options="{'no_create': True, 'no_create_edit': True, 'no_quick_create': True}"/>
                            <field name="product_id"
                                   readonly="state != 'borrador' or production_order_id"
                                   options="{'no_create': True, 'no_create_edit': True, 'no_quick_create': True}"/>
                            <field name="lot_id"
                                   readonly="state != 'borrador' or (production_order_id and lot_id)"
                                   options="{'no_create': True, 'no_create_edit': True, 'no_quick_create': True}"
                                   domain="[('product_id', '=', product_id)]"/>
                            <field name="folio"
                                   placeholder="Ej. folio físico de producción / lote impreso"/>
                            <field name="code"
                                   placeholder="Código interno del producto; se llena desde Producto/OP si existe"/>
                            <field name="previous_process_type_id"
                                   readonly="1"
                                   invisible="process_gate_open"/>
                            <field name="previous_process_inspection_id"
                                   readonly="1"
                                   invisible="not previous_process_inspection_id"/>
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
                                   placeholder="Cliente; si no existe, créelo desde Contactos o desde este selector según permisos."/>
                            <field name="shift"/>
                            <field name="plant"/>
                            <field name="date_inspection" readonly="1"/>
                        </group>
                    </group>

                    <notebook>
                        <page string="Medidas y Propiedades"
                              invisible="state == 'borrador' or process_code == 'octagono' or capture_mode == 'additional_only' or (not show_largo and not show_ancho and not show_espesor and not show_hexagono and not show_resistencia and not show_apariencia and not show_humedad and not show_pegado and not show_retiramiento and not show_calibracion and not show_engomado)"
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

                        <page string="Octágono"
                              invisible="state == 'borrador' or process_code != 'octagono'"
                              name="oct">
                            <!-- FOLIO-QM-ODOO18-075: matriz dedicada de Octágono. -->
                            <div class="alert alert-warning" role="alert">
                                <i class="fa fa-ban"/>
                                En Octágono no se captura <b>Espesor</b> ni <b>Retiramiento</b>.
                                Retiramiento corresponde a Guillotina y se expresa en cm.
                            </div>

                            <group>
                                <group string="Medidas">
                                    <field name="ancho" string="Ancho (mm)"/>
                                    <field name="hexagono" string="Hexágono" widget="radio"/>
                                    <field name="calibracion"
                                           string="Calibración"
                                           placeholder="Ej. 0.0010"/>
                                    <field name="engomado" widget="radio"/>
                                    <field name="oct_alineacion" string="Alineación" widget="radio"/>
                                    <field name="corte_guillotina"
                                           string="Corte de Guillotina"
                                           widget="radio"/>
                                </group>

                                <group string="Producción">
                                    <field name="numero_corrida"/>
                                    <field name="folio"
                                           placeholder="Folio físico/documental del lote"/>
                                    <field name="code"
                                           placeholder="Código interno del producto"/>
                                </group>
                            </group>

                            <group>
                                <group string="Papel">
                                    <field name="papel_ancho" string="Ancho"/>
                                    <field name="papel_gramaje" string="Gramaje"/>
                                    <field name="papel_proveedor_id"
                                           string="Proveedor de Rollos"
                                           context="{'default_supplier_rank': 1}"/>
                                </group>

                                <group string="Adhesivo">
                                    <field name="adhesivo_lote1" string="Lote 1"/>
                                    <field name="adhesivo_lote2" string="Lote 2"/>
                                </group>
                            </group>
                        </page>

                        <page string="Guillotina (Extras)"
                              invisible="process_code != 'guillotina'"
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
                              invisible="state == 'borrador' or process_code == 'octagono' or (not show_papel and not show_adhesivo and not show_tipo_hexagono and not show_numero_corrida and not show_corte_guillotina)"
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
                            <div class="alert alert-warning" role="alert"
                                 invisible="process_code not in ('acabado_empaque', 'impresion')">
                                <i class="fa fa-exclamation-triangle"/>
                                <strong>
                                    <field name="process_type_id" nolabel="1" readonly="1"/>:
                                </strong>
                                este proceso solo permite atributos adicionales con resultado
                                <b>Cumple</b> o <b>No Cumple</b>. No se permite N/A ni valores numéricos.
                            </div>

                            <p class="text-muted" invisible="process_code in ('acabado_empaque', 'impresion')">
                                <i class="fa fa-info-circle"/>
                                CUMPLE / NO CUMPLE / N/A u OK / NO OK / N/A — sin duplicados con Medidas y Propiedades.
                            </p>

                            <field name="line_ids">
                                <list editable="bottom">
                                    <field name="process_code" column_invisible="1"/>
                                    <field name="strict_binary_result" column_invisible="1"/>
                                    <field name="sequence" widget="handle"/>
                                    <field name="name"/>
                                    <field name="attribute_type"/>
                                    <field name="result_mode"/>

                                    <field name="value_float"
                                           invisible="attribute_type != 'float' or strict_binary_result"/>
                                    <field name="value_char"
                                           invisible="attribute_type not in ('char','selection') or strict_binary_result"/>

                                    <field name="value_ok"
                                           string="OK/NO OK/N/A"
                                           invisible="attribute_type != 'boolean' or result_mode != 'ok' or strict_binary_result"
                                           widget="badge"
                                           decoration-success="value_ok == 'ok'"
                                           decoration-danger="value_ok == 'no_ok'"/>

                                    <field name="value_cumple"
                                           string="Cumple/NC"
                                           invisible="attribute_type != 'boolean' or result_mode != 'cumple'"
                                           widget="badge"
                                           decoration-success="value_cumple == 'cumple'"
                                           decoration-danger="value_cumple == 'no_cumple'"/>

                                    <field name="min_value"
                                           invisible="attribute_type != 'float' or strict_binary_result"/>
                                    <field name="max_value"
                                           invisible="attribute_type != 'float' or strict_binary_result"/>
                                    <field name="unit"
                                           invisible="strict_binary_result"/>
                                    <field name="allow_zero"
                                           invisible="attribute_type != 'float' or strict_binary_result"/>

                                    <field name="result"
                                           widget="badge"
                                           column_invisible="parent.process_code in ('acabado_empaque', 'impresion')"
                                           decoration-success="result in ('cumple','ok')"
                                           decoration-danger="result in ('no_cumple','no_ok')"/>
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
</odoo>```

## ./views/quality_menus.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <menuitem id="menu_quality_root"
              name="Calidad"
              web_icon="quality_management,static/description/icon.png"
              sequence="45"/>

    <menuitem id="menu_quality_inspection"
              name="Inspecciones"
              parent="menu_quality_root"
              action="action_quality_inspection"
              sequence="10"/>

    <menuitem id="menu_quality_releases"
              name="Liberaciones"
              parent="menu_quality_root"
              sequence="20"/>

    <menuitem id="menu_quality_sample_release"
              name="Muestras"
              parent="menu_quality_releases"
              action="action_quality_sample_release"
              sequence="10"/>

    <menuitem id="menu_quality_drawing_release"
              name="Planos"
              parent="menu_quality_releases"
              action="action_quality_drawing_release"
              sequence="20"/>

    <!-- FOLIO-QM-ODOO18-069: Troqueles se mueve de la raíz del módulo a Liberaciones. -->
    <menuitem id="menu_quality_troquel"
              name="Troqueles"
              parent="menu_quality_releases"
              action="action_quality_troquel"
              sequence="30"
              groups="quality_management.group_quality_manager"/>

    <menuitem id="menu_quality_certificate"
              name="Certificados"
              parent="menu_quality_root"
              action="action_quality_certificate"
              sequence="30"
              groups="quality_management.group_quality_manager"/>

    <menuitem id="menu_quality_corrective_action"
              name="Acciones Correctivas"
              parent="menu_quality_root"
              action="action_quality_corrective_action"
              sequence="40"
              groups="quality_management.group_quality_manager"/>

    <menuitem id="menu_quality_customer_return"
              name="Devoluciones"
              parent="menu_quality_root"
              action="action_quality_customer_return"
              sequence="50"/>

    <menuitem id="menu_quality_customer_document"
              name="Documentos de Cliente"
              parent="menu_quality_root"
              action="action_quality_customer_document"
              sequence="60"/>

    <menuitem id="menu_quality_config"
              name="Configuración"
              parent="menu_quality_root"
              sequence="100"
              groups="quality_management.group_quality_admin"/>

    <menuitem id="menu_quality_process_type"
              name="Tipos de Proceso"
              parent="menu_quality_config"
              action="action_quality_process_type"
              sequence="5"/>

    <menuitem id="menu_quality_attribute_template"
              name="Plantillas de Atributos"
              parent="menu_quality_config"
              action="action_quality_attribute_template"
              sequence="10"/>
</odoo>```

## ./views/quality_process_route_views.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_quality_process_route_list" model="ir.ui.view">
        <field name="name">quality.process.route.list</field>
        <field name="model">quality.process.route</field>
        <field name="arch" type="xml">
            <list>
                <field name="sequence" widget="handle"/>
                <field name="name"/>
                <field name="active"/>
            </list>
        </field>
    </record>

    <record id="view_quality_process_route_form" model="ir.ui.view">
        <field name="name">quality.process.route.form</field>
        <field name="model">quality.process.route</field>
        <field name="arch" type="xml">
            <form string="Ruta de Proceso">
                <sheet>
                    <div class="oe_title">
                        <h1><field name="name" placeholder="Ruta..."/></h1>
                    </div>
                    <group>
                        <group>
                            <field name="sequence"/>
                            <field name="active"/>
                        </group>
                        <group>
                            <field name="company_id" groups="base.group_multi_company"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Pasos">
                            <field name="line_ids">
                                <list editable="bottom">
                                    <field name="sequence" widget="handle"/>
                                    <field name="process_type_id"/>
                                    <field name="is_optional"/>
                                    <field name="notes"/>
                                </list>
                            </field>
                        </page>
                        <page string="Productos">
                            <field name="product_tmpl_ids"/>
                        </page>
                        <page string="Categorías">
                            <field name="product_categ_ids"/>
                        </page>
                        <page string="Notas">
                            <field name="notes"/>
                        </page>
                    </notebook>
                </sheet>
            </form>
        </field>
    </record>

    <record id="action_quality_process_route" model="ir.actions.act_window">
        <field name="name">Rutas de Proceso</field>
        <field name="res_model">quality.process.route</field>
        <field name="view_mode">list,form</field>
    </record>

    <menuitem id="menu_quality_process_route"
              name="Rutas de Proceso"
              parent="menu_quality_config"
              action="action_quality_process_route"
              sequence="20"/>

    <record id="view_product_template_form_quality_route" model="ir.ui.view">
        <field name="name">product.template.form.quality.route</field>
        <field name="model">product.template</field>
        <field name="inherit_id" ref="product.product_template_form_view"/>
        <field name="arch" type="xml">
            <!-- FOLIO-QM-ODOO18-049: se inserta la ruta en la página de calidad existente del producto. -->
            <xpath expr="//page[@name='quality']" position="inside">
                <separator string="Ruta de Proceso"/>
                <group>
                    <field name="quality_route_id"
                           options="{'no_create': True}"/>
                </group>
            </xpath>
        </field>
    </record>
</odoo>```

## ./views/quality_process_type_views.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_quality_process_type_list" model="ir.ui.view">
        <field name="name">quality.process.type.list</field>
        <field name="model">quality.process.type</field>
        <field name="arch" type="xml">
            <list editable="bottom">
                <field name="sequence" widget="handle"/>
                <field name="name"/>
                <field name="code"/>
                <field name="show_largo"/>
                <field name="show_ancho"/>
                <field name="show_espesor"/>
                <field name="show_hexagono"/>
                <field name="show_resistencia"/>
                <field name="show_apariencia"/>
                <field name="show_humedad"/>
                <field name="show_pegado"/>
                <field name="show_retiramiento"/>
                <field name="show_calibracion"/>
                <field name="show_engomado"/>
                <field name="show_ranurado"/>
                <field name="show_troquelado"/>
                <field name="show_papel"/>
                <field name="show_adhesivo"/>
                <field name="active"/>
            </list>
        </field>
    </record>

    <record id="view_quality_process_type_form" model="ir.ui.view">
        <field name="name">quality.process.type.form</field>
        <field name="model">quality.process.type</field>
        <field name="arch" type="xml">
            <form string="Tipo de Proceso">
                <sheet>
                    <div class="oe_title">
                        <h1><field name="name" placeholder="Nombre del proceso..."/></h1>
                    </div>
                    <group>
                        <group>
                            <field name="code"/>
                            <field name="sequence"/>
                            <field name="active"/>
                        </group>
                        <group>
                            <field name="description"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Campos Visibles en Inspección">
                            <group string="Medidas Dimensionales">
                                <group>
                                    <field name="show_largo"/>
                                    <field name="show_ancho"/>
                                    <field name="show_espesor"/>
                                </group>
                                <group>
                                    <field name="show_hexagono"/>
                                    <field name="show_resistencia"/>
                                    <field name="show_apariencia"/>
                                </group>
                            </group>
                            <group string="Propiedades">
                                <group>
                                    <field name="show_humedad"/>
                                    <field name="show_pegado"/>
                                    <field name="show_retiramiento"/>
                                    <field name="show_calibracion"/>
                                </group>
                                <group>
                                    <field name="show_engomado"/>
                                    <field name="show_ranurado"/>
                                    <field name="show_troquelado"/>
                                </group>
                            </group>
                            <group string="Datos de Producción">
                                <group>
                                    <field name="show_papel"/>
                                    <field name="show_adhesivo"/>
                                </group>
                                <group>
                                    <field name="show_tipo_hexagono"/>
                                    <field name="show_corte_guillotina"/>
                                    <field name="show_numero_corrida"/>
                                </group>
                            </group>
                        </page>
                        <page string="Plantillas de Atributos">
                            <field name="attribute_template_ids">
                                <list editable="bottom">
                                    <field name="sequence" widget="handle"/>
                                    <field name="name"/>
                                    <field name="attribute_type"/>
                                    <field name="selection_options" invisible="attribute_type != 'selection'"/>
                                    <field name="min_value" invisible="attribute_type != 'float'"/>
                                    <field name="max_value" invisible="attribute_type != 'float'"/>
                                    <field name="unit"/>
                                    <field name="is_required"/>
                                </list>
                            </field>
                        </page>
                    </notebook>
                </sheet>
            </form>
        </field>
    </record>

    <record id="action_quality_process_type" model="ir.actions.act_window">
        <field name="name">Tipos de Proceso</field>
        <field name="res_model">quality.process.type</field>
        <field name="view_mode">list,form</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Crear un nuevo tipo de proceso de calidad
            </p>
            <p>Configure qué campos se muestran en la inspección para cada proceso.</p>
        </field>
    </record>
</odoo>
```

## ./views/quality_retention_views.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_quality_inspection_form_retention" model="ir.ui.view">
        <field name="name">quality.inspection.form.retention</field>
        <field name="model">quality.inspection</field>
        <field name="inherit_id" ref="quality_management.view_quality_inspection_form"/>
        <field name="arch" type="xml">
            <!-- FOLIO-QM-ODOO18-048: retention_state se agrega como campo técnico para que las expresiones del header carguen en Odoo 18. -->
            <xpath expr="//sheet" position="inside">
                <field name="retention_state" invisible="1"/>
            </xpath>

            <xpath expr="//header" position="inside">
                <button name="action_accept_correction"
                        string="Producción: Aceptar Corrección"
                        type="object"
                        invisible="state != 'retenido' or retention_state not in ('retenido','en_correccion')"/>
                <button name="action_correction_done"
                        string="Marcar Corrección Hecha"
                        type="object" class="btn-primary"
                        invisible="state != 'retenido' or retention_state not in ('retenido','en_correccion')"/>
                <button name="action_start_reinspection"
                        string="Iniciar Reinspección"
                        type="object" class="btn-warning"
                        invisible="retention_state != 'correccion_hecha'"
                        groups="quality_management.group_quality_inspector"/>
                <button name="action_accept_after_retention"
                        string="Aceptar tras Reinspección"
                        type="object" class="btn-primary"
                        invisible="retention_state != 'reinspeccion'"
                        groups="quality_management.group_quality_inspector"/>
                <button name="action_reject_after_retention"
                        string="Rechazar tras Reinspección"
                        type="object" class="btn-danger"
                        invisible="retention_state != 'reinspeccion'"
                        groups="quality_management.group_quality_inspector"/>
            </xpath>

            <xpath expr="//notebook" position="inside">
                <page string="Retención / Reinspección" name="retention"
                      invisible="retention_state == 'none'">
                    <group>
                        <group>
                            <field name="retention_state" readonly="1"/>
                            <field name="retention_correction_done_by" readonly="1"/>
                            <field name="retention_correction_done_date" readonly="1"/>
                        </group>
                    </group>
                    <separator string="Notas de Corrección"/>
                    <field name="retention_correction_notes"
                           placeholder="Detalle de la corrección aplicada por Producción..."/>
                    <separator string="Bitácora"/>
                    <field name="retention_log_ids" readonly="1">
                        <list>
                            <field name="date"/>
                            <field name="user_id"/>
                            <field name="retention_state_after"/>
                            <field name="description"/>
                        </list>
                    </field>
                </page>
            </xpath>
        </field>
    </record>
</odoo>```

## ./views/quality_sample_release_views.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
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
                                    <!-- FOLIO-QM-ODOO18-046: se agregan result_mode y value_ok para soportar OK/NO OK/N/A en muestras. -->
                                    <field name="result_mode"/>
                                    <field name="value_float" invisible="attribute_type != 'float'"/>
                                    <field name="value_char" invisible="attribute_type not in ('char', 'selection')"/>
                                    <field name="value_cumple"
                                           invisible="attribute_type != 'boolean' or result_mode != 'cumple'"
                                           widget="badge"
                                           decoration-success="value_cumple == 'cumple'"
                                           decoration-danger="value_cumple == 'no_cumple'"/>
                                    <field name="value_ok"
                                           invisible="attribute_type != 'boolean' or result_mode != 'ok'"
                                           widget="badge"
                                           decoration-success="value_ok == 'ok'"
                                           decoration-danger="value_ok == 'no_ok'"/>
                                    <field name="min_value" invisible="attribute_type != 'float'"/>
                                    <field name="max_value" invisible="attribute_type != 'float'"/>
                                    <field name="unit" placeholder="mm, cm, in, %..."/>
                                    <field name="allow_zero" invisible="attribute_type != 'float'"/>
                                    <field name="result" widget="badge"
                                           decoration-success="result in ('cumple','ok')"
                                           decoration-danger="result in ('no_cumple','no_ok')"/>
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
</odoo>```

## ./views/quality_troquel_validation_views.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_troquel_validation_list" model="ir.ui.view">
        <field name="name">quality.troquel.validation.list</field>
        <field name="model">quality.troquel.validation</field>
        <field name="arch" type="xml">
            <list decoration-success="state == 'aprobado'"
                  decoration-danger="state == 'rechazado'">
                <field name="name"/>
                <field name="troquel_id"/>
                <field name="date"/>
                <field name="dimensional_ok" widget="boolean_toggle"/>
                <field name="functional_ok" widget="boolean_toggle"/>
                <field name="state" widget="badge"/>
            </list>
        </field>
    </record>

    <!-- FOLIO-QM-ODOO18-050: search view requerido para que search_default_troquel_id funcione desde smart button. -->
    <record id="view_troquel_validation_search" model="ir.ui.view">
        <field name="name">quality.troquel.validation.search</field>
        <field name="model">quality.troquel.validation</field>
        <field name="arch" type="xml">
            <search string="Validaciones de Troquel">
                <field name="name"/>
                <field name="troquel_id"/>
                <filter string="Aprobadas" name="approved" domain="[('state','=','aprobado')]"/>
                <filter string="Rechazadas" name="rejected" domain="[('state','=','rechazado')]"/>
                <group expand="0" string="Agrupar por">
                    <filter string="Troquel" name="group_troquel" context="{'group_by': 'troquel_id'}"/>
                    <filter string="Estado" name="group_state" context="{'group_by': 'state'}"/>
                </group>
            </search>
        </field>
    </record>

    <record id="view_troquel_validation_form" model="ir.ui.view">
        <field name="name">quality.troquel.validation.form</field>
        <field name="model">quality.troquel.validation</field>
        <field name="arch" type="xml">
            <form string="Validación de Troquel">
                <header>
                    <button name="action_start" string="Iniciar Validación"
                            type="object" class="btn-primary"
                            invisible="state != 'borrador'"/>
                    <button name="action_approve" string="Aprobar"
                            type="object" class="btn-primary"
                            invisible="state != 'en_validacion'"/>
                    <button name="action_reject" string="Rechazar"
                            type="object" class="btn-danger"
                            invisible="state != 'en_validacion'"/>
                    <field name="state" widget="statusbar"/>
                </header>
                <sheet>
                    <div class="oe_title">
                        <h1><field name="name" readonly="1"/></h1>
                    </div>
                    <group>
                        <group>
                            <field name="troquel_id"/>
                            <field name="date"/>
                        </group>
                        <group>
                            <field name="convoked_quality"/>
                            <field name="quality_user_id"
                                   invisible="not convoked_quality"/>
                            <field name="convoked_production"/>
                            <field name="production_user_id"
                                   invisible="not convoked_production"/>
                            <field name="design_user_id"/>
                        </group>
                    </group>
                    <group>
                        <field name="dimensional_ok" readonly="1"/>
                        <field name="functional_ok" readonly="1"/>
                        <field name="overall_ok" readonly="1"/>
                    </group>
                    <notebook>
                        <page string="Mediciones / Pruebas">
                            <field name="line_ids">
                                <list editable="bottom">
                                    <field name="sequence" widget="handle"/>
                                    <field name="test_type"/>
                                    <field name="name"/>
                                    <field name="expected"/>
                                    <field name="measured"/>
                                    <field name="tolerance"/>
                                    <field name="result" widget="badge"
                                           decoration-success="result == 'cumple'"
                                           decoration-danger="result == 'no_cumple'"/>
                                    <field name="notes"/>
                                </list>
                            </field>
                        </page>
                        <page string="Observaciones">
                            <field name="notes"/>
                        </page>
                    </notebook>
                </sheet>
                <chatter/>
            </form>
        </field>
    </record>

    <record id="action_troquel_validation" model="ir.actions.act_window">
        <field name="name">Validaciones de Troquel</field>
        <field name="res_model">quality.troquel.validation</field>
        <field name="view_mode">list,form</field>
        <field name="search_view_id" ref="view_troquel_validation_search"/>
    </record>

    <record id="view_troquel_repair_list" model="ir.ui.view">
        <field name="name">quality.troquel.repair.list</field>
        <field name="model">quality.troquel.repair</field>
        <field name="arch" type="xml">
            <list decoration-success="state == 'finalizada'"
                  decoration-danger="state == 'rechazada'">
                <field name="name"/>
                <field name="troquel_id"/>
                <field name="repair_type"/>
                <field name="proveedor_id"/>
                <field name="date_started"/>
                <field name="date_finished"/>
                <field name="state" widget="badge"/>
            </list>
        </field>
    </record>

    <record id="view_troquel_repair_search" model="ir.ui.view">
        <field name="name">quality.troquel.repair.search</field>
        <field name="model">quality.troquel.repair</field>
        <field name="arch" type="xml">
            <search string="Reparaciones de Troquel">
                <field name="name"/>
                <field name="troquel_id"/>
                <field name="proveedor_id"/>
                <filter string="En Curso" name="open" domain="[('state','=','en_curso')]"/>
                <filter string="Finalizadas" name="done" domain="[('state','=','finalizada')]"/>
                <group expand="0" string="Agrupar por">
                    <filter string="Troquel" name="group_troquel" context="{'group_by': 'troquel_id'}"/>
                    <filter string="Estado" name="group_state" context="{'group_by': 'state'}"/>
                </group>
            </search>
        </field>
    </record>

    <record id="view_troquel_repair_form" model="ir.ui.view">
        <field name="name">quality.troquel.repair.form</field>
        <field name="model">quality.troquel.repair</field>
        <field name="arch" type="xml">
            <form string="Reparación de Troquel">
                <header>
                    <button name="action_finish" string="Finalizar"
                            type="object" class="btn-primary"
                            invisible="state != 'en_curso'"/>
                    <field name="state" widget="statusbar"/>
                </header>
                <sheet>
                    <div class="oe_title">
                        <h1><field name="name" readonly="1"/></h1>
                    </div>
                    <group>
                        <group>
                            <field name="troquel_id"/>
                            <field name="repair_type"/>
                            <field name="proveedor_id"
                                   invisible="repair_type != 'proveedor'"/>
                        </group>
                        <group>
                            <field name="date_started"/>
                            <field name="date_finished"/>
                            <field name="days_estimated"/>
                            <field name="cost"/>
                            <field name="currency_id" invisible="1"/>
                        </group>
                    </group>
                    <separator string="Desglose de Reparación"/>
                    <field name="description"/>
                </sheet>
                <chatter/>
            </form>
        </field>
    </record>

    <record id="action_troquel_repair" model="ir.actions.act_window">
        <field name="name">Reparaciones de Troquel</field>
        <field name="res_model">quality.troquel.repair</field>
        <field name="view_mode">list,form</field>
        <field name="search_view_id" ref="view_troquel_repair_search"/>
    </record>

    <record id="view_quality_troquel_form_extended" model="ir.ui.view">
        <field name="name">quality.troquel.form.extended</field>
        <field name="model">quality.troquel</field>
        <field name="inherit_id" ref="quality_management.view_quality_troquel_form"/>
        <field name="arch" type="xml">
            <xpath expr="//header" position="inside">
                <button name="action_open_validation"
                        string="Nueva Validación" type="object"
                        class="btn-secondary"
                        groups="quality_management.group_quality_manager"/>
                <button name="action_open_repair"
                        string="Nueva Reparación" type="object"
                        class="btn-secondary"
                        invisible="state not in ('reparacion_interna','reparacion_proveedor','danado')"
                        groups="quality_management.group_quality_manager"/>
            </xpath>

            <xpath expr="//sheet/div[@class='oe_title']" position="before">
                <div class="oe_button_box" name="button_box">
                    <field name="needs_review" invisible="1"/>
                    <button name="%(action_troquel_validation)d"
                            type="action"
                            class="oe_stat_button" icon="fa-check-square-o"
                            context="{'search_default_troquel_id': id}"
                            groups="quality_management.group_quality_manager">
                        <field name="validation_count" widget="statinfo"
                               string="Validaciones"/>
                    </button>
                    <button name="%(action_troquel_repair)d"
                            type="action"
                            class="oe_stat_button" icon="fa-wrench"
                            context="{'search_default_troquel_id': id}"
                            groups="quality_management.group_quality_manager">
                        <field name="repair_count" widget="statinfo"
                               string="Reparaciones"/>
                    </button>
                </div>
            </xpath>

            <xpath expr="//field[@name='pieces_per_review']" position="after">
                <field name="pieces_produced"/>
                <field name="needs_review" readonly="1"/>
            </xpath>
        </field>
    </record>

    <menuitem id="menu_quality_troquel_validation"
              name="Validaciones de Troquel"
              parent="menu_quality_config"
              action="action_troquel_validation"
              sequence="40"/>

    <menuitem id="menu_quality_troquel_repair"
              name="Reparaciones de Troquel"
              parent="menu_quality_config"
              action="action_troquel_repair"
              sequence="45"/>
</odoo>```

## ./views/quality_troquel_views.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
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
</odoo>
```

## ./views/res_company_views.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_company_form_quality_stamp" model="ir.ui.view">
        <field name="name">res.company.form.quality.stamp</field>
        <field name="model">res.company</field>
        <field name="inherit_id" ref="base.view_company_form"/>
        <field name="arch" type="xml">
            <xpath expr="//sheet" position="inside">
                <group string="Calidad">
                    <field name="quality_stamp" widget="image"
                           options="{'size': [200, 200]}"/>
                </group>
            </xpath>
        </field>
    </record>
</odoo>```

## ./wizards/__init__.py
```py
from . import certificate_wizard
from . import certificate_wizard_hardening
```

## ./wizards/certificate_wizard_hardening.py
```py
# -*- coding: utf-8 -*-

import re
import unicodedata

from odoo import models, _


def _slug(value):
    value = value or ""
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    value = re.sub(r"[^a-zA-Z0-9]+", "_", value.lower()).strip("_")
    return value


class QualityCertificateWizardHardening(models.TransientModel):
    _inherit = "quality.certificate.wizard"

    def _selection_label(self, record, field_name, value):
        if not value:
            return False
        return dict(record._fields[field_name].selection).get(value, value)

    def action_create_certificate(self):
        self.ensure_one()
        insp = self.inspection_id

        vals = {
            "inspection_id": insp.id,
            "partner_id": self.partner_id.id,
            "certified_by": self.env.user.id,
        }

        if self.include_largo and insp.largo:
            vals["certified_largo"] = insp.largo
        if self.include_ancho and (insp.ancho or getattr(insp, "oct_ancho", 0.0)):
            vals["certified_ancho"] = insp.ancho or insp.oct_ancho
        if self.include_espesor and insp.espesor:
            vals["certified_espesor"] = insp.espesor

        # FOLIO-QM-ODOO18-075:
        # Octágono usa valores Selection para Hexágono. El certificado debe guardar
        # la etiqueta textual, no escribir "tipo_1" en un campo Float legacy.
        hex_sources = [
            ("hexagono", insp.hexagono),
            ("oct_hexagono_tipo", getattr(insp, "oct_hexagono_tipo", False)),
            ("oct_hexagono", getattr(insp, "oct_hexagono", False)),
            ("tipo_hexagono", insp.tipo_hexagono),
        ]
        for field_name, hex_value in hex_sources:
            if self.include_hexagono and hex_value:
                vals["certified_hexagono_label"] = self._selection_label(insp, field_name, hex_value)
                break

        if self.include_resistencia and insp.resistencia:
            vals["certified_resistencia"] = insp.resistencia
        if self.include_apariencia and insp.apariencia:
            vals["certified_apariencia"] = self._selection_label(insp, "apariencia", insp.apariencia)
        if self.include_humedad and insp.humedad_pct:
            vals["certified_humedad"] = insp.humedad_pct

        if self.include_pegado:
            pegado_value = insp.pegado_result or getattr(insp, "oct_pegado", False)
            if pegado_value:
                field_name = "pegado_result" if insp.pegado_result else "oct_pegado"
                vals["certified_pegado"] = self._selection_label(insp, field_name, pegado_value)

        if (
            self.include_retiramiento
            and insp.process_code != "octagono"
            and (getattr(insp, "reticula_extendida", 0.0) or getattr(insp, "oct_retiramiento", 0.0))
        ):
            # FOLIO-QM-ODOO18-075: Retiramiento corresponde a Guillotina y se certifica en cm.
            vals["certified_retiramiento"] = insp.reticula_extendida or insp.oct_retiramiento
        if self.include_calibracion and insp.calibracion:
            # FOLIO-QM-ODOO18-075: conservar precisión 0.0010 en certificado.
            vals["certified_calibracion"] = round(insp.calibracion, 4)
        if self.include_engomado and insp.engomado:
            vals["certified_engomado"] = self._selection_label(insp, "engomado", insp.engomado)

        cert = self.env["quality.certificate"].create(vals)

        if self.include_all_attributes and insp.line_ids:
            seen = set()
            unique_ids = []
            for line in insp.line_ids:
                key = line.normalized_name or _slug(line.name)
                if not key or key in seen:
                    continue
                if line.result not in ("cumple", "ok"):
                    continue
                if line.attribute_type == "float" and not line.allow_zero and not line.value_float:
                    continue
                seen.add(key)
                unique_ids.append(line.id)
            cert.attribute_ids = [(6, 0, unique_ids)]

        return {
            "type": "ir.actions.act_window",
            "name": _("Certificado"),
            "res_model": "quality.certificate",
            "res_id": cert.id,
            "view_mode": "form",
            "target": "current",
        }

```

## ./wizards/certificate_wizard_views.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <record id="view_quality_certificate_wizard_form" model="ir.ui.view">
        <field name="name">quality.certificate.wizard.form</field>
        <field name="model">quality.certificate.wizard</field>
        <field name="arch" type="xml">
            <form string="Crear Certificado de Calidad">
                <field name="inspection_type" invisible="1"/>
                <group>
                    <group>
                        <field name="inspection_id"/>
                        <field name="partner_id"/>
                        <field name="process_type_id" readonly="1"/>
                    </group>
                </group>
                <separator string="Seleccione los atributos a incluir en el certificado"/>
                <group>
                    <group>
                        <field name="include_largo"/>
                        <field name="include_ancho"/>
                        <field name="include_espesor"/>
                        <field name="include_hexagono"/>
                        <field name="include_resistencia"/>
                        <field name="include_apariencia"/>
                    </group>
                    <group>
                        <field name="include_humedad"/>
                        <field name="include_pegado"/>
                        <field name="include_retiramiento"/>
                        <field name="include_calibracion"/>
                        <field name="include_engomado"/>
                        <field name="include_all_attributes"/>
                    </group>
                </group>
                <footer>
                    <button name="action_create_certificate" string="Crear Certificado"
                            type="object" class="btn-primary"/>
                    <button string="Cancelar" class="btn-secondary" special="cancel"/>
                </footer>
            </form>
        </field>
    </record>
</odoo>
```

## ./wizards/certificate_wizard.py
```py
from odoo import models, fields, api, _


class QualityCertificateWizard(models.TransientModel):
    _name = 'quality.certificate.wizard'
    _description = 'Asistente para Crear Certificado'

    inspection_id = fields.Many2one(
        'quality.inspection', 'Inspección',
        required=True, readonly=True
    )
    partner_id = fields.Many2one(
        'res.partner', 'Cliente', required=True
    )
    inspection_type = fields.Selection(
        related='inspection_id.inspection_type'
    )
    process_type_id = fields.Many2one(
        related='inspection_id.process_type_id'
    )
    # Checkboxes
    include_largo = fields.Boolean('Incluir Largo', default=True)
    include_ancho = fields.Boolean('Incluir Ancho', default=True)
    include_espesor = fields.Boolean('Incluir Espesor', default=True)
    include_hexagono = fields.Boolean('Incluir Hexágono', default=True)
    include_resistencia = fields.Boolean('Incluir Resistencia', default=True)
    include_apariencia = fields.Boolean('Incluir Apariencia')
    include_humedad = fields.Boolean('Incluir % Humedad')
    include_pegado = fields.Boolean('Incluir Pegado')
    include_retiramiento = fields.Boolean('Incluir Retiramiento')
    include_calibracion = fields.Boolean('Incluir Calibración')
    include_engomado = fields.Boolean('Incluir Engomado')
    # Incluir todos los atributos adicionales
    include_all_attributes = fields.Boolean(
        'Incluir Atributos Adicionales', default=True
    )

    def action_create_certificate(self):
        self.ensure_one()
        insp = self.inspection_id
        vals = {
            'inspection_id': insp.id,
            'partner_id': self.partner_id.id,
            'certified_by': self.env.user.id,
        }
        # Poblar según selección
        if self.include_largo and insp.largo:
            vals['certified_largo'] = insp.largo
        if self.include_ancho:
            vals['certified_ancho'] = insp.ancho or insp.oct_ancho
        if self.include_espesor:
            vals['certified_espesor'] = insp.espesor or insp.oct_espesor
        if self.include_hexagono:
            # FOLIO-QM-ODOO18-075:
            # Hexágono es selección textual; no debe escribirse en certified_hexagono (Float).
            hex_sources = [
                ('hexagono', insp.hexagono),
                ('oct_hexagono_tipo', getattr(insp, 'oct_hexagono_tipo', False)),
                ('oct_hexagono', getattr(insp, 'oct_hexagono', False)),
                ('tipo_hexagono', insp.tipo_hexagono),
            ]
            for field_name, hex_value in hex_sources:
                if hex_value:
                    vals['certified_hexagono_label'] = dict(
                        insp._fields[field_name].selection
                    ).get(hex_value, hex_value)
                    break
        if self.include_resistencia and insp.resistencia:
            vals['certified_resistencia'] = insp.resistencia
        if self.include_apariencia and insp.apariencia:
            vals['certified_apariencia'] = dict(
                insp._fields['apariencia'].selection
            ).get(insp.apariencia, '')
        if self.include_humedad and insp.humedad_pct:
            vals['certified_humedad'] = insp.humedad_pct
        if self.include_pegado:
            pegado_val = insp.pegado_result or insp.oct_pegado
            if pegado_val:
                source_field = 'pegado_result' if insp.pegado_result else 'oct_pegado'
                vals['certified_pegado'] = dict(
                    insp._fields[source_field].selection
                ).get(pegado_val, '')
        if (
            self.include_retiramiento
            and insp.process_code != 'octagono'
            and (getattr(insp, 'reticula_extendida', 0.0) or insp.oct_retiramiento)
        ):
            vals['certified_retiramiento'] = getattr(insp, 'reticula_extendida', 0.0) or insp.oct_retiramiento
        if self.include_calibracion and insp.calibracion:
            vals['certified_calibracion'] = round(insp.calibracion, 4)
        if self.include_engomado and insp.engomado:
            vals['certified_engomado'] = dict(
                insp._fields['engomado'].selection
            ).get(insp.engomado, '')

        cert = self.env['quality.certificate'].create(vals)

        # Vincular atributos adicionales si se solicitó (con dedupe por nombre)
        if self.include_all_attributes and insp.line_ids:
            seen = set()
            unique_ids = []
            for line in insp.line_ids:
                key = (line.name or "").strip().lower()
                if key and key not in seen:
                    seen.add(key)
                    unique_ids.append(line.id)
            cert.attribute_ids = [(6, 0, unique_ids)]

        return {
            'type': 'ir.actions.act_window',
            'name': _('Certificado'),
            'res_model': 'quality.certificate',
            'res_id': cert.id,
            'view_mode': 'form',
            'target': 'current',
        }
```

