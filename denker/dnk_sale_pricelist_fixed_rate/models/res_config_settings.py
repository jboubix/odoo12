# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
from datetime import datetime, timedelta
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError, RedirectWarning, ValidationError, AccessError

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    dnk_usd_fixed_rate = fields.Monetary(
            related='company_id.dnk_usd_fixed_rate',
            string="- USD Fixed Rate", currency_field='currency_id',
            help="USD Fixed Rate to use on pricelists configured to use it.")
