# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    dnk_customer_product_code = fields.Char('- Customer Product Code')

    @api.multi
    def _prepare_invoice_line(self, qty):
        res = super(SaleOrderLine,self)._prepare_invoice_line(qty)
        res.update({'dnk_customer_product_code': self.dnk_customer_product_code})
        return res


    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        res =  super(SaleOrderLine, self).product_id_change()
        self.order_id.update_customer_code()
        return res
