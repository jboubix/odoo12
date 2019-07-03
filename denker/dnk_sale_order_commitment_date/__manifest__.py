# © 2016 OdooMRP team
# © 2016 AvanzOSC
# © 2016 Serv. Tecnol. Avanzados - Pedro M. Baeza
# © 2016 Eficent Business and IT Consulting Services, S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# -*- coding: utf-8 -*-
{
    'name': "Denker - Sale Order Commitment Date",

    'summary': """
        Muestra el campo "Fecha de compromiso" al Reporte del Pedido (PDF).""",

    'author': "José Candelas",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales',
    'version': '12.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['sale', 'crm'],

    # always loaded
    'data': [
        'views/mail_commitment_date_template_data.xml',
        'wizard/sale_order_line_set_recommitment_date_view.xml',
        'views/crm_team_views.xml',
        'views/partner_views.xml',
        'views/sale_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
