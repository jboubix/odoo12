# -*- coding: utf-8 -*-
{
        'name': 'Denker - Promise to Pay',

    'summary': """
        This module adds a Promise to Pay field to Account Invoice.
    """,

    'description': """
        This module adds a Promise to Pay field to Account Invoice.

    """,

    'author': "Servicios Corporativos Denker - BC",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Account',
    'version': '11.0.1.1',
    # any module necessary for this one to work correctly
    'depends': ['account', 'dnk_sale_order_line_menu'],

    # always loaded
    'data': [
        'views/account_invoice.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
