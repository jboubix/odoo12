# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
from datetime import datetime, timedelta
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError, RedirectWarning, ValidationError, AccessError

class SaleOrder(models.Model):
    _inherit = "sale.order"


    @api.model
    def _get_price_list_domain(self):
        res = []
        if not self.env.user.has_group('custom_dnk.group_pricelist_manager'):
            if self.partner_id.property_product_pricelist:
                pricelist_search = self.env['product.pricelist'].search([('dnk_pricelist_level','>=',self.partner_id.property_product_pricelist.dnk_pricelist_level)])
                self.dnk_price_list_domain_ids = pricelist_search.ids
            else:
                self.dnk_price_list_domain_ids = []
        return res


    dnk_price_list_domain_ids = fields.Many2many(
        'product.pricelist', 'sale_pricelist_rel',
        'sale_order_id', 'pricelist_id', compute=_get_price_list_domain)

    @api.multi
    @api.onchange('partner_id')
    def _get_available_price_list(self):
        res = {'domain': {'pricelist_id': []}}
        if not self.env.user.has_group('custom_dnk.group_pricelist_manager'):
            if self.partner_id.property_product_pricelist:
                pricelist_search = self.env['product.pricelist'].search([('dnk_pricelist_level','>=',self.partner_id.property_product_pricelist.dnk_pricelist_level)])
                res['domain']['pricelist_id'] = [('id', 'in', pricelist_search.ids)]
            else:
                res['domain']['pricelist_id'] = [('id', 'in', (0))]
                warning = {
                           'title': 'Invalid Customer !',
                           'message': 'This customer does not have a defined price list, please assign it one!',
                           }
                return {'warning': warning}
        return res
