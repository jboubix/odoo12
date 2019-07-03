# -*- coding: utf-8 -*-
{
    'name': "Denker - Quality Alert Mods",

    'summary': """
        Módulo para la hacer cambios a las vistas de las alertas de calidad.
    """,

    'description': """
        Módulo para hacer cambios a las vistas de las alertas de calidad.
    """,

    'author': "Servicios Corporativos Denker - BC",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'MRM',
    'version': '11.0.1.1',
    # any module necessary for this one to work correctly
    'depends' : ['account', 'sale', 'mrp'],

    # always loaded
    'data': [
        'views/quality_alerts.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
