# -*- coding: utf-8 -*-
{
    'name': "Denker - Account Custom Views",

    'summary': """
        Este módulo hace cambios de Vistas de Contabilidad requeridos por Grupo Denker""",

    'description': """
        Mostrar el campo Concepto (communication) en la vista de lista de Pagos (account_payment).
    """,

    'author': "José Candelas",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales',
    'version': '12.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['sale', 'dnk_groups_categories'],

    # always loaded
    'data': [
        #'security/sale_order_security.xml',
        'views/account_payment_views.xml',
        'views/account_analytic_line_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
