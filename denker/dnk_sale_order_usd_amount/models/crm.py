# -*- coding: utf-8 -*-
from odoo import api, fields, models
from lxml import etree

class CRMLead(models.Model):
    _inherit = "crm.lead"

    def _dnk_compute_sale_amount_total_usd(self):
        for lead in self:
            total = 0.0
            sales_orders = self.env['sale.order'].search([('opportunity_id', '=', lead.id)])
            for order in sales_orders:
                if order.state not in ('draft', 'sent', 'cancel'):
                    total += order.dnk_amount_untaxed_usd
            lead.dnk_sale_amount_total_usd = total

    dnk_sale_amount_total_usd = fields.Float(compute='_dnk_compute_sale_amount_total_usd', string="Sum of Orders", help="Untaxed Total of Confirmed Orders USD")
