# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools

class SaleOrderPartner(models.Model):
    _inherit = "sale.order"

    @api.multi
    def _prepare_invoice(self):
        res = super(SaleOrderPartner, self)._prepare_invoice()
        res.update({'fiscal_position_id': self.partner_id.commercial_partner_id.property_account_position_id.id or False,
                    'l10n_mx_edi_usage': self.partner_id.commercial_partner_id.dnk_l10n_mx_edi_usage or False,
                    'l10n_mx_edi_payment_method_id': self.partner_id.commercial_partner_id.dnk_l10n_mx_edi_payment_method_id.id or False, })
        return res
