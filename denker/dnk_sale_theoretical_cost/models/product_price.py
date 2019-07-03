# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo.addons import decimal_precision as dp
from odoo import models, fields, api

class PricelistItem(models.Model):
    _inherit = "product.pricelist.item"


    base = fields.Selection([
        ('list_price', 'Public Price'),
        ('standard_price', 'Cost'),
        ('dnk_theoretical_cost_converted', 'Theoretical Cost'),
        ('pricelist', 'Other Pricelist')], "Based on",
        default='list_price', required=True,
        help='Base price for computation.\n'
             'Public Price: The base price will be the Sale/public Price.\n'
             'Cost Price : The base price will be the cost price.\n'
             'Theoretical Cost : The base price will be the theoretical cost price.\n'
             'Other Pricelist : Computation of the base price based on another Pricelist.')
