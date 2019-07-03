# © 2016 OdooMRP team
# © 2016 AvanzOSC
# © 2016 Serv. Tecnol. Avanzados - Pedro M. Baeza
# © 2016 Eficent Business and IT Consulting Services, S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from datetime import timedelta


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    team_id = fields.Many2one('crm.team', 'Sales Channel', related='order_id.team_id', compute='_get_crm_team', store=True)
    dnk_is_invoiced_not_delivered = fields.Boolean(compute='_get_is_invoiced_not_delivered',
                                              string="- Invoiced Not Delivered",
                                              store=True)
    dnk_is_pending_delivery = fields.Boolean(compute='_get_is_pending_delivery',
                                              string="- Pending Delivery",
                                              store=True)
    dnk_qty_to_deliver = fields.Float(compute='_get_qty_to_deliver',
                                          string="- Qty to Deliver",
                                          store=True)
    dnk_usd_amount_to_deliver = fields.Monetary(compute='_get_qty_to_deliver',
                                          string="- USD Amount to Deliver",
                                          currency_field='currency_id',
                                          help="Subtotal price of products to deliver in USD.",
                                          store=True)
    dnk_subfamily_id = fields.Many2one('product.category', '- Subfamily',
                                        required=False, store=True, readonly=False,
                                        related='product_id.categ_id')
    dnk_family_id = fields.Many2one('product.category', '- Family',
                                        required=False, store=True, readonly=False,
                                        related='product_id.categ_id.parent_id')
    dnk_color_id = fields.Many2one('product.category', '- Color',
                                    required=False, store=True, readonly=False,
                                    related='product_id.categ_id.parent_id.parent_id')
    dnk_order_warehouse_id = fields.Many2one(
                                    'stock.warehouse', string='- Warehouse',
                                    related='order_id.warehouse_id', store=True,
                                    required=False, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})


    @api.multi
    @api.depends('product_uom_qty', 'qty_delivered', 'order_id.pricelist_id')
    def _get_qty_to_deliver(self):
        for line in self:
            line.dnk_qty_to_deliver = line.product_uom_qty - line.qty_delivered

            if line.currency_id.name == 'USD':
                line.dnk_usd_amount_to_deliver = (line.product_uom_qty - line.qty_delivered) * line.price_unit
            elif line.currency_id.name  == 'MXN':
                res_currency = self.env['res.currency']
                date = self._context.get('date') or fields.Datetime.now()
                res_currency_usd_id = 3
                exchange_rate = res_currency.search([('name', '=', 'USD')]).rate
                line.dnk_usd_amount_to_deliver = (line.product_uom_qty - line.qty_delivered) * line.price_unit * exchange_rate

    @api.multi
    @api.depends('qty_invoiced', 'qty_delivered')
    def _get_is_invoiced_not_delivered(self):
        for line in self:
            line.dnk_is_invoiced_not_delivered = line.qty_invoiced > line.qty_delivered


    @api.multi
    @api.depends('product_uom_qty', 'qty_delivered')
    def _get_is_pending_delivery(self):
        for line in self:
            line.dnk_is_pending_delivery = line.qty_delivered < line.product_uom_qty


    @api.multi
    @api.depends('order_id.team_id')
    def _get_crm_team(self):
        for rec in self:
            if rec.order_id.team_id:
                rec.team_id = rec.order_id.team_id.id
        return
