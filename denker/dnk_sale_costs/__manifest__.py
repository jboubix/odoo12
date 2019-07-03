# © 2016 OdooMRP team
# © 2016 AvanzOSC
# © 2016 Serv. Tecnol. Avanzados - Pedro M. Baeza
# © 2016 Eficent Business and IT Consulting Services, S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# -*- coding: utf-8 -*-
{
    'name': "Denker - Product Costs",

    'summary': """
        Agrega campos de costos a los productos y a las variantes de productos.
        También crea un grupo de usuarios que serán los que podrán ver este campo y el costo (standard_price)
        """,

    'description': """
    """,

    'author': "Servicios Corporativos Denker - BC",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales',
    'version': '12.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['product', 'sale', 'base', 'mrp'],

    # always loaded
    'data': [
        'views/product_views.xml',
        'views/res_company.xml',
        'views/costs.xml',
        'security/ir.model.access.csv',
        'security/res_groups.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
