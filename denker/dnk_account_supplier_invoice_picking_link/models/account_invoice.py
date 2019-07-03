# © 2016 OdooMRP team
# © 2016 AvanzOSC
# © 2016 Serv. Tecnol. Avanzados - Pedro M. Baeza
# © 2016 Eficent Business and IT Consulting Services, S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'


    purchase_picking_ids = fields.Many2many(
        comodel_name='stock.picking',
        string='Related Pickings',
        readonly=True,
        copy=False,
        help="Related pickings "
             "(only when the invoice has been generated from a purchase order).",
    )

    #@api.depends(purchase_id)

    #picking_ids = fields.Many2many(
    #    comodel_name='stock.picking',
    #    string='Related Pickings',
    #    readonly=True,
    #    copy=False,
    #    help="Related pickings "
    #         "(only when the invoice has been generated from a sale order).",
    #    )
