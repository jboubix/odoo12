# -*- coding: utf-8 -*-

from odoo import models, fields, api

class dnk_client_requirements_topay(models.Model):
    _name = "dnk.account.requirements.to.pay"
    _rec_name = 'dnk_name'
    _order = 'dnk_sequence,dnk_name'
    dnk_name = fields.Char('- Name')
    dnk_sequence = fields.Integer('- Sequence')
