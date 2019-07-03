# -*- encoding: utf-8 -*-
from odoo import api, fields, models, _

class StockMove(models.Model):
    _inherit = "product.product"


    def _default_sale_delay(self):
        return self.product_tmpl_id.sale_delay

    sale_delay = fields.Float('Customer Lead Time', default=lambda self: self._default_sale_delay(), help="The average delay in days between the confirmation of the customer order and the delivery of the finished products. It's the time you promise to your customers.")


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    def _get_customer_lead(self, product_tmpl_id):
        return self.product_id.sale_delay
