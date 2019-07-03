# -*- coding: utf-8 -*-
{
    'name': "Denker - CRM Opportunities",

    'summary': """
        Se gregan a las oportunidades campos adicionales como Familia y Subfamilia.
    """,

    'description': """
        Se gregan a las oportunidades campos adicionales como Familia y Subfamilia.

    """,

    'author': "Servicios Corporativos Denker - BC",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'CRM',
    'version': '11.0.1.1',
    # any module necessary for this one to work correctly
    'depends': ['base','crm','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/crm_view.xml',
        'views/res_partner.xml',
        #'views/sale_order.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
