# -*- coding: utf-8 -*-
# See README.rst file on addons root folder for license details
{
    'name': "Denker - Sale Pricelist Level",

    'summary': """
        Es posible cotizar con la listas de precios de igual o menor nivel (más caras) a la definida al cliente.
        """,

    'description': """
        Este módulo agrega el campo "Nivel" a las listas de precio, para ordenar las listas de más caras a más baratas,
        esto para que al cotizar a un cliente se restrinja el uso de Listas de Precios más baratas a la definida por el cliente.
    """,

    'author': "José Candelas",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Product',
    'version': '12.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['sale', 'dnk_groups_categories'],

    # always loaded
    'data': [
        'security/pricelist_security.xml',
        'views/pricelist_views.xml',
        'views/sale_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
