## ./__init__.py
```py
from . import models
from . import wizards
```

## ./__manifest__.py
```py
{
    'name': 'Gestión de Calidad - Hexágonos Mexicanos',
    'version': '18.0.2.1.0',
    'category': 'Manufacturing/Quality',
    'summary': 'Módulo integral de gestión de calidad para industria del cartón',
    'description': """
        Gestión de Calidad para Hexágonos Mexicanos
        =============================================
        - Tipos de Proceso configurables (no hardcoded)
        - Liberación de Muestras con reporte PDF
        - Liberación de Planos con visor PDF embebido
        - Inspección de PP y PT con atributos dinámicos
        - Generación de Certificados con reporte PDF
        - Acciones Correctivas/Preventivas (8D) con reporte
        - Devolución de Clientes con reporte PDF
        - Documentos solicitados por clientes con reporte PDF
        - Visor PDF embebido en formularios
        - Visor de evidencia inline (imágenes, videos, PDFs)
        - Integración con Ventas, Contactos y Manufactura (smart buttons)
    """,
    'author': 'Alphaqueb Consulting SAS',
    'website': 'https://alphaqueb.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'project',
        'mrp',
        'sale',
        'stock',
        'product',
        'contacts',
        'hr',
    ],
    'data': [
        # Security
        'security/quality_groups.xml',
        'security/ir.model.access.csv',
        'security/quality_rules.xml',
        # Data
        'data/sequence_data.xml',
        'data/process_type_data.xml',
        'data/cron_data.xml',
        # Wizards
        'wizards/certificate_wizard_views.xml',
        # Views
        'views/quality_process_type_views.xml',
        'views/quality_attribute_template_views.xml',
        'views/quality_sample_release_views.xml',
        'views/quality_drawing_release_views.xml',
        'views/quality_inspection_views.xml',
        'views/quality_certificate_views.xml',
        'views/quality_corrective_action_views.xml',
        'views/quality_customer_return_views.xml',
        'views/quality_customer_document_views.xml',
        'views/quality_dashboard_views.xml',
        # Inherited views (integration with sale, contacts, mrp)
        'views/quality_inherited_views.xml',
        # Menus (AFTER views)
        'views/quality_menus.xml',
        # Reports
        'reports/report_quality_certificate.xml',
        'reports/report_8d.xml',
        'reports/report_inspection_summary.xml',
        'reports/report_sample_release.xml',
        'reports/report_drawing_release.xml',
        'reports/report_customer_return.xml',
        'reports/report_customer_document.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'quality_management/static/src/css/quality_pdf_viewer.css',
            'quality_management/static/src/css/quality_evidence_viewer.css',
            'quality_management/static/src/js/evidence_viewer_widget.js',
            'quality_management/static/src/xml/evidence_viewer_widget.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
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
        <!-- Laminadora y Remanejo -->
        <record id="process_type_laminadora" model="quality.process.type">
            <field name="name">Laminadora y Remanejo</field>
            <field name="code">laminadora_remanejo</field>
            <field name="sequence">10</field>
            <field name="show_largo" eval="True"/>
            <field name="show_ancho" eval="True"/>
            <field name="show_espesor" eval="True"/>
            <field name="show_hexagono" eval="True"/>
            <field name="show_resistencia" eval="True"/>
            <field name="show_apariencia" eval="True"/>
            <field name="show_humedad" eval="True"/>
            <field name="show_pegado" eval="True"/>
            <field name="show_ranurado" eval="True"/>
            <field name="show_troquelado" eval="True"/>
            <field name="description">Proceso de laminado y remanejo de cartón. Incluye mediciones dimensionales, ranurado y troquelado.</field>
        </record>

        <!-- Octágono -->
        <record id="process_type_octagono" model="quality.process.type">
            <field name="name">Octágono</field>
            <field name="code">octagono</field>
            <field name="sequence">20</field>
            <field name="show_ancho" eval="True"/>
            <field name="show_espesor" eval="True"/>
            <field name="show_hexagono" eval="True"/>
            <field name="show_retiramiento" eval="True"/>
            <field name="show_pegado" eval="True"/>
            <field name="description">Proceso de formado octagonal. Mediciones de ancho, espesor, hexágono, retiramiento y pegado.</field>
        </record>

        <!-- Guillotina y Pegado -->
        <record id="process_type_guillotina" model="quality.process.type">
            <field name="name">Guillotina y Pegado</field>
            <field name="code">guillotina_pegado</field>
            <field name="sequence">30</field>
            <field name="show_calibracion" eval="True"/>
            <field name="show_engomado" eval="True"/>
            <field name="show_papel" eval="True"/>
            <field name="show_adhesivo" eval="True"/>
            <field name="show_tipo_hexagono" eval="True"/>
            <field name="show_corte_guillotina" eval="True"/>
            <field name="show_numero_corrida" eval="True"/>
            <field name="description">Proceso de corte en guillotina y pegado. Incluye datos de papel, adhesivo, calibración y engomado.</field>
        </record>

        <!-- Ejemplos de nuevos procesos que el usuario puede agregar -->
        <record id="process_type_impresion" model="quality.process.type">
            <field name="name">Impresión</field>
            <field name="code">impresion</field>
            <field name="sequence">40</field>
            <field name="show_apariencia" eval="True"/>
            <field name="show_humedad" eval="True"/>
            <field name="description">Proceso de impresión sobre cartón. Inspección visual de apariencia y humedad.</field>
        </record>

        <record id="process_type_troquelado_plano" model="quality.process.type">
            <field name="name">Troquelado Plano</field>
            <field name="code">troquelado_plano</field>
            <field name="sequence">50</field>
            <field name="show_largo" eval="True"/>
            <field name="show_ancho" eval="True"/>
            <field name="show_espesor" eval="True"/>
            <field name="show_troquelado" eval="True"/>
            <field name="show_apariencia" eval="True"/>
            <field name="description">Proceso de troquelado plano. Mediciones dimensionales y capturas de troquelado.</field>
        </record>

        <record id="process_type_acabado" model="quality.process.type">
            <field name="name">Acabado y Empaque</field>
            <field name="code">acabado_empaque</field>
            <field name="sequence">60</field>
            <field name="show_apariencia" eval="True"/>
            <field name="show_largo" eval="True"/>
            <field name="show_ancho" eval="True"/>
            <field name="description">Inspección final de acabado y empaque antes de envío al cliente.</field>
        </record>
    </data>
</odoo>
```

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
from . import quality_attribute_template
from . import quality_sample_release
from . import quality_drawing_release
from . import quality_inspection
from . import quality_inspection_line
from . import quality_inspection_ranurado
from . import quality_inspection_troquelado
from . import quality_certificate
from . import quality_corrective_action
from . import quality_action_line
from . import quality_customer_return
from . import quality_customer_document
from . import quality_inherited_models```

## ./models/quality_action_line.py
```py
from odoo import models, fields, api


class QualityActionLine(models.Model):
    _name = 'quality.action.line'
    _description = 'Línea de Acción Correctiva'
    _order = 'date_due, id'

    corrective_id = fields.Many2one(
        'quality.corrective.action', 'Acción Correctiva',
        required=True, ondelete='cascade'
    )
    description = fields.Text('Descripción de la Acción', required=True)
    responsible_id = fields.Many2one(
        'res.users', 'Responsable', required=True
    )
    date_due = fields.Date('Fecha de Cumplimiento', required=True)
    date_completed = fields.Date('Fecha de Cumplimiento Real')
    evidence_ids = fields.Many2many(
        'ir.attachment', 'quality_action_evidence_rel',
        'action_line_id', 'attachment_id',
        string='Evidencia'
    )
    state = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completada', 'Completada'),
        ('vencida', 'Vencida'),
    ], string='Estado', default='pendiente', required=True)
    delay_days = fields.Integer(
        'Días de Atraso', compute='_compute_delay_days', store=True
    )
    notes = fields.Text('Notas')

    @api.depends('date_due', 'state')
    def _compute_delay_days(self):
        today = fields.Date.today()
        for line in self:
            if line.date_due and line.state in ('pendiente', 'en_proceso', 'vencida'):
                delta = (today - line.date_due).days
                line.delay_days = max(0, delta)
            else:
                line.delay_days = 0

    def action_start(self):
        for rec in self:
            rec.state = 'en_proceso'

    def action_complete(self):
        for rec in self:
            rec.state = 'completada'
            rec.date_completed = fields.Date.today()

    def action_reopen(self):
        for rec in self:
            rec.state = 'en_proceso'
            rec.date_completed = False
```

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
        ('boolean', 'Sí/No'),
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
```

## ./models/quality_certificate.py
```py
from odoo import models, fields, api, _


class QualityCertificate(models.Model):
    _name = 'quality.certificate'
    _description = 'Certificado de Calidad'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_generated desc, id desc'

    name = fields.Char(
        'Referencia', required=True, readonly=True,
        default='Nuevo', copy=False
    )
    inspection_id = fields.Many2one(
        'quality.inspection', 'Inspección Fuente',
        required=True, tracking=True,
        domain=[('state', '=', 'aceptado')]
    )
    partner_id = fields.Many2one(
        'res.partner', 'Cliente', required=True, tracking=True
    )
    product_id = fields.Many2one(
        related='inspection_id.product_id', string='Producto', store=True
    )
    process_type_id = fields.Many2one(
        related='inspection_id.process_type_id',
        string='Tipo de Proceso', store=True
    )
    # Legacy
    inspection_type = fields.Selection(
        related='inspection_id.inspection_type',
        string='Tipo (Legacy)', store=True
    )
    attribute_ids = fields.Many2many(
        'quality.inspection.line',
        'quality_certificate_attribute_rel',
        'certificate_id', 'line_id',
        string='Atributos del Certificado'
    )
    # Snapshot de valores
    certified_largo = fields.Float('Largo (mm)')
    certified_ancho = fields.Float('Ancho (mm)')
    certified_espesor = fields.Float('Espesor (mm)')
    certified_hexagono = fields.Float('Hexágono')
    certified_resistencia = fields.Float('Resistencia')
    certified_apariencia = fields.Char('Apariencia')
    certified_humedad = fields.Float('% Humedad')
    certified_pegado = fields.Char('Pegado')
    certified_retiramiento = fields.Float('Retiramiento')
    certified_calibracion = fields.Float('Calibración')
    certified_engomado = fields.Char('Engomado')
    date_generated = fields.Date(
        'Fecha de Generación', required=True,
        default=fields.Date.context_today
    )
    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('generado', 'Generado'),
        ('enviado', 'Enviado'),
    ], string='Estado', default='borrador', required=True,
        tracking=True, copy=False)
    report_pdf = fields.Binary('PDF del Certificado', attachment=True)
    report_pdf_name = fields.Char('Nombre del PDF')
    certified_by = fields.Many2one(
        'res.users', 'Certificado por',
        required=True, default=lambda self: self.env.user,
        tracking=True
    )
    company_id = fields.Many2one(
        'res.company', 'Compañía',
        default=lambda self: self.env.company
    )
    folio = fields.Char(
        related='inspection_id.folio', string='Folio', store=True
    )
    lot_id = fields.Many2one(
        related='inspection_id.lot_id', string='Lote', store=True
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'quality.certificate') or 'Nuevo'
        return super().create(vals_list)

    def action_generate(self):
        for rec in self:
            rec.state = 'generado'
            rec.message_post(
                body=_('Certificado generado por %s') % self.env.user.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_send_email(self):
        self.ensure_one()
        template = self.env.ref(
            'quality_management.email_template_quality_certificate',
            raise_if_not_found=False
        )
        compose_form = self.env.ref('mail.email_compose_message_wizard_form')
        ctx = {
            'default_model': 'quality.certificate',
            'default_res_ids': self.ids,
            'default_template_id': template.id if template else False,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }

    def action_mark_sent(self):
        for rec in self:
            rec.state = 'enviado'
            rec.message_post(
                body=_('Certificado enviado al cliente %s') % rec.partner_id.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_print_certificate(self):
        return self.env.ref(
            'quality_management.action_report_quality_certificate'
        ).report_action(self)
```

## ./models/quality_corrective_action.py
```py
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import timedelta


class QualityCorrectiveAction(models.Model):
    _name = 'quality.corrective.action'
    _description = 'Acción Correctiva/Preventiva'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_opened desc, id desc'

    name = fields.Char(
        'Referencia', required=True, readonly=True,
        default='Nuevo', copy=False
    )
    origin_type = fields.Selection([
        ('inspeccion', 'Inspección'),
        ('auditoria_interna', 'Auditoría Interna'),
        ('auditoria_externa', 'Auditoría Externa'),
        ('devolucion', 'Devolución'),
        ('otro', 'Otro'),
    ], string='Tipo de Origen', required=True, tracking=True)
    origin_description = fields.Text(
        'Descripción del Incumplimiento', required=True
    )
    origin_inspection_id = fields.Many2one(
        'quality.inspection', 'Inspección Origen'
    )
    origin_return_id = fields.Many2one(
        'quality.customer.return', 'Devolución Origen'
    )
    responsible_id = fields.Many2one(
        'res.users', 'Responsable General',
        required=True, tracking=True
    )
    action_line_ids = fields.One2many(
        'quality.action.line', 'corrective_id',
        string='Acciones Específicas'
    )
    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('abierta', 'Abierta'),
        ('en_proceso', 'En Proceso'),
        ('cerrada', 'Cerrada'),
        ('no_procede', 'No Procede'),
    ], string='Estado', default='borrador', required=True,
        tracking=True, copy=False)
    date_opened = fields.Date(
        'Fecha de Apertura', required=True,
        default=fields.Date.context_today
    )
    date_closed = fields.Date('Fecha de Cierre', tracking=True)
    action_count = fields.Integer(
        'Total de Acciones', compute='_compute_action_stats'
    )
    action_completed_count = fields.Integer(
        'Acciones Completadas', compute='_compute_action_stats'
    )
    action_overdue_count = fields.Integer(
        'Acciones Vencidas', compute='_compute_action_stats'
    )
    progress = fields.Float(
        'Progreso (%)', compute='_compute_action_stats'
    )
    company_id = fields.Many2one(
        'res.company', 'Compañía',
        default=lambda self: self.env.company
    )

    @api.depends('action_line_ids', 'action_line_ids.state')
    def _compute_action_stats(self):
        for rec in self:
            lines = rec.action_line_ids
            rec.action_count = len(lines)
            rec.action_completed_count = len(
                lines.filtered(lambda l: l.state == 'completada')
            )
            rec.action_overdue_count = len(
                lines.filtered(lambda l: l.state == 'vencida')
            )
            rec.progress = (
                (rec.action_completed_count / rec.action_count * 100)
                if rec.action_count else 0.0
            )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'quality.corrective.action') or 'Nuevo'
        return super().create(vals_list)

    def action_open(self):
        for rec in self:
            rec.state = 'abierta'
            rec.message_post(
                body=_('Acción correctiva abierta por %s') % self.env.user.name,
                subtype_xmlid='mail.mt_comment',
            )
            rec.activity_schedule(
                'mail.mail_activity_data_todo',
                date_deadline=fields.Date.today() + timedelta(days=1),
                summary=_('Acción correctiva asignada: %s') % rec.name,
                user_id=rec.responsible_id.id,
            )

    def action_in_progress(self):
        for rec in self:
            rec.state = 'en_proceso'

    def action_close(self):
        for rec in self:
            pending = rec.action_line_ids.filtered(
                lambda l: l.state not in ('completada',)
            )
            if pending:
                raise UserError(_(
                    'No se puede cerrar: hay %d acción(es) sin completar.'
                ) % len(pending))
            rec.state = 'cerrada'
            rec.date_closed = fields.Date.today()
            rec.activity_feedback(
                ['mail.mail_activity_data_todo'],
                feedback=_('Acción correctiva cerrada')
            )
            rec.message_post(
                body=_('✅ Acción correctiva CERRADA por %s') % self.env.user.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_no_proceed(self):
        for rec in self:
            rec.state = 'no_procede'
            rec.date_closed = fields.Date.today()
            rec.message_post(
                body=_('Acción correctiva marcada como NO PROCEDE por %s') % self.env.user.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_reopen(self):
        for rec in self:
            rec.state = 'en_proceso'
            rec.date_closed = False

    def action_print_8d(self):
        return self.env.ref(
            'quality_management.action_report_8d'
        ).report_action(self)

    @api.model
    def _cron_check_overdue_actions(self):
        today = fields.Date.today()
        overdue_lines = self.env['quality.action.line'].search([
            ('state', 'in', ('pendiente', 'en_proceso')),
            ('date_due', '<', today),
        ])
        for line in overdue_lines:
            line.state = 'vencida'
            days = (today - line.date_due).days
            line.delay_days = days
            line.corrective_id.message_post(
                body=_(
                    '⚠️ Acción vencida: "%s" - Responsable: %s - '
                    'Días de atraso: %d'
                ) % (line.description[:80], line.responsible_id.name, days),
                subtype_xmlid='mail.mt_comment',
            )
            line.corrective_id.activity_schedule(
                'mail.mail_activity_data_todo',
                date_deadline=today,
                summary=_(
                    'Acción vencida (%d días): %s'
                ) % (days, line.description[:50]),
                user_id=line.responsible_id.id,
            )
```

## ./models/quality_customer_document.py
```py
from odoo import models, fields, api, _
from datetime import timedelta


class QualityCustomerDocument(models.Model):
    _name = 'quality.customer.document'
    _description = 'Documento Solicitado por Cliente'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_requested desc, id desc'

    name = fields.Char(
        'Referencia', required=True, readonly=True,
        default='Nuevo', copy=False
    )
    partner_id = fields.Many2one(
        'res.partner', 'Cliente Solicitante',
        required=True, tracking=True
    )
    document_type = fields.Selection([
        ('rohs', 'RoHS'),
        ('psw', 'PSW'),
        ('ppap', 'PPAP'),
        ('apariencia', 'Apariencia'),
        ('pfmea', 'PFMEA'),
        ('diagrama_flujo', 'Diagrama de Flujo'),
        ('especificacion_empaque', 'Especificación de Empaque'),
        ('carta_garantia', 'Carta Garantía'),
        ('otro', 'Otro'),
    ], string='Tipo de Documento', required=True, tracking=True)
    description = fields.Text('Descripción Adicional')
    requires_dimensions = fields.Boolean(
        'Implica Mediciones Dimensionales', required=True, tracking=True
    )
    client_format_ids = fields.Many2many(
        'ir.attachment', 'quality_doc_client_format_rel',
        'document_id', 'attachment_id',
        string='Formatos del Cliente'
    )
    result_document_ids = fields.Many2many(
        'ir.attachment', 'quality_doc_result_rel',
        'document_id', 'attachment_id',
        string='Documentos Generados'
    )
    # PDF principal para preview embebido
    main_pdf = fields.Binary('Documento Principal (PDF)', attachment=True)
    main_pdf_name = fields.Char('Nombre del Documento')
    requested_by = fields.Many2one(
        'res.users', 'Solicitante (Ventas)',
        required=True, default=lambda self: self.env.user,
        tracking=True
    )
    responsible_id = fields.Many2one(
        'res.users', 'Responsable en Calidad',
        required=True, tracking=True
    )
    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
        ('enviado', 'Enviado'),
    ], string='Estado', default='borrador', required=True,
        tracking=True, copy=False)
    date_requested = fields.Date(
        'Fecha de Solicitud', required=True,
        default=fields.Date.context_today
    )
    date_due = fields.Date(
        'Fecha Límite', compute='_compute_date_due',
        store=True, readonly=False
    )
    date_completed = fields.Date('Fecha de Entrega Real')
    company_id = fields.Many2one(
        'res.company', 'Compañía',
        default=lambda self: self.env.company
    )

    @api.depends('date_requested', 'requires_dimensions')
    def _compute_date_due(self):
        for rec in self:
            if rec.date_requested:
                days = 7 if rec.requires_dimensions else 5
                rec.date_due = rec.date_requested + timedelta(days=days)
            else:
                rec.date_due = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'quality.customer.document') or 'Nuevo'
        return super().create(vals_list)

    def action_start(self):
        for rec in self:
            rec.state = 'en_proceso'
            rec.activity_schedule(
                'mail.mail_activity_data_todo',
                date_deadline=rec.date_due,
                summary=_('Generar documento de calidad: %s - %s') % (
                    rec.name,
                    dict(rec._fields['document_type'].selection).get(
                        rec.document_type, ''
                    ),
                ),
                user_id=rec.responsible_id.id,
            )

    def action_complete(self):
        for rec in self:
            rec.state = 'completado'
            rec.date_completed = fields.Date.today()
            rec.activity_feedback(
                ['mail.mail_activity_data_todo'],
                feedback=_('Documento completado')
            )
            rec.message_post(
                body=_(
                    '✅ Documento completado por Calidad. '
                    'Ventas: proceder a enviar al cliente %s.'
                ) % rec.partner_id.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_send(self):
        for rec in self:
            rec.state = 'enviado'
            rec.message_post(
                body=_('Documento enviado al cliente %s') % rec.partner_id.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_print_customer_document(self):
        return self.env.ref(
            'quality_management.action_report_customer_document'
        ).report_action(self)
```

## ./models/quality_customer_return.py
```py
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import timedelta


class QualityCustomerReturn(models.Model):
    _name = 'quality.customer.return'
    _description = 'Devolución de Cliente'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_received desc, id desc'

    name = fields.Char(
        'Referencia', required=True, readonly=True,
        default='Nuevo', copy=False
    )
    partner_id = fields.Many2one(
        'res.partner', 'Cliente', required=True, tracking=True
    )
    sale_order_id = fields.Many2one(
        'sale.order', 'Orden de Venta Original', tracking=True
    )
    defect_type = fields.Selection([
        ('dimensional', 'Dimensional'),
        ('apariencia', 'Apariencia'),
        ('funcional', 'Funcional'),
        ('empaque', 'Empaque'),
        ('otro', 'Otro'),
    ], string='Tipo de Defecto', required=True, tracking=True)
    defect_pieces = fields.Integer('Piezas con Defecto', required=True)
    return_reason = fields.Text('Motivo de la Devolución', required=True)
    production_date = fields.Date('Fecha de Producción', required=True)
    evidence_ids = fields.Many2many(
        'ir.attachment', 'quality_return_evidence_rel',
        'return_id', 'attachment_id',
        string='Evidencia Fotográfica', required=True
    )
    # PDF de evidencia con preview
    evidence_pdf = fields.Binary('Reporte de Evidencia (PDF)', attachment=True)
    evidence_pdf_name = fields.Char('Nombre del Reporte')
    pallets_returned = fields.Boolean('Se Regresan Tarimas')
    pallet_return_date = fields.Date('Fecha Retorno de Tarimas')
    claim_format_id = fields.Many2one(
        'ir.attachment', 'Formato de Reclamación'
    )
    affects_functionality = fields.Boolean(
        'Afecta Funcionalidad', tracking=True
    )
    corrective_action_id = fields.Many2one(
        'quality.corrective.action', '8D Generado',
        readonly=True, tracking=True
    )
    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('evaluacion_ventas', 'Evaluación Ventas'),
        ('evaluacion_calidad', 'Evaluación Calidad'),
        ('en_8d', 'En 8D'),
        ('cerrada', 'Cerrada'),
        ('no_procede', 'No Procede'),
    ], string='Estado', default='borrador', required=True,
        tracking=True, copy=False)
    date_received = fields.Date(
        'Fecha de Recepción', required=True,
        default=fields.Date.context_today
    )
    days_since_production = fields.Integer(
        'Días desde Producción',
        compute='_compute_days_since_production'
    )
    is_within_period = fields.Boolean(
        'Dentro de Periodo',
        compute='_compute_days_since_production'
    )
    company_id = fields.Many2one(
        'res.company', 'Compañía',
        default=lambda self: self.env.company
    )

    @api.depends('production_date', 'date_received')
    def _compute_days_since_production(self):
        for rec in self:
            if rec.production_date and rec.date_received:
                delta = (rec.date_received - rec.production_date).days
                rec.days_since_production = delta
                rec.is_within_period = delta < 30
            else:
                rec.days_since_production = 0
                rec.is_within_period = True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'quality.customer.return') or 'Nuevo'
        return super().create(vals_list)

    def action_submit_sales(self):
        for rec in self:
            if not rec.is_within_period:
                rec.state = 'no_procede'
                rec.message_post(
                    body=_(
                        'Devolución NO PROCEDE: fecha de producción mayor a '
                        '30 días (%d días).'
                    ) % rec.days_since_production,
                    subtype_xmlid='mail.mt_comment',
                )
                return
            rec.state = 'evaluacion_ventas'
            rec.message_post(
                body=_('Devolución registrada, en evaluación por Ventas.'),
                subtype_xmlid='mail.mt_comment',
            )

    def action_submit_quality(self):
        for rec in self:
            rec.state = 'evaluacion_calidad'
            quality_users = self.env.ref(
                'quality_management.group_quality_manager'
            ).users
            for user in quality_users:
                rec.activity_schedule(
                    'mail.mail_activity_data_todo',
                    date_deadline=fields.Date.today() + timedelta(days=3),
                    summary=_('Evaluar devolución: %s') % rec.name,
                    user_id=user.id,
                )
            rec.message_post(
                body=_('Devolución enviada a evaluación de Calidad.'),
                subtype_xmlid='mail.mt_comment',
            )
            if rec.pallets_returned:
                rec.message_post(
                    body=_(
                        '📦 Se retornaron tarimas a planta. '
                        'Logística/Producción: evaluar físicamente.'
                    ),
                    subtype_xmlid='mail.mt_comment',
                )

    def action_generate_8d(self):
        for rec in self:
            ca = self.env['quality.corrective.action'].create({
                'origin_type': 'devolucion',
                'origin_description': _(
                    'Devolución de cliente: %s\n'
                    'Tipo de defecto: %s\n'
                    'Piezas: %d\n'
                    'Motivo: %s'
                ) % (
                    rec.partner_id.name,
                    dict(rec._fields['defect_type'].selection).get(rec.defect_type, ''),
                    rec.defect_pieces,
                    rec.return_reason,
                ),
                'origin_return_id': rec.id,
                'responsible_id': self.env.user.id,
            })
            rec.corrective_action_id = ca.id
            rec.state = 'en_8d'
            rec.message_post(
                body=_('8D generado: %s') % ca.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_close(self):
        for rec in self:
            rec.state = 'cerrada'
            rec.message_post(
                body=_('Devolución cerrada por %s') % self.env.user.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_no_proceed(self):
        for rec in self:
            rec.state = 'no_procede'
            rec.message_post(
                body=_('Devolución marcada como NO PROCEDE.'),
                subtype_xmlid='mail.mt_comment',
            )

    def action_print_customer_return(self):
        return self.env.ref(
            'quality_management.action_report_customer_return'
        ).report_action(self)
```

## ./models/quality_drawing_release.py
```py
from odoo import models, fields, api, _
from datetime import timedelta


class QualityDrawingRelease(models.Model):
    _name = 'quality.drawing.release'
    _description = 'Liberación de Planos'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_requested desc, id desc'

    name = fields.Char(
        'Referencia', required=True, readonly=True,
        default='Nuevo', copy=False
    )
    partner_id = fields.Many2one(
        'res.partner', 'Cliente', required=True, tracking=True
    )
    sale_order_id = fields.Many2one(
        'sale.order', 'Orden de Venta', tracking=True
    )
    drawing_attachment_ids = fields.Many2many(
        'ir.attachment', 'quality_drawing_attachment_rel',
        'drawing_id', 'attachment_id',
        string='Plano y Cotización/Dibujo', required=True
    )
    # PDF principal para preview embebido
    drawing_pdf = fields.Binary('Plano Principal (PDF)', attachment=True)
    drawing_pdf_name = fields.Char('Nombre del Plano')
    requested_by = fields.Many2one(
        'res.users', 'Solicitante (Ventas)',
        required=True, default=lambda self: self.env.user,
        tracking=True
    )
    inspector_id = fields.Many2one(
        'res.users', 'Inspector de Calidad', tracking=True
    )
    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('en_revision', 'En Revisión'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
    ], string='Estado', default='borrador', required=True,
        tracking=True, copy=False)
    rejection_reason = fields.Text('Motivo de Rechazo')
    date_requested = fields.Date(
        'Fecha de Solicitud', required=True,
        default=fields.Date.context_today
    )
    date_released = fields.Date('Fecha de Liberación')
    company_id = fields.Many2one(
        'res.company', 'Compañía',
        default=lambda self: self.env.company
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'quality.drawing.release') or 'Nuevo'
        return super().create(vals_list)

    def action_submit_review(self):
        for rec in self:
            rec.state = 'en_revision'
            quality_users = self.env.ref(
                'quality_management.group_quality_inspector'
            ).users
            if rec.inspector_id:
                quality_users = rec.inspector_id
            for user in quality_users:
                rec.activity_schedule(
                    'mail.mail_activity_data_todo',
                    date_deadline=fields.Date.today() + timedelta(days=3),
                    summary=_('Revisión de plano: %s') % rec.name,
                    user_id=user.id,
                )
            rec.message_post(
                body=_('Solicitud de revisión de plano enviada por %s') % rec.requested_by.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_accept(self):
        for rec in self:
            rec.state = 'aceptado'
            rec.date_released = fields.Date.today()
            rec.activity_feedback(
                ['mail.mail_activity_data_todo'],
                feedback=_('Plano liberado')
            )
            rec.message_post(
                body=_('✅ Plano LIBERADO por %s') % self.env.user.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_reject(self):
        for rec in self:
            if not rec.rejection_reason:
                raise models.ValidationError(
                    _('Debe capturar el motivo de rechazo.')
                )
            rec.state = 'rechazado'
            rec.activity_feedback(
                ['mail.mail_activity_data_todo'],
                feedback=_('Plano rechazado: %s') % rec.rejection_reason
            )
            rec.message_post(
                body=_('❌ Plano RECHAZADO por %s.\nMotivo: %s') % (
                    self.env.user.name, rec.rejection_reason),
                subtype_xmlid='mail.mt_comment',
            )

    def action_reset_draft(self):
        for rec in self:
            rec.state = 'borrador'
            rec.rejection_reason = False

    def action_print_drawing_release(self):
        return self.env.ref(
            'quality_management.action_report_drawing_release'
        ).report_action(self)
```

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
        ('boolean', 'Sí/No'),
        ('char', 'Texto'),
    ], string='Tipo de Dato', default='float')
    value_float = fields.Float('Valor Numérico')
    value_char = fields.Char('Valor Texto')
    value_boolean = fields.Boolean('Valor Sí/No')
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
```

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
    medida = fields.Float('Medida (mm)', required=True)
    resultado = fields.Selection([
        ('cumple', 'Cumple'),
        ('no_cumple', 'No Cumple'),
    ], string='Resultado', default='cumple')
    notas = fields.Char('Notas')
```

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
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import timedelta


class QualityInspection(models.Model):
    _name = 'quality.inspection'
    _description = 'Inspección de PP/PT'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_inspection desc, id desc'

    name = fields.Char(
        'Referencia', required=True, readonly=True,
        default='Nuevo', copy=False
    )
    # ── Tipo de proceso dinámico ──
    process_type_id = fields.Many2one(
        'quality.process.type', 'Tipo de Proceso',
        required=True, tracking=True
    )
    inspection_type = fields.Selection([
        ('laminadora_remanejo', 'Laminadora y Remanejo'),
        ('octagono', 'Octágono'),
        ('guillotina_pegado', 'Guillotina y Pegado'),
    ], string='Tipo (Legacy)',
        compute='_compute_inspection_type', store=True)
    # ── Visibilidad dinámica ──
    show_largo = fields.Boolean(related='process_type_id.show_largo')
    show_ancho = fields.Boolean(related='process_type_id.show_ancho')
    show_espesor = fields.Boolean(related='process_type_id.show_espesor')
    show_hexagono = fields.Boolean(related='process_type_id.show_hexagono')
    show_resistencia = fields.Boolean(related='process_type_id.show_resistencia')
    show_apariencia = fields.Boolean(related='process_type_id.show_apariencia')
    show_humedad = fields.Boolean(related='process_type_id.show_humedad')
    show_pegado = fields.Boolean(related='process_type_id.show_pegado')
    show_retiramiento = fields.Boolean(related='process_type_id.show_retiramiento')
    show_calibracion = fields.Boolean(related='process_type_id.show_calibracion')
    show_engomado = fields.Boolean(related='process_type_id.show_engomado')
    show_ranurado = fields.Boolean(related='process_type_id.show_ranurado')
    show_troquelado = fields.Boolean(related='process_type_id.show_troquelado')
    show_papel = fields.Boolean(related='process_type_id.show_papel')
    show_adhesivo = fields.Boolean(related='process_type_id.show_adhesivo')
    show_tipo_hexagono = fields.Boolean(related='process_type_id.show_tipo_hexagono')
    show_corte_guillotina = fields.Boolean(related='process_type_id.show_corte_guillotina')
    show_numero_corrida = fields.Boolean(related='process_type_id.show_numero_corrida')
    # ── Datos generales ──
    production_order_id = fields.Many2one(
        'mrp.production', 'Orden de Producción', tracking=True
    )
    lot_id = fields.Many2one('stock.lot', 'Lote de Fabricación', tracking=True)
    product_id = fields.Many2one(
        'product.product', 'Producto', required=True, tracking=True
    )
    operator_id = fields.Many2one('hr.employee', 'Operador', required=True)
    supervisor_id = fields.Many2one('hr.employee', 'Supervisor', required=True)
    partner_id = fields.Many2one(
        'res.partner', 'Cliente', required=True, tracking=True
    )
    folio = fields.Char('Folio de Producción', required=True)
    code = fields.Char('Código de Producto', required=True)
    shift = fields.Selection([
        ('turno_1', 'Turno 1'),
        ('turno_2', 'Turno 2'),
        ('turno_3', 'Turno 3'),
    ], string='Turno', required=True)
    plant = fields.Selection([
        ('planta_1', 'Planta 1'),
        ('planta_2', 'Planta 2'),
    ], string='Planta', required=True)
    inspector_id = fields.Many2one(
        'res.users', 'Inspector de Calidad',
        required=True, default=lambda self: self.env.user,
        tracking=True
    )
    date_inspection = fields.Datetime(
        'Fecha y Hora de Inspección', required=True,
        default=fields.Datetime.now
    )
    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('en_proceso', 'En Proceso'),
        ('aceptado', 'Aceptado'),
        ('retenido', 'Retenido'),
        ('rechazado', 'Rechazado'),
    ], string='Estado', default='borrador', required=True,
        tracking=True, copy=False)
    is_pp = fields.Boolean('Producto en Proceso')
    is_pt = fields.Boolean('Producto Terminado')
    line_ids = fields.One2many(
        'quality.inspection.line', 'inspection_id',
        string='Atributos Capturados'
    )
    # ── Campos de medición ──
    largo = fields.Float('Largo (mm)')
    ancho = fields.Float('Ancho (mm)')
    espesor = fields.Float('Espesor (mm)')
    hexagono = fields.Float('Hexágono')
    resistencia = fields.Float('Resistencia')
    apariencia = fields.Selection([
        ('buena', 'Buena'),
        ('regular', 'Regular'),
        ('mala', 'Mala'),
    ], string='Apariencia')
    humedad_pct = fields.Float('% Humedad')
    ranurado_ids = fields.One2many(
        'quality.inspection.ranurado', 'inspection_id',
        string='Capturas de Ranurado'
    )
    troquelado_ids = fields.One2many(
        'quality.inspection.troquelado', 'inspection_id',
        string='Capturas de Troquelado'
    )
    pegado_result = fields.Selection([
        ('cumple', 'Cumple'),
        ('no_cumple', 'No Cumple'),
    ], string='Resultado de Pegado')
    oct_ancho = fields.Float('Ancho Octágono (mm)')
    oct_espesor = fields.Float('Espesor Octágono (mm)')
    oct_hexagono = fields.Float('Hexágono Octágono')
    oct_retiramiento = fields.Float('Retiramiento')
    oct_pegado = fields.Selection([
        ('cumple', 'Cumple'),
        ('no_cumple', 'No Cumple'),
    ], string='Pegado Octágono')
    numero_corrida = fields.Char('Número de Corrida')
    papel_ancho = fields.Float('Ancho del Papel')
    papel_gramaje = fields.Float('Gramaje del Papel')
    papel_proveedor_id = fields.Many2one(
        'res.partner', 'Proveedor del Papel',
        domain=[('supplier_rank', '>', 0)]
    )
    adhesivo_lote1 = fields.Char('Lote 1 Adhesivo')
    adhesivo_lote2 = fields.Char('Lote 2 Adhesivo')
    tipo_hexagono = fields.Selection([
        ('tipo_a', 'Tipo A'),
        ('tipo_b', 'Tipo B'),
        ('tipo_c', 'Tipo C'),
    ], string='Tipo de Hexágono')
    calibracion = fields.Float('Calibración')
    engomado = fields.Selection([
        ('cumple', 'Cumple'),
        ('no_cumple', 'No Cumple'),
    ], string='Engomado')
    corte_guillotina = fields.Boolean('Corte en Guillotina')
    # ── Evidencia con preview ──
    evidence_pdf = fields.Binary('Documento de Evidencia (PDF)', attachment=True)
    evidence_pdf_name = fields.Char('Nombre del Documento')
    # ── General ──
    notes = fields.Html('Observaciones')
    certificate_ids = fields.One2many(
        'quality.certificate', 'inspection_id', string='Certificados'
    )
    certificate_count = fields.Integer(compute='_compute_certificate_count')
    company_id = fields.Many2one(
        'res.company', 'Compañía',
        default=lambda self: self.env.company
    )

    @api.depends('process_type_id', 'process_type_id.code')
    def _compute_inspection_type(self):
        legacy_codes = ('laminadora_remanejo', 'octagono', 'guillotina_pegado')
        for rec in self:
            code = rec.process_type_id.code if rec.process_type_id else False
            rec.inspection_type = code if code in legacy_codes else False

    @api.depends('certificate_ids')
    def _compute_certificate_count(self):
        for rec in self:
            rec.certificate_count = len(rec.certificate_ids)

    @api.onchange('process_type_id')
    def _onchange_process_type_id(self):
        if self.process_type_id and self.process_type_id.attribute_template_ids:
            lines = []
            for tmpl in self.process_type_id.attribute_template_ids:
                lines.append((0, 0, {
                    'attribute_template_id': tmpl.id,
                    'name': tmpl.name,
                    'attribute_type': tmpl.attribute_type,
                    'min_value': tmpl.min_value,
                    'max_value': tmpl.max_value,
                    'unit': tmpl.unit,
                    'sequence': tmpl.sequence,
                }))
            self.line_ids = lines

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'quality.inspection') or 'Nuevo'
        return super().create(vals_list)

    def action_start(self):
        for rec in self:
            rec.state = 'en_proceso'

    def action_accept(self):
        for rec in self:
            rec.state = 'aceptado'
            rec.message_post(
                body=_('✅ Inspección ACEPTADA por %s') % self.env.user.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_retain(self):
        for rec in self:
            rec.state = 'retenido'
            rec.message_post(
                body=_(
                    '⚠️ Producto RETENIDO por %s. '
                    'Lote: %s - Se notifica a Programación/Producción.'
                ) % (self.env.user.name, rec.lot_id.name or 'N/A'),
                subtype_xmlid='mail.mt_comment',
            )
            if rec.production_order_id and rec.production_order_id.user_id:
                rec.activity_schedule(
                    'mail.mail_activity_data_todo',
                    date_deadline=fields.Date.today() + timedelta(days=1),
                    summary=_('Producto retenido en calidad: %s') % rec.name,
                    user_id=rec.production_order_id.user_id.id,
                )

    def action_reject(self):
        for rec in self:
            rec.state = 'rechazado'
            rec.message_post(
                body=_('❌ Inspección RECHAZADA por %s') % self.env.user.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_reset_draft(self):
        for rec in self:
            rec.state = 'borrador'

    def action_create_certificate(self):
        self.ensure_one()
        if self.state != 'aceptado':
            raise UserError(_(
                'Solo se pueden crear certificados de inspecciones aceptadas.'
            ))
        return {
            'type': 'ir.actions.act_window',
            'name': _('Crear Certificado'),
            'res_model': 'quality.certificate.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_inspection_id': self.id,
                'default_partner_id': self.partner_id.id,
            },
        }

    def action_view_certificates(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Certificados'),
            'res_model': 'quality.certificate',
            'view_mode': 'list,form',
            'domain': [('inspection_id', '=', self.id)],
            'context': {'default_inspection_id': self.id},
        }

    def action_print_inspection(self):
        return self.env.ref(
            'quality_management.action_report_inspection_summary'
        ).report_action(self)
```

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

## ./models/quality_sample_release.py
```py
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import timedelta


class QualitySampleRelease(models.Model):
    _name = 'quality.sample.release'
    _description = 'Liberación de Muestras'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_requested desc, id desc'

    name = fields.Char(
        'Referencia', required=True, readonly=True,
        default='Nuevo', copy=False
    )
    project_task_id = fields.Many2one(
        'project.task', 'Tarea de Proyecto',
        required=True, tracking=True,
        help='Tarea del proyecto Muestras & Prototipos'
    )
    product_id = fields.Many2one(
        'product.product', 'Producto/Muestra',
        required=True, tracking=True
    )
    requested_by = fields.Many2one(
        'res.users', 'Solicitante (Diseño)',
        required=True, default=lambda self: self.env.user,
        tracking=True
    )
    inspector_id = fields.Many2one(
        'res.users', 'Inspector de Calidad', tracking=True
    )
    date_requested = fields.Date(
        'Fecha de Solicitud', required=True,
        default=fields.Date.context_today
    )
    date_inspected = fields.Date('Fecha de Inspección', tracking=True)
    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('en_inspeccion', 'En Inspección'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
    ], string='Estado', default='borrador', required=True,
        tracking=True, copy=False)
    inspection_line_ids = fields.One2many(
        'quality.inspection.line', 'sample_release_id',
        string='Atributos Inspeccionados'
    )
    # PDF de especificación con preview
    spec_pdf = fields.Binary('Especificación (PDF)', attachment=True)
    spec_pdf_name = fields.Char('Nombre Especificación')
    notes = fields.Html('Observaciones')
    company_id = fields.Many2one(
        'res.company', 'Compañía',
        default=lambda self: self.env.company
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'quality.sample.release') or 'Nuevo'
        return super().create(vals_list)

    def action_submit_inspection(self):
        for rec in self:
            rec.state = 'en_inspeccion'
            quality_users = self.env.ref(
                'quality_management.group_quality_inspector'
            ).users
            if rec.inspector_id:
                quality_users = rec.inspector_id
            for user in quality_users:
                rec.activity_schedule(
                    'mail.mail_activity_data_todo',
                    date_deadline=fields.Date.today() + timedelta(days=2),
                    summary=_('Inspección de muestra: %s') % rec.name,
                    user_id=user.id,
                )
            rec.message_post(
                body=_('Solicitud de inspección enviada por %s') % rec.requested_by.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_accept(self):
        for rec in self:
            if rec.inspection_line_ids:
                failing = rec.inspection_line_ids.filtered(
                    lambda l: l.result == 'no_cumple'
                )
                if failing:
                    raise UserError(_(
                        'No se puede liberar: hay %d atributo(s) que no cumplen.'
                    ) % len(failing))
            rec.state = 'aceptado'
            rec.date_inspected = fields.Date.today()
            rec.activity_feedback(
                ['mail.mail_activity_data_todo'],
                feedback=_('Muestra aceptada')
            )
            rec.message_post(
                body=_('✅ Muestra ACEPTADA y liberada por %s') % self.env.user.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_reject(self):
        for rec in self:
            rec.state = 'rechazado'
            rec.date_inspected = fields.Date.today()
            rec.activity_feedback(
                ['mail.mail_activity_data_todo'],
                feedback=_('Muestra rechazada')
            )
            rec.message_post(
                body=_('❌ Muestra RECHAZADA por %s. Se notifica a Diseño.') % self.env.user.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_reset_draft(self):
        for rec in self:
            rec.state = 'borrador'

    def action_print_sample_release(self):
        return self.env.ref(
            'quality_management.action_report_sample_release'
        ).report_action(self)
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

                        <h4>D3 - Plan de Acciones</h4>
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

                        <!-- Estado visual -->
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
</odoo>
```

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

                        <t t-if="doc.state == 'aceptado'">
                            <div class="text-center" style="margin-bottom: 15px;">
                                <span style="background-color: #28a745; color: white; padding: 5px 20px; border-radius: 4px; font-size: 16px; font-weight: bold;">
                                    ✅ PLANO LIBERADO
                                </span>
                            </div>
                        </t>
                        <t t-if="doc.state == 'rechazado'">
                            <div class="text-center" style="margin-bottom: 15px;">
                                <span style="background-color: #dc3545; color: white; padding: 5px 20px; border-radius: 4px; font-size: 16px; font-weight: bold;">
                                    ❌ PLANO RECHAZADO
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

                        <t t-if="doc.state == 'rechazado' and doc.rejection_reason">
                            <h4>Motivo de Rechazo</h4>
                            <div style="border: 2px solid #dc3545; padding: 10px; margin-bottom: 15px; min-height: 40px; background-color: #fff5f5;">
                                <span t-field="doc.rejection_reason"/>
                            </div>
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
</odoo>
```

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
                                    <td><span t-field="doc.supervisor_id.name"/></td>
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

                        <!-- Medidas dinámicas -->
                        <t t-if="doc.show_largo or doc.show_ancho or doc.show_espesor or doc.show_hexagono or doc.show_resistencia or doc.show_apariencia or doc.show_humedad or doc.show_pegado or doc.show_retiramiento or doc.show_calibracion or doc.show_engomado">
                            <h4>Medidas - <span t-field="doc.process_type_id.name"/></h4>
                            <table class="table table-bordered table-sm">
                                <thead><tr class="table-active">
                                    <th t-if="doc.show_largo">Largo</th>
                                    <th t-if="doc.show_ancho">Ancho</th>
                                    <th t-if="doc.show_espesor">Espesor</th>
                                    <th t-if="doc.show_hexagono">Hexágono</th>
                                    <th t-if="doc.show_resistencia">Resistencia</th>
                                    <th t-if="doc.show_apariencia">Apariencia</th>
                                    <th t-if="doc.show_humedad">% Humedad</th>
                                    <th t-if="doc.show_pegado">Pegado</th>
                                    <th t-if="doc.show_retiramiento">Retiramiento</th>
                                    <th t-if="doc.show_calibracion">Calibración</th>
                                    <th t-if="doc.show_engomado">Engomado</th>
                                </tr></thead>
                                <tbody><tr>
                                    <td t-if="doc.show_largo" class="text-center"><span t-field="doc.largo"/></td>
                                    <td t-if="doc.show_ancho" class="text-center"><span t-esc="doc.ancho or doc.oct_ancho"/></td>
                                    <td t-if="doc.show_espesor" class="text-center"><span t-esc="doc.espesor or doc.oct_espesor"/></td>
                                    <td t-if="doc.show_hexagono" class="text-center"><span t-esc="doc.hexagono or doc.oct_hexagono"/></td>
                                    <td t-if="doc.show_resistencia" class="text-center"><span t-field="doc.resistencia"/></td>
                                    <td t-if="doc.show_apariencia" class="text-center"><span t-field="doc.apariencia"/></td>
                                    <td t-if="doc.show_humedad" class="text-center"><span t-field="doc.humedad_pct"/>%</td>
                                    <td t-if="doc.show_pegado" class="text-center"><span t-esc="doc.pegado_result or doc.oct_pegado or ''"/></td>
                                    <td t-if="doc.show_retiramiento" class="text-center"><span t-field="doc.oct_retiramiento"/></td>
                                    <td t-if="doc.show_calibracion" class="text-center"><span t-field="doc.calibracion"/></td>
                                    <td t-if="doc.show_engomado" class="text-center"><span t-field="doc.engomado"/></td>
                                </tr></tbody>
                            </table>
                        </t>

                        <!-- Datos de producción -->
                        <t t-if="doc.show_numero_corrida or doc.show_papel or doc.show_adhesivo">
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

                        <!-- Ranurado -->
                        <t t-if="doc.ranurado_ids">
                            <h5>Ranurado</h5>
                            <table class="table table-bordered table-sm">
                                <thead><tr class="table-active">
                                    <th>N°</th><th>Medida (mm)</th><th>Resultado</th>
                                </tr></thead>
                                <tbody>
                                    <tr t-foreach="doc.ranurado_ids" t-as="r">
                                        <td><span t-field="r.sequence"/></td>
                                        <td class="text-center"><span t-field="r.medida"/></td>
                                        <td class="text-center"><span t-field="r.resultado"/></td>
                                    </tr>
                                </tbody>
                            </table>
                        </t>

                        <!-- Troquelado -->
                        <t t-if="doc.troquelado_ids">
                            <h5>Troquelado</h5>
                            <table class="table table-bordered table-sm">
                                <thead><tr class="table-active">
                                    <th>N°</th><th>Medida (mm)</th><th>Resultado</th>
                                </tr></thead>
                                <tbody>
                                    <tr t-foreach="doc.troquelado_ids" t-as="t_line">
                                        <td><span t-field="t_line.sequence"/></td>
                                        <td class="text-center"><span t-field="t_line.medida"/></td>
                                        <td class="text-center"><span t-field="t_line.resultado"/></td>
                                    </tr>
                                </tbody>
                            </table>
                        </t>

                        <!-- Atributos adicionales -->
                        <t t-if="doc.line_ids">
                            <h5>Atributos Adicionales</h5>
                            <table class="table table-bordered table-sm">
                                <thead><tr class="table-active">
                                    <th>Atributo</th><th>Valor</th><th>Rango</th><th>Resultado</th>
                                </tr></thead>
                                <tbody>
                                    <tr t-foreach="doc.line_ids" t-as="attr">
                                        <td><span t-field="attr.name"/></td>
                                        <td class="text-center">
                                            <span t-if="attr.attribute_type == 'float'" t-field="attr.value_float"/>
                                            <span t-if="attr.attribute_type in ('char', 'selection')" t-field="attr.value_char"/>
                                            <span t-if="attr.attribute_type == 'boolean'" t-field="attr.value_boolean"/>
                                        </td>
                                        <td class="text-center">
                                            <t t-if="attr.min_value or attr.max_value">
                                                <span t-field="attr.min_value"/> - <span t-field="attr.max_value"/> <span t-field="attr.unit"/>
                                            </t>
                                        </td>
                                        <td class="text-center"><span t-field="attr.result"/></td>
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
                                    <p>Supervisor</p>
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
                                    <td class="text-center">mm</td>
                                </tr>
                                <tr t-if="doc.certified_hexagono">
                                    <td>Hexágono</td>
                                    <td class="text-center"><span t-field="doc.certified_hexagono"/></td>
                                    <td class="text-center">mm</td>
                                </tr>
                                <tr t-if="doc.certified_resistencia">
                                    <td>Resistencia</td>
                                    <td class="text-center"><span t-field="doc.certified_resistencia"/></td>
                                    <td class="text-center">-</td>
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
                                    <td class="text-center">mm</td>
                                </tr>
                                <tr t-if="doc.certified_calibracion">
                                    <td>Calibración</td>
                                    <td class="text-center"><span t-field="doc.certified_calibracion"/></td>
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
                                            <span t-if="attr.attribute_type == 'boolean'" t-field="attr.value_boolean"/>
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
                                    <p>____________________________</p>
                                    <p>Sello de la Empresa</p>
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

                        <!-- Estado como sello visual -->
                        <t t-if="doc.state == 'aceptado'">
                            <div class="text-center" style="margin-bottom: 15px;">
                                <span style="background-color: #28a745; color: white; padding: 5px 20px; border-radius: 4px; font-size: 16px; font-weight: bold;">
                                    ✅ MUESTRA LIBERADA
                                </span>
                            </div>
                        </t>
                        <t t-if="doc.state == 'rechazado'">
                            <div class="text-center" style="margin-bottom: 15px;">
                                <span style="background-color: #dc3545; color: white; padding: 5px 20px; border-radius: 4px; font-size: 16px; font-weight: bold;">
                                    ❌ MUESTRA RECHAZADA
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
                                            <span t-if="line.attribute_type == 'boolean'" t-field="line.value_boolean"/>
                                        </td>
                                        <td class="text-center">
                                            <t t-if="line.min_value or line.max_value">
                                                <span t-field="line.min_value"/> - <span t-field="line.max_value"/>
                                            </t>
                                        </td>
                                        <td class="text-center"><span t-field="line.unit"/></td>
                                        <td class="text-center">
                                            <span t-if="line.result == 'cumple'" style="color: green; font-weight: bold;">CUMPLE</span>
                                            <span t-if="line.result == 'no_cumple'" style="color: red; font-weight: bold;">NO CUMPLE</span>
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
</odoo>
```

## ./security/quality_groups.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <record id="module_category_quality" model="ir.module.category">
            <field name="name">Calidad</field>
            <field name="sequence">50</field>
        </record>

        <record id="group_quality_inspector" model="res.groups">
            <field name="name">Inspector de Calidad</field>
            <field name="category_id" ref="module_category_quality"/>
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
</odoo>
```

## ./security/quality_rules.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <record id="rule_inspection_inspector_own" model="ir.rule">
            <field name="name">Inspector: solo sus inspecciones</field>
            <field name="model_id" ref="model_quality_inspection"/>
            <field name="domain_force">[('inspector_id', '=', user.id)]</field>
            <field name="groups" eval="[(4, ref('group_quality_inspector'))]"/>
        </record>
        <record id="rule_inspection_manager_all" model="ir.rule">
            <field name="name">Manager: todas las inspecciones</field>
            <field name="model_id" ref="model_quality_inspection"/>
            <field name="domain_force">[(1, '=', 1)]</field>
            <field name="groups" eval="[(4, ref('group_quality_manager'))]"/>
        </record>
        <record id="rule_sample_release_sale" model="ir.rule">
            <field name="name">Ventas: solo sus solicitudes de muestra</field>
            <field name="model_id" ref="model_quality_sample_release"/>
            <field name="domain_force">['|', ('requested_by', '=', user.id), ('state', 'in', ['aceptado', 'rechazado'])]</field>
            <field name="groups" eval="[(4, ref('sales_team.group_sale_salesman'))]"/>
        </record>
        <record id="rule_drawing_release_sale" model="ir.rule">
            <field name="name">Ventas: solo sus solicitudes de plano</field>
            <field name="model_id" ref="model_quality_drawing_release"/>
            <field name="domain_force">['|', ('requested_by', '=', user.id), ('state', 'in', ['aceptado', 'rechazado'])]</field>
            <field name="groups" eval="[(4, ref('sales_team.group_sale_salesman'))]"/>
        </record>
        <record id="rule_customer_return_sale" model="ir.rule">
            <field name="name">Ventas: devoluciones de sus clientes</field>
            <field name="model_id" ref="model_quality_customer_return"/>
            <field name="domain_force">[(1, '=', 1)]</field>
            <field name="groups" eval="[(4, ref('sales_team.group_sale_salesman'))]"/>
        </record>
        <record id="rule_sample_release_manager" model="ir.rule">
            <field name="name">Manager: todas las liberaciones de muestra</field>
            <field name="model_id" ref="model_quality_sample_release"/>
            <field name="domain_force">[(1, '=', 1)]</field>
            <field name="groups" eval="[(4, ref('group_quality_manager'))]"/>
        </record>
        <record id="rule_drawing_release_manager" model="ir.rule">
            <field name="name">Manager: todas las liberaciones de plano</field>
            <field name="model_id" ref="model_quality_drawing_release"/>
            <field name="domain_force">[(1, '=', 1)]</field>
            <field name="groups" eval="[(4, ref('group_quality_manager'))]"/>
        </record>
        <record id="rule_corrective_action_manager" model="ir.rule">
            <field name="name">Manager: todas las acciones correctivas</field>
            <field name="model_id" ref="model_quality_corrective_action"/>
            <field name="domain_force">[(1, '=', 1)]</field>
            <field name="groups" eval="[(4, ref('group_quality_manager'))]"/>
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
                <field name="process_type_id"/>
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
                        <group>
                            <field name="name"/>
                            <field name="process_type_id"/>
                            <field name="attribute_type"/>
                            <field name="is_required"/>
                        </group>
                        <group>
                            <field name="unit"/>
                            <field name="min_value" invisible="attribute_type != 'float'"/>
                            <field name="max_value" invisible="attribute_type != 'float'"/>
                            <field name="selection_options" invisible="attribute_type != 'selection'"/>
                        </group>
                    </group>
                </sheet>
            </form>
        </field>
    </record>

    <record id="action_quality_attribute_template" model="ir.actions.act_window">
        <field name="name">Plantillas de Atributos</field>
        <field name="res_model">quality.attribute.template</field>
        <field name="view_mode">list,form</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Crear una plantilla de atributo de calidad
            </p>
            <p>Configure los atributos de inspección por tipo de proceso.</p>
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
                    <button name="action_mark_sent" string="Marcar como Enviado"
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
                            <field name="product_id"/>
                            <field name="process_type_id"/>
                        </group>
                        <group>
                            <field name="folio"/>
                            <field name="lot_id"/>
                            <field name="date_generated"/>
                            <field name="certified_by"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Valores Certificados">
                            <group>
                                <group>
                                    <field name="certified_largo" invisible="certified_largo == 0"/>
                                    <field name="certified_ancho" invisible="certified_ancho == 0"/>
                                    <field name="certified_espesor" invisible="certified_espesor == 0"/>
                                    <field name="certified_hexagono" invisible="certified_hexagono == 0"/>
                                    <field name="certified_resistencia" invisible="certified_resistencia == 0"/>
                                </group>
                                <group>
                                    <field name="certified_apariencia" invisible="not certified_apariencia"/>
                                    <field name="certified_humedad" invisible="certified_humedad == 0"/>
                                    <field name="certified_pegado" invisible="not certified_pegado"/>
                                    <field name="certified_retiramiento" invisible="certified_retiramiento == 0"/>
                                    <field name="certified_calibracion" invisible="certified_calibracion == 0"/>
                                    <field name="certified_engomado" invisible="not certified_engomado"/>
                                </group>
                            </group>
                        </page>
                        <page string="Atributos Seleccionados">
                            <field name="attribute_ids">
                                <list>
                                    <field name="name"/>
                                    <field name="value_float"/>
                                    <field name="value_char"/>
                                    <field name="result"/>
                                </list>
                            </field>
                        </page>
                        <page string="PDF Generado" invisible="not report_pdf">
                            <group>
                                <field name="report_pdf" filename="report_pdf_name"/>
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
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Los certificados se generan desde inspecciones aceptadas
            </p>
        </field>
    </record>
</odoo>
```

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
                <field name="responsible_id"/>
                <field name="date_opened"/>
                <field name="action_count"/>
                <field name="action_completed_count"/>
                <field name="action_overdue_count" decoration-danger="action_overdue_count > 0"/>
                <field name="progress" widget="progressbar"/>
                <field name="state" widget="badge"
                       decoration-success="state == 'cerrada'"
                       decoration-info="state in ('abierta', 'en_proceso')"
                       decoration-muted="state == 'no_procede'"/>
            </list>
        </field>
    </record>

    <!-- Formulario separado para quality.action.line para ver evidencia inline -->
    <record id="view_quality_action_line_form" model="ir.ui.view">
        <field name="name">quality.action.line.form</field>
        <field name="model">quality.action.line</field>
        <field name="arch" type="xml">
            <form string="Detalle de Acción">
                <group>
                    <group>
                        <field name="description"/>
                        <field name="responsible_id"/>
                        <field name="state" widget="badge"
                               decoration-success="state == 'completada'"
                               decoration-danger="state == 'vencida'"
                               decoration-info="state == 'en_proceso'"/>
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
            <form string="Acción Correctiva/Preventiva">
                <header>
                    <button name="action_open" string="Abrir"
                            type="object" class="btn-primary"
                            invisible="state != 'borrador'"
                            groups="quality_management.group_quality_manager"/>
                    <button name="action_in_progress" string="En Proceso"
                            type="object"
                            invisible="state != 'abierta'"/>
                    <button name="action_close" string="Cerrar"
                            type="object" class="btn-primary"
                            invisible="state not in ('abierta', 'en_proceso')"
                            groups="quality_management.group_quality_manager"/>
                    <button name="action_no_proceed" string="No Procede"
                            type="object" class="btn-secondary"
                            invisible="state != 'borrador'"
                            groups="quality_management.group_quality_manager"/>
                    <button name="action_reopen" string="Reabrir"
                            type="object"
                            invisible="state not in ('cerrada', 'no_procede')"
                            groups="quality_management.group_quality_manager"/>
                    <button name="action_print_8d" string="Imprimir 8D"
                            type="object" class="btn-secondary" icon="fa-print"/>
                    <field name="state" widget="statusbar"
                           statusbar_visible="borrador,abierta,en_proceso,cerrada"/>
                </header>
                <sheet>
                    <div class="oe_title">
                        <h1><field name="name" readonly="1"/></h1>
                    </div>
                    <group>
                        <group>
                            <field name="origin_type"/>
                            <field name="origin_inspection_id"
                                   invisible="origin_type != 'inspeccion'"/>
                            <field name="origin_return_id"
                                   invisible="origin_type != 'devolucion'"/>
                            <field name="responsible_id"/>
                        </group>
                        <group>
                            <field name="date_opened"/>
                            <field name="date_closed"/>
                            <field name="progress" widget="progressbar"/>
                        </group>
                    </group>
                    <separator string="Descripción del Incumplimiento"/>
                    <field name="origin_description"/>
                    <notebook>
                        <page string="Acciones" name="actions">
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
                                <i class="fa fa-info-circle"/> Para ver la evidencia con vista previa (imágenes, videos, PDFs), abra cada línea de acción en modo formulario.
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
                <filter string="Abiertas" name="open"
                        domain="[('state', 'in', ('abierta', 'en_proceso'))]"/>
                <filter string="Con Acciones Vencidas" name="overdue"
                        domain="[('action_line_ids.state', '=', 'vencida')]"/>
                <filter string="Cerradas" name="closed"
                        domain="[('state', '=', 'cerrada')]"/>
                <group expand="0" string="Agrupar por">
                    <filter string="Tipo de Origen" name="group_origin" context="{'group_by': 'origin_type'}"/>
                    <filter string="Responsable" name="group_resp" context="{'group_by': 'responsible_id'}"/>
                    <filter string="Estado" name="group_state" context="{'group_by': 'state'}"/>
                </group>
            </search>
        </field>
    </record>

    <record id="action_quality_corrective_action" model="ir.actions.act_window">
        <field name="name">Acciones Correctivas/Preventivas</field>
        <field name="res_model">quality.corrective.action</field>
        <field name="view_mode">list,form</field>
        <field name="context">{'search_default_open': 1}</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Crear una acción correctiva o preventiva
            </p>
        </field>
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
                <field name="requires_dimensions"/>
                <field name="requested_by"/>
                <field name="responsible_id"/>
                <field name="date_requested"/>
                <field name="date_due"/>
                <field name="state" widget="badge"
                       decoration-success="state == 'enviado'"
                       decoration-info="state in ('en_proceso', 'completado')"/>
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
                    <button name="action_print_customer_document" string="Imprimir"
                            type="object" class="btn-secondary" icon="fa-print"/>
                    <field name="state" widget="statusbar"
                           statusbar_visible="borrador,en_proceso,completado,enviado"/>
                </header>
                <sheet>
                    <div class="oe_title">
                        <h1><field name="name" readonly="1"/></h1>
                    </div>
                    <group>
                        <group>
                            <field name="partner_id"/>
                            <field name="document_type"/>
                            <field name="requires_dimensions"/>
                            <field name="requested_by"/>
                        </group>
                        <group>
                            <field name="responsible_id"/>
                            <field name="date_requested"/>
                            <field name="date_due"/>
                            <field name="date_completed"/>
                        </group>
                    </group>
                    <field name="description" placeholder="Descripción adicional del requerimiento..."/>
                    <notebook>
                        <page string="Documento Principal PDF">
                            <group>
                                <field name="main_pdf" filename="main_pdf_name"/>
                                <field name="main_pdf_name" invisible="1"/>
                            </group>
                            <div invisible="not main_pdf" class="o_quality_pdf_preview">
                                <field name="main_pdf" widget="pdf_viewer" readonly="1"/>
                            </div>
                        </page>
                        <page string="Formatos del Cliente">
                            <field name="client_format_ids" widget="many2many_binary"/>
                        </page>
                        <page string="Documentos Generados">
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
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Registrar solicitud de documento de cliente
            </p>
        </field>
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
                  decoration-info="state in ('evaluacion_ventas', 'evaluacion_calidad')">
                <field name="name"/>
                <field name="partner_id"/>
                <field name="defect_type"/>
                <field name="defect_pieces"/>
                <field name="production_date"/>
                <field name="days_since_production"/>
                <field name="date_received"/>
                <field name="corrective_action_id" optional="show"/>
                <field name="state" widget="badge"
                       decoration-success="state == 'cerrada'"
                       decoration-danger="state == 'no_procede'"
                       decoration-info="state in ('evaluacion_ventas', 'evaluacion_calidad')"
                       decoration-warning="state == 'en_8d'"/>
            </list>
        </field>
    </record>

    <record id="view_quality_customer_return_form" model="ir.ui.view">
        <field name="name">quality.customer.return.form</field>
        <field name="model">quality.customer.return</field>
        <field name="arch" type="xml">
            <form string="Devolución de Cliente">
                <header>
                    <button name="action_submit_sales" string="Registrar / Evaluar"
                            type="object" class="btn-primary"
                            invisible="state != 'borrador'"/>
                    <button name="action_submit_quality" string="Enviar a Calidad"
                            type="object" class="btn-primary"
                            invisible="state != 'evaluacion_ventas'"/>
                    <button name="action_generate_8d" string="Generar 8D"
                            type="object" class="btn-primary"
                            invisible="state != 'evaluacion_calidad'"
                            groups="quality_management.group_quality_manager"/>
                    <button name="action_no_proceed" string="No Procede"
                            type="object" class="btn-secondary"
                            invisible="state not in ('evaluacion_ventas', 'evaluacion_calidad')"
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
                        <strong>⚠️ Fuera de periodo:</strong> La fecha de producción
                        tiene más de 30 días (<field name="days_since_production" nolabel="1"/> días).
                        Esta devolución podría no proceder.
                    </div>
                    <group>
                        <group string="Datos del Cliente">
                            <field name="partner_id"/>
                            <field name="sale_order_id"/>
                            <field name="date_received"/>
                            <field name="production_date"/>
                            <field name="days_since_production"/>
                            <field name="is_within_period" invisible="1"/>
                        </group>
                        <group string="Detalle del Defecto">
                            <field name="defect_type"/>
                            <field name="defect_pieces"/>
                            <field name="affects_functionality"/>
                        </group>
                    </group>
                    <separator string="Motivo de la Devolución"/>
                    <field name="return_reason"/>
                    <notebook>
                        <page string="Evidencia">
                            <group string="Adjuntar Evidencia (imágenes, videos, PDFs)">
                                <field name="evidence_ids" widget="many2many_binary" nolabel="1"/>
                            </group>
                            <separator string="Vista Previa de Evidencia"/>
                            <field name="evidence_ids" widget="evidence_viewer" nolabel="1"/>
                        </page>
                        <page string="Evidencia PDF">
                            <group>
                                <field name="evidence_pdf" filename="evidence_pdf_name"/>
                                <field name="evidence_pdf_name" invisible="1"/>
                            </group>
                            <div invisible="not evidence_pdf" class="o_quality_pdf_preview">
                                <field name="evidence_pdf" widget="pdf_viewer" readonly="1"/>
                            </div>
                        </page>
                        <page string="Tarimas">
                            <group>
                                <field name="pallets_returned"/>
                                <field name="pallet_return_date"
                                       invisible="not pallets_returned"/>
                            </group>
                        </page>
                        <page string="Formato de Reclamación">
                            <group>
                                <field name="claim_format_id"/>
                            </group>
                        </page>
                        <page string="8D" invisible="not corrective_action_id">
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
                        domain="[('state', 'not in', ('cerrada', 'no_procede'))]"/>
                <filter string="En 8D" name="in_8d"
                        domain="[('state', '=', 'en_8d')]"/>
                <group expand="0" string="Agrupar por">
                    <filter string="Cliente" name="group_partner" context="{'group_by': 'partner_id'}"/>
                    <filter string="Tipo de Defecto" name="group_defect" context="{'group_by': 'defect_type'}"/>
                    <filter string="Estado" name="group_state" context="{'group_by': 'state'}"/>
                </group>
            </search>
        </field>
    </record>

    <record id="action_quality_customer_return" model="ir.actions.act_window">
        <field name="name">Devoluciones de Clientes</field>
        <field name="res_model">quality.customer.return</field>
        <field name="view_mode">list,form</field>
        <field name="context">{'search_default_open': 1}</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Registrar una devolución de cliente
            </p>
        </field>
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
            <list decoration-success="state == 'aceptado'"
                  decoration-danger="state == 'rechazado'"
                  decoration-info="state == 'en_revision'">
                <field name="name"/>
                <field name="partner_id"/>
                <field name="sale_order_id" optional="show"/>
                <field name="requested_by"/>
                <field name="inspector_id"/>
                <field name="date_requested"/>
                <field name="state" widget="badge"
                       decoration-success="state == 'aceptado'"
                       decoration-danger="state == 'rechazado'"
                       decoration-info="state == 'en_revision'"/>
            </list>
        </field>
    </record>

    <record id="view_quality_drawing_release_form" model="ir.ui.view">
        <field name="name">quality.drawing.release.form</field>
        <field name="model">quality.drawing.release</field>
        <field name="arch" type="xml">
            <form string="Liberación de Plano">
                <header>
                    <button name="action_submit_review" string="Enviar a Revisión"
                            type="object" class="btn-primary"
                            invisible="state != 'borrador'"/>
                    <button name="action_accept" string="Liberar"
                            type="object" class="btn-primary"
                            invisible="state != 'en_revision'"
                            groups="quality_management.group_quality_inspector"/>
                    <button name="action_reject" string="Rechazar"
                            type="object" class="btn-danger"
                            invisible="state != 'en_revision'"
                            groups="quality_management.group_quality_inspector"/>
                    <button name="action_print_drawing_release" string="Imprimir"
                            type="object" class="btn-secondary" icon="fa-print"/>
                    <button name="action_reset_draft" string="Regresar a Borrador"
                            type="object"
                            invisible="state not in ('rechazado',)"
                            groups="quality_management.group_quality_manager"/>
                    <field name="state" widget="statusbar"
                           statusbar_visible="borrador,en_revision,aceptado"/>
                </header>
                <sheet>
                    <div class="oe_title">
                        <h1><field name="name" readonly="1"/></h1>
                    </div>
                    <group>
                        <group>
                            <field name="partner_id"/>
                            <field name="sale_order_id"/>
                            <field name="requested_by"/>
                        </group>
                        <group>
                            <field name="inspector_id"/>
                            <field name="date_requested"/>
                            <field name="date_released"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Plano PDF">
                            <group>
                                <field name="drawing_pdf" filename="drawing_pdf_name"/>
                                <field name="drawing_pdf_name" invisible="1"/>
                            </group>
                            <div invisible="not drawing_pdf" class="o_quality_pdf_preview">
                                <field name="drawing_pdf" widget="pdf_viewer" readonly="1"/>
                            </div>
                        </page>
                        <page string="Documentos Adjuntos">
                            <field name="drawing_attachment_ids" widget="many2many_binary"/>
                        </page>
                        <page string="Rechazo" invisible="state != 'rechazado'">
                            <field name="rejection_reason" placeholder="Motivo de rechazo..."/>
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
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Crear solicitud de liberación de plano
            </p>
        </field>
    </record>
</odoo>
```

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
                  decoration-danger="state in ('rechazado', 'retenido')"
                  decoration-info="state == 'en_proceso'">
                <field name="name"/>
                <field name="process_type_id"/>
                <field name="product_id"/>
                <field name="partner_id"/>
                <field name="folio"/>
                <field name="shift"/>
                <field name="inspector_id"/>
                <field name="date_inspection"/>
                <field name="is_pp" optional="show"/>
                <field name="is_pt" optional="show"/>
                <field name="state" widget="badge"
                       decoration-success="state == 'aceptado'"
                       decoration-danger="state in ('rechazado', 'retenido')"
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
                    <button name="action_start" string="Iniciar Inspección"
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
                            invisible="state not in ('rechazado', 'retenido')"
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
                    <!-- Campos booleanos de visibilidad (hidden) -->
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

                    <group>
                        <group string="Datos Generales">
                            <field name="process_type_id"/>
                            <field name="product_id"/>
                            <field name="production_order_id"/>
                            <field name="lot_id"/>
                            <field name="folio"/>
                            <field name="code"/>
                        </group>
                        <group string="Personal y Ubicación">
                            <field name="operator_id"/>
                            <field name="supervisor_id"/>
                            <field name="inspector_id"/>
                            <field name="partner_id"/>
                            <field name="shift"/>
                            <field name="plant"/>
                            <field name="date_inspection"/>
                        </group>
                    </group>
                    <group>
                        <group>
                            <field name="is_pp"/>
                        </group>
                        <group>
                            <field name="is_pt"/>
                        </group>
                    </group>
                    <notebook>
                        <!-- Medidas dinámicas -->
                        <page string="Medidas y Propiedades"
                              invisible="not show_largo and not show_ancho and not show_espesor and not show_hexagono and not show_resistencia and not show_apariencia and not show_humedad and not show_pegado and not show_retiramiento and not show_calibracion and not show_engomado">
                            <group>
                                <group string="Medidas Dimensionales">
                                    <field name="largo" invisible="not show_largo"/>
                                    <field name="ancho" invisible="not show_ancho"/>
                                    <field name="espesor" invisible="not show_espesor"/>
                                    <field name="hexagono" invisible="not show_hexagono"/>
                                </group>
                                <group string="Propiedades">
                                    <field name="resistencia" invisible="not show_resistencia"/>
                                    <field name="apariencia" invisible="not show_apariencia"/>
                                    <field name="humedad_pct" invisible="not show_humedad"/>
                                    <field name="pegado_result" invisible="not show_pegado"/>
                                    <field name="oct_retiramiento" invisible="not show_retiramiento"/>
                                    <field name="calibracion" invisible="not show_calibracion"/>
                                    <field name="engomado" invisible="not show_engomado"/>
                                </group>
                            </group>
                        </page>
                        <!-- Ranurado -->
                        <page string="Ranurado" invisible="not show_ranurado">
                            <field name="ranurado_ids">
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
                        <!-- Troquelado -->
                        <page string="Troquelado" invisible="not show_troquelado">
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
                        <!-- Datos de Producción (papel, adhesivo, etc) -->
                        <page string="Datos de Producción"
                              invisible="not show_papel and not show_adhesivo and not show_tipo_hexagono and not show_numero_corrida and not show_corte_guillotina">
                            <group>
                                <group string="Producción" invisible="not show_numero_corrida and not show_tipo_hexagono and not show_corte_guillotina">
                                    <field name="numero_corrida" invisible="not show_numero_corrida"/>
                                    <field name="tipo_hexagono" invisible="not show_tipo_hexagono"/>
                                    <field name="corte_guillotina" invisible="not show_corte_guillotina"/>
                                </group>
                                <group string="Papel" invisible="not show_papel">
                                    <field name="papel_ancho"/>
                                    <field name="papel_gramaje"/>
                                    <field name="papel_proveedor_id"/>
                                </group>
                            </group>
                            <group invisible="not show_adhesivo">
                                <group string="Adhesivo">
                                    <field name="adhesivo_lote1"/>
                                    <field name="adhesivo_lote2"/>
                                </group>
                            </group>
                        </page>
                        <!-- Atributos adicionales -->
                        <page string="Atributos Adicionales">
                            <field name="line_ids">
                                <list editable="bottom">
                                    <field name="sequence" widget="handle"/>
                                    <field name="name"/>
                                    <field name="attribute_type"/>
                                    <field name="value_float" invisible="attribute_type != 'float'"/>
                                    <field name="value_char" invisible="attribute_type not in ('char', 'selection')"/>
                                    <field name="value_boolean" invisible="attribute_type != 'boolean'" widget="boolean_toggle"/>
                                    <field name="min_value" invisible="attribute_type != 'float'"/>
                                    <field name="max_value" invisible="attribute_type != 'float'"/>
                                    <field name="unit"/>
                                    <field name="result" widget="badge"
                                           decoration-success="result == 'cumple'"
                                           decoration-danger="result == 'no_cumple'"/>
                                    <field name="notes"/>
                                </list>
                            </field>
                        </page>
                        <!-- Evidencia PDF -->
                        <page string="Evidencia PDF">
                            <group>
                                <field name="evidence_pdf" filename="evidence_pdf_name"/>
                                <field name="evidence_pdf_name" invisible="1"/>
                            </group>
                            <div invisible="not evidence_pdf" class="o_quality_pdf_preview">
                                <field name="evidence_pdf" widget="pdf_viewer" readonly="1"/>
                            </div>
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

    <record id="view_quality_inspection_search" model="ir.ui.view">
        <field name="name">quality.inspection.search</field>
        <field name="model">quality.inspection</field>
        <field name="arch" type="xml">
            <search string="Inspecciones">
                <field name="name"/>
                <field name="product_id"/>
                <field name="partner_id"/>
                <field name="folio"/>
                <field name="inspector_id"/>
                <field name="process_type_id"/>
                <filter string="Hoy" name="today"
                        domain="[('date_inspection', '&gt;=', datetime.datetime.combine(context_today(), datetime.time(0,0,0))),
                                 ('date_inspection', '&lt;=', datetime.datetime.combine(context_today(), datetime.time(23,59,59)))]"/>
                <separator/>
                <filter string="Aceptadas" name="accepted" domain="[('state', '=', 'aceptado')]"/>
                <filter string="Retenidas" name="retained" domain="[('state', '=', 'retenido')]"/>
                <filter string="Rechazadas" name="rejected" domain="[('state', '=', 'rechazado')]"/>
                <group expand="0" string="Agrupar por">
                    <filter string="Tipo de Proceso" name="group_type" context="{'group_by': 'process_type_id'}"/>
                    <filter string="Turno" name="group_shift" context="{'group_by': 'shift'}"/>
                    <filter string="Planta" name="group_plant" context="{'group_by': 'plant'}"/>
                    <filter string="Inspector" name="group_inspector" context="{'group_by': 'inspector_id'}"/>
                    <filter string="Operador" name="group_operator" context="{'group_by': 'operator_id'}"/>
                    <filter string="Estado" name="group_state" context="{'group_by': 'state'}"/>
                    <filter string="Fecha" name="group_date" context="{'group_by': 'date_inspection:day'}"/>
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
                <field name="shift" type="row"/>
            </pivot>
        </field>
    </record>

    <record id="action_quality_inspection" model="ir.actions.act_window">
        <field name="name">Inspecciones</field>
        <field name="res_model">quality.inspection</field>
        <field name="view_mode">list,form,pivot</field>
        <field name="context">{'search_default_today': 1}</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Crear una nueva inspección de calidad
            </p>
            <p>Capture los datos de inspección de PP y PT.</p>
        </field>
    </record>
</odoo>
```

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

    <menuitem id="menu_quality_certificate"
              name="Certificados"
              parent="menu_quality_root"
              action="action_quality_certificate"
              sequence="30"
              groups="group_quality_manager"/>

    <menuitem id="menu_quality_corrective_action"
              name="Acciones Correctivas"
              parent="menu_quality_root"
              action="action_quality_corrective_action"
              sequence="40"
              groups="group_quality_manager"/>

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

    <!-- Configuración -->
    <menuitem id="menu_quality_config"
              name="Configuración"
              parent="menu_quality_root"
              sequence="100"
              groups="group_quality_admin"/>

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
</odoo>
```

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
                <field name="product_id"/>
                <field name="project_task_id"/>
                <field name="requested_by"/>
                <field name="inspector_id"/>
                <field name="date_requested"/>
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
                    <button name="action_submit_inspection" string="Enviar a Inspección"
                            type="object" class="btn-primary"
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
                        <group>
                            <field name="project_task_id"/>
                            <field name="product_id"/>
                            <field name="requested_by"/>
                        </group>
                        <group>
                            <field name="inspector_id"/>
                            <field name="date_requested"/>
                            <field name="date_inspected"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Atributos de Inspección">
                            <field name="inspection_line_ids">
                                <list editable="bottom">
                                    <field name="sequence" widget="handle"/>
                                    <field name="name"/>
                                    <field name="attribute_type"/>
                                    <field name="value_float" invisible="attribute_type != 'float'"/>
                                    <field name="value_char" invisible="attribute_type not in ('char', 'selection')"/>
                                    <field name="value_boolean" invisible="attribute_type != 'boolean'"/>
                                    <field name="min_value" invisible="attribute_type != 'float'"/>
                                    <field name="max_value" invisible="attribute_type != 'float'"/>
                                    <field name="unit"/>
                                    <field name="result" widget="badge"
                                           decoration-success="result == 'cumple'"
                                           decoration-danger="result == 'no_cumple'"/>
                                </list>
                            </field>
                        </page>
                        <page string="Especificación PDF">
                            <group>
                                <field name="spec_pdf" filename="spec_pdf_name"/>
                                <field name="spec_pdf_name" invisible="1"/>
                            </group>
                            <div invisible="not spec_pdf" class="o_quality_pdf_preview">
                                <field name="spec_pdf" widget="pdf_viewer" readonly="1"/>
                            </div>
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

    <record id="view_quality_sample_release_kanban" model="ir.ui.view">
        <field name="name">quality.sample.release.kanban</field>
        <field name="model">quality.sample.release</field>
        <field name="arch" type="xml">
            <kanban default_group_by="state" class="o_kanban_small_column">
                <field name="name"/>
                <field name="product_id"/>
                <field name="state"/>
                <field name="requested_by"/>
                <templates>
                    <t t-name="card">
                        <field name="name" class="fw-bold"/>
                        <field name="product_id"/>
                        <field name="requested_by"/>
                        <field name="date_requested"/>
                    </t>
                </templates>
            </kanban>
        </field>
    </record>

    <record id="action_quality_sample_release" model="ir.actions.act_window">
        <field name="name">Liberación de Muestras</field>
        <field name="res_model">quality.sample.release</field>
        <field name="view_mode">list,form,kanban</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Crear solicitud de liberación de muestra
            </p>
        </field>
    </record>
</odoo>
```

## ./wizards/__init__.py
```py
from . import certificate_wizard
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
            vals['certified_hexagono'] = insp.hexagono or insp.oct_hexagono
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
        if self.include_retiramiento and insp.oct_retiramiento:
            vals['certified_retiramiento'] = insp.oct_retiramiento
        if self.include_calibracion and insp.calibracion:
            vals['certified_calibracion'] = insp.calibracion
        if self.include_engomado and insp.engomado:
            vals['certified_engomado'] = dict(
                insp._fields['engomado'].selection
            ).get(insp.engomado, '')

        cert = self.env['quality.certificate'].create(vals)

        # Vincular atributos adicionales si se solicitó
        if self.include_all_attributes and insp.line_ids:
            cert.attribute_ids = [(6, 0, insp.line_ids.ids)]

        return {
            'type': 'ir.actions.act_window',
            'name': _('Certificado'),
            'res_model': 'quality.certificate',
            'res_id': cert.id,
            'view_mode': 'form',
            'target': 'current',
        }
```

## ./__init__.py
```py
from . import models
from . import wizards
```

## ./__manifest__.py
```py
{
    'name': 'Gestión de Calidad - Hexágonos Mexicanos',
    'version': '18.0.2.1.0',
    'category': 'Manufacturing/Quality',
    'summary': 'Módulo integral de gestión de calidad para industria del cartón',
    'description': """
        Gestión de Calidad para Hexágonos Mexicanos
        =============================================
        - Tipos de Proceso configurables (no hardcoded)
        - Liberación de Muestras con reporte PDF
        - Liberación de Planos con visor PDF embebido
        - Inspección de PP y PT con atributos dinámicos
        - Generación de Certificados con reporte PDF
        - Acciones Correctivas/Preventivas (8D) con reporte
        - Devolución de Clientes con reporte PDF
        - Documentos solicitados por clientes con reporte PDF
        - Visor PDF embebido en formularios
        - Visor de evidencia inline (imágenes, videos, PDFs)
        - Integración con Ventas, Contactos y Manufactura (smart buttons)
    """,
    'author': 'Alphaqueb Consulting SAS',
    'website': 'https://alphaqueb.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'project',
        'mrp',
        'sale',
        'stock',
        'product',
        'contacts',
        'hr',
    ],
    'data': [
        # Security
        'security/quality_groups.xml',
        'security/ir.model.access.csv',
        'security/quality_rules.xml',
        # Data
        'data/sequence_data.xml',
        'data/process_type_data.xml',
        'data/cron_data.xml',
        # Wizards
        'wizards/certificate_wizard_views.xml',
        # Views
        'views/quality_process_type_views.xml',
        'views/quality_attribute_template_views.xml',
        'views/quality_sample_release_views.xml',
        'views/quality_drawing_release_views.xml',
        'views/quality_inspection_views.xml',
        'views/quality_certificate_views.xml',
        'views/quality_corrective_action_views.xml',
        'views/quality_customer_return_views.xml',
        'views/quality_customer_document_views.xml',
        'views/quality_dashboard_views.xml',
        # Inherited views (integration with sale, contacts, mrp)
        'views/quality_inherited_views.xml',
        # Menus (AFTER views)
        'views/quality_menus.xml',
        # Reports
        'reports/report_quality_certificate.xml',
        'reports/report_8d.xml',
        'reports/report_inspection_summary.xml',
        'reports/report_sample_release.xml',
        'reports/report_drawing_release.xml',
        'reports/report_customer_return.xml',
        'reports/report_customer_document.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'quality_management/static/src/css/quality_pdf_viewer.css',
            'quality_management/static/src/css/quality_evidence_viewer.css',
            'quality_management/static/src/js/evidence_viewer_widget.js',
            'quality_management/static/src/xml/evidence_viewer_widget.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
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
        <!-- Laminadora y Remanejo -->
        <record id="process_type_laminadora" model="quality.process.type">
            <field name="name">Laminadora y Remanejo</field>
            <field name="code">laminadora_remanejo</field>
            <field name="sequence">10</field>
            <field name="show_largo" eval="True"/>
            <field name="show_ancho" eval="True"/>
            <field name="show_espesor" eval="True"/>
            <field name="show_hexagono" eval="True"/>
            <field name="show_resistencia" eval="True"/>
            <field name="show_apariencia" eval="True"/>
            <field name="show_humedad" eval="True"/>
            <field name="show_pegado" eval="True"/>
            <field name="show_ranurado" eval="True"/>
            <field name="show_troquelado" eval="True"/>
            <field name="description">Proceso de laminado y remanejo de cartón. Incluye mediciones dimensionales, ranurado y troquelado.</field>
        </record>

        <!-- Octágono -->
        <record id="process_type_octagono" model="quality.process.type">
            <field name="name">Octágono</field>
            <field name="code">octagono</field>
            <field name="sequence">20</field>
            <field name="show_ancho" eval="True"/>
            <field name="show_espesor" eval="True"/>
            <field name="show_hexagono" eval="True"/>
            <field name="show_retiramiento" eval="True"/>
            <field name="show_pegado" eval="True"/>
            <field name="description">Proceso de formado octagonal. Mediciones de ancho, espesor, hexágono, retiramiento y pegado.</field>
        </record>

        <!-- Guillotina y Pegado -->
        <record id="process_type_guillotina" model="quality.process.type">
            <field name="name">Guillotina y Pegado</field>
            <field name="code">guillotina_pegado</field>
            <field name="sequence">30</field>
            <field name="show_calibracion" eval="True"/>
            <field name="show_engomado" eval="True"/>
            <field name="show_papel" eval="True"/>
            <field name="show_adhesivo" eval="True"/>
            <field name="show_tipo_hexagono" eval="True"/>
            <field name="show_corte_guillotina" eval="True"/>
            <field name="show_numero_corrida" eval="True"/>
            <field name="description">Proceso de corte en guillotina y pegado. Incluye datos de papel, adhesivo, calibración y engomado.</field>
        </record>

        <!-- Ejemplos de nuevos procesos que el usuario puede agregar -->
        <record id="process_type_impresion" model="quality.process.type">
            <field name="name">Impresión</field>
            <field name="code">impresion</field>
            <field name="sequence">40</field>
            <field name="show_apariencia" eval="True"/>
            <field name="show_humedad" eval="True"/>
            <field name="description">Proceso de impresión sobre cartón. Inspección visual de apariencia y humedad.</field>
        </record>

        <record id="process_type_troquelado_plano" model="quality.process.type">
            <field name="name">Troquelado Plano</field>
            <field name="code">troquelado_plano</field>
            <field name="sequence">50</field>
            <field name="show_largo" eval="True"/>
            <field name="show_ancho" eval="True"/>
            <field name="show_espesor" eval="True"/>
            <field name="show_troquelado" eval="True"/>
            <field name="show_apariencia" eval="True"/>
            <field name="description">Proceso de troquelado plano. Mediciones dimensionales y capturas de troquelado.</field>
        </record>

        <record id="process_type_acabado" model="quality.process.type">
            <field name="name">Acabado y Empaque</field>
            <field name="code">acabado_empaque</field>
            <field name="sequence">60</field>
            <field name="show_apariencia" eval="True"/>
            <field name="show_largo" eval="True"/>
            <field name="show_ancho" eval="True"/>
            <field name="description">Inspección final de acabado y empaque antes de envío al cliente.</field>
        </record>
    </data>
</odoo>
```

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
from . import quality_attribute_template
from . import quality_sample_release
from . import quality_drawing_release
from . import quality_inspection
from . import quality_inspection_line
from . import quality_inspection_ranurado
from . import quality_inspection_troquelado
from . import quality_certificate
from . import quality_corrective_action
from . import quality_action_line
from . import quality_customer_return
from . import quality_customer_document
from . import quality_inherited_models```

## ./models/quality_action_line.py
```py
from odoo import models, fields, api


class QualityActionLine(models.Model):
    _name = 'quality.action.line'
    _description = 'Línea de Acción Correctiva'
    _order = 'date_due, id'

    corrective_id = fields.Many2one(
        'quality.corrective.action', 'Acción Correctiva',
        required=True, ondelete='cascade'
    )
    description = fields.Text('Descripción de la Acción', required=True)
    responsible_id = fields.Many2one(
        'res.users', 'Responsable', required=True
    )
    date_due = fields.Date('Fecha de Cumplimiento', required=True)
    date_completed = fields.Date('Fecha de Cumplimiento Real')
    evidence_ids = fields.Many2many(
        'ir.attachment', 'quality_action_evidence_rel',
        'action_line_id', 'attachment_id',
        string='Evidencia'
    )
    state = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completada', 'Completada'),
        ('vencida', 'Vencida'),
    ], string='Estado', default='pendiente', required=True)
    delay_days = fields.Integer(
        'Días de Atraso', compute='_compute_delay_days', store=True
    )
    notes = fields.Text('Notas')

    @api.depends('date_due', 'state')
    def _compute_delay_days(self):
        today = fields.Date.today()
        for line in self:
            if line.date_due and line.state in ('pendiente', 'en_proceso', 'vencida'):
                delta = (today - line.date_due).days
                line.delay_days = max(0, delta)
            else:
                line.delay_days = 0

    def action_start(self):
        for rec in self:
            rec.state = 'en_proceso'

    def action_complete(self):
        for rec in self:
            rec.state = 'completada'
            rec.date_completed = fields.Date.today()

    def action_reopen(self):
        for rec in self:
            rec.state = 'en_proceso'
            rec.date_completed = False
```

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
        ('boolean', 'Sí/No'),
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
```

## ./models/quality_certificate.py
```py
from odoo import models, fields, api, _


class QualityCertificate(models.Model):
    _name = 'quality.certificate'
    _description = 'Certificado de Calidad'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_generated desc, id desc'

    name = fields.Char(
        'Referencia', required=True, readonly=True,
        default='Nuevo', copy=False
    )
    inspection_id = fields.Many2one(
        'quality.inspection', 'Inspección Fuente',
        required=True, tracking=True,
        domain=[('state', '=', 'aceptado')]
    )
    partner_id = fields.Many2one(
        'res.partner', 'Cliente', required=True, tracking=True
    )
    product_id = fields.Many2one(
        related='inspection_id.product_id', string='Producto', store=True
    )
    process_type_id = fields.Many2one(
        related='inspection_id.process_type_id',
        string='Tipo de Proceso', store=True
    )
    # Legacy
    inspection_type = fields.Selection(
        related='inspection_id.inspection_type',
        string='Tipo (Legacy)', store=True
    )
    attribute_ids = fields.Many2many(
        'quality.inspection.line',
        'quality_certificate_attribute_rel',
        'certificate_id', 'line_id',
        string='Atributos del Certificado'
    )
    # Snapshot de valores
    certified_largo = fields.Float('Largo (mm)')
    certified_ancho = fields.Float('Ancho (mm)')
    certified_espesor = fields.Float('Espesor (mm)')
    certified_hexagono = fields.Float('Hexágono')
    certified_resistencia = fields.Float('Resistencia')
    certified_apariencia = fields.Char('Apariencia')
    certified_humedad = fields.Float('% Humedad')
    certified_pegado = fields.Char('Pegado')
    certified_retiramiento = fields.Float('Retiramiento')
    certified_calibracion = fields.Float('Calibración')
    certified_engomado = fields.Char('Engomado')
    date_generated = fields.Date(
        'Fecha de Generación', required=True,
        default=fields.Date.context_today
    )
    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('generado', 'Generado'),
        ('enviado', 'Enviado'),
    ], string='Estado', default='borrador', required=True,
        tracking=True, copy=False)
    report_pdf = fields.Binary('PDF del Certificado', attachment=True)
    report_pdf_name = fields.Char('Nombre del PDF')
    certified_by = fields.Many2one(
        'res.users', 'Certificado por',
        required=True, default=lambda self: self.env.user,
        tracking=True
    )
    company_id = fields.Many2one(
        'res.company', 'Compañía',
        default=lambda self: self.env.company
    )
    folio = fields.Char(
        related='inspection_id.folio', string='Folio', store=True
    )
    lot_id = fields.Many2one(
        related='inspection_id.lot_id', string='Lote', store=True
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'quality.certificate') or 'Nuevo'
        return super().create(vals_list)

    def action_generate(self):
        for rec in self:
            rec.state = 'generado'
            rec.message_post(
                body=_('Certificado generado por %s') % self.env.user.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_send_email(self):
        self.ensure_one()
        template = self.env.ref(
            'quality_management.email_template_quality_certificate',
            raise_if_not_found=False
        )
        compose_form = self.env.ref('mail.email_compose_message_wizard_form')
        ctx = {
            'default_model': 'quality.certificate',
            'default_res_ids': self.ids,
            'default_template_id': template.id if template else False,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }

    def action_mark_sent(self):
        for rec in self:
            rec.state = 'enviado'
            rec.message_post(
                body=_('Certificado enviado al cliente %s') % rec.partner_id.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_print_certificate(self):
        return self.env.ref(
            'quality_management.action_report_quality_certificate'
        ).report_action(self)
```

## ./models/quality_corrective_action.py
```py
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import timedelta


class QualityCorrectiveAction(models.Model):
    _name = 'quality.corrective.action'
    _description = 'Acción Correctiva/Preventiva'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_opened desc, id desc'

    name = fields.Char(
        'Referencia', required=True, readonly=True,
        default='Nuevo', copy=False
    )
    origin_type = fields.Selection([
        ('inspeccion', 'Inspección'),
        ('auditoria_interna', 'Auditoría Interna'),
        ('auditoria_externa', 'Auditoría Externa'),
        ('devolucion', 'Devolución'),
        ('otro', 'Otro'),
    ], string='Tipo de Origen', required=True, tracking=True)
    origin_description = fields.Text(
        'Descripción del Incumplimiento', required=True
    )
    origin_inspection_id = fields.Many2one(
        'quality.inspection', 'Inspección Origen'
    )
    origin_return_id = fields.Many2one(
        'quality.customer.return', 'Devolución Origen'
    )
    responsible_id = fields.Many2one(
        'res.users', 'Responsable General',
        required=True, tracking=True
    )
    action_line_ids = fields.One2many(
        'quality.action.line', 'corrective_id',
        string='Acciones Específicas'
    )
    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('abierta', 'Abierta'),
        ('en_proceso', 'En Proceso'),
        ('cerrada', 'Cerrada'),
        ('no_procede', 'No Procede'),
    ], string='Estado', default='borrador', required=True,
        tracking=True, copy=False)
    date_opened = fields.Date(
        'Fecha de Apertura', required=True,
        default=fields.Date.context_today
    )
    date_closed = fields.Date('Fecha de Cierre', tracking=True)
    action_count = fields.Integer(
        'Total de Acciones', compute='_compute_action_stats'
    )
    action_completed_count = fields.Integer(
        'Acciones Completadas', compute='_compute_action_stats'
    )
    action_overdue_count = fields.Integer(
        'Acciones Vencidas', compute='_compute_action_stats'
    )
    progress = fields.Float(
        'Progreso (%)', compute='_compute_action_stats'
    )
    company_id = fields.Many2one(
        'res.company', 'Compañía',
        default=lambda self: self.env.company
    )

    @api.depends('action_line_ids', 'action_line_ids.state')
    def _compute_action_stats(self):
        for rec in self:
            lines = rec.action_line_ids
            rec.action_count = len(lines)
            rec.action_completed_count = len(
                lines.filtered(lambda l: l.state == 'completada')
            )
            rec.action_overdue_count = len(
                lines.filtered(lambda l: l.state == 'vencida')
            )
            rec.progress = (
                (rec.action_completed_count / rec.action_count * 100)
                if rec.action_count else 0.0
            )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'quality.corrective.action') or 'Nuevo'
        return super().create(vals_list)

    def action_open(self):
        for rec in self:
            rec.state = 'abierta'
            rec.message_post(
                body=_('Acción correctiva abierta por %s') % self.env.user.name,
                subtype_xmlid='mail.mt_comment',
            )
            rec.activity_schedule(
                'mail.mail_activity_data_todo',
                date_deadline=fields.Date.today() + timedelta(days=1),
                summary=_('Acción correctiva asignada: %s') % rec.name,
                user_id=rec.responsible_id.id,
            )

    def action_in_progress(self):
        for rec in self:
            rec.state = 'en_proceso'

    def action_close(self):
        for rec in self:
            pending = rec.action_line_ids.filtered(
                lambda l: l.state not in ('completada',)
            )
            if pending:
                raise UserError(_(
                    'No se puede cerrar: hay %d acción(es) sin completar.'
                ) % len(pending))
            rec.state = 'cerrada'
            rec.date_closed = fields.Date.today()
            rec.activity_feedback(
                ['mail.mail_activity_data_todo'],
                feedback=_('Acción correctiva cerrada')
            )
            rec.message_post(
                body=_('✅ Acción correctiva CERRADA por %s') % self.env.user.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_no_proceed(self):
        for rec in self:
            rec.state = 'no_procede'
            rec.date_closed = fields.Date.today()
            rec.message_post(
                body=_('Acción correctiva marcada como NO PROCEDE por %s') % self.env.user.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_reopen(self):
        for rec in self:
            rec.state = 'en_proceso'
            rec.date_closed = False

    def action_print_8d(self):
        return self.env.ref(
            'quality_management.action_report_8d'
        ).report_action(self)

    @api.model
    def _cron_check_overdue_actions(self):
        today = fields.Date.today()
        overdue_lines = self.env['quality.action.line'].search([
            ('state', 'in', ('pendiente', 'en_proceso')),
            ('date_due', '<', today),
        ])
        for line in overdue_lines:
            line.state = 'vencida'
            days = (today - line.date_due).days
            line.delay_days = days
            line.corrective_id.message_post(
                body=_(
                    '⚠️ Acción vencida: "%s" - Responsable: %s - '
                    'Días de atraso: %d'
                ) % (line.description[:80], line.responsible_id.name, days),
                subtype_xmlid='mail.mt_comment',
            )
            line.corrective_id.activity_schedule(
                'mail.mail_activity_data_todo',
                date_deadline=today,
                summary=_(
                    'Acción vencida (%d días): %s'
                ) % (days, line.description[:50]),
                user_id=line.responsible_id.id,
            )
```

## ./models/quality_customer_document.py
```py
from odoo import models, fields, api, _
from datetime import timedelta


class QualityCustomerDocument(models.Model):
    _name = 'quality.customer.document'
    _description = 'Documento Solicitado por Cliente'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_requested desc, id desc'

    name = fields.Char(
        'Referencia', required=True, readonly=True,
        default='Nuevo', copy=False
    )
    partner_id = fields.Many2one(
        'res.partner', 'Cliente Solicitante',
        required=True, tracking=True
    )
    document_type = fields.Selection([
        ('rohs', 'RoHS'),
        ('psw', 'PSW'),
        ('ppap', 'PPAP'),
        ('apariencia', 'Apariencia'),
        ('pfmea', 'PFMEA'),
        ('diagrama_flujo', 'Diagrama de Flujo'),
        ('especificacion_empaque', 'Especificación de Empaque'),
        ('carta_garantia', 'Carta Garantía'),
        ('otro', 'Otro'),
    ], string='Tipo de Documento', required=True, tracking=True)
    description = fields.Text('Descripción Adicional')
    requires_dimensions = fields.Boolean(
        'Implica Mediciones Dimensionales', required=True, tracking=True
    )
    client_format_ids = fields.Many2many(
        'ir.attachment', 'quality_doc_client_format_rel',
        'document_id', 'attachment_id',
        string='Formatos del Cliente'
    )
    result_document_ids = fields.Many2many(
        'ir.attachment', 'quality_doc_result_rel',
        'document_id', 'attachment_id',
        string='Documentos Generados'
    )
    # PDF principal para preview embebido
    main_pdf = fields.Binary('Documento Principal (PDF)', attachment=True)
    main_pdf_name = fields.Char('Nombre del Documento')
    requested_by = fields.Many2one(
        'res.users', 'Solicitante (Ventas)',
        required=True, default=lambda self: self.env.user,
        tracking=True
    )
    responsible_id = fields.Many2one(
        'res.users', 'Responsable en Calidad',
        required=True, tracking=True
    )
    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
        ('enviado', 'Enviado'),
    ], string='Estado', default='borrador', required=True,
        tracking=True, copy=False)
    date_requested = fields.Date(
        'Fecha de Solicitud', required=True,
        default=fields.Date.context_today
    )
    date_due = fields.Date(
        'Fecha Límite', compute='_compute_date_due',
        store=True, readonly=False
    )
    date_completed = fields.Date('Fecha de Entrega Real')
    company_id = fields.Many2one(
        'res.company', 'Compañía',
        default=lambda self: self.env.company
    )

    @api.depends('date_requested', 'requires_dimensions')
    def _compute_date_due(self):
        for rec in self:
            if rec.date_requested:
                days = 7 if rec.requires_dimensions else 5
                rec.date_due = rec.date_requested + timedelta(days=days)
            else:
                rec.date_due = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'quality.customer.document') or 'Nuevo'
        return super().create(vals_list)

    def action_start(self):
        for rec in self:
            rec.state = 'en_proceso'
            rec.activity_schedule(
                'mail.mail_activity_data_todo',
                date_deadline=rec.date_due,
                summary=_('Generar documento de calidad: %s - %s') % (
                    rec.name,
                    dict(rec._fields['document_type'].selection).get(
                        rec.document_type, ''
                    ),
                ),
                user_id=rec.responsible_id.id,
            )

    def action_complete(self):
        for rec in self:
            rec.state = 'completado'
            rec.date_completed = fields.Date.today()
            rec.activity_feedback(
                ['mail.mail_activity_data_todo'],
                feedback=_('Documento completado')
            )
            rec.message_post(
                body=_(
                    '✅ Documento completado por Calidad. '
                    'Ventas: proceder a enviar al cliente %s.'
                ) % rec.partner_id.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_send(self):
        for rec in self:
            rec.state = 'enviado'
            rec.message_post(
                body=_('Documento enviado al cliente %s') % rec.partner_id.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_print_customer_document(self):
        return self.env.ref(
            'quality_management.action_report_customer_document'
        ).report_action(self)
```

## ./models/quality_customer_return.py
```py
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import timedelta


class QualityCustomerReturn(models.Model):
    _name = 'quality.customer.return'
    _description = 'Devolución de Cliente'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_received desc, id desc'

    name = fields.Char(
        'Referencia', required=True, readonly=True,
        default='Nuevo', copy=False
    )
    partner_id = fields.Many2one(
        'res.partner', 'Cliente', required=True, tracking=True
    )
    sale_order_id = fields.Many2one(
        'sale.order', 'Orden de Venta Original', tracking=True
    )
    defect_type = fields.Selection([
        ('dimensional', 'Dimensional'),
        ('apariencia', 'Apariencia'),
        ('funcional', 'Funcional'),
        ('empaque', 'Empaque'),
        ('otro', 'Otro'),
    ], string='Tipo de Defecto', required=True, tracking=True)
    defect_pieces = fields.Integer('Piezas con Defecto', required=True)
    return_reason = fields.Text('Motivo de la Devolución', required=True)
    production_date = fields.Date('Fecha de Producción', required=True)
    evidence_ids = fields.Many2many(
        'ir.attachment', 'quality_return_evidence_rel',
        'return_id', 'attachment_id',
        string='Evidencia Fotográfica', required=True
    )
    # PDF de evidencia con preview
    evidence_pdf = fields.Binary('Reporte de Evidencia (PDF)', attachment=True)
    evidence_pdf_name = fields.Char('Nombre del Reporte')
    pallets_returned = fields.Boolean('Se Regresan Tarimas')
    pallet_return_date = fields.Date('Fecha Retorno de Tarimas')
    claim_format_id = fields.Many2one(
        'ir.attachment', 'Formato de Reclamación'
    )
    affects_functionality = fields.Boolean(
        'Afecta Funcionalidad', tracking=True
    )
    corrective_action_id = fields.Many2one(
        'quality.corrective.action', '8D Generado',
        readonly=True, tracking=True
    )
    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('evaluacion_ventas', 'Evaluación Ventas'),
        ('evaluacion_calidad', 'Evaluación Calidad'),
        ('en_8d', 'En 8D'),
        ('cerrada', 'Cerrada'),
        ('no_procede', 'No Procede'),
    ], string='Estado', default='borrador', required=True,
        tracking=True, copy=False)
    date_received = fields.Date(
        'Fecha de Recepción', required=True,
        default=fields.Date.context_today
    )
    days_since_production = fields.Integer(
        'Días desde Producción',
        compute='_compute_days_since_production'
    )
    is_within_period = fields.Boolean(
        'Dentro de Periodo',
        compute='_compute_days_since_production'
    )
    company_id = fields.Many2one(
        'res.company', 'Compañía',
        default=lambda self: self.env.company
    )

    @api.depends('production_date', 'date_received')
    def _compute_days_since_production(self):
        for rec in self:
            if rec.production_date and rec.date_received:
                delta = (rec.date_received - rec.production_date).days
                rec.days_since_production = delta
                rec.is_within_period = delta < 30
            else:
                rec.days_since_production = 0
                rec.is_within_period = True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'quality.customer.return') or 'Nuevo'
        return super().create(vals_list)

    def action_submit_sales(self):
        for rec in self:
            if not rec.is_within_period:
                rec.state = 'no_procede'
                rec.message_post(
                    body=_(
                        'Devolución NO PROCEDE: fecha de producción mayor a '
                        '30 días (%d días).'
                    ) % rec.days_since_production,
                    subtype_xmlid='mail.mt_comment',
                )
                return
            rec.state = 'evaluacion_ventas'
            rec.message_post(
                body=_('Devolución registrada, en evaluación por Ventas.'),
                subtype_xmlid='mail.mt_comment',
            )

    def action_submit_quality(self):
        for rec in self:
            rec.state = 'evaluacion_calidad'
            quality_users = self.env.ref(
                'quality_management.group_quality_manager'
            ).users
            for user in quality_users:
                rec.activity_schedule(
                    'mail.mail_activity_data_todo',
                    date_deadline=fields.Date.today() + timedelta(days=3),
                    summary=_('Evaluar devolución: %s') % rec.name,
                    user_id=user.id,
                )
            rec.message_post(
                body=_('Devolución enviada a evaluación de Calidad.'),
                subtype_xmlid='mail.mt_comment',
            )
            if rec.pallets_returned:
                rec.message_post(
                    body=_(
                        '📦 Se retornaron tarimas a planta. '
                        'Logística/Producción: evaluar físicamente.'
                    ),
                    subtype_xmlid='mail.mt_comment',
                )

    def action_generate_8d(self):
        for rec in self:
            ca = self.env['quality.corrective.action'].create({
                'origin_type': 'devolucion',
                'origin_description': _(
                    'Devolución de cliente: %s\n'
                    'Tipo de defecto: %s\n'
                    'Piezas: %d\n'
                    'Motivo: %s'
                ) % (
                    rec.partner_id.name,
                    dict(rec._fields['defect_type'].selection).get(rec.defect_type, ''),
                    rec.defect_pieces,
                    rec.return_reason,
                ),
                'origin_return_id': rec.id,
                'responsible_id': self.env.user.id,
            })
            rec.corrective_action_id = ca.id
            rec.state = 'en_8d'
            rec.message_post(
                body=_('8D generado: %s') % ca.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_close(self):
        for rec in self:
            rec.state = 'cerrada'
            rec.message_post(
                body=_('Devolución cerrada por %s') % self.env.user.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_no_proceed(self):
        for rec in self:
            rec.state = 'no_procede'
            rec.message_post(
                body=_('Devolución marcada como NO PROCEDE.'),
                subtype_xmlid='mail.mt_comment',
            )

    def action_print_customer_return(self):
        return self.env.ref(
            'quality_management.action_report_customer_return'
        ).report_action(self)
```

## ./models/quality_drawing_release.py
```py
from odoo import models, fields, api, _
from datetime import timedelta


class QualityDrawingRelease(models.Model):
    _name = 'quality.drawing.release'
    _description = 'Liberación de Planos'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_requested desc, id desc'

    name = fields.Char(
        'Referencia', required=True, readonly=True,
        default='Nuevo', copy=False
    )
    partner_id = fields.Many2one(
        'res.partner', 'Cliente', required=True, tracking=True
    )
    sale_order_id = fields.Many2one(
        'sale.order', 'Orden de Venta', tracking=True
    )
    drawing_attachment_ids = fields.Many2many(
        'ir.attachment', 'quality_drawing_attachment_rel',
        'drawing_id', 'attachment_id',
        string='Plano y Cotización/Dibujo', required=True
    )
    # PDF principal para preview embebido
    drawing_pdf = fields.Binary('Plano Principal (PDF)', attachment=True)
    drawing_pdf_name = fields.Char('Nombre del Plano')
    requested_by = fields.Many2one(
        'res.users', 'Solicitante (Ventas)',
        required=True, default=lambda self: self.env.user,
        tracking=True
    )
    inspector_id = fields.Many2one(
        'res.users', 'Inspector de Calidad', tracking=True
    )
    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('en_revision', 'En Revisión'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
    ], string='Estado', default='borrador', required=True,
        tracking=True, copy=False)
    rejection_reason = fields.Text('Motivo de Rechazo')
    date_requested = fields.Date(
        'Fecha de Solicitud', required=True,
        default=fields.Date.context_today
    )
    date_released = fields.Date('Fecha de Liberación')
    company_id = fields.Many2one(
        'res.company', 'Compañía',
        default=lambda self: self.env.company
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'quality.drawing.release') or 'Nuevo'
        return super().create(vals_list)

    def action_submit_review(self):
        for rec in self:
            rec.state = 'en_revision'
            quality_users = self.env.ref(
                'quality_management.group_quality_inspector'
            ).users
            if rec.inspector_id:
                quality_users = rec.inspector_id
            for user in quality_users:
                rec.activity_schedule(
                    'mail.mail_activity_data_todo',
                    date_deadline=fields.Date.today() + timedelta(days=3),
                    summary=_('Revisión de plano: %s') % rec.name,
                    user_id=user.id,
                )
            rec.message_post(
                body=_('Solicitud de revisión de plano enviada por %s') % rec.requested_by.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_accept(self):
        for rec in self:
            rec.state = 'aceptado'
            rec.date_released = fields.Date.today()
            rec.activity_feedback(
                ['mail.mail_activity_data_todo'],
                feedback=_('Plano liberado')
            )
            rec.message_post(
                body=_('✅ Plano LIBERADO por %s') % self.env.user.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_reject(self):
        for rec in self:
            if not rec.rejection_reason:
                raise models.ValidationError(
                    _('Debe capturar el motivo de rechazo.')
                )
            rec.state = 'rechazado'
            rec.activity_feedback(
                ['mail.mail_activity_data_todo'],
                feedback=_('Plano rechazado: %s') % rec.rejection_reason
            )
            rec.message_post(
                body=_('❌ Plano RECHAZADO por %s.\nMotivo: %s') % (
                    self.env.user.name, rec.rejection_reason),
                subtype_xmlid='mail.mt_comment',
            )

    def action_reset_draft(self):
        for rec in self:
            rec.state = 'borrador'
            rec.rejection_reason = False

    def action_print_drawing_release(self):
        return self.env.ref(
            'quality_management.action_report_drawing_release'
        ).report_action(self)
```

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
        ('boolean', 'Sí/No'),
        ('char', 'Texto'),
    ], string='Tipo de Dato', default='float')
    value_float = fields.Float('Valor Numérico')
    value_char = fields.Char('Valor Texto')
    value_boolean = fields.Boolean('Valor Sí/No')
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
```

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
    medida = fields.Float('Medida (mm)', required=True)
    resultado = fields.Selection([
        ('cumple', 'Cumple'),
        ('no_cumple', 'No Cumple'),
    ], string='Resultado', default='cumple')
    notas = fields.Char('Notas')
```

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
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import timedelta


class QualityInspection(models.Model):
    _name = 'quality.inspection'
    _description = 'Inspección de PP/PT'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_inspection desc, id desc'

    name = fields.Char(
        'Referencia', required=True, readonly=True,
        default='Nuevo', copy=False
    )
    # ── Tipo de proceso dinámico ──
    process_type_id = fields.Many2one(
        'quality.process.type', 'Tipo de Proceso',
        required=True, tracking=True
    )
    inspection_type = fields.Selection([
        ('laminadora_remanejo', 'Laminadora y Remanejo'),
        ('octagono', 'Octágono'),
        ('guillotina_pegado', 'Guillotina y Pegado'),
    ], string='Tipo (Legacy)',
        compute='_compute_inspection_type', store=True)
    # ── Visibilidad dinámica ──
    show_largo = fields.Boolean(related='process_type_id.show_largo')
    show_ancho = fields.Boolean(related='process_type_id.show_ancho')
    show_espesor = fields.Boolean(related='process_type_id.show_espesor')
    show_hexagono = fields.Boolean(related='process_type_id.show_hexagono')
    show_resistencia = fields.Boolean(related='process_type_id.show_resistencia')
    show_apariencia = fields.Boolean(related='process_type_id.show_apariencia')
    show_humedad = fields.Boolean(related='process_type_id.show_humedad')
    show_pegado = fields.Boolean(related='process_type_id.show_pegado')
    show_retiramiento = fields.Boolean(related='process_type_id.show_retiramiento')
    show_calibracion = fields.Boolean(related='process_type_id.show_calibracion')
    show_engomado = fields.Boolean(related='process_type_id.show_engomado')
    show_ranurado = fields.Boolean(related='process_type_id.show_ranurado')
    show_troquelado = fields.Boolean(related='process_type_id.show_troquelado')
    show_papel = fields.Boolean(related='process_type_id.show_papel')
    show_adhesivo = fields.Boolean(related='process_type_id.show_adhesivo')
    show_tipo_hexagono = fields.Boolean(related='process_type_id.show_tipo_hexagono')
    show_corte_guillotina = fields.Boolean(related='process_type_id.show_corte_guillotina')
    show_numero_corrida = fields.Boolean(related='process_type_id.show_numero_corrida')
    # ── Datos generales ──
    production_order_id = fields.Many2one(
        'mrp.production', 'Orden de Producción', tracking=True
    )
    lot_id = fields.Many2one('stock.lot', 'Lote de Fabricación', tracking=True)
    product_id = fields.Many2one(
        'product.product', 'Producto', required=True, tracking=True
    )
    operator_id = fields.Many2one('hr.employee', 'Operador', required=True)
    supervisor_id = fields.Many2one('hr.employee', 'Supervisor', required=True)
    partner_id = fields.Many2one(
        'res.partner', 'Cliente', required=True, tracking=True
    )
    folio = fields.Char('Folio de Producción', required=True)
    code = fields.Char('Código de Producto', required=True)
    shift = fields.Selection([
        ('turno_1', 'Turno 1'),
        ('turno_2', 'Turno 2'),
        ('turno_3', 'Turno 3'),
    ], string='Turno', required=True)
    plant = fields.Selection([
        ('planta_1', 'Planta 1'),
        ('planta_2', 'Planta 2'),
    ], string='Planta', required=True)
    inspector_id = fields.Many2one(
        'res.users', 'Inspector de Calidad',
        required=True, default=lambda self: self.env.user,
        tracking=True
    )
    date_inspection = fields.Datetime(
        'Fecha y Hora de Inspección', required=True,
        default=fields.Datetime.now
    )
    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('en_proceso', 'En Proceso'),
        ('aceptado', 'Aceptado'),
        ('retenido', 'Retenido'),
        ('rechazado', 'Rechazado'),
    ], string='Estado', default='borrador', required=True,
        tracking=True, copy=False)
    is_pp = fields.Boolean('Producto en Proceso')
    is_pt = fields.Boolean('Producto Terminado')
    line_ids = fields.One2many(
        'quality.inspection.line', 'inspection_id',
        string='Atributos Capturados'
    )
    # ── Campos de medición ──
    largo = fields.Float('Largo (mm)')
    ancho = fields.Float('Ancho (mm)')
    espesor = fields.Float('Espesor (mm)')
    hexagono = fields.Float('Hexágono')
    resistencia = fields.Float('Resistencia')
    apariencia = fields.Selection([
        ('buena', 'Buena'),
        ('regular', 'Regular'),
        ('mala', 'Mala'),
    ], string='Apariencia')
    humedad_pct = fields.Float('% Humedad')
    ranurado_ids = fields.One2many(
        'quality.inspection.ranurado', 'inspection_id',
        string='Capturas de Ranurado'
    )
    troquelado_ids = fields.One2many(
        'quality.inspection.troquelado', 'inspection_id',
        string='Capturas de Troquelado'
    )
    pegado_result = fields.Selection([
        ('cumple', 'Cumple'),
        ('no_cumple', 'No Cumple'),
    ], string='Resultado de Pegado')
    oct_ancho = fields.Float('Ancho Octágono (mm)')
    oct_espesor = fields.Float('Espesor Octágono (mm)')
    oct_hexagono = fields.Float('Hexágono Octágono')
    oct_retiramiento = fields.Float('Retiramiento')
    oct_pegado = fields.Selection([
        ('cumple', 'Cumple'),
        ('no_cumple', 'No Cumple'),
    ], string='Pegado Octágono')
    numero_corrida = fields.Char('Número de Corrida')
    papel_ancho = fields.Float('Ancho del Papel')
    papel_gramaje = fields.Float('Gramaje del Papel')
    papel_proveedor_id = fields.Many2one(
        'res.partner', 'Proveedor del Papel',
        domain=[('supplier_rank', '>', 0)]
    )
    adhesivo_lote1 = fields.Char('Lote 1 Adhesivo')
    adhesivo_lote2 = fields.Char('Lote 2 Adhesivo')
    tipo_hexagono = fields.Selection([
        ('tipo_a', 'Tipo A'),
        ('tipo_b', 'Tipo B'),
        ('tipo_c', 'Tipo C'),
    ], string='Tipo de Hexágono')
    calibracion = fields.Float('Calibración')
    engomado = fields.Selection([
        ('cumple', 'Cumple'),
        ('no_cumple', 'No Cumple'),
    ], string='Engomado')
    corte_guillotina = fields.Boolean('Corte en Guillotina')
    # ── Evidencia con preview ──
    evidence_pdf = fields.Binary('Documento de Evidencia (PDF)', attachment=True)
    evidence_pdf_name = fields.Char('Nombre del Documento')
    # ── General ──
    notes = fields.Html('Observaciones')
    certificate_ids = fields.One2many(
        'quality.certificate', 'inspection_id', string='Certificados'
    )
    certificate_count = fields.Integer(compute='_compute_certificate_count')
    company_id = fields.Many2one(
        'res.company', 'Compañía',
        default=lambda self: self.env.company
    )

    @api.depends('process_type_id', 'process_type_id.code')
    def _compute_inspection_type(self):
        legacy_codes = ('laminadora_remanejo', 'octagono', 'guillotina_pegado')
        for rec in self:
            code = rec.process_type_id.code if rec.process_type_id else False
            rec.inspection_type = code if code in legacy_codes else False

    @api.depends('certificate_ids')
    def _compute_certificate_count(self):
        for rec in self:
            rec.certificate_count = len(rec.certificate_ids)

    @api.onchange('process_type_id')
    def _onchange_process_type_id(self):
        if self.process_type_id and self.process_type_id.attribute_template_ids:
            lines = []
            for tmpl in self.process_type_id.attribute_template_ids:
                lines.append((0, 0, {
                    'attribute_template_id': tmpl.id,
                    'name': tmpl.name,
                    'attribute_type': tmpl.attribute_type,
                    'min_value': tmpl.min_value,
                    'max_value': tmpl.max_value,
                    'unit': tmpl.unit,
                    'sequence': tmpl.sequence,
                }))
            self.line_ids = lines

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'quality.inspection') or 'Nuevo'
        return super().create(vals_list)

    def action_start(self):
        for rec in self:
            rec.state = 'en_proceso'

    def action_accept(self):
        for rec in self:
            rec.state = 'aceptado'
            rec.message_post(
                body=_('✅ Inspección ACEPTADA por %s') % self.env.user.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_retain(self):
        for rec in self:
            rec.state = 'retenido'
            rec.message_post(
                body=_(
                    '⚠️ Producto RETENIDO por %s. '
                    'Lote: %s - Se notifica a Programación/Producción.'
                ) % (self.env.user.name, rec.lot_id.name or 'N/A'),
                subtype_xmlid='mail.mt_comment',
            )
            if rec.production_order_id and rec.production_order_id.user_id:
                rec.activity_schedule(
                    'mail.mail_activity_data_todo',
                    date_deadline=fields.Date.today() + timedelta(days=1),
                    summary=_('Producto retenido en calidad: %s') % rec.name,
                    user_id=rec.production_order_id.user_id.id,
                )

    def action_reject(self):
        for rec in self:
            rec.state = 'rechazado'
            rec.message_post(
                body=_('❌ Inspección RECHAZADA por %s') % self.env.user.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_reset_draft(self):
        for rec in self:
            rec.state = 'borrador'

    def action_create_certificate(self):
        self.ensure_one()
        if self.state != 'aceptado':
            raise UserError(_(
                'Solo se pueden crear certificados de inspecciones aceptadas.'
            ))
        return {
            'type': 'ir.actions.act_window',
            'name': _('Crear Certificado'),
            'res_model': 'quality.certificate.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_inspection_id': self.id,
                'default_partner_id': self.partner_id.id,
            },
        }

    def action_view_certificates(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Certificados'),
            'res_model': 'quality.certificate',
            'view_mode': 'list,form',
            'domain': [('inspection_id', '=', self.id)],
            'context': {'default_inspection_id': self.id},
        }

    def action_print_inspection(self):
        return self.env.ref(
            'quality_management.action_report_inspection_summary'
        ).report_action(self)
```

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

## ./models/quality_sample_release.py
```py
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import timedelta


class QualitySampleRelease(models.Model):
    _name = 'quality.sample.release'
    _description = 'Liberación de Muestras'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_requested desc, id desc'

    name = fields.Char(
        'Referencia', required=True, readonly=True,
        default='Nuevo', copy=False
    )
    project_task_id = fields.Many2one(
        'project.task', 'Tarea de Proyecto',
        required=True, tracking=True,
        help='Tarea del proyecto Muestras & Prototipos'
    )
    product_id = fields.Many2one(
        'product.product', 'Producto/Muestra',
        required=True, tracking=True
    )
    requested_by = fields.Many2one(
        'res.users', 'Solicitante (Diseño)',
        required=True, default=lambda self: self.env.user,
        tracking=True
    )
    inspector_id = fields.Many2one(
        'res.users', 'Inspector de Calidad', tracking=True
    )
    date_requested = fields.Date(
        'Fecha de Solicitud', required=True,
        default=fields.Date.context_today
    )
    date_inspected = fields.Date('Fecha de Inspección', tracking=True)
    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('en_inspeccion', 'En Inspección'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
    ], string='Estado', default='borrador', required=True,
        tracking=True, copy=False)
    inspection_line_ids = fields.One2many(
        'quality.inspection.line', 'sample_release_id',
        string='Atributos Inspeccionados'
    )
    # PDF de especificación con preview
    spec_pdf = fields.Binary('Especificación (PDF)', attachment=True)
    spec_pdf_name = fields.Char('Nombre Especificación')
    notes = fields.Html('Observaciones')
    company_id = fields.Many2one(
        'res.company', 'Compañía',
        default=lambda self: self.env.company
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'Nuevo') == 'Nuevo':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'quality.sample.release') or 'Nuevo'
        return super().create(vals_list)

    def action_submit_inspection(self):
        for rec in self:
            rec.state = 'en_inspeccion'
            quality_users = self.env.ref(
                'quality_management.group_quality_inspector'
            ).users
            if rec.inspector_id:
                quality_users = rec.inspector_id
            for user in quality_users:
                rec.activity_schedule(
                    'mail.mail_activity_data_todo',
                    date_deadline=fields.Date.today() + timedelta(days=2),
                    summary=_('Inspección de muestra: %s') % rec.name,
                    user_id=user.id,
                )
            rec.message_post(
                body=_('Solicitud de inspección enviada por %s') % rec.requested_by.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_accept(self):
        for rec in self:
            if rec.inspection_line_ids:
                failing = rec.inspection_line_ids.filtered(
                    lambda l: l.result == 'no_cumple'
                )
                if failing:
                    raise UserError(_(
                        'No se puede liberar: hay %d atributo(s) que no cumplen.'
                    ) % len(failing))
            rec.state = 'aceptado'
            rec.date_inspected = fields.Date.today()
            rec.activity_feedback(
                ['mail.mail_activity_data_todo'],
                feedback=_('Muestra aceptada')
            )
            rec.message_post(
                body=_('✅ Muestra ACEPTADA y liberada por %s') % self.env.user.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_reject(self):
        for rec in self:
            rec.state = 'rechazado'
            rec.date_inspected = fields.Date.today()
            rec.activity_feedback(
                ['mail.mail_activity_data_todo'],
                feedback=_('Muestra rechazada')
            )
            rec.message_post(
                body=_('❌ Muestra RECHAZADA por %s. Se notifica a Diseño.') % self.env.user.name,
                subtype_xmlid='mail.mt_comment',
            )

    def action_reset_draft(self):
        for rec in self:
            rec.state = 'borrador'

    def action_print_sample_release(self):
        return self.env.ref(
            'quality_management.action_report_sample_release'
        ).report_action(self)
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

                        <h4>D3 - Plan de Acciones</h4>
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

                        <!-- Estado visual -->
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
</odoo>
```

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

                        <t t-if="doc.state == 'aceptado'">
                            <div class="text-center" style="margin-bottom: 15px;">
                                <span style="background-color: #28a745; color: white; padding: 5px 20px; border-radius: 4px; font-size: 16px; font-weight: bold;">
                                    ✅ PLANO LIBERADO
                                </span>
                            </div>
                        </t>
                        <t t-if="doc.state == 'rechazado'">
                            <div class="text-center" style="margin-bottom: 15px;">
                                <span style="background-color: #dc3545; color: white; padding: 5px 20px; border-radius: 4px; font-size: 16px; font-weight: bold;">
                                    ❌ PLANO RECHAZADO
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

                        <t t-if="doc.state == 'rechazado' and doc.rejection_reason">
                            <h4>Motivo de Rechazo</h4>
                            <div style="border: 2px solid #dc3545; padding: 10px; margin-bottom: 15px; min-height: 40px; background-color: #fff5f5;">
                                <span t-field="doc.rejection_reason"/>
                            </div>
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
</odoo>
```

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
                                    <td><span t-field="doc.supervisor_id.name"/></td>
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

                        <!-- Medidas dinámicas -->
                        <t t-if="doc.show_largo or doc.show_ancho or doc.show_espesor or doc.show_hexagono or doc.show_resistencia or doc.show_apariencia or doc.show_humedad or doc.show_pegado or doc.show_retiramiento or doc.show_calibracion or doc.show_engomado">
                            <h4>Medidas - <span t-field="doc.process_type_id.name"/></h4>
                            <table class="table table-bordered table-sm">
                                <thead><tr class="table-active">
                                    <th t-if="doc.show_largo">Largo</th>
                                    <th t-if="doc.show_ancho">Ancho</th>
                                    <th t-if="doc.show_espesor">Espesor</th>
                                    <th t-if="doc.show_hexagono">Hexágono</th>
                                    <th t-if="doc.show_resistencia">Resistencia</th>
                                    <th t-if="doc.show_apariencia">Apariencia</th>
                                    <th t-if="doc.show_humedad">% Humedad</th>
                                    <th t-if="doc.show_pegado">Pegado</th>
                                    <th t-if="doc.show_retiramiento">Retiramiento</th>
                                    <th t-if="doc.show_calibracion">Calibración</th>
                                    <th t-if="doc.show_engomado">Engomado</th>
                                </tr></thead>
                                <tbody><tr>
                                    <td t-if="doc.show_largo" class="text-center"><span t-field="doc.largo"/></td>
                                    <td t-if="doc.show_ancho" class="text-center"><span t-esc="doc.ancho or doc.oct_ancho"/></td>
                                    <td t-if="doc.show_espesor" class="text-center"><span t-esc="doc.espesor or doc.oct_espesor"/></td>
                                    <td t-if="doc.show_hexagono" class="text-center"><span t-esc="doc.hexagono or doc.oct_hexagono"/></td>
                                    <td t-if="doc.show_resistencia" class="text-center"><span t-field="doc.resistencia"/></td>
                                    <td t-if="doc.show_apariencia" class="text-center"><span t-field="doc.apariencia"/></td>
                                    <td t-if="doc.show_humedad" class="text-center"><span t-field="doc.humedad_pct"/>%</td>
                                    <td t-if="doc.show_pegado" class="text-center"><span t-esc="doc.pegado_result or doc.oct_pegado or ''"/></td>
                                    <td t-if="doc.show_retiramiento" class="text-center"><span t-field="doc.oct_retiramiento"/></td>
                                    <td t-if="doc.show_calibracion" class="text-center"><span t-field="doc.calibracion"/></td>
                                    <td t-if="doc.show_engomado" class="text-center"><span t-field="doc.engomado"/></td>
                                </tr></tbody>
                            </table>
                        </t>

                        <!-- Datos de producción -->
                        <t t-if="doc.show_numero_corrida or doc.show_papel or doc.show_adhesivo">
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

                        <!-- Ranurado -->
                        <t t-if="doc.ranurado_ids">
                            <h5>Ranurado</h5>
                            <table class="table table-bordered table-sm">
                                <thead><tr class="table-active">
                                    <th>N°</th><th>Medida (mm)</th><th>Resultado</th>
                                </tr></thead>
                                <tbody>
                                    <tr t-foreach="doc.ranurado_ids" t-as="r">
                                        <td><span t-field="r.sequence"/></td>
                                        <td class="text-center"><span t-field="r.medida"/></td>
                                        <td class="text-center"><span t-field="r.resultado"/></td>
                                    </tr>
                                </tbody>
                            </table>
                        </t>

                        <!-- Troquelado -->
                        <t t-if="doc.troquelado_ids">
                            <h5>Troquelado</h5>
                            <table class="table table-bordered table-sm">
                                <thead><tr class="table-active">
                                    <th>N°</th><th>Medida (mm)</th><th>Resultado</th>
                                </tr></thead>
                                <tbody>
                                    <tr t-foreach="doc.troquelado_ids" t-as="t_line">
                                        <td><span t-field="t_line.sequence"/></td>
                                        <td class="text-center"><span t-field="t_line.medida"/></td>
                                        <td class="text-center"><span t-field="t_line.resultado"/></td>
                                    </tr>
                                </tbody>
                            </table>
                        </t>

                        <!-- Atributos adicionales -->
                        <t t-if="doc.line_ids">
                            <h5>Atributos Adicionales</h5>
                            <table class="table table-bordered table-sm">
                                <thead><tr class="table-active">
                                    <th>Atributo</th><th>Valor</th><th>Rango</th><th>Resultado</th>
                                </tr></thead>
                                <tbody>
                                    <tr t-foreach="doc.line_ids" t-as="attr">
                                        <td><span t-field="attr.name"/></td>
                                        <td class="text-center">
                                            <span t-if="attr.attribute_type == 'float'" t-field="attr.value_float"/>
                                            <span t-if="attr.attribute_type in ('char', 'selection')" t-field="attr.value_char"/>
                                            <span t-if="attr.attribute_type == 'boolean'" t-field="attr.value_boolean"/>
                                        </td>
                                        <td class="text-center">
                                            <t t-if="attr.min_value or attr.max_value">
                                                <span t-field="attr.min_value"/> - <span t-field="attr.max_value"/> <span t-field="attr.unit"/>
                                            </t>
                                        </td>
                                        <td class="text-center"><span t-field="attr.result"/></td>
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
                                    <p>Supervisor</p>
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
                                    <td class="text-center">mm</td>
                                </tr>
                                <tr t-if="doc.certified_hexagono">
                                    <td>Hexágono</td>
                                    <td class="text-center"><span t-field="doc.certified_hexagono"/></td>
                                    <td class="text-center">mm</td>
                                </tr>
                                <tr t-if="doc.certified_resistencia">
                                    <td>Resistencia</td>
                                    <td class="text-center"><span t-field="doc.certified_resistencia"/></td>
                                    <td class="text-center">-</td>
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
                                    <td class="text-center">mm</td>
                                </tr>
                                <tr t-if="doc.certified_calibracion">
                                    <td>Calibración</td>
                                    <td class="text-center"><span t-field="doc.certified_calibracion"/></td>
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
                                            <span t-if="attr.attribute_type == 'boolean'" t-field="attr.value_boolean"/>
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
                                    <p>____________________________</p>
                                    <p>Sello de la Empresa</p>
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

                        <!-- Estado como sello visual -->
                        <t t-if="doc.state == 'aceptado'">
                            <div class="text-center" style="margin-bottom: 15px;">
                                <span style="background-color: #28a745; color: white; padding: 5px 20px; border-radius: 4px; font-size: 16px; font-weight: bold;">
                                    ✅ MUESTRA LIBERADA
                                </span>
                            </div>
                        </t>
                        <t t-if="doc.state == 'rechazado'">
                            <div class="text-center" style="margin-bottom: 15px;">
                                <span style="background-color: #dc3545; color: white; padding: 5px 20px; border-radius: 4px; font-size: 16px; font-weight: bold;">
                                    ❌ MUESTRA RECHAZADA
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
                                            <span t-if="line.attribute_type == 'boolean'" t-field="line.value_boolean"/>
                                        </td>
                                        <td class="text-center">
                                            <t t-if="line.min_value or line.max_value">
                                                <span t-field="line.min_value"/> - <span t-field="line.max_value"/>
                                            </t>
                                        </td>
                                        <td class="text-center"><span t-field="line.unit"/></td>
                                        <td class="text-center">
                                            <span t-if="line.result == 'cumple'" style="color: green; font-weight: bold;">CUMPLE</span>
                                            <span t-if="line.result == 'no_cumple'" style="color: red; font-weight: bold;">NO CUMPLE</span>
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
</odoo>
```

## ./security/quality_groups.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <record id="module_category_quality" model="ir.module.category">
            <field name="name">Calidad</field>
            <field name="sequence">50</field>
        </record>

        <record id="group_quality_inspector" model="res.groups">
            <field name="name">Inspector de Calidad</field>
            <field name="category_id" ref="module_category_quality"/>
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
</odoo>
```

## ./security/quality_rules.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data>
        <record id="rule_inspection_inspector_own" model="ir.rule">
            <field name="name">Inspector: solo sus inspecciones</field>
            <field name="model_id" ref="model_quality_inspection"/>
            <field name="domain_force">[('inspector_id', '=', user.id)]</field>
            <field name="groups" eval="[(4, ref('group_quality_inspector'))]"/>
        </record>
        <record id="rule_inspection_manager_all" model="ir.rule">
            <field name="name">Manager: todas las inspecciones</field>
            <field name="model_id" ref="model_quality_inspection"/>
            <field name="domain_force">[(1, '=', 1)]</field>
            <field name="groups" eval="[(4, ref('group_quality_manager'))]"/>
        </record>
        <record id="rule_sample_release_sale" model="ir.rule">
            <field name="name">Ventas: solo sus solicitudes de muestra</field>
            <field name="model_id" ref="model_quality_sample_release"/>
            <field name="domain_force">['|', ('requested_by', '=', user.id), ('state', 'in', ['aceptado', 'rechazado'])]</field>
            <field name="groups" eval="[(4, ref('sales_team.group_sale_salesman'))]"/>
        </record>
        <record id="rule_drawing_release_sale" model="ir.rule">
            <field name="name">Ventas: solo sus solicitudes de plano</field>
            <field name="model_id" ref="model_quality_drawing_release"/>
            <field name="domain_force">['|', ('requested_by', '=', user.id), ('state', 'in', ['aceptado', 'rechazado'])]</field>
            <field name="groups" eval="[(4, ref('sales_team.group_sale_salesman'))]"/>
        </record>
        <record id="rule_customer_return_sale" model="ir.rule">
            <field name="name">Ventas: devoluciones de sus clientes</field>
            <field name="model_id" ref="model_quality_customer_return"/>
            <field name="domain_force">[(1, '=', 1)]</field>
            <field name="groups" eval="[(4, ref('sales_team.group_sale_salesman'))]"/>
        </record>
        <record id="rule_sample_release_manager" model="ir.rule">
            <field name="name">Manager: todas las liberaciones de muestra</field>
            <field name="model_id" ref="model_quality_sample_release"/>
            <field name="domain_force">[(1, '=', 1)]</field>
            <field name="groups" eval="[(4, ref('group_quality_manager'))]"/>
        </record>
        <record id="rule_drawing_release_manager" model="ir.rule">
            <field name="name">Manager: todas las liberaciones de plano</field>
            <field name="model_id" ref="model_quality_drawing_release"/>
            <field name="domain_force">[(1, '=', 1)]</field>
            <field name="groups" eval="[(4, ref('group_quality_manager'))]"/>
        </record>
        <record id="rule_corrective_action_manager" model="ir.rule">
            <field name="name">Manager: todas las acciones correctivas</field>
            <field name="model_id" ref="model_quality_corrective_action"/>
            <field name="domain_force">[(1, '=', 1)]</field>
            <field name="groups" eval="[(4, ref('group_quality_manager'))]"/>
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
                <field name="process_type_id"/>
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
                        <group>
                            <field name="name"/>
                            <field name="process_type_id"/>
                            <field name="attribute_type"/>
                            <field name="is_required"/>
                        </group>
                        <group>
                            <field name="unit"/>
                            <field name="min_value" invisible="attribute_type != 'float'"/>
                            <field name="max_value" invisible="attribute_type != 'float'"/>
                            <field name="selection_options" invisible="attribute_type != 'selection'"/>
                        </group>
                    </group>
                </sheet>
            </form>
        </field>
    </record>

    <record id="action_quality_attribute_template" model="ir.actions.act_window">
        <field name="name">Plantillas de Atributos</field>
        <field name="res_model">quality.attribute.template</field>
        <field name="view_mode">list,form</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Crear una plantilla de atributo de calidad
            </p>
            <p>Configure los atributos de inspección por tipo de proceso.</p>
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
                    <button name="action_mark_sent" string="Marcar como Enviado"
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
                            <field name="product_id"/>
                            <field name="process_type_id"/>
                        </group>
                        <group>
                            <field name="folio"/>
                            <field name="lot_id"/>
                            <field name="date_generated"/>
                            <field name="certified_by"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Valores Certificados">
                            <group>
                                <group>
                                    <field name="certified_largo" invisible="certified_largo == 0"/>
                                    <field name="certified_ancho" invisible="certified_ancho == 0"/>
                                    <field name="certified_espesor" invisible="certified_espesor == 0"/>
                                    <field name="certified_hexagono" invisible="certified_hexagono == 0"/>
                                    <field name="certified_resistencia" invisible="certified_resistencia == 0"/>
                                </group>
                                <group>
                                    <field name="certified_apariencia" invisible="not certified_apariencia"/>
                                    <field name="certified_humedad" invisible="certified_humedad == 0"/>
                                    <field name="certified_pegado" invisible="not certified_pegado"/>
                                    <field name="certified_retiramiento" invisible="certified_retiramiento == 0"/>
                                    <field name="certified_calibracion" invisible="certified_calibracion == 0"/>
                                    <field name="certified_engomado" invisible="not certified_engomado"/>
                                </group>
                            </group>
                        </page>
                        <page string="Atributos Seleccionados">
                            <field name="attribute_ids">
                                <list>
                                    <field name="name"/>
                                    <field name="value_float"/>
                                    <field name="value_char"/>
                                    <field name="result"/>
                                </list>
                            </field>
                        </page>
                        <page string="PDF Generado" invisible="not report_pdf">
                            <group>
                                <field name="report_pdf" filename="report_pdf_name"/>
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
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Los certificados se generan desde inspecciones aceptadas
            </p>
        </field>
    </record>
</odoo>
```

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
                <field name="responsible_id"/>
                <field name="date_opened"/>
                <field name="action_count"/>
                <field name="action_completed_count"/>
                <field name="action_overdue_count" decoration-danger="action_overdue_count > 0"/>
                <field name="progress" widget="progressbar"/>
                <field name="state" widget="badge"
                       decoration-success="state == 'cerrada'"
                       decoration-info="state in ('abierta', 'en_proceso')"
                       decoration-muted="state == 'no_procede'"/>
            </list>
        </field>
    </record>

    <!-- Formulario separado para quality.action.line para ver evidencia inline -->
    <record id="view_quality_action_line_form" model="ir.ui.view">
        <field name="name">quality.action.line.form</field>
        <field name="model">quality.action.line</field>
        <field name="arch" type="xml">
            <form string="Detalle de Acción">
                <group>
                    <group>
                        <field name="description"/>
                        <field name="responsible_id"/>
                        <field name="state" widget="badge"
                               decoration-success="state == 'completada'"
                               decoration-danger="state == 'vencida'"
                               decoration-info="state == 'en_proceso'"/>
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
            <form string="Acción Correctiva/Preventiva">
                <header>
                    <button name="action_open" string="Abrir"
                            type="object" class="btn-primary"
                            invisible="state != 'borrador'"
                            groups="quality_management.group_quality_manager"/>
                    <button name="action_in_progress" string="En Proceso"
                            type="object"
                            invisible="state != 'abierta'"/>
                    <button name="action_close" string="Cerrar"
                            type="object" class="btn-primary"
                            invisible="state not in ('abierta', 'en_proceso')"
                            groups="quality_management.group_quality_manager"/>
                    <button name="action_no_proceed" string="No Procede"
                            type="object" class="btn-secondary"
                            invisible="state != 'borrador'"
                            groups="quality_management.group_quality_manager"/>
                    <button name="action_reopen" string="Reabrir"
                            type="object"
                            invisible="state not in ('cerrada', 'no_procede')"
                            groups="quality_management.group_quality_manager"/>
                    <button name="action_print_8d" string="Imprimir 8D"
                            type="object" class="btn-secondary" icon="fa-print"/>
                    <field name="state" widget="statusbar"
                           statusbar_visible="borrador,abierta,en_proceso,cerrada"/>
                </header>
                <sheet>
                    <div class="oe_title">
                        <h1><field name="name" readonly="1"/></h1>
                    </div>
                    <group>
                        <group>
                            <field name="origin_type"/>
                            <field name="origin_inspection_id"
                                   invisible="origin_type != 'inspeccion'"/>
                            <field name="origin_return_id"
                                   invisible="origin_type != 'devolucion'"/>
                            <field name="responsible_id"/>
                        </group>
                        <group>
                            <field name="date_opened"/>
                            <field name="date_closed"/>
                            <field name="progress" widget="progressbar"/>
                        </group>
                    </group>
                    <separator string="Descripción del Incumplimiento"/>
                    <field name="origin_description"/>
                    <notebook>
                        <page string="Acciones" name="actions">
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
                                <i class="fa fa-info-circle"/> Para ver la evidencia con vista previa (imágenes, videos, PDFs), abra cada línea de acción en modo formulario.
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
                <filter string="Abiertas" name="open"
                        domain="[('state', 'in', ('abierta', 'en_proceso'))]"/>
                <filter string="Con Acciones Vencidas" name="overdue"
                        domain="[('action_line_ids.state', '=', 'vencida')]"/>
                <filter string="Cerradas" name="closed"
                        domain="[('state', '=', 'cerrada')]"/>
                <group expand="0" string="Agrupar por">
                    <filter string="Tipo de Origen" name="group_origin" context="{'group_by': 'origin_type'}"/>
                    <filter string="Responsable" name="group_resp" context="{'group_by': 'responsible_id'}"/>
                    <filter string="Estado" name="group_state" context="{'group_by': 'state'}"/>
                </group>
            </search>
        </field>
    </record>

    <record id="action_quality_corrective_action" model="ir.actions.act_window">
        <field name="name">Acciones Correctivas/Preventivas</field>
        <field name="res_model">quality.corrective.action</field>
        <field name="view_mode">list,form</field>
        <field name="context">{'search_default_open': 1}</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Crear una acción correctiva o preventiva
            </p>
        </field>
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
                <field name="requires_dimensions"/>
                <field name="requested_by"/>
                <field name="responsible_id"/>
                <field name="date_requested"/>
                <field name="date_due"/>
                <field name="state" widget="badge"
                       decoration-success="state == 'enviado'"
                       decoration-info="state in ('en_proceso', 'completado')"/>
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
                    <button name="action_print_customer_document" string="Imprimir"
                            type="object" class="btn-secondary" icon="fa-print"/>
                    <field name="state" widget="statusbar"
                           statusbar_visible="borrador,en_proceso,completado,enviado"/>
                </header>
                <sheet>
                    <div class="oe_title">
                        <h1><field name="name" readonly="1"/></h1>
                    </div>
                    <group>
                        <group>
                            <field name="partner_id"/>
                            <field name="document_type"/>
                            <field name="requires_dimensions"/>
                            <field name="requested_by"/>
                        </group>
                        <group>
                            <field name="responsible_id"/>
                            <field name="date_requested"/>
                            <field name="date_due"/>
                            <field name="date_completed"/>
                        </group>
                    </group>
                    <field name="description" placeholder="Descripción adicional del requerimiento..."/>
                    <notebook>
                        <page string="Documento Principal PDF">
                            <group>
                                <field name="main_pdf" filename="main_pdf_name"/>
                                <field name="main_pdf_name" invisible="1"/>
                            </group>
                            <div invisible="not main_pdf" class="o_quality_pdf_preview">
                                <field name="main_pdf" widget="pdf_viewer" readonly="1"/>
                            </div>
                        </page>
                        <page string="Formatos del Cliente">
                            <field name="client_format_ids" widget="many2many_binary"/>
                        </page>
                        <page string="Documentos Generados">
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
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Registrar solicitud de documento de cliente
            </p>
        </field>
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
                  decoration-info="state in ('evaluacion_ventas', 'evaluacion_calidad')">
                <field name="name"/>
                <field name="partner_id"/>
                <field name="defect_type"/>
                <field name="defect_pieces"/>
                <field name="production_date"/>
                <field name="days_since_production"/>
                <field name="date_received"/>
                <field name="corrective_action_id" optional="show"/>
                <field name="state" widget="badge"
                       decoration-success="state == 'cerrada'"
                       decoration-danger="state == 'no_procede'"
                       decoration-info="state in ('evaluacion_ventas', 'evaluacion_calidad')"
                       decoration-warning="state == 'en_8d'"/>
            </list>
        </field>
    </record>

    <record id="view_quality_customer_return_form" model="ir.ui.view">
        <field name="name">quality.customer.return.form</field>
        <field name="model">quality.customer.return</field>
        <field name="arch" type="xml">
            <form string="Devolución de Cliente">
                <header>
                    <button name="action_submit_sales" string="Registrar / Evaluar"
                            type="object" class="btn-primary"
                            invisible="state != 'borrador'"/>
                    <button name="action_submit_quality" string="Enviar a Calidad"
                            type="object" class="btn-primary"
                            invisible="state != 'evaluacion_ventas'"/>
                    <button name="action_generate_8d" string="Generar 8D"
                            type="object" class="btn-primary"
                            invisible="state != 'evaluacion_calidad'"
                            groups="quality_management.group_quality_manager"/>
                    <button name="action_no_proceed" string="No Procede"
                            type="object" class="btn-secondary"
                            invisible="state not in ('evaluacion_ventas', 'evaluacion_calidad')"
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
                        <strong>⚠️ Fuera de periodo:</strong> La fecha de producción
                        tiene más de 30 días (<field name="days_since_production" nolabel="1"/> días).
                        Esta devolución podría no proceder.
                    </div>
                    <group>
                        <group string="Datos del Cliente">
                            <field name="partner_id"/>
                            <field name="sale_order_id"/>
                            <field name="date_received"/>
                            <field name="production_date"/>
                            <field name="days_since_production"/>
                            <field name="is_within_period" invisible="1"/>
                        </group>
                        <group string="Detalle del Defecto">
                            <field name="defect_type"/>
                            <field name="defect_pieces"/>
                            <field name="affects_functionality"/>
                        </group>
                    </group>
                    <separator string="Motivo de la Devolución"/>
                    <field name="return_reason"/>
                    <notebook>
                        <page string="Evidencia">
                            <group string="Adjuntar Evidencia (imágenes, videos, PDFs)">
                                <field name="evidence_ids" widget="many2many_binary" nolabel="1"/>
                            </group>
                            <separator string="Vista Previa de Evidencia"/>
                            <field name="evidence_ids" widget="evidence_viewer" nolabel="1"/>
                        </page>
                        <page string="Evidencia PDF">
                            <group>
                                <field name="evidence_pdf" filename="evidence_pdf_name"/>
                                <field name="evidence_pdf_name" invisible="1"/>
                            </group>
                            <div invisible="not evidence_pdf" class="o_quality_pdf_preview">
                                <field name="evidence_pdf" widget="pdf_viewer" readonly="1"/>
                            </div>
                        </page>
                        <page string="Tarimas">
                            <group>
                                <field name="pallets_returned"/>
                                <field name="pallet_return_date"
                                       invisible="not pallets_returned"/>
                            </group>
                        </page>
                        <page string="Formato de Reclamación">
                            <group>
                                <field name="claim_format_id"/>
                            </group>
                        </page>
                        <page string="8D" invisible="not corrective_action_id">
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
                        domain="[('state', 'not in', ('cerrada', 'no_procede'))]"/>
                <filter string="En 8D" name="in_8d"
                        domain="[('state', '=', 'en_8d')]"/>
                <group expand="0" string="Agrupar por">
                    <filter string="Cliente" name="group_partner" context="{'group_by': 'partner_id'}"/>
                    <filter string="Tipo de Defecto" name="group_defect" context="{'group_by': 'defect_type'}"/>
                    <filter string="Estado" name="group_state" context="{'group_by': 'state'}"/>
                </group>
            </search>
        </field>
    </record>

    <record id="action_quality_customer_return" model="ir.actions.act_window">
        <field name="name">Devoluciones de Clientes</field>
        <field name="res_model">quality.customer.return</field>
        <field name="view_mode">list,form</field>
        <field name="context">{'search_default_open': 1}</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Registrar una devolución de cliente
            </p>
        </field>
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
            <list decoration-success="state == 'aceptado'"
                  decoration-danger="state == 'rechazado'"
                  decoration-info="state == 'en_revision'">
                <field name="name"/>
                <field name="partner_id"/>
                <field name="sale_order_id" optional="show"/>
                <field name="requested_by"/>
                <field name="inspector_id"/>
                <field name="date_requested"/>
                <field name="state" widget="badge"
                       decoration-success="state == 'aceptado'"
                       decoration-danger="state == 'rechazado'"
                       decoration-info="state == 'en_revision'"/>
            </list>
        </field>
    </record>

    <record id="view_quality_drawing_release_form" model="ir.ui.view">
        <field name="name">quality.drawing.release.form</field>
        <field name="model">quality.drawing.release</field>
        <field name="arch" type="xml">
            <form string="Liberación de Plano">
                <header>
                    <button name="action_submit_review" string="Enviar a Revisión"
                            type="object" class="btn-primary"
                            invisible="state != 'borrador'"/>
                    <button name="action_accept" string="Liberar"
                            type="object" class="btn-primary"
                            invisible="state != 'en_revision'"
                            groups="quality_management.group_quality_inspector"/>
                    <button name="action_reject" string="Rechazar"
                            type="object" class="btn-danger"
                            invisible="state != 'en_revision'"
                            groups="quality_management.group_quality_inspector"/>
                    <button name="action_print_drawing_release" string="Imprimir"
                            type="object" class="btn-secondary" icon="fa-print"/>
                    <button name="action_reset_draft" string="Regresar a Borrador"
                            type="object"
                            invisible="state not in ('rechazado',)"
                            groups="quality_management.group_quality_manager"/>
                    <field name="state" widget="statusbar"
                           statusbar_visible="borrador,en_revision,aceptado"/>
                </header>
                <sheet>
                    <div class="oe_title">
                        <h1><field name="name" readonly="1"/></h1>
                    </div>
                    <group>
                        <group>
                            <field name="partner_id"/>
                            <field name="sale_order_id"/>
                            <field name="requested_by"/>
                        </group>
                        <group>
                            <field name="inspector_id"/>
                            <field name="date_requested"/>
                            <field name="date_released"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Plano PDF">
                            <group>
                                <field name="drawing_pdf" filename="drawing_pdf_name"/>
                                <field name="drawing_pdf_name" invisible="1"/>
                            </group>
                            <div invisible="not drawing_pdf" class="o_quality_pdf_preview">
                                <field name="drawing_pdf" widget="pdf_viewer" readonly="1"/>
                            </div>
                        </page>
                        <page string="Documentos Adjuntos">
                            <field name="drawing_attachment_ids" widget="many2many_binary"/>
                        </page>
                        <page string="Rechazo" invisible="state != 'rechazado'">
                            <field name="rejection_reason" placeholder="Motivo de rechazo..."/>
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
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Crear solicitud de liberación de plano
            </p>
        </field>
    </record>
</odoo>
```

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
                  decoration-danger="state in ('rechazado', 'retenido')"
                  decoration-info="state == 'en_proceso'">
                <field name="name"/>
                <field name="process_type_id"/>
                <field name="product_id"/>
                <field name="partner_id"/>
                <field name="folio"/>
                <field name="shift"/>
                <field name="inspector_id"/>
                <field name="date_inspection"/>
                <field name="is_pp" optional="show"/>
                <field name="is_pt" optional="show"/>
                <field name="state" widget="badge"
                       decoration-success="state == 'aceptado'"
                       decoration-danger="state in ('rechazado', 'retenido')"
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
                    <button name="action_start" string="Iniciar Inspección"
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
                            invisible="state not in ('rechazado', 'retenido')"
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
                    <!-- Campos booleanos de visibilidad (hidden) -->
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

                    <group>
                        <group string="Datos Generales">
                            <field name="process_type_id"/>
                            <field name="product_id"/>
                            <field name="production_order_id"/>
                            <field name="lot_id"/>
                            <field name="folio"/>
                            <field name="code"/>
                        </group>
                        <group string="Personal y Ubicación">
                            <field name="operator_id"/>
                            <field name="supervisor_id"/>
                            <field name="inspector_id"/>
                            <field name="partner_id"/>
                            <field name="shift"/>
                            <field name="plant"/>
                            <field name="date_inspection"/>
                        </group>
                    </group>
                    <group>
                        <group>
                            <field name="is_pp"/>
                        </group>
                        <group>
                            <field name="is_pt"/>
                        </group>
                    </group>
                    <notebook>
                        <!-- Medidas dinámicas -->
                        <page string="Medidas y Propiedades"
                              invisible="not show_largo and not show_ancho and not show_espesor and not show_hexagono and not show_resistencia and not show_apariencia and not show_humedad and not show_pegado and not show_retiramiento and not show_calibracion and not show_engomado">
                            <group>
                                <group string="Medidas Dimensionales">
                                    <field name="largo" invisible="not show_largo"/>
                                    <field name="ancho" invisible="not show_ancho"/>
                                    <field name="espesor" invisible="not show_espesor"/>
                                    <field name="hexagono" invisible="not show_hexagono"/>
                                </group>
                                <group string="Propiedades">
                                    <field name="resistencia" invisible="not show_resistencia"/>
                                    <field name="apariencia" invisible="not show_apariencia"/>
                                    <field name="humedad_pct" invisible="not show_humedad"/>
                                    <field name="pegado_result" invisible="not show_pegado"/>
                                    <field name="oct_retiramiento" invisible="not show_retiramiento"/>
                                    <field name="calibracion" invisible="not show_calibracion"/>
                                    <field name="engomado" invisible="not show_engomado"/>
                                </group>
                            </group>
                        </page>
                        <!-- Ranurado -->
                        <page string="Ranurado" invisible="not show_ranurado">
                            <field name="ranurado_ids">
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
                        <!-- Troquelado -->
                        <page string="Troquelado" invisible="not show_troquelado">
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
                        <!-- Datos de Producción (papel, adhesivo, etc) -->
                        <page string="Datos de Producción"
                              invisible="not show_papel and not show_adhesivo and not show_tipo_hexagono and not show_numero_corrida and not show_corte_guillotina">
                            <group>
                                <group string="Producción" invisible="not show_numero_corrida and not show_tipo_hexagono and not show_corte_guillotina">
                                    <field name="numero_corrida" invisible="not show_numero_corrida"/>
                                    <field name="tipo_hexagono" invisible="not show_tipo_hexagono"/>
                                    <field name="corte_guillotina" invisible="not show_corte_guillotina"/>
                                </group>
                                <group string="Papel" invisible="not show_papel">
                                    <field name="papel_ancho"/>
                                    <field name="papel_gramaje"/>
                                    <field name="papel_proveedor_id"/>
                                </group>
                            </group>
                            <group invisible="not show_adhesivo">
                                <group string="Adhesivo">
                                    <field name="adhesivo_lote1"/>
                                    <field name="adhesivo_lote2"/>
                                </group>
                            </group>
                        </page>
                        <!-- Atributos adicionales -->
                        <page string="Atributos Adicionales">
                            <field name="line_ids">
                                <list editable="bottom">
                                    <field name="sequence" widget="handle"/>
                                    <field name="name"/>
                                    <field name="attribute_type"/>
                                    <field name="value_float" invisible="attribute_type != 'float'"/>
                                    <field name="value_char" invisible="attribute_type not in ('char', 'selection')"/>
                                    <field name="value_boolean" invisible="attribute_type != 'boolean'" widget="boolean_toggle"/>
                                    <field name="min_value" invisible="attribute_type != 'float'"/>
                                    <field name="max_value" invisible="attribute_type != 'float'"/>
                                    <field name="unit"/>
                                    <field name="result" widget="badge"
                                           decoration-success="result == 'cumple'"
                                           decoration-danger="result == 'no_cumple'"/>
                                    <field name="notes"/>
                                </list>
                            </field>
                        </page>
                        <!-- Evidencia PDF -->
                        <page string="Evidencia PDF">
                            <group>
                                <field name="evidence_pdf" filename="evidence_pdf_name"/>
                                <field name="evidence_pdf_name" invisible="1"/>
                            </group>
                            <div invisible="not evidence_pdf" class="o_quality_pdf_preview">
                                <field name="evidence_pdf" widget="pdf_viewer" readonly="1"/>
                            </div>
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

    <record id="view_quality_inspection_search" model="ir.ui.view">
        <field name="name">quality.inspection.search</field>
        <field name="model">quality.inspection</field>
        <field name="arch" type="xml">
            <search string="Inspecciones">
                <field name="name"/>
                <field name="product_id"/>
                <field name="partner_id"/>
                <field name="folio"/>
                <field name="inspector_id"/>
                <field name="process_type_id"/>
                <filter string="Hoy" name="today"
                        domain="[('date_inspection', '&gt;=', datetime.datetime.combine(context_today(), datetime.time(0,0,0))),
                                 ('date_inspection', '&lt;=', datetime.datetime.combine(context_today(), datetime.time(23,59,59)))]"/>
                <separator/>
                <filter string="Aceptadas" name="accepted" domain="[('state', '=', 'aceptado')]"/>
                <filter string="Retenidas" name="retained" domain="[('state', '=', 'retenido')]"/>
                <filter string="Rechazadas" name="rejected" domain="[('state', '=', 'rechazado')]"/>
                <group expand="0" string="Agrupar por">
                    <filter string="Tipo de Proceso" name="group_type" context="{'group_by': 'process_type_id'}"/>
                    <filter string="Turno" name="group_shift" context="{'group_by': 'shift'}"/>
                    <filter string="Planta" name="group_plant" context="{'group_by': 'plant'}"/>
                    <filter string="Inspector" name="group_inspector" context="{'group_by': 'inspector_id'}"/>
                    <filter string="Operador" name="group_operator" context="{'group_by': 'operator_id'}"/>
                    <filter string="Estado" name="group_state" context="{'group_by': 'state'}"/>
                    <filter string="Fecha" name="group_date" context="{'group_by': 'date_inspection:day'}"/>
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
                <field name="shift" type="row"/>
            </pivot>
        </field>
    </record>

    <record id="action_quality_inspection" model="ir.actions.act_window">
        <field name="name">Inspecciones</field>
        <field name="res_model">quality.inspection</field>
        <field name="view_mode">list,form,pivot</field>
        <field name="context">{'search_default_today': 1}</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Crear una nueva inspección de calidad
            </p>
            <p>Capture los datos de inspección de PP y PT.</p>
        </field>
    </record>
</odoo>
```

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

    <menuitem id="menu_quality_certificate"
              name="Certificados"
              parent="menu_quality_root"
              action="action_quality_certificate"
              sequence="30"
              groups="group_quality_manager"/>

    <menuitem id="menu_quality_corrective_action"
              name="Acciones Correctivas"
              parent="menu_quality_root"
              action="action_quality_corrective_action"
              sequence="40"
              groups="group_quality_manager"/>

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

    <!-- Configuración -->
    <menuitem id="menu_quality_config"
              name="Configuración"
              parent="menu_quality_root"
              sequence="100"
              groups="group_quality_admin"/>

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
</odoo>
```

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
                <field name="product_id"/>
                <field name="project_task_id"/>
                <field name="requested_by"/>
                <field name="inspector_id"/>
                <field name="date_requested"/>
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
                    <button name="action_submit_inspection" string="Enviar a Inspección"
                            type="object" class="btn-primary"
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
                        <group>
                            <field name="project_task_id"/>
                            <field name="product_id"/>
                            <field name="requested_by"/>
                        </group>
                        <group>
                            <field name="inspector_id"/>
                            <field name="date_requested"/>
                            <field name="date_inspected"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Atributos de Inspección">
                            <field name="inspection_line_ids">
                                <list editable="bottom">
                                    <field name="sequence" widget="handle"/>
                                    <field name="name"/>
                                    <field name="attribute_type"/>
                                    <field name="value_float" invisible="attribute_type != 'float'"/>
                                    <field name="value_char" invisible="attribute_type not in ('char', 'selection')"/>
                                    <field name="value_boolean" invisible="attribute_type != 'boolean'"/>
                                    <field name="min_value" invisible="attribute_type != 'float'"/>
                                    <field name="max_value" invisible="attribute_type != 'float'"/>
                                    <field name="unit"/>
                                    <field name="result" widget="badge"
                                           decoration-success="result == 'cumple'"
                                           decoration-danger="result == 'no_cumple'"/>
                                </list>
                            </field>
                        </page>
                        <page string="Especificación PDF">
                            <group>
                                <field name="spec_pdf" filename="spec_pdf_name"/>
                                <field name="spec_pdf_name" invisible="1"/>
                            </group>
                            <div invisible="not spec_pdf" class="o_quality_pdf_preview">
                                <field name="spec_pdf" widget="pdf_viewer" readonly="1"/>
                            </div>
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

    <record id="view_quality_sample_release_kanban" model="ir.ui.view">
        <field name="name">quality.sample.release.kanban</field>
        <field name="model">quality.sample.release</field>
        <field name="arch" type="xml">
            <kanban default_group_by="state" class="o_kanban_small_column">
                <field name="name"/>
                <field name="product_id"/>
                <field name="state"/>
                <field name="requested_by"/>
                <templates>
                    <t t-name="card">
                        <field name="name" class="fw-bold"/>
                        <field name="product_id"/>
                        <field name="requested_by"/>
                        <field name="date_requested"/>
                    </t>
                </templates>
            </kanban>
        </field>
    </record>

    <record id="action_quality_sample_release" model="ir.actions.act_window">
        <field name="name">Liberación de Muestras</field>
        <field name="res_model">quality.sample.release</field>
        <field name="view_mode">list,form,kanban</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Crear solicitud de liberación de muestra
            </p>
        </field>
    </record>
</odoo>
```

## ./wizards/__init__.py
```py
from . import certificate_wizard
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
            vals['certified_hexagono'] = insp.hexagono or insp.oct_hexagono
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
        if self.include_retiramiento and insp.oct_retiramiento:
            vals['certified_retiramiento'] = insp.oct_retiramiento
        if self.include_calibracion and insp.calibracion:
            vals['certified_calibracion'] = insp.calibracion
        if self.include_engomado and insp.engomado:
            vals['certified_engomado'] = dict(
                insp._fields['engomado'].selection
            ).get(insp.engomado, '')

        cert = self.env['quality.certificate'].create(vals)

        # Vincular atributos adicionales si se solicitó
        if self.include_all_attributes and insp.line_ids:
            cert.attribute_ids = [(6, 0, insp.line_ids.ids)]

        return {
            'type': 'ir.actions.act_window',
            'name': _('Certificado'),
            'res_model': 'quality.certificate',
            'res_id': cert.id,
            'view_mode': 'form',
            'target': 'current',
        }
```

