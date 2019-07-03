# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    dnk_promise_to_pay = fields.Date(string="- Promise To Pay", help="Promise To Pay")
