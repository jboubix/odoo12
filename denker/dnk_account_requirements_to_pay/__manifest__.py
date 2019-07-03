# -*- coding: utf-8 -*-
{
    'name': "Denker Client Requirements to pay",

    'summary': """
        Client Requirements to pay""",

    'description': """
        Adds to invoice the field "client requirements to pay".
    """,

    'author': "Servicios Corporativos Denker - BC",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full lis
    'category': 'Account Invoice',
    'version': '10.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['account','dnk_account_payment_solution'],

    # always loaded
    'data': [
        'data/requirements_to_pay_data.xml',
        'views/account_invoice.xml',
        #'security/res_groups.xml',
        'security/ir.model.access.csv',
        # 'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
