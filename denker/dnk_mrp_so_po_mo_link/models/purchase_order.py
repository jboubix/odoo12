# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2015 Deltatech All Rights Reserved
#                    Dorin Hongu <dhongu(@)gmail(.)com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import api
from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    dnk_sale_order_line_ids = fields.Many2many(
                                comodel_name='sale.order.line', string="- Sale Order Line",
                                relation='dnk_purchase_order_sale_order_line_link',
                                column1='purchase_order', column2='sale_order_line_id',
                                compute='_compute_sale_order_by_origin',
                                readonly=False, store=True)


    @api.multi
    @api.depends('origin', 'order_line')
    def _compute_sale_order_by_origin(self):
        SaleOrder = self.env['sale.order']
        SaleOrderLine = self.env['sale.order.line']
        for purchase_order in self:
            # Extraer los números de pedidos en la forma SO001, SO002, SO003
            if not purchase_order.origin:
                break
            origin_list = purchase_order.origin.replace(' ','').split(',')
            sale_orders_line_list = []

            for sale_order in origin_list:
                # Buscar el pedido de origin en el catálogo de pedidos
                sale_order = SaleOrder.search([('name', '=', sale_order)])
                if sale_order:
                    # Buscar la Línea de Pedido Correcta
                    for sale_order_line in sale_order.order_line:
                        for purchase_order_line in purchase_order.order_line:
                            if sale_order_line.product_id.id == purchase_order_line.product_id.id: # and \
                                # not sale_order_line.dnk_purchase_order_id:
                                # sale_order_line.product_uom_qty == purchase_order.product_qty and \
                                sale_orders_line_list.append(sale_order_line.id)
                                #purchase_order.sale_order_line_id = sale_order_line.id
                                sale_order_line.write({'dnk_purchase_order_id': purchase_order.id})
                                #sale_order_line.dnk_purchase_order_id = production.id
                                break

            purchase_order.dnk_sale_order_line_ids = sale_orders_line_list


    @api.multi
    @api.depends('group_id')
    def _compute_sale_order(self):
        for purchase in self:
            if purchase.group_id:
                sale_order = self.env['sale.order']
                sale = sale_order.search([('procurement_group_id', '=', purchase.group_id.id)])
                if sale:
                    # purchase.sale_order_id = sale.id
                    # Buscar la Línea de Pedido relacionada al pedido
                    for sale_order_line in sale.order_line:
                        if sale_order_line.product_id.id == purchase.product_id.id and \
                           sale_order_line.product_uom_qty == purchase.product_qty and \
                           not sale_order_line.dnk_purchase_order_id:
                            purchase.dnk_sale_order_line_ids = [sale_order_line.id]
                            sale_order_line.write({'dnk_purchase_order_id': purchase.id})
                            break


class PurchaseOrderLine(models.Model):

    _inherit = 'purchase.order.line'

    dnk_procurement_group_id = fields.Many2one('procurement.group', '- Procurement Group')

    def _merge_in_existing_line(self, product_id, product_qty, product_uom,
                                location_id, name, origin, values):
        """Do no merge PO lines if procurement group is different."""
        if values.get('group_id') != self.dnk_procurement_group_id:
            return False
        super()._merge_in_existing_line(product_id, product_qty, product_uom,
                                        location_id, name, origin, values)


class ProcurementRule(models.Model):

    _inherit = 'procurement.rule'

    @api.multi
    def _prepare_purchase_order_line(self, product_id, product_qty,
                                     product_uom, values, po, supplier):
        """Add procurement group to values"""
        res = super()._prepare_purchase_order_line(
            product_id, product_qty, product_uom, values, po, supplier)
        procurement_group = values.get('group_id')
        if procurement_group:
            res['procurement_group_id'] = procurement_group.id
        return res
