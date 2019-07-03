# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools, _
from odoo.api import Environment


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"


    #Eliminar en siguiente actualización, ya dejó de utilizarse.
    dnk_capture_price_unit = fields.Boolean(
        string="Capture Price Unit",
        help="If checked, the Price Unit isn't going to be calculated with the UDS Fixed Rate in Pricelists configured to use it.",
        default=False)

    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):

        result = super(SaleOrderLine, self).product_uom_change()
        if self.order_id.pricelist_id and self.order_id.partner_id:
            if self.order_id.pricelist_id.dnk_use_usd_fixed_rate:
                #date = self._context.get('date') or fields.Datetime.now()
                #res_currency_usd_id = self.env['res.currency'].search([('name', '=', 'USD')]).id
                res_currency = self.env['res.currency']
                #usd_current_exchange_rate = res_currency_rate.search([('currency_id', '=', res_currency_usd_id), ('name', '<=', date)], limit=1, order="name desc").rate
                usd_current_exchange_rate = res_currency.search([('name', '=', 'USD')]).rate
                usd_fixed_rate = self.order_id.company_id.dnk_usd_fixed_rate
                # Calcular el precio basado en la Tasa Fija de USD configurada en la compañía
                self.price_unit = round(self.price_unit * usd_current_exchange_rate * usd_fixed_rate, 4)
        return result
