# -*- coding: utf-8 -*-
{
    'name': 'Denker - Quotation by Volume',

    'summary': """
        This module adds automatically Sale Order Lines by Volume.
        The quantity of lines to add are the quantity of times de product appears in the Pricelist.
    """,

    'author': "Grupo Denker - José Candelas - jcandelas@grupodenker.com",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sale',
    'version': '12.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'dnk_sale_order_commitment_date', 'dnk_product_customer_code', 'dnk_sale_pricelist_fixed_rate'], #

    # always loaded
    'data': [
        'views/product_views.xml',
        'views/sale_order_line_views.xml',
        'views/sale_report_templates.xml',
        'views/sale_order_views.xml',
    ],
}
