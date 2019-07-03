# © 2016 OdooMRP team
# © 2016 AvanzOSC
# © 2016 Serv. Tecnol. Avanzados - Pedro M. Baeza
# © 2016 Eficent Business and IT Consulting Services, S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': "Denker - Purchase Order and Production Order to Sale Order Link",

    'summary': """
        Este módulo agrega un enlace de las Orden de Producción o de las Líneas de Orden de Compra hacia las Líneas de Pedidos de Ventas y viceversa.""",

    'author': "José Candelas",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales',
    'version': '12.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['sale', 'mrp', 'purchase', 'dnk_groups_categories', 'web_tree_dynamic_colored_field'],

    # always loaded
    'data': [
        'security/security.xml',
        'views/mrp_production_views.xml',
        #'views/purchase_order_views.xml',
        'views/sale_order_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'post_init_hook': 'post_init_hook',
}
