# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import string


class AccountMove(models.Model):
    _inherit = 'account.move'

    dnk_product_default_code = fields.Char(string='- Product Internal Reference', related='stock_move_id.product_id.default_code')


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    dnk_product_default_code = fields.Char(string='- Product Internal Reference', related='product_id.default_code')
