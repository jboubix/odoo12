
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class Company(models.Model):
    _inherit = 'res.company'

    dnk_usd_fixed_rate = fields.Monetary(
            string="- USD Fixed Rate", currency_field='currency_id',
            help="USD Fixed Rate to use on pricelists configured to use it.", default=22.0)
