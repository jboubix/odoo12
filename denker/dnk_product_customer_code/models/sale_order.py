# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, AccessError

class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends('partner_id','order_line')
    @api.onchange('partner_id')
    @api.multi
    def update_customer_code(self):
        if self.order_line:
            customer_codes = self.env['dnk.customer.product.code']

            for line in self.order_line:
                if line.product_id:
                    product_code = customer_codes.search([('dnk_product_id', '=', line.product_id.id), ('dnk_partner_id', '=', line.order_id.partner_id.commercial_partner_id.id)], limit=1, order="dnk_sequence desc").dnk_product_code
                    if product_code :
                        line.dnk_customer_product_code = product_code


    @api.multi
    def action_confirm(self):
        res = super(SaleOrder,self).action_confirm()
        self.add_customer_to_product()
        return res

    @api.multi
    def add_customer_to_product(self):
        for line in self.order_line:
            partner = self.partner_id if not self.partner_id.parent_id else self.partner_id.parent_id
            if partner not in line.product_id.dnk_customer_ids.mapped('dnk_partner_id') and line.dnk_customer_product_code:
                product_code_info = {
                    'dnk_partner_id': partner.commercial_partner_id.id,
                    'dnk_product_code': line.dnk_customer_product_code,
                    'dnk_product_id':line.product_id.id,
                    'dnk_sequence': max(line.product_id.dnk_customer_ids.mapped('dnk_sequence')) + 1 if line.product_id.dnk_customer_ids else 1,
                }
                vals = {
                    'dnk_customer_ids': [(0, 0, product_code_info)],
                }
                try:
                    line.product_id.write(vals)
                except AccessError:  # no write access rights -> just ignore
                    break
