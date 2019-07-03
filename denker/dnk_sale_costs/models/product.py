# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo.addons import decimal_precision as dp
from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def _default_currency(self):
        return self.env.user.company_id.currency_id

    dnk_cost_mp = fields.Float(
        string="- Cost Materials",
        compute='_compute_cost',
        inverse='_set_cost',
        digits=dp.get_precision('Product Price'), groups="base.group_user")

    dnk_cost_mo = fields.Float(
        string="- Cost Labor",
        inverse='_set_cost',
        digits=dp.get_precision('Product Price'), groups="base.group_user")

    dnk_cost_gif = fields.Float(
        string="- GIF Cost",
        inverse='_set_cost',
        digits=dp.get_precision('Product Price'), groups="base.group_user")

    dnk_costs_currency_id = fields.Many2one('res.currency', string='- MP Cost Currency', default=_default_currency)

    dnk_product_cost_ids = fields.One2many('dnk.product.costs', 'dnk_product_tmpl_id', string="- Denker Costs (USD)")


    @api.one
    def _set_cost(self):
        if len(self.product_variant_ids) == 1:
            self.product_variant_ids.dnk_cost_mp = self.dnk_cost_mp


    @api.depends('product_variant_ids', 'product_variant_ids.standard_price')
    def _compute_cost(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)

        for template in unique_variants:
            template.dnk_costs_currency_id = template.product_variant_ids.dnk_costs_currency_id
            template.dnk_cost_mp = template.product_variant_ids.dnk_cost_mp
        for template in (self - unique_variants):
            template.dnk_cost_mp = 0.0
            if template.product_variant_ids:
                template.dnk_costs_currency_id = template.product_variant_ids[0].dnk_costs_currency_id


class ProductProduct(models.Model):
    _inherit = "product.product"

    dnk_cost_mp = fields.Float(
        string="- MP Cost",
        company_dependent=True,
        digits=dp.get_precision('Product Price'), groups="base.group_user")
    dnk_cost_mo = fields.Float(
        string="- MO Cost",
        company_dependent=True,
        digits=dp.get_precision('Product Price'), groups="base.group_user")
    dnk_cost_gif = fields.Float(
        string="- GIF Cost",
        company_dependent=True,
        digits=dp.get_precision('Product Price'), groups="base.group_user")

    dnk_costs_currency_id = fields.Many2one('res.currency', string='- MP Cost Currency', related='product_tmpl_id.dnk_costs_currency_id')

    dnk_product_cost_ids = fields.One2many('dnk.product.costs', 'dnk_product_id', string="- Denker Costs (USD)")
