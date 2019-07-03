{
    "name": "Denker - Customer Export Information",
    "version": "12.0.1",
    'author': 'Servicios Corporativos Denker - BC',
    'website': 'www.grupodenker.com',
    'license': 'AGPL-3',
    "category": "Accounting",
    'summary': 'Módulo para agregar una etiqueta que se agregará al PDF de facturas cuando es una exportación.',
    "description": """  Módulo para agregar etiqueta a la factura de exportación. """,
    'depends': ['account'],
    'data': [
        #'views/account_invoice.xml',
        'views/report_invoice.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
}
