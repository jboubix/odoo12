# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp
from openerp.exceptions import UserError, RedirectWarning, ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    dnk_minimum_quantity = fields.Text('- Minimun Qty.', store=True)
    dnk_volume_prices = fields.Text('- Volume Prices', store=True)


    @api.model
    def write(self, vals):
        if self.product_id.dnk_volume_quotation:
            dnk_minimum_quantity, dnk_volume_prices = self._get_volume_prices_per_sale_line(self.order_id, self.product_id, self.product_uom, self.product_uom_qty, self.price_unit)
            vals_append = {
                'dnk_minimum_quantity': dnk_minimum_quantity,
                'dnk_volume_prices': dnk_volume_prices,
            }
            vals.update(vals_append)
        return super(SaleOrderLine, self).write(vals)


    @api.model
    def create(self, vals):
        product = self.env['product.product'].browse(vals.get('product_id'))

        if product.dnk_volume_quotation:
            sale_order = self.env['sale.order'].browse(vals.get('order_id'))
            product_uom = self.env['product.uom'].browse(vals.get('product_uom'))
            product_uom_qty = vals.get('product_uom_qty')
            price_unit = vals.get('price_unit')
            if price_unit is None:
                price_unit = 0.0
            dnk_minimum_quantity, dnk_volume_prices = self._get_volume_prices_per_sale_line(sale_order, product, product_uom, product_uom_qty, price_unit)

            vals_append = {
                'dnk_minimum_quantity': dnk_minimum_quantity,
                'dnk_volume_prices': dnk_volume_prices,
            }
            vals.update(vals_append)

        return super(SaleOrderLine, self).create(vals)


    def _formatLang(self, value, show_currency=True):
            lang = self.order_id.partner_id.lang
            lang_objs = self.env['res.lang'].search([('code', '=', lang)])
            if not lang_objs:
                lang_objs = self.env['res.lang'].search([], limit=1)
            lang_obj = lang_objs[0]

            decimals_quantity = self.env['decimal.precision'].search([('name', '=', 'Product Price')])
            if decimals_quantity:
                decimals_quantity = decimals_quantity[0].digits
            else:
                decimals_quantity = 2

            res = lang_obj.format('%.' + str(decimals_quantity) + 'f', value, grouping=True, monetary=True)
            currency_obj = self.order_id.currency_id

            if show_currency and currency_obj and currency_obj.symbol:
                if currency_obj.position == 'after':
                    res = '%s%s' % (res, currency_obj.symbol)
                elif currency_obj and currency_obj.position == 'before':
                    res = '%s%s' % (currency_obj.symbol, res)
            return res


    def _get_volume_prices_per_sale_line(self, order_id, product_id, product_uom, product_uom_qty, price_unit):
        if not (product_id and order_id.partner_id
           and order_id.pricelist_id):
            return('', '')

        # Buscar la Categoría del Producto en las Líneas de la Lista de precios
        search_pricelist_id = -1
        ProductPriceListItem = self.env['product.pricelist.item']
        price_list = ProductPriceListItem.search(
            [('pricelist_id', '=', order_id.pricelist_id.id),
             ('categ_id', '=', product_id.categ_id.id)])
        if len(price_list)>=1:
            search_pricelist_id = price_list[0].base_pricelist_id.id
        else:
            # Buscar la Categoría Padre de la Categoría del Producto en las Líneas de la Lista de precios
            if product_id.categ_id.parent_id:
                price_list = ProductPriceListItem.search(
                    [('pricelist_id', '=', order_id.pricelist_id.id),
                     ('categ_id', '=', product_id.categ_id.parent_id.id)])
                if len(price_list)>=1:
                    search_pricelist_id = price_list[0].base_pricelist_id.id

        # Si no se encontró la categoría del producto en la líneas de la lista de precios,
        # buscar en la primera línea de la lista de precios la tarifa
        if search_pricelist_id == -1 and len(order_id.pricelist_id.item_ids)>0:
            if order_id.pricelist_id.item_ids[0].base == 'pricelist':
                ProductPriceListItem = self.env['product.pricelist.item']
                price_list = ProductPriceListItem.search(
                    [('pricelist_id', '=', order_id.pricelist_id.item_ids[0].base_pricelist_id.id),
                     ('categ_id', '=', product_id.categ_id.id)])
                if len(price_list)>=1:
                    search_pricelist_id = price_list[0].base_pricelist_id.id
                else:
                    # Buscar la Categoría Padre de la Categoría del Producto en las Líneas de la Lista de precios
                    if product_id.categ_id.parent_id:
                        price_list = ProductPriceListItem.search(
                            [('pricelist_id', '=', order_id.pricelist_id.item_ids[0].base_pricelist_id.id),
                             ('categ_id', '=', product_id.categ_id.parent_id.id)])
                        if len(price_list)>=1:
                            search_pricelist_id = price_list[0].base_pricelist_id.id
            else:
                search_pricelist_id = order_id.pricelist_id.id

        # Falta buscar por Variante
        ProductPriceListItem = self.env['product.pricelist.item']
        price_list = ProductPriceListItem.search(
            [('pricelist_id', '=', search_pricelist_id),
             ('product_tmpl_id', '=', product_id.product_tmpl_id.id)], order="min_quantity DESC")

        context_partner = dict(self.env.context, partner_id=order_id.partner_id.id, date=order_id.date_order)
        pricelist_context = dict(context_partner, uom=product_uom.id)

        str_prices = ''
        str_mininimum_quantity = ''
        unit_price = ""
        if product_id.dnk_volume_quotation:
            for price in price_list:
                if price.id and price.min_quantity:
                    # Comando para debuggear:
                    # sudo su - odoo9dev -c "/opt/odoo9dev/odoo/openerp-server --config /etc/odoo9dev/odoo.conf --dev"
                    # tarifa_publica = self.env['res.lang'].search([('name', '=', 'Nombre de la tarifa publica')])
                    # context_partner = dict(self.env.context, partner_id=order_id.partner_id.id, date=order_id.date_order)
                    # pricelist_context = dict(context_partner, uom=product_uom.id)
                    # tarifa_publica..with_context(pricelist_context).get_product_price_rule(product_id, price.min_quantity, order_id.partner_id)
                    unit_price, rule_id = order_id.pricelist_id.with_context(pricelist_context).get_product_price_rule(product_id, price.min_quantity, order_id.partner_id)

                    ########################################################################
                    # dnk_sale_pricelist_fixed_rate
                    # Aquí es donde debo calcular con la Tasa Fija en USD si la Lista de Precio está configurada.
                    if order_id.pricelist_id.dnk_use_usd_fixed_rate:
                        date = self._context.get('date') or fields.Datetime.now()
                        res_currency_usd_id = self.env['res.currency'].search([('name', '=', 'USD')]).id
                        res_currency_rate = self.env['res.currency.rate']
                        usd_current_exchange_rate = res_currency_rate.search([('currency_id', '=', res_currency_usd_id), ('name', '<=', date)], limit=1, order="name desc").rate

                        usd_fixed_rate = order_id.company_id.dnk_usd_fixed_rate

                        unit_price = unit_price * usd_current_exchange_rate * usd_fixed_rate
                    ########################################################################

                    str_prices += self._formatLang(unit_price, show_currency=False) + "\n"
                    str_mininimum_quantity += '{:0,.2f}'.format(price.min_quantity) + "\n"
        else:
            product = product_id.with_context(
                lang=order_id.partner_id.lang,
                partner=order_id.partner_id.id,
                quantity=product_uom_qty,
                date=order_id.date_order,
                pricelist=order_id.pricelist_id.id,
                uom=product_uom.id,
                fiscal_position=self.env.context.get('fiscal_position')
            )
            unit_price, rule_id = order_id.pricelist_id.with_context(pricelist_context).get_product_price_rule(product_id, product_uom_qty, order_id.partner_id)

            ########################################################################
            # dnk_sale_pricelist_fixed_rate
            # Aquí es donde debo calcular con la Tasa Fija en USD si la Lista de Precio está configurada.
            if order_id.pricelist_id.dnk_use_usd_fixed_rate:
                date = self._context.get('date') or fields.Datetime.now()
                res_currency_usd_id = self.env['res.currency'].search([('name', '=', 'USD')]).id
                res_currency_rate = self.env['res.currency.rate']
                usd_current_exchange_rate = res_currency_rate.search([('currency_id', '=', res_currency_usd_id), ('name', '<=', date)], limit=1, order="name desc").rate

                usd_fixed_rate = order_id.company_id.dnk_usd_fixed_rate

                unit_price = unit_price * usd_current_exchange_rate * usd_fixed_rate
            ########################################################################
            price_unit = unit_price

        if str_prices == "" or str_mininimum_quantity == "":
            str_prices = self._formatLang(price_unit, show_currency=False)
            str_mininimum_quantity = '{:0,.2f}'.format(product_uom_qty)

        return(str_mininimum_quantity, str_prices)


    @api.onchange('country_id')
    def _onchange_country(self):
        if hasattr(super(ResCompany, self), '_onchange_country'):
            super(ResCompany, self)._onchange_country()


    @api.onchange('product_id', 'product_uom_qty')
    def _get_volume_prices(self):
        for sale_order_line in self:
            if sale_order_line.product_id.dnk_volume_quotation:
                dnk_minimum_quantity, dnk_volume_prices = self._get_volume_prices_per_sale_line(sale_order_line.order_id, sale_order_line.product_id, self.product_uom, self.product_uom_qty, self.price_unit)

                sale_order_line.dnk_minimum_quantity = dnk_minimum_quantity
                sale_order_line.dnk_volume_prices = dnk_volume_prices


    def open_view_wizard(self):
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'dnk_sale_volume_quotation.check_stock_wizard',
            'type': 'ir.actions.act_window',
            'context': context,
        }
