# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp
from openerp.exceptions import UserError, RedirectWarning, ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    dnk_volume_quotation = fields.Boolean('- Volume Quotation', default=True)
