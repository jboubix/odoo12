# -*- coding: utf-8 -*-
# See README.rst file on addons root folder for license details
{
    'name': "Denker - Product Price Currency",

    'summary': """
        Con este módulo es posible determinar la moneda del precio de venta de un producto.
        """,

    'description': """
        Con este módulo es posible determinar la moneda del precio de venta de un producto.
    """,

    'author': "José Candelas",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Product',
    'version': '12.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['product'],

    # always loaded
    'data': [
        'views/product_view.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
