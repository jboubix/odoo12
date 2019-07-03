{
    "name": "Denker - Add Untaxed USD Amount to Sale Order",
    "version": "11.0.1",
    'author': 'Servicios Corporativos Denker - BC',
    'website': 'www.grupodenker.com',
    'license': 'AGPL-3',
    "category": "Sale Order",
    'summary': 'Se agrega el campo de monto en USD a Pedidos de Venta y Cotizaciones.',
    "description": """ This module add Untaxed USD amount in Sale Order and Sale Order Line .""",
    'depends': ['sale'],
    'data': [
        'views/sale_order.xml',
        'views/crm.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
}
