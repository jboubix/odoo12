# -*- coding: utf-8 -*-
from odoo import api, fields, models


class InvoiceToSaleOrder(models.Model):
    _inherit = "account.invoice"

    dnk_sale_order = fields.Many2one('sale.order', string='- Sale Order', store=True, copy=True)
