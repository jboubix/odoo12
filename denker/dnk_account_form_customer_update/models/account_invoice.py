# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools

class AccountingInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    @api.onchange('partner_id')
    @api.depends('partner_id')
    def dnk_update_cfdi_partner_info(self):
        if self.partner_id:
            self.fiscal_position_id = self.partner_id.commercial_partner_id.property_account_position_id.id or False
            self.l10n_mx_edi_usage = self.partner_id.commercial_partner_id.dnk_l10n_mx_edi_usage or False
            self.l10n_mx_edi_payment_method_id = self.partner_id.commercial_partner_id.dnk_l10n_mx_edi_payment_method_id.id or False
