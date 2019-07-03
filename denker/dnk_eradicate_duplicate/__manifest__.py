# © 2016 OdooMRP team
# © 2016 AvanzOSC
# © 2016 Serv. Tecnol. Avanzados - Pedro M. Baeza
# © 2016 Eficent Business and IT Consulting Services, S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': "Denker - Eradicate Duplicate",

    'summary': """
        Este módulo erradica la acción "Duplicar" en la vista de formulario algunos modelos.
        """,

    'description': """
        Este módulo erradica la acción "Duplicar" en la vista de formulario para los siguientes modelos:
            1) Manufacturing Order (mrp.production)
            2) Transfer (stock.picking)
            3) Out Invoice (account.invoice)
            4) Out Refunds (account.invoice)
    """,

    'author': "José Candelas",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Tools',
    'version': '12.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['mrp', 'stock'],

    # always loaded
    'data': [
        'security/account_invoice_security.xml',
        'views/mrp_production_views.xml',
        'views/stock_picking_views.xml',
        'views/account_invoice_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
