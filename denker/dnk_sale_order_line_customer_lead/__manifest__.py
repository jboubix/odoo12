# © 2016 OdooMRP team
# © 2016 AvanzOSC
# © 2016 Serv. Tecnol. Avanzados - Pedro M. Baeza
# © 2016 Eficent Business and IT Consulting Services, S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# -*- coding: utf-8 -*-
{
    'name': "Denker - Sale Order Line Customer Lead",

    'summary': """
        Agrega el campo "Días de Entrega" a las líneas de una Order de Venta,
        de acuerdo a la política de entrega definida en el producto (campo "Plazo de entrega del cliente")""",

    'author': "José Candelas",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales',
    'version': '12.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['sale', 'dnk_sale_order_commitment_date'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'security/sale_order_security.xml',
        'views/sale_order_line_views.xml',
        'views/sale_report_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
