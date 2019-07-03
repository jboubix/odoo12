# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools

class AddAmountUSDtoSaleOrder(models.Model):
    _inherit = "account.invoice"

    @api.multi
    @api.depends('amount_untaxed','currency_id','residual')
    def _update_untaxed_amount_usd(self):
        res_currency_rate = self.env['res.currency.rate']
        date = self._context.get('date') or fields.Datetime.now()
        res_currency_usd_id = self.env['res.currency'].search([('name', '=', 'USD')]).id
        for rec in self:
            if rec.currency_id.name  == 'USD':
                rec.dnk_amount_untaxed_usd = rec.amount_untaxed
                rec.dnk_residual_usd = rec.residual
            elif rec.currency_id.name  == 'MXN':
                exchange_rate = res_currency_rate.search([('currency_id', '=', res_currency_usd_id), ('name', '<=', date)], limit=1, order="name desc").rate
                rec.dnk_amount_untaxed_usd = rec.amount_untaxed * exchange_rate
                rec.dnk_residual_usd = rec.residual * exchange_rate


    dnk_amount_untaxed_usd = fields.Float('- Untaxed Amount USD', compute="_update_untaxed_amount_usd", store=True)
    dnk_residual_usd = fields.Float('- Residual USD', compute="_update_untaxed_amount_usd", store=True)
