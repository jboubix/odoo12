# -*- coding: utf-8 -*-
{
    'name': "Denker - Customer Product Code",

    'summary': """
        Módulo para agregar el Código del producto del Cliente.
    """,

    'description': """
        Módulo para agregar el Código del producto del Cliente.

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
        'views/product_template.xml',
        'views/account_invoice.xml',
        'views/sale_order.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
