# -*- coding: utf-8 -*-
# See README.rst file on addons root folder for license details
{
    'name': "Denker - Product Hide Cost and Sale Price",

    'summary': """
        Con este módulo es posible esconder el costo de los productos.
        """,

    'description': """
        Con este módulo es posible esconder el costo de los productos. Excepto a un grupo de usuarios
    """,

    'author': "José Candelas",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Product',
    'version': '12.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['product', 'dnk_groups_categories', 'dnk_sale_theoretical_cost', 'dnk_product_price_currency'],

    # always loaded
    'data': [
        'security/security.xml',
        'views/product_hide_cost.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
