# -*- coding: utf-8 -*-
{
    'name': "Denker - Account Followup Mail",

    'summary': """
        This module change the default recipient of the Followup Mail from the Invoice Contact to the email of the partner.""",

    'author': "José Candelas",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Account',
    'version': '12.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['account', 'account_reports'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/report_followup.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
