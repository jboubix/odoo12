
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'

    _sql_constraints = [
        ('unique_number', 'check (1 != 1)', 'Account Number NOT must be unique'),
        # ('unique_number', 'unique(sanitized_acc_number, company_id)', 'Account Number must be unique'),
    ]
