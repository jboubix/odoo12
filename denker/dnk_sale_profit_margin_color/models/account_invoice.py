# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _



class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    dnk_profit_margin_color = fields.Char('- Color')
    dnk_profit_margin_html = fields.Char('- ', readonly=True)
    dnk_profit_margin_ratio = fields.Float('- Margin Ratio')

    @api.onchange('price_unit','discount')
    def dnk_onchange_price(self):
        self.dnk_getmargin_profit()


    @api.onchange('product_id')
    def _onchange_product_id(self):
        res = super(AccountInvoiceLine, self)._onchange_product_id()
        self.dnk_getmargin_profit()
        return res

    def dnk_get_color(self):
        if self.dnk_profit_margin_ratio >= 0.5:
            self.dnk_profit_margin_html = "<div style='text-align:center height: 25px; width: 25px; background-color: #0040FF; border-radius: 50%; display: inline-block;'> <span>&nbsp;</span></div>";
            self.dnk_profit_margin_color = "Blue"
        elif self.dnk_profit_margin_ratio >= 0.4:
            self.dnk_profit_margin_html = "<div style='text-align:center height: 25px; width: 25px; background-color: #04B404; border-radius: 50%; display: inline-block;'> <span>&nbsp;</span></div>";
            self.dnk_profit_margin_color = "Green"
        elif self.dnk_profit_margin_ratio >= 0.3:
            self.dnk_profit_margin_html = "<div style='text-align:center height: 25px; width: 25px; background-color: #FFFF00; border-radius: 50%; display: inline-block;'> <span>&nbsp;</span></div>";
            self.dnk_profit_margin_color = "Yellow"
        elif self.dnk_profit_margin_ratio >= 0.2:
            self.dnk_profit_margin_html = "<div style='text-align:center height: 25px; width: 25px; background-color: #A4A4A4; border-radius: 50%; display: inline-block;'> <span>&nbsp;</span></div>";
            self.dnk_profit_margin_color = "Gray"
        else:
            self.dnk_profit_margin_html = "<div style='text-align:center height: 25px; width: 25px; background-color: #000000; border-radius: 50%; display: inline-block;'> <span>&nbsp;</span></div>";
            self.dnk_profit_margin_color = "Black"


    def dnk_getmargin_profit(self):
        if self.price_unit > 0 and self.product_id.dnk_cost_mp > 0:
            # Primero checar la moneda de sale order
            if self.invoice_id.currency_id == self.product_id.dnk_costs_currency_id:
                self.dnk_profit_margin_ratio =(self.price_unit-(self.product_id.dnk_cost_mp+self.product_id.dnk_cost_mo+self.product_id.dnk_cost_gif))/self.price_unit
                self.dnk_get_color()
            else :
                #Lo haré sólo tomando en cuenta la moneda del precio
                #porque se supone que el precio siempre estará en USD
                # y como siempre está el producto en USD y son diferentes, entonces la lista de precios es MXN
                #if self.product_id.dnk_costs_currency_id.name == 'MXN':
                    self.dnk_profit_margin_ratio = ((self.price_unit/self.invoice_id.company_id.dnk_usd_cost_fixed_rate)-(self.product_id.dnk_cost_mp+self.product_id.dnk_cost_mo+self.product_id.dnk_cost_gif))/(self.price_unit/self.invoice_id.company_id.dnk_usd_cost_fixed_rate)
                    self.dnk_get_color()
                #else :
                #    self.dnk_profit_margin_ratio = ((self.invoice_id.company_id.dnk_usd_cost_fixed_rate/self.price_unit)-(self.product_id.dnk_cost_mp+self.product_id.dnk_cost_mo+self.product_id.dnk_cost_gif))/(self.invoice_id.company_id.dnk_usd_cost_fixed_rate/self.price_unit)
                #    self.dnk_get_color()

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    def _write(self, vals):
        for rec in self:
            for linea in rec.invoice_line_ids:
                linea.dnk_getmargin_profit()
        res = super(AccountInvoice, self)._write(vals)
        return res
