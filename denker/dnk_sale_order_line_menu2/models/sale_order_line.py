# © 2016 OdooMRP team
# © 2016 AvanzOSC
# © 2016 Serv. Tecnol. Avanzados - Pedro M. Baeza
# © 2016 Eficent Business and IT Consulting Services, S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # Fecha de confirmación
    dnk_order_confirmation_date = fields.Datetime(related='order_id.confirmation_date',
                                                  string='- Confirmation Date',
                                                  index=True,
                                                  help="Date on which the sales order is confirmed.",
                                                  store=True)
    # Etiqueta del SO
    dnk_order_tag_ids = fields.Many2many(related='order_id.tag_ids', string='Tags', help="Tags of the Sales Order.")
