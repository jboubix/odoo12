# -*- coding: utf-8 -*-

{
    "name": "Denker - Credit Limit Groups",
    "version": "12.0.1",
    'author': 'Servicios Corporativos Denker - BC',
    'website': 'www.grupodenker.com',
    'license': 'AGPL-3',
    'summary': 'Actualizar grupos a los campos del módulo de Límite de crédito.',
    "category": "Account Invoice",
    "description": """ Actualizar grupos a los campos del módulo de Límite de crédito.""",
    'depends': ['account', 'sale','dnk_groups_categories','credit_limit_alert'],
    'data': [
            'security/res_groups.xml',
            'views/res_partner.xml',
            'views/sale_order.xml',
            'views/account_invoice.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
}
