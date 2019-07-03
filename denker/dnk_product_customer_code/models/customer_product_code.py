# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _

class CustomerProductCode(models.Model):
    _name = "dnk.customer.product.code"
    _description = "Customer Product Code"
    _order = 'dnk_sequence'

    @api.onchange('dnk_partner_id')
    @api.multi
    def dnk_get_partner_name(self):
        for partner in self:
            partner.dnk_name = partner.dnk_partner_id.name or False


    dnk_name = fields.Char ("- Customer", compute="dnk_get_partner_name")
    dnk_partner_id = fields.Many2one(
        'res.partner', '- Customer',
        domain=[('customer', '=', True)], ondelete='cascade',  required=True,
        help="Customer", store=True)
    dnk_product_code = fields.Char('- Customer Product Code')
    dnk_sequence = fields.Integer('- Sequence', default=1)
    dnk_product_tmpl_id = fields.Many2one('product.template', '- Product Template', index=True, ondelete='cascade')
    dnk_product_id = fields.Many2one('product.product', '- Product', index=True, ondelete='cascade')
