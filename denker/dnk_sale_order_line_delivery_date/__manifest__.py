# © 2016 OdooMRP team
# © 2016 AvanzOSC
# © 2016 Serv. Tecnol. Avanzados - Pedro M. Baeza
# © 2016 Eficent Business and IT Consulting Services, S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Sale Order Line Date",
    "version": "11.0.1.0.0",
    "author": "OdooMRP team,"
              "AvanzOSC,"
              "Serv. Tecnol. Avanzados - Pedro M. Baeza,"
              "Odoo Community Association (OCA)",
    "website": "https://odoo-community.org/",
    "category": "Sales Management",
    "license": "AGPL-3",
    "depends": [
        "sale_order_dates",
    ],
    "data": [
        "views/sale_order_view.xml",
    ],
    "installable": True,

    'name': "Denker - Sale Order Line Deliveries",

    'summary': """
        Este módulo agrega el campo: Días de Entrega y Feche de en tregahace cambios de Vistas de Ventas requeridos por Grupo Denker""",

    'author': "José Candelas",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales',
    'version': '12.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['sale', 'crm', 'sale_order_line_date'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/sale_order_security.xml',
        'views/sale_order_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
