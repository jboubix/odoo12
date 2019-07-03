# © 2016 OdooMRP team
# © 2016 AvanzOSC
# © 2016 Serv. Tecnol. Avanzados - Pedro M. Baeza
# © 2016 Eficent Business and IT Consulting Services, S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# -*- coding: utf-8 -*-
{
    'name': "Denker - Account Supplier Invoice Picking Link",

    'summary': """
        Muestra el submenú Líneas de Pedidos dentro del menú Pedidos en la aplicación de Ventas, para mostrar una vista de lista de Líneas de Pedidos""",

    'author': "José Candelas",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '12.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['account', 'purchase'],

    # always loaded
    'data': [
        'views/account_supplier_invoice_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
