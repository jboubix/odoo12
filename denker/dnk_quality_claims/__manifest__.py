# -*- coding: utf-8 -*-
{
    'name': "Denker - Quality Claims",

    'summary': """
        Módulo para la administración de quejas.
    """,

    'description': """
        Módulo para la administración de quejas.
    """,

    'author': "Servicios Corporativos Denker - BC",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'MRM',
    'version': '11.0.1.1',
    # any module necessary for this one to work correctly
    'depends' : ['account', 'sale'],

    # always loaded
    'data': [
        'data/ir_sequence.xml',
        'data/quality_claims_stages.xml',
        'data/quality_claims_tags.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        #'views/ir_attachment.xml',
        'views/quality_claims.xml',
        #'views/crm.xml',
        #'views/product_category.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
