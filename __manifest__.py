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
        'views/res_company_views.xml',
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
}