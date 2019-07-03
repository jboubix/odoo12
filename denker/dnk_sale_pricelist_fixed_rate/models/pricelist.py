# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError, RedirectWarning
import odoo.addons.decimal_precision as dp
from odoo.api import Environment


class Pricelist(models.Model):
    _inherit = "product.pricelist"

    dnk_use_usd_fixed_rate = fields.Boolean(
                            string='- Use USD Fixed Rate',
                            help='If checked, the price list use de USD Fixed Rate to convert prices',
                            default=False)
