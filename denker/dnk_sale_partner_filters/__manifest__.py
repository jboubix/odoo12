# -*- coding: utf-8 -*-
{
    'name': "Denker - Partner Filter in Sale Order",

    'summary': """
        Módulo para agregar Filtros a los Clientes en el Pedido.
    """,

    'description': """
        Módulo para agregar Filtros a los Clientes en el Pedido.

    """,

    'author': "Servicios Corporativos Denker - BC",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Products',
    'version': '11.0.1.1',
    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'sale'],

    # always loaded
    'data': [
        'views/sale_order.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
