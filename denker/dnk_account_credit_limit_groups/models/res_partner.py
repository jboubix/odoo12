# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools


class DnkPartner (models.Model):
    _inherit = "res.partner"

    @api.multi
    def _get_accounting_edit_form(self):

        for rec in self:
            if self.env.user.has_group('dnk_account_credit_limit_groups.dnk_account_credit_limit_group') :
                rec.dnk_edit_accounting_fields = True
            else :
                rec.dnk_edit_accounting_fields = False

    dnk_edit_accounting_fields = fields.Boolean('- Edit Accounting Fields?', compute='_get_accounting_edit_form', store=False)
