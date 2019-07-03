# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta
from odoo import api, fields, models, _
import string


class QualityAlert(models.Model):
    _inherit = 'quality.alert'

    dnk_subfamily = fields.Many2one('product.category', string='- Subfamily', related='product_tmpl_id.categ_id', store=True)
    dnk_family = fields.Many2one('product.category', string='- Family', related='dnk_subfamily.parent_id', store=True)
    dnk_color = fields.Many2one('product.category', string='- Color', related='dnk_family.parent_id', store=True)
    dnk_product_default_code = fields.Char(string='- Product Internal Reference', compute='_get_product_default_code', store=True)

    @api.multi
    @api.depends('product_id', 'product_id.default_code')
    def _get_product_default_code(self):
        for production in self:
            production.dnk_product_default_code = production.product_id.default_code
