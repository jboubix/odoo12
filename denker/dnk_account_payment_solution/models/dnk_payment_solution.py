# -*- coding: utf-8 -*-

from odoo import models, fields, api

class dnk_account_payment_solution(models.Model):
    _name = "dnk.account.payment.solution"
    _rec_name = 'dnk_name'
    _order = 'dnk_sequence,dnk_name'
    dnk_name = fields.Char('- Name')
    dnk_sequence = fields.Integer('- Sequence')
