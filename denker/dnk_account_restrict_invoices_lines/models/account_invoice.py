# -*- coding: utf-8 -*-
from odoo import models, fields, api


class DnkRestrictAccountInvoiceLines(models.Model):
    _inherit = "account.invoice.line"

    @api.multi
    def _check_account_group(self):
        for rec in self:
            if self.env.user.has_group('dnk_account_restrict_invoices_lines.dnk_account_invoice_lines_admin') :
                rec.dnk_mod_invoice_line_ids = True
            else :
                rec.dnk_mod_invoice_line_ids = False

    dnk_mod_invoice_line_ids = fields.Boolean(String='- Edit Account Invoice Lines', compute='_check_account_group', store=False)
