# © 2016 OdooMRP team
# © 2016 AvanzOSC
# © 2016 Serv. Tecnol. Avanzados - Pedro M. Baeza
# © 2016 Eficent Business and IT Consulting Services, S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    dnk_mrp_production_id = fields.Many2one('mrp.production', string="- MO", readonly=False,
                                    copy=False, store=True)
    dnk_mrp_production_state = fields.Selection([
        ('confirmed', 'Confirmed'),
        ('planned', 'Planned'),
        ('progress', 'In Progress'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')], string='- MO State', related='dnk_mrp_production_id.state', readonly=True,
        copy=False, track_visibility='onchange', store=True)
    dnk_mrp_production_date_planned_start = fields.Datetime(
        string='- MO Deadline Start', copy=False,
        store=True, related='dnk_mrp_production_id.date_planned_start', readonly=True)

    """ Queda pendiente para la versión 2
    dnk_purchase_order_id = fields.Many2one('purchase.order', string="- PO", readonly=False,
                                    copy=False)
    dnk_purchase_order_state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')], string='- PO State', related='dnk_purchase_order_id.state', readonly=False,
        copy=False, track_visibility='onchange')
    """
