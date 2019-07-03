# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools

class AddAmountUSDtoSaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.multi
    @api.depends('price_subtotal')
    def _update_price_subtotal_usd(self):
        res_currency_rate = self.env['res.currency.rate']
        date = self._context.get('date') or fields.Datetime.now()
        res_currency_usd_id = self.env['res.currency'].search([('name', '=', 'USD')]).id
        for rec in self:
            if rec.order_id.pricelist_id.currency_id.name  == 'USD':
                rec.dnk_price_subtotal_usd = rec.price_subtotal
            elif rec.order_id.pricelist_id.currency_id.name  == 'MXN':
                exchange_rate = res_currency_rate.search([('currency_id', '=', res_currency_usd_id), ('name', '<=', date)], limit=1, order="name desc").rate
                rec.dnk_price_subtotal_usd = rec.price_subtotal * exchange_rate

    dnk_price_subtotal_usd = fields.Float('- Subtotal USD', compute="_update_price_subtotal_usd", store=True)
