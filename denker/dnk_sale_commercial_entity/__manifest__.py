# -*- coding: utf-8 -*-
{
        'name': 'Denker - Commercial Entity',

    'summary': """
        This module adds the Commercial Entity field to Sale Order.
    """,

    'description': """
        This module adds the Commercial Entity field to Sale Order.

    """,

    'author': "Servicios Corporativos Denker - BC",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sale',
    'version': '11.0.1.1',
    # any module necessary for this one to work correctly
    'depends': ['sale', 'dnk_sale_order_line_menu'],

    # always loaded
    'data': [
        'views/sale_order.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
