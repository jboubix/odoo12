# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _

class ResPartner(models.Model):
    _inherit = "res.partner"

    dnk_recommitment_notification = fields.Boolean(
        string='- Recommitment Notification', help='If checked, every change of "Recommitment Date" a mail notification is sent to the customer',
        default=True, store=True)
