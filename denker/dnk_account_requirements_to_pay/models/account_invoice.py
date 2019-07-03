# -*- coding: utf-8 -*-

from odoo import models, fields, api


class dnk_acc_requirements_topay_rel(models.Model):
    _inherit = "account.invoice"

    dnk_client_requirements = fields.Many2many(
        comodel_name='dnk.account.requirements.to.pay',
        relation='dnk_account_requirements_to_pay_rel',
        string="- Requirements to Payment",)
