# -*- encoding: utf-8 -*-
from odoo import api, fields, models, _

class StockQuant(models.Model):
    _inherit = "stock.quant"

    dnk_standard_price = fields.Float(string='- Cost', related='product_tmpl_id.standard_price', track_visibility='onchange')
