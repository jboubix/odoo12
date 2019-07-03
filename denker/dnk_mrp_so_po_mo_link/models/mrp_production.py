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
import datetime


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    dnk_sale_order_line_ids = fields.Many2many(
            comodel_name='sale.order.line', string="- Sale Order Line",
            relation='dnk_production_order_sale_order_line_link',
            column1='dnk_mrp_production_id', column2='sale_order_line_id',
            compute='_compute_sale_order_by_origin',
            readonly=False, store=True)
    dnk_minimum_commitment_date = fields.Datetime(string="- Min. Commitment Date",
            compute='_compute_sale_order_by_origin',
            readonly=True, store=True)
    dnk_planned_late = fields.Boolean(
            string='Planned Late', default=False,
            compute='_compute_planned_late',
            store=True,
            help="If True the MO is planned late base on the minimum final commitment date.")


    @api.depends('dnk_sale_order_line_ids.dnk_final_commitment_date', 'date_planned_start')
    def _compute_planned_late(self):
        for mrp_production in self:
            if mrp_production.dnk_sale_order_line_ids:
                final_commitment_date_list = []
                for sale_order_line in mrp_production.dnk_sale_order_line_ids:
                    if sale_order_line.dnk_final_commitment_date != False:
                        final_commitment_date_list.append(datetime.datetime.strptime(sale_order_line.dnk_final_commitment_date, '%Y-%m-%d %H:%M:%S'))

                if len(final_commitment_date_list)>0:
                    days = datetime.datetime.strptime(mrp_production.date_planned_start, '%Y-%m-%d %H:%M:%S').date() - min(final_commitment_date_list).date()
                    if days.days < 1:
                        mrp_production.dnk_planned_late = True
                    else:
                        mrp_production.dnk_planned_late = False


    @api.multi
    @api.depends('origin')
    def _compute_sale_order_by_origin(self):
        SaleOrder = self.env['sale.order']
        SaleOrderLine = self.env['sale.order.line']

        for mrp_production in self:
            if hasattr(self, '_origin'):
                mrp_production_id = self._origin.id
            else:
                mrp_production_id = mrp_production.id

            # Si ya existe una línea de SO ligada a esta MO, elimiar el enlace
            sale_order_lines = SaleOrderLine.search([('dnk_mrp_production_id', '=', mrp_production.id)])
            for sale_order_line in sale_order_lines:
                sale_order_line.write({'dnk_mrp_production_id': False})

            # Si el campo "origin" está vacío, no hay nada que buscar
            if not mrp_production.origin:
                break

            origin_list = mrp_production.origin.replace(' ','').split(',')
            sale_orders_line_list = []
            final_commitment_date_list = []
            # Extraer los números de pedidos en la forma SO001, SO002, SO003
            for sale_order in origin_list:
                # Buscar el pedido de origin en el catálogo de pedidos
                sale_order = SaleOrder.search([('name', '=', sale_order)])
                if sale_order:
                    # Buscar la Línea de Pedido Correcta
                    for sale_order_line in sale_order.order_line:
                        # Ligar la MO con una línea de SO sólo si la línea de SO no está ligada con una MO
                        if sale_order_line.product_id.id == mrp_production.product_id.id and \
                            (not sale_order_line.dnk_mrp_production_id or mrp_production_id == sale_order_line.dnk_mrp_production_id.id):
                            # sale_order_line.product_uom_qty == mrp_production.product_qty and \
                            sale_orders_line_list.append(sale_order_line.id)
                            if sale_order_line.dnk_final_commitment_date != False:
                                final_commitment_date_list.append(sale_order_line.dnk_final_commitment_date)
                            sale_order_line.write({'dnk_mrp_production_id': mrp_production.id})
                            #sale_order_line.dnk_mrp_production_id = production.id
                            break

            mrp_production.dnk_sale_order_line_ids = sale_orders_line_list
            # print("############################################################")
            # print(final_commitment_date_list)
            if len(final_commitment_date_list)>0:
                mrp_production.dnk_minimum_commitment_date = min(final_commitment_date_list)


    @api.multi
    @api.depends('procurement_group_id')
    def _compute_sale_order(self):
        for production in self:
            if production.procurement_group_id:
                sale_order = self.env['sale.order']
                sale = sale_order.search([('procurement_group_id', '=', production.procurement_group_id.id)])
                if sale:
                    # Buscar la Línea de Pedido relacionada al pedido
                    for sale_order_line in sale.order_line:
                        if sale_order_line.product_id.id == production.product_id.id and \
                           not sale_order_line.dnk_mrp_production_id:
                            production.dnk_sale_order_line_ids = [sale_order_line.id]
                            sale_order_line.write({'dnk_mrp_production_id': production.id})
                            break


    # CANCELAR ESTO SEGÚN RICARDO CASTRO 2019-01-30
    # Desligar la MO de la Sale Order Line si se cancela la MO
    """@api.multi
    def action_cancel(self):
        res = super(MrpProduction, self).action_cancel()

        # Desligar las Líneas de Pedidos con la MO al cancelarla
        SaleOrderLine = self.env['sale.order.line']
        for mrp_production in self:
            # Si ya existe una línea de SO ligada a esta MO, elimiar el enlace
            sale_order_lines = SaleOrderLine.search([('dnk_mrp_production_id', '=', mrp_production.id)])
            for sale_order_line in sale_order_lines:
                sale_order_line.write({'dnk_mrp_production_id': False})

            vals = {
                'dnk_sale_order_line_ids': [(5)],
                'origin': False,
            }
            try:
                mrp_production.write(vals)
            except AccessError:  # no write access rights -> just ignore
                break

        return res"""


    # CANCELAR ESTO SEGÚN RICARDO CASTRO 2019-01-30
    # Desligar la MO de la Sale Order Line si se marca como hecho la MO
    """@api.multi
    def button_mark_done(self):
        res = super(MrpProduction, self).button_mark_done()

        # Desligar las Líneas de Pedidos con la MO al cancelarla
        SaleOrderLine = self.env['sale.order.line']
        for mrp_production in self:
            # Si ya existe una línea de SO ligada a esta MO, elimiar el enlace
            sale_order_lines = SaleOrderLine.search([('dnk_mrp_production_id', '=', mrp_production.id)])
            for sale_order_line in sale_order_lines:
                sale_order_line.write({'dnk_mrp_production_id': False})

            vals = {
                'dnk_sale_order_line_ids': [(5)],
                'origin': False,
            }
            try:
                mrp_production.write(vals)
            except AccessError:  # no write access rights -> just ignore
                break

        return res"""


    @api.multi
    def _prepare_invoice_line(self, qty):
        res = super(SaleOrderLine,self)._prepare_invoice_line(qty)
        res.update({'dnk_customer_product_code': self.dnk_customer_product_code})
        return res
