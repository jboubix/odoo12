# -*- coding: utf-8 -*-
{
    'name': "Denker - Orden de Compra",

    'summary': """
        Se agregan los campos para guardar un documento para la orden de compra y en el pedido de venta
        para que se adjunte en el correo de la factura.
    """,

    'description': """
        Se agregan los campos para guardar un documento para la orden de compra y en el pedido de venta
        para que se adjunte en el correo de la factura.

    """,

    'author': "Servicios Corporativos Denker - BC",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'CRM',
    'version': '11.0.1.1',
    # any module necessary for this one to work correctly
    'depends': ['base', 'sale','account','dnk_invoice_link_to_sale_order'],

    # always loaded
    'data': [
        'views/res_partner.xml',
        'views/sale_order.xml',
        'views/account_invoice.xml',
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}
