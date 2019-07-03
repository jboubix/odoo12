# -*- coding: utf-8 -*-
{
    'name': 'Denker - Account Invoice Template',

    'summary': """
        Este módulo modifica el diseño de la factura para que cumpla con las características necesarias para Grupo Denker.
    """,

    'description': """
        1. Al facturar a un contacto de un cliente, eliminar el nombre del contacto para dejar solamente el nombre de la empresa.
    """,

    'author': "Grupo Denker - José Candelas - jcandelas@grupodenker.com",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '12.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['account'],

    # always loaded
    'data': [
        'views/report_invoice.xml',
    ],
}
