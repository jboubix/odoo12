# -*- coding: utf-8 -*-
{
    'name': "Denker - Product Development",

    'summary': """
        Módulo para Desarrollo de Productos.
    """,

    'description': """
        Módulo para Desarrollo de Productos.

    """,

    'author': "Servicios Corporativos Denker - BC",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'MRM',
    'version': '11.0.1.1',
    # any module necessary for this one to work correctly
    'depends' : ['sale_crm', 'account', 'dnk_crm_opportunities', 'dnk_groups_categories'],

    # always loaded
    'data': [
        'data/ir_sequence.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/ir_attachment.xml',
        'views/product_development.xml',
        'views/crm.xml',
        'views/product_category.xml',
        'data/dnk_crm_pd_materials.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
