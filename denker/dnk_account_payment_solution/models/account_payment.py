# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountPayment(models.Model):
    _inherit = "account.payment"

    #'Autorización de Banco'
    dnk_bank_authorization = fields.Char(string='- Bank Authorization', help='Bank Authorization Code')


class AccountRegisterPayments(models.TransientModel):
    _inherit = 'account.register.payments'

    dnk_bank_authorization = fields.Char(string='- Bank Authorization', help='Bank Authorization Code')


    @api.multi
    def _prepare_payment_vals(self, invoices):
        res = super(AccountRegisterPayments, self)._prepare_payment_vals(invoices)
        res['dnk_bank_authorization'] = self.dnk_bank_authorization  # noqa
        res['communication'] = self.communication  # noqa
        return res
