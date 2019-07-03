
# -*- coding: utf-8 -*-
from odoo import api, fields, models

class Partner(models.Model):
    _inherit = "res.partner"


    dnk_is_final_customer = fields.Boolean('- Is Final Customer?')
