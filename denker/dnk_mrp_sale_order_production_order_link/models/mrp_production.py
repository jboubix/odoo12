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


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    sale_order_id = fields.Many2one('sale.order', string="Sale Order", readonly=True,
                                    compute="_compute_sale_order", store=True)
    sale_order_line_id = fields.Many2one('sale.order.line', string="Sale Order Line", readonly=True,
                                         compute="_compute_sale_order", store=True)
    partner_id = fields.Many2one(related='sale_order_id.partner_id', readonly=True,
        string='Customer', store=True)
    requested_date = fields.Datetime(related='sale_order_line_id.requested_date', readonly=True,
                                      string='Commitment Date', store=True)

    @api.multi
    @api.depends('procurement_group_id')
    def _compute_sale_order(self):
        for production in self:
            if production.procurement_group_id:
                sale_order = self.env['sale.order']
                sale = sale_order.search([('procurement_group_id', '=', production.procurement_group_id.id)])
                if sale:
                    production.sale_order_id = sale.id
                    # Buscar la Línea de Pedido relacionada al pedido
                    #for sale_order_line in sale.order_line:
                    for sale_order_line in sale.order_line:
                        if sale_order_line.product_id.id == production.product_id.id and \
                           sale_order_line.product_uom_qty == production.product_qty and \
                           not sale_order_line.mrp_production_id:
                            production.sale_order_line_id = sale_order_line.id
                            sale_order_line.write({'mrp_production_id': production.id})
                            #sale_order_line.mrp_production_id = production.id
                            break
