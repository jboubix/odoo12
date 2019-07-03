# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools


class SaleOrder(models.Model):
    _inherit = "sale.order"

    dnk_commercial_partner_id = fields.Many2one('res.partner', string='- Commercial Entity', compute_sudo=True,
        related='partner_id.commercial_partner_id', store=True, readonly=True,
        help="The commercial entity for this Sale Order")

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    dnk_commercial_partner_id = fields.Many2one('res.partner', string='- Commercial Entity', compute_sudo=True,
        related='order_id.partner_id.commercial_partner_id', store=True, readonly=True,
        help="The commercial entity for this Sale Order")
