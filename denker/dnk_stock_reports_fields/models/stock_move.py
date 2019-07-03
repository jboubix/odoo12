# -*- encoding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp

class StockMove(models.Model):
    _inherit = "stock.move"

    dnk_subfamily = fields.Many2one('product.category',string='- Subfamily', related='product_id.product_tmpl_id.categ_id', track_visibility='onchange')
    dnk_family = fields.Many2one('product.category',string='- Family', related='dnk_subfamily.parent_id', track_visibility='onchange')
    dnk_color = fields.Many2one('product.category',string='- Color', related='dnk_family.parent_id', track_visibility='onchange')
    dnk_standard_price = fields.Float(
        string='Cost',
        digits=dp.get_precision('Product Price'),
        related='product_id.standard_price',
        groups="base.group_user",
        help = "Cost used for stock valuation in standard price and as a first price to set in average/fifo. "
               "Also used as a base price for pricelists. "
               "Expressed in the default unit of measure of the product.")
    dnk_theoretical_cost = fields.Float(
        string="- Theoretical Cost",
        related='product_id.dnk_theoretical_cost',
        digits=dp.get_precision('Product Price'), groups="base.group_user")
    dnk_theoretical_cost_currency_id = fields.Many2one(
        'res.currency', string='- Theoretical Cost Currency',
        related='product_id.dnk_theoretical_cost_currency_id')
    dnk_mo_date_planned_start = fields.Datetime(
        string='- MO Deadline Start', copy=False, store=True,
        compute='get_mo_date_planned_start')

    @api.multi
    @api.depends('raw_material_production_id', 'raw_material_production_id.date_planned_start')
    def get_mo_date_planned_start(self):
        for stock_move in self:
            stock_move.dnk_mo_date_planned_start = stock_move.raw_material_production_id.date_planned_start


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    dnk_subfamily = fields.Many2one('product.category',string='- Subfamily', related='product_id.product_tmpl_id.categ_id', track_visibility='onchange')
    dnk_family = fields.Many2one('product.category',string='- Family', related='dnk_subfamily.parent_id', track_visibility='onchange')
    dnk_color = fields.Many2one('product.category',string='- Color', related='dnk_family.parent_id', track_visibility='onchange')
