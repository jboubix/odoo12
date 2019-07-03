# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _

class ProductAttribute(models.Model):
    _inherit = 'product.attribute'

    show_in_invoice = fields.Boolean(
        string='Show in Invoice', default=True,
        help='If checked, this Attribute will be shown in Invoice Lines Description.', required=True)
