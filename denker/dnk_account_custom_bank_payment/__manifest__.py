# -*- coding: utf-8 -*-
# See README.rst file on addons root folder for license details
{
    'name': "Denker - Account Custom Bank Payment",

    'summary': """
        Nombra el pago creado desde un "Extracto bancario" con el consecutivo correspondiente en vez de con el nombre del "Extracto bancario".
        """,

    'description': """
        1. Nombra el pago creado desde un "Extracto bancario" con el consecutivo correspondiente en vez de con el nombre del "Extracto bancario".
        2. Transfiere la cuenta bancaria del cliente de la línea del "Extracto bancario" hacia el pago resultante.
    """,

    'author': "José Candelas",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '12.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['account', 'l10n_mx_edi_payment_bank'],

    # always loaded
    'data': [
        #'views/res_config_settings_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
