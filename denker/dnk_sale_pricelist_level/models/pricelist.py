# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError, RedirectWarning
import odoo.addons.decimal_precision as dp
from odoo.api import Environment


class Pricelist(models.Model):
    _inherit = "product.pricelist"

    dnk_pricelist_level = fields.Integer(
                            string='Pricelist Level',
                            help='Lower level is cheaper and higher is more expensive',
                            default=10)
