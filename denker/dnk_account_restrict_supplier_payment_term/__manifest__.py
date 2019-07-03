{
    "name": "Denker - Restrict Supplier Payment Term",
    "version": "11.0.1",
    'author': 'Servicios Corporativos Denker - BC',
    'website': 'www.grupodenker.com',
    'license': 'AGPL-3',
    "category": "Base",
    'summary': 'Módulo para restringir el plazo de pago del Proveedor.',
    "description": """ Módulo para restringir el plazo de pago del Proveedor.""",
    'depends': ['base'],
    'data': [
        'views/res_groups.xml',
        'views/res_partner.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
}
