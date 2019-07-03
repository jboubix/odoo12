# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api, _
from openerp.exceptions import UserError, RedirectWarning, ValidationError
from datetime import datetime, timedelta, date


class crm_team_transit_days(models.Model):
    _inherit = "crm.team"

    @api.onchange('dnk_abbreviation')
    def _upper_abbreviation(self):
        if self.dnk_abbreviation:
            self.dnk_abbreviation = self.dnk_abbreviation.upper()


    dnk_transit_days = fields.Integer(
                    string='- Transit Days',
                    help='Days elapsed when the package arrives at the branch',
                    default=3)
    dnk_abbreviation = fields.Char(
                    string='- Abbreviation',
                    help='Abbreviation', size=2)
