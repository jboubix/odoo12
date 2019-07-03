# -*- coding: utf-8 -*-
{
    'name': "Denker - Account Payment Solution",

    'summary': """
        Add Payment Solution Field to Invoice""",

    'description': """
        Add Payment Solution Field to Invoice".
    """,

    'author': "Servicios Corporativos Denker - BC",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full lis
    'category': 'Account',
    'version': '10.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['account'],

    # always loaded
    'data': [
        'data/payment_solutions.xml',
        'views/account_invoice.xml',
        # 'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/account_payment_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
