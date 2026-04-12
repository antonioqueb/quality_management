{
    'name': 'Gestión de Calidad - Hexágonos Mexicanos',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing/Quality',
    'summary': 'Módulo integral de gestión de calidad para industria del cartón',
    'description': """
        Gestión de Calidad para Hexágonos Mexicanos
        =============================================
        - Liberación de Muestras
        - Liberación de Planos
        - Inspección de PP y PT (Laminadora, Octágono, Guillotina)
        - Generación de Certificados
        - Acciones Correctivas/Preventivas
        - Devolución de Clientes (8D)
        - Documentos solicitados por clientes
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
        'data/cron_data.xml',
        # Wizards
        'wizards/certificate_wizard_views.xml',
        # Views (actions defined here)
        'views/quality_attribute_template_views.xml',
        'views/quality_sample_release_views.xml',
        'views/quality_drawing_release_views.xml',
        'views/quality_inspection_views.xml',
        'views/quality_certificate_views.xml',
        'views/quality_corrective_action_views.xml',
        'views/quality_customer_return_views.xml',
        'views/quality_customer_document_views.xml',
        'views/quality_dashboard_views.xml',
        # Menus (AFTER views so actions exist)
        'views/quality_menus.xml',
        # Reports
        'reports/report_quality_certificate.xml',
        'reports/report_8d.xml',
        'reports/report_inspection_summary.xml',
    ],
    'assets': {},
    'installable': True,
    'application': True,
    'auto_install': False,
}