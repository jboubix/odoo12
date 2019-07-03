{
    "name": "Denker - Restrict Purchase Orders Lines",
    "version": "11.0.1",
    'author': 'Servicios Corporativos Denker - BC',
    'website': 'www.grupodenker.com',
    'license': 'AGPL-3',
    "category": "Base",
    'summary': 'Módulo para restringir la edición de las líneas de la Orden de Compra.',
    "description": """ Módulo para restringir la edición de las líneas de la Orden de Compra.""",
    'depends': ['base','purchase'],
    'data': [
        'views/purchase_order.xml',
        'views/res_groups.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
}
