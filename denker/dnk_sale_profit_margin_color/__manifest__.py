# -*- coding: utf-8 -*-
{
    'name': "Denker - Profit Margin Color",

    'summary': """
        Módulo para asignar color de acuerdo al margen de utilidad.
    """,

    'description': """
        Módulo para asignar color de acuerdo al margen de utilidad
    """,

    'author': "Servicios Corporativos Denker - BC",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'CRM',
    'version': '11.0.1.1',
    # any module necessary for this one to work correctly
    'depends' : ['account','sale', 'dnk_sale_costs'],

    # always loaded
    'data': [
        #'data/ir_sequence.xml',
        #'security/res_groups.xml',
        #'security/ir.model.access.csv',
        #'views/ir_attachment.xml',
        'views/sale_order.xml',
        'views/account_invoice.xml',
        #'views/crm.xml',
        #'views/product_category.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
