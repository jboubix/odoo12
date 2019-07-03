# -*- coding: utf-8 -*-
{
    'name': "Denker - Sale Custom Views",

    'summary': """
        Este módulo hace cambios de Vistas de Ventas requeridos por Grupo Denker""",

    'description': """
        Oculta el botón de "Crear" en Cotizaciones y Pedidos de Ventas.
        Muestra el botón "Enviar por Correo" en un Pedido de Venta en estado "Hecho".
    """,

    'author': "José Candelas",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales',
    'version': '12.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['sale', 'purchase', 'dnk_groups_categories'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/sale_order_security.xml',
        'views/sale_order_views.xml',
        'views/product_template_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
