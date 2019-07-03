#  GNU nano 2.5.3                                                      Archivo: hooks.py

# Copyright 2004 Tiny SPRL
# Copyright 2016 Sodexis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, SUPERUSER_ID


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    res_ids = env['mrp.production'].search([
        ('origin', '!=', False),
    ]).mapped('id')
    env['mrp.production'].browse(res_ids)._compute_sale_order_by_origin()
