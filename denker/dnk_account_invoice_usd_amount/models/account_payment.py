# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools

class AddAmountUSDtoAccountPayment(models.Model):
    _inherit = "account.payment"

    @api.depends('amount','currency_id')
    def _update_amount_usd(self):
        res_currency_rate = self.env['res.currency.rate']
        date = self._context.get('date') or fields.Datetime.now()
        res_currency_usd_id = self.env['res.currency'].search([('name', '=', 'USD')]).id

        for rec in self:
            if rec.currency_id.name  == 'USD':
                rec.dnk_amount_usd = rec.amount
            elif rec.currency_id.name  == 'MXN':
                exchange_rate = res_currency_rate.search([('currency_id', '=', res_currency_usd_id), ('name', '<=', date)], limit=1, order="name desc").rate
                rec.dnk_amount_usd = rec.amount * exchange_rate


    dnk_amount_usd = fields.Float('- Amount USD', compute="_update_amount_usd", store=True)
