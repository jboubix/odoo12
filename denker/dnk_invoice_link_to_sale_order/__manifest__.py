# -*- coding: utf-8 -*-
{
    'name': "Denker - Relación entre Pedido y Factura",

    'summary': """
        Se agrega la relación para ligar el pedido con la factura.
    """,

    'description': """
        Se agrega la relación para ligar el pedido con la factura.

    """,

    'author': "Servicios Corporativos Denker - BC",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Account',
    'version': '11.0.1.1',
    # any module necessary for this one to work correctly
    'depends': ['base', 'sale','account'],

    # always loaded
    'data': [
        'views/account_invoice.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
