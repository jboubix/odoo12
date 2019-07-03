# -*- coding: utf-8 -*-

from odoo import models, fields, api


class dnk_account_payment_solution(models.Model):
    _inherit = "account.invoice"


    dnk_payment_solution = fields.Many2many(
        comodel_name='dnk.account.payment.solution',
        relation='dnk_account_payment_solution_rel',
        string="- Payment Solution",)
