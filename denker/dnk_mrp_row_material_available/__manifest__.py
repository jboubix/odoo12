# © 2016 OdooMRP team
# © 2016 AvanzOSC
# © 2016 Serv. Tecnol. Avanzados - Pedro M. Baeza
# © 2016 Eficent Business and IT Consulting Services, S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': "Denker - MRP Row Material Available",

    'summary': """
        Este módulo impide terminar una order de producción si las materias primas no están totalmente disponibles.""",

    'description': """
        Este módulo impide terminar una order de producción si las materias primas no están totalmente disponibles.
Esconde los botones "MARCAR COMO HECHO" y "REGISTRAR INVENTARIO" si la Disponibilidad es diferente a "Reservado".
Crea el grupo "Finish Production without Materials Available", el cual puede terminar una MO sin tener todo las Materias Primas Disponibles.""",

    'author': "José Candelas",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Manufacturing',
    'version': '12.0.1.0',

    # any module necessary for this one to work correctly
    'depends': ['mrp', 'dnk_groups_categories'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/mrp_security.xml',
        'views/mrp_production_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
