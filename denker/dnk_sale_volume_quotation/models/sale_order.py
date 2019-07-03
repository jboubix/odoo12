# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp
from openerp.exceptions import UserError, RedirectWarning, ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    dnk_customer_service_rep_id = fields.Many2one('res.users', string='- Customer Service Rep', track_visibility='onchange')
