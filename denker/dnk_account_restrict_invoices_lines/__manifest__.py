{
    "name": "Denker - Restrict Account Invoice Lines",
    "version": "12.0.1",
    'author': 'Servicios Corporativos Denker - BC',
    'website': 'www.grupodenker.com',
    'license': 'AGPL-3',
    "category": "Base",
    'summary': 'Módulo para restringir la edición de las líneas de la factura.',
    "description": """ Módulo para restringir la edición de las líneas de la factura.""",
    'depends': ['base','account'],
    'data': [
        'views/account_invoice.xml',
        'views/res_groups.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
}
