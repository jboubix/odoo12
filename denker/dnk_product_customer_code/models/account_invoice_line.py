# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _

class DnkAccountCustomerProductCode(models.Model):
    _inherit = "account.invoice.line"

    dnk_customer_product_code = fields.Char('- Customer Product Code')

class DnkAccountCustomerProductCode(models.Model):
    _inherit = "account.invoice"

    @api.depends('partner_id','invoice_line_ids')
    @api.onchange('partner_id')
    @api.multi
    def update_customer_code(self):
        if self.invoice_line_ids:
            if self.dnk_sale_order:
                sale_order_lines = self.env['sale.order.line']
                for invoice_line in  self.invoice_line_ids:
                    self._cr.execute("SELECT order_line_id FROM sale_order_line_invoice_rel WHERE invoice_line_id = %s", params=[invoice_line.id])
                    sale_line_id = self.env.cr.fetchone()
                    if sale_line_id:
                        invoice_line.dnk_customer_product_code = sale_order_lines.search([('id', '=', sale_line_id[0])], limit=1).dnk_customer_product_code or False
