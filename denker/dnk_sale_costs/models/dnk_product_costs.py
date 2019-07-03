# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _, SUPERUSER_ID
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, AccessError, ValidationError

class DnkBomsTemp(models.Model):
    _name = 'dnk.mrp.bom'
    _rec_name = 'dnk_product_id'

    @api.model
    def create(self, vals):
        print (vals)
        return super(DnkBomsTemp, self).create(vals)




    dnk_product_id = fields.Many2one('product.product', '- Product', ondelete='cascade')
    dnk_product_tmpl_id = fields.Many2one('product.template', '- Product Template')
    dnk_bom_id = fields.Many2one('mrp.bom')
    name = fields.Char('mrp.bom', related='dnk_bom_id.code')
    dnk_bom_cost = fields.Float(string="- Bom Cost", digits=dp.get_precision('Product Price'), groups="base.group_user")
    #dnk_bom_ids = fields.One2many('mrp.bom', 'product_id', string='- Bill Of Materials',default=lambda self: self.env['dnk.product.costs']._get_dnk_bom_ids(), ondelete='cascade')
    #dnk_bom_lines_ids = fields.One2many('mrp.bom.line', related='dnk_bom_ids.bom_line_ids')

    #dnk_tmpl_bom_ids = fields.One2many('mrp.bom', 'product_tmpl_id', string='- Bill Of Materials', default=lambda self: self.env['dnk.product.costs']._get_dnk_tmpl_bom_ids(), ondelete='cascade')
    #dnk_tmpl_bom_ids = fields.One2many('mrp.bom', related='dnk_product_tmpl_id.bom_ids')
    #dnk_tmpl_bom_lines_ids = fields.One2many('mrp.bom.line', related='dnk_tmpl_bom_ids.bom_line_ids')

class DnkProductCosts(models.Model):
    _name = 'dnk.product.costs'
    _rec_name = 'dnk_name'

    #@api.multi
    #def get_lines(self, boms):
    #    product_lines = []
    #    for bom in boms:
    #        products = bom.product_id
    #        if not products:
    #            products = bom.product_tmpl_id.product_variant_ids
    #        for product in products:
    #            attributes = []
    #            for value in product.attribute_value_ids:
    #                attributes += [(value.attribute_id.name, value.name)]
    #            result, result2 = bom.explode(product, 1)
    #            product_line = {'bom': bom, 'name': product.name, 'lines': [], 'total': 0.0,
    #                            'currency': self.env.user.company_id.currency_id,
    #                            'product_uom_qty': bom.product_qty,
    #                            'product_uom': bom.product_uom_id,
    #                            'attributes': attributes}
    #            total = 0.0
    #            for bom_line, line_data in result2:
    #                price_uom = bom_line.product_id.uom_id._compute_price(bom_line.product_id.standard_price, bom_line.product_uom_id)
    #                line = {
    #                    'product_id': bom_line.product_id,
    #                    'product_uom_qty': line_data['qty'], #line_data needed for phantom bom explosion
    #                    'product_uom': bom_line.product_uom_id,
    #                    'price_unit': price_uom,
    #                    'total_price': price_uom * line_data['qty'],
    #                }
    #                total += line['total_price']
    #                product_line['lines'] += [line]
    #            product_line['total'] = total
    #            product_lines += [product_line]
    #    return product_lines

    #@api.model
    #def dnk_get_report_values(self):
    #    for rec in self:
    #        boms = self.env['mrp.bom'].browse(docids)
    #        res = self.get_lines(boms)
    #    return {'lines': res}

    @api.model
    def _get_dnk_product_id(self):
        if 'active_model' in self._context and self._context['active_model'] == 'product.product':
            return self._context['active_id']
    @api.model
    def _get_dnk_product_tmpl_id(self):
        if 'active_model' in self._context and self._context['active_model'] == 'product.template':
            return self._context['active_id']

    @api.model
    def _get_dnk_product_cost_id(self):
        product_lines = []
        if 'active_model' in self._context and self._context['active_model'] == 'product.template':
            boms = self.env['product.template'].search([('id', '=', self._context['active_id'])]).bom_ids
            for bom in  boms:
                print (bom.id)
                total_price = 0
                lines = self.env['mrp.bom.line'].search([('bom_id', '=', bom.id)])
                for bom_line in lines:
                    price_uom = bom_line.product_id.uom_id._compute_price(bom_line.product_id.standard_price, bom_line.product_uom_id)
                    total_price = total_price + (price_uom * bom_line.product_qty)
                    print ('total_price %s ', total_price)
                dnk_bom_cost = self.env['dnk.mrp.bom'].create(
                {'dnk_product_tmpl_id': self._context['active_id'],
                'dnk_bom_id': bom.id,
                'name':bom.code,
                'dnk_bom_cost': total_price})
        return 0

    #@api.model
    #def _get_dnk_bom_ids(self):
    #    if 'active_model' in self._context and self._context['active_model'] == 'product.product':
    #        return self.env['product.product'].search([('id', '=', self._context['active_id'])]).bom_ids


    #@api.model
    #def _get_dnk_tmpl_bom_ids(self):
    #    if 'active_model' in self._context and self._context['active_model'] == 'product.template':
    #        return self.env['product.template'].search([('id', '=', self._context['active_id'])]).bom_ids

    @api.model
    def _get_total_cost(self):
        self.dnk_cost_total = self.dnk_cost_mp+self.dnk_cost_mo+self.dnk_cost_gif

    @api.model
    def _update_product_cost(self):
        productos =  self.env['product.product']
        dnk_product_cost = dnk_costos.search([('id', '=', self._origin.id)], limit =1)

    @api.model
    def create(self, vals):
        if 'active_model' in self._context:
            NombreMod = self._context['active_model']
            id = self._context['active_id']
        else:
            if vals['dnk_product_tmpl_id']:
                NombreMod = 'product.template'
                id = vals['dnk_product_tmpl_id']
            else:
                NombreMod = 'product.product'
                id = vals['dnk_product_id']
        vals['dnk_name'] = self.env[NombreMod].search([('id', '=', id)]).default_code
        Productos =  self.env[NombreMod]
        producto = Productos.browse(id)
        producto.dnk_cost_mp =  vals['dnk_cost_mp']
        producto.dnk_cost_mo =  vals['dnk_cost_mo']
        producto.dnk_cost_gif = vals['dnk_cost_gif']
        producto.dnk_costs_currency_id = 3 # sustituir esto
        if NombreMod == 'product.template':
            vals['dnk_usd_cost_fixed_rate']  = producto.company_id.dnk_usd_cost_fixed_rate
            vals['dnk_product_tmpl_id'] = id
            vals['dnk_tmpl_bom_ids'] = producto.bom_ids
        else :
            vals['dnk_usd_cost_fixed_rate']  = producto.product_tmpl_id.company_id.dnk_usd_cost_fixed_rate
            vals['dnk_product_id'] = id
            vals['dnk_bom_ids'] = producto.bom_ids
            print ("ESTOY EN CREATE")
            print(vals['dnk_bom_ids'])
        vals['dnk_cost_total'] = vals['dnk_cost_mp']+vals['dnk_cost_mo']+vals['dnk_cost_gif']
        return super(DnkProductCosts, self).create(vals)

    @api.multi
    def dnk_change_costs(self):
        return {'type': 'ir.actions.act_window_close'}

    dnk_name = fields.Char(string='- Default Code', index=True, readonly=True, default=lambda self: _('New'))
    dnk_company_id = fields.Many2one('res.company',string='- Company', default=lambda self: self.env['res.company']._company_default_get(), readonly=True, track_visibility='onchange')
    dnk_active = fields.Boolean('- Activo', default=True)

    dnk_cost_std = fields.Float(string="- Standard Cost", digits=dp.get_precision('Product Price'), groups="base.group_user")
    dnk_cost_mp = fields.Float(string="- Material Cost", digits=dp.get_precision('Product Price'), groups="base.group_user")
    dnk_cost_mo = fields.Float(string="- Labor Cost", digits=dp.get_precision('Product Price'), groups="base.group_user")
    dnk_cost_gif = fields.Float(string="- GIF Cost", digits=dp.get_precision('Product Price'), groups="base.group_user")
    dnk_cost_total =  fields.Float(string="- Total Cost", digits=dp.get_precision('Product Price'), readonly=True, compute="_get_total_cost", store=True, groups="base.group_user")

    dnk_currency_rate = fields.Many2one('res.currency', string='- Cost Currency', default=3, readonly=True)
    dnk_usd_cost_fixed_rate = fields.Monetary(string="- USD Cost Fixed Rate", currency_field='dnk_currency_rate', readonly=True, help="USD Cost Fixed Rate to use on Margin.")
    dnk_product_id = fields.Many2one('product.product', '- Product', ondelete='cascade', default=lambda self: self.env['dnk.product.costs']._get_dnk_product_id())
    dnk_product_tmpl_id = fields.Many2one('product.template', '- Product Template',default=lambda self: self.env['dnk.product.costs']._get_dnk_product_tmpl_id())
    dnk_mrp_product_bom_cost = fields.Many2one('dnk.mrp.bom',  default=lambda self: self.env['dnk.product.costs']._get_dnk_product_cost_id())
    dnk_mrp_product_tmpl_bom_cost = fields.One2many('dnk.mrp.bom', 'dnk_product_tmpl_id')
    dnk_bom_ids = fields.One2many('mrp.bom', related='dnk_product_id.bom_ids')

    #dnk_bom_ids = fields.One2many('mrp.bom', 'product_id', string='- Bill Of Materials',default=lambda self: self.env['dnk.product.costs']._get_dnk_bom_ids(), ondelete='cascade')
    dnk_bom_lines_ids = fields.One2many('mrp.bom.line', related='dnk_bom_ids.bom_line_ids')

    #dnk_tmpl_bom_ids = fields.One2many('mrp.bom', 'product_tmpl_id', string='- Bill Of Materials', default=lambda self: self.env['dnk.product.costs']._get_dnk_tmpl_bom_ids(), ondelete='cascade')
    dnk_tmpl_bom_ids = fields.One2many('mrp.bom', related='dnk_product_tmpl_id.bom_ids')
    dnk_tmpl_bom_lines_ids = fields.One2many('mrp.bom.line', related='dnk_tmpl_bom_ids.bom_line_ids')
