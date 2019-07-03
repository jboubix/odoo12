# © 2016 OdooMRP team
# © 2016 AvanzOSC
# © 2016 Serv. Tecnol. Avanzados - Pedro M. Baeza
# © 2016 Eficent Business and IT Consulting Services, S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# -*- coding: utf-8 -*-
{
    'name': "Denker - Account Invoice Line Short Name",

    'summary': """
        Acorta los nombres de los productos de la variantes en la líneas de la facturas.
    """,

    'description': """
        Acorta los nombres de los productos de la variantes en la líneas de la facturas.
        Se agrega un campo en los atributos para seleccionar cual sí o cual no aparecerá en las facturas.
    """,

    'author': "José Candelas",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '12.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['account', 'sale', 'product'],

    # always loaded
    'data': [
        'views/product_attribute_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
