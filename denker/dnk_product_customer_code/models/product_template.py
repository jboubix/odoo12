# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.osv import expression
import re

class ProductTemplate(models.Model):
    _inherit = "product.template"

    dnk_customer_ids = fields.One2many(comodel_name='dnk.customer.product.code', inverse_name='dnk_product_tmpl_id', string='- Customers')


class ProductProduct(models.Model):
    _inherit = "product.product"

    dnk_product_code = fields.Char('Internal Reference', compute='dnk_get_product_code')

    @api.one
    def dnk_get_product_code(self):
        for cus_info in self.customer_ids:
            if cus_info.name.id == self._context.get('partner_id'):
                self.dnk_product_code = cus_info.product_code or self.default_code
        else:
            self.dnk_product_code = self.default_code

    #@api.multi
    #def name_get(self):
        # TDE: this could be cleaned a bit I think

    #    def _name_get(d):
    #        name = d.get('name', '')
    #        code = self._context.get('display_default_code', True) and d.get('default_code', False) or False
    #        if code:
    #            name = '[%s] %s' % (code,name)
    #        return (d['id'], name)

    #    partner_id = self._context.get('partner_id')
    #    if partner_id:
    #        partner_ids = [partner_id, self.env['res.partner'].browse(partner_id).commercial_partner_id.id]
    #    else:
    #        partner_ids = []

        # all user don't have access to seller and partner
        # check access and use superuser
    #    self.check_access_rights("read")
    #    self.check_access_rule("read")

    #    result = []
    #    for product in self.sudo():
            # display only the attributes with multiple possible values on the template
    #        variable_attributes = product.attribute_line_ids.filtered(lambda l: len(l.value_ids) > 1).mapped('attribute_id')
    #        variant = product.attribute_value_ids._variant_name(variable_attributes)

    #        name = variant and "%s (%s)" % (product.name, variant) or product.name
    #        sellers = []
    #        customers = []
    #        if partner_ids:
    #            sellers = [x for x in product.seller_ids if (x.name.id in partner_ids) and (x.product_id == product)]
    #            if not sellers:
    #                sellers = [x for x in product.seller_ids if (x.name.id in partner_ids) and not x.product_id]
    #            #customers = [x for x in product.dnk_customer_ids if (x.dnk_partner_id.commercial_partner_id.id in partner_ids) and (x.dnk_product_tmpl_id == product.product_tmpl_id)]
    #            customers = [x for x in product.dnk_customer_ids if (x.dnk_product_tmpl_id == product.product_tmpl_id)]
    #            if not customers:
    #                customers = [x for x in product.dnk_customer_ids if (x.dnk_partner_id.id in partner_ids) and not x.dnk_product_id]
    #        if customers:
    #                mydict = {
    #                          'id': product.id,
    #                          'name': product.name or name,
    #                          'default_code': product.default_code,
    #                          }
    #                temp = _name_get(mydict)
    #                if temp not in result:
    #                    result.append(temp)
    #        elif sellers:
    #            for s in sellers:
    #                seller_variant = s.product_name and (
    #                    variant and "%s (%s)" % (s.product_name, variant) or s.product_name
    #                    ) or False
    #                mydict = {
    #                          'id': product.id,
    #                          'name': seller_variant or name,
    #                          'default_code': s.product_code or product.default_code,
    #                          }
    #                temp = _name_get(mydict)
    #                if temp not in result:
    #                    result.append(temp)
    #        else:
    #            mydict = {
    #                      'id': product.id,
    #                      'name': name,
    #                      'default_code': product.default_code,

    #                      }
    #            result.append(_name_get(mydict))
    #    return result

    #@api.model
    #def name_search(self, name='', args=None, operator='ilike', limit=100):
    #    if not args:
    #        args = []
    #    if name:
    #        positive_operators = ['=', 'ilike', '=ilike', 'like', '=like']
    #        products = self.env['product.product']
    #        if operator in positive_operators:
    #            products = self.search([('default_code', '=', name)] + args, limit=limit)
    #            if not products:
    #                products = self.search([('barcode', '=', name)] + args, limit=limit)
    #        if not products and operator not in expression.NEGATIVE_TERM_OPERATORS:
    #            # Do not merge the 2 next lines into one single search, SQL search performance would be abysmal
    #            # on a database with thousands of matching products, due to the huge merge+unique needed for the
    #            # OR operator (and given the fact that the 'name' lookup results come from the ir.translation table
    #            # Performing a quick memory merge of ids in Python will give much better performance
    #            products = self.search(args + [('default_code', operator, name)], limit=limit)
    #            if not limit or len(products) < limit:
    #                # we may underrun the limit because of dupes in the results, that's fine
    #                limit2 = (limit - len(products)) if limit else False
    #                products += self.search(args + [('name', operator, name), ('id', 'not in', products.ids)], limit=limit2)
    #        elif not products and operator in expression.NEGATIVE_TERM_OPERATORS:
    #            domain = expression.OR([
    #                ['&', ('default_code', operator, name), ('name', operator, name)],
    #                ['&', ('default_code', '=', False), ('name', operator, name)],
    #            ])
    #            domain = expression.AND([args, domain])
    #            products = self.search(domain, limit=limit)
    #        if not products and operator in positive_operators:
    #            ptrn = re.compile('(\[(.*?)\])')
    #            res = ptrn.search(name)
    #            if res:
    #                products = self.search([('default_code', '=', res.group(2))] + args, limit=limit)
    #        # still no results, partner in context: search on supplier info as last hope to find something
    #        if not products and self._context.get('partner_id'):
    #            commercial_partner_id = self.env['res.partner'].search([('id', '=', self._context.get('partner_id'))]).commercial_partner_id
    #            customers = self.env['dnk.customer.product.code'].search([
    #                ('dnk_partner_id', '=', commercial_partner_id.id),
    #                ('dnk_product_code', operator, name)])
    #            if customers:
    #                products = self.search([('product_tmpl_id.dnk_customer_ids', 'in', customers.ids)], limit=limit)

    #            else:
    #                suppliers = self.env['product.supplierinfo'].search([
    #                ('name', '=', self._context.get('partner_id')),
    #                '|',
    #                ('product_code', operator, name),
    #                ('product_name', operator, name)])
    #                if suppliers:
    #                    products = self.search([('product_tmpl_id.seller_ids', 'in', suppliers.ids)], limit=limit)
    #    else:
    #        products = self.search(args, limit=limit)
    #    return products.name_get()
