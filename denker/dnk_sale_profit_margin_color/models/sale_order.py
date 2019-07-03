# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    dnk_profit_margin_color = fields.Char('- Color')
    dnk_profit_margin_html = fields.Char('- ', readonly=True)
    dnk_profit_margin_ratio = fields.Float('- Margin Ratio')


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
        if self.price_unit and  self.price_unit > 0:
            dnk_price = self.price_unit
        else:
            dnk_price = self.product_id.price
        print (self.product_id.dnk_cost_mp+self.product_id.dnk_cost_mo+self.product_id.dnk_cost_gif)
        if dnk_price > 0 and self.product_id.dnk_cost_mp > 0:
            # Primero checar la moneda de sale order
            if self.order_id.pricelist_id.currency_id == self.product_id.dnk_costs_currency_id:
                self.dnk_profit_margin_ratio =(dnk_price-(self.product_id.dnk_cost_mp+self.product_id.dnk_cost_mo+self.product_id.dnk_cost_gif))/dnk_price
                self.dnk_get_color()
            else :
                #Lo haré sólo tomando en cuenta la moneda del precio
                #porque se supone que el precio siempre estará en USD
                # y como siempre está el producto en USD y son diferentes, entonces la lista de precios es MXN
                #if self.product_id.dnk_costs_currency_id.name == 'MXN':
                self.dnk_profit_margin_ratio = ((dnk_price/self.order_id.company_id.dnk_usd_cost_fixed_rate)-(self.product_id.dnk_cost_mp+self.product_id.dnk_cost_mo+self.product_id.dnk_cost_gif))/(dnk_price/self.order_id.company_id.dnk_usd_cost_fixed_rate)
                self.dnk_get_color()
                #else :
                #    self.dnk_profit_margin_ratio = ((self.order_id.company_id.dnk_usd_cost_fixed_rate/dnk_price)-(self.product_id.dnk_cost_mp+self.product_id.dnk_cost_mo+self.product_id.dnk_cost_gif))/(self.order_id.company_id.dnk_usd_cost_fixed_rate/dnk_price)
                #    self.dnk_get_color()



    #@api.onchange('product_id')
    #@api.depends('product_id',)
    #def product_id_change(self):
    #    res = super(SaleOrderLine, self).product_id_change()
    #    self.dnk_getmargin_profit()

    #    return res

    @api.onchange('price_unit','product_id','product_id.price')
    @api.depends('price_unit','product_id','product_id.price')
    def dnk_onchange_price(self):
            self.dnk_getmargin_profit()



class SaleOrder(models.Model):
    _inherit = "sale.order"


    @api.multi
    @api.onchange('order_line')
    @api.depends('order_line')
    def dnk_profit_margin(self):
        for rec in self:
            for linea in rec.order_line:
                linea.dnk_getmargin_profit()


    @api.multi
    def write(self, vals):
        res = super(SaleOrder, self)._write(vals)
        self.dnk_profit_margin()
        return res
