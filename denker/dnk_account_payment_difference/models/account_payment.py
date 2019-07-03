# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools

class PaymentDifference(models.TransientModel):
    _inherit = "account.register.payments"

    @api.one
    @api.depends('invoice_ids', 'amount', 'payment_date', 'currency_id')
    def _compute_payment_difference(self):
        context = dict(self._context or {})
        active_model = context.get('active_model')
        active_ids = context.get('active_ids')
        self.dnk_invoice_ids = self.env[active_model].browse(active_ids)
        if len(self.dnk_invoice_ids) == 0:
            return
        if self.dnk_invoice_ids[0].type in ['in_invoice', 'out_refund']:
            self.dnk_payment_difference = self.amount - self.compute_total_invoices_amount()
        else:
            self.dnk_payment_difference = self.compute_total_invoices_amount() - self.amount

    @api.model
    def compute_total_invoices_amount(self):
        """ Compute the sum of the residual of invoices, expressed in the payment currency """
        payment_currency = self.currency_id or self.journal_id.currency_id or self.journal_id.company_id.currency_id or self.env.user.company_id.currency_id

        total = 0
        for inv in self.dnk_invoice_ids:
            if inv.currency_id == payment_currency:
                total += inv.residual_signed
            else:
                total += inv.company_currency_id.with_context(date=self.payment_date).compute(
                    inv.residual_company_signed, payment_currency)
        return abs(total)


    def create_payment(self):
        if not self.multi:
            return super(PaymentDifference, self).create_payment()
        for partner in self.dnk_partner_ids:
            context = dict(self._context)
            payment = self.env['account.payment'].with_context(context).create(
                self.get_payment_vals_multi_vendor(partner.id))
            payment.post()
        return {'type': 'ir.actions.act_window_close'}

    def get_payment_vals(self):
        """ Hook for extension """
        return {
            'journal_id': self.journal_id.id,
            'payment_method_id': self.payment_method_id.id,
            'payment_date': self.payment_date,
            'communication': self.communication,
            'invoice_ids': [(4, inv.id, None) for inv in self._get_invoices()],
            'payment_type': self.payment_type,
            'amount': self.amount,
            'currency_id': self.currency_id.id,
            'partner_id': self.dnk_partner_id.id,
            'partner_type': self.partner_type,
            'payment_difference_handling': self.payment_difference_handling,
            'writeoff_account_id': self.writeoff_account_id.id,
        }

    dnk_partner_ids = fields.Many2many('res.partner', 'dnk_partner_payment_rel', 'partner_id', 'payment_id', '- Partner')
    dnk_invoice_ids = fields.Many2many('account.invoice', 'account_invoice_payment_rel', 'payment_id', 'invoice_id', string="- Invoices", copy=False, readonly=True)
    dnk_payment_difference = fields.Monetary(string="- Payment Difference", compute='_compute_payment_difference', readonly=True)
    dnk_payment_difference_handling = fields.Selection([('open', 'Keep open'), ('reconcile', 'Mark invoice as fully paid')], default='open', string="- Payment Difference", copy=False)
    dnk_writeoff_account_id = fields.Many2one('account.account', string="- Difference Account", domain=[('deprecated', '=', False)], copy=False)
