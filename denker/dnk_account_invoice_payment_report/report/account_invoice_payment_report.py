# -*- coding: utf-8 -*-

from odoo import tools
from odoo import models, fields, api


class AccountInvoiceReport(models.Model):
    _name = "account.invoice.payment.report"
    _description = "Invoice Payments Statistics"
    _auto = False
    _rec_name = 'date'


    account_invoice_id = fields.Many2one('account.invoice', string='Invoice', readonly=True)
    account_invoice_number = fields.Char(string='Invoice Number', readonly=True)
    account_invoice_state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('paid', 'Paid'),
        ('cancel', 'Cancelled')
        ], string='Invoice Status', readonly=True)
    account_invoice_type = fields.Selection([
        ('out_invoice', 'Customer Invoice'),
        ('in_invoice', 'Vendor Bill'),
        ('out_refund', 'Customer Credit Note'),
        ('in_refund', 'Vendor Credit Note'),
        ], readonly=True)
    date_invoice = fields.Date(readonly=True)
    commercial_partner_id = fields.Many2one('res.partner', string='Partner', readonly=True)
    account_invoice_amount_untaxed_usd = fields.Float(string='Invoice Amount Untaxed USD', readonly=True)
    user_id = fields.Many2one('res.users', string='Salesperson', readonly=True)
    team_id = fields.Many2one('crm.team', string='Sales Channel', readonly=True)
    #payment_amount = fields.Float(string='Payment Amount', readonly=True)
    payment_currency_id = fields.Many2one('res.currency', string='Currency', readonly=True)
    payment_id = fields.Many2one('account.payment', string='Payment', readonly=True)
    date = fields.Date(string='Payment Date', readonly=True)
    #payment_year = fields.Date(string='Payment Year', readonly=True)
    #payment_month = fields.Date(string='Payment Month', readonly=True)
    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    dnk_price_subtotal_usd = fields.Float(string='Price Subtotal', readonly=True)
    quantity = fields.Float(string='Quantity', readonly=True)
    prorated_payment_amount = fields.Float(string='Payment Amount', readonly=True)
    color_id = fields.Many2one('product.category', string='Color', readonly=True)
    family_id = fields.Many2one('product.category', string='Family', readonly=True)
    subfamily_id = fields.Many2one('product.category', string='Subfamily', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', readonly=True)

    _order = 'date desc'


    def _select(self):
        select_str = """
            SELECT aml_apr.id AS id, ai.id as account_invoice_id, ai.number AS account_invoice_number, ai.state AS account_invoice_state, ai.type AS account_invoice_type, ai.date_invoice, ai.commercial_partner_id,
                ai.dnk_amount_untaxed_usd AS account_invoice_amount_untaxed_usd, ai.dnk_residual_usd AS account_invoice_residual_usd, ai.company_id,
                ai.amount_untaxed AS account_invoice_amount_untaxed, ai.amount_tax AS account_invoice_amount_tax, ai.amount_total AS account_invoice_amount_total,
                ai.untaxed_percent AS account_invoice_untaxed_percent, ai.user_id AS user_id, ai.team_id AS team_id,
                aml.amount_currency AS payment_amount, aml.currency_id AS payment_currency_id, aml.payment_id AS payment_id, aml.date AS date,
                to_date(CONCAT(to_char(EXTRACT(YEAR FROM aml.date), '9999'), '0101'), 'YYYYMMDD') AS payment_year,
                to_date(CONCAT(to_char(EXTRACT(YEAR FROM aml.date), '9999'), to_char(EXTRACT(MONTH FROM aml.date), '09'), '01'), 'YYYY MMDD') AS payment_month,
                ail.product_id, ail.dnk_price_subtotal_usd, ail.quantity,
                color.id AS color_id, color.name AS color, family.id AS family_id, subfamily.id AS subfamily_id,
                CASE WHEN aml_apr.currency_name IS NULL THEN (aml_apr.amount*(SELECT rcr.rate FROM res_currency rc
                INNER JOIN res_currency_rate rcr ON rc.id = rcr.currency_id
                WHERE rc.name = 'USD' AND rcr.name <= aml.date ORDER BY rcr.name DESC LIMIT 1)/ai.dnk_amount_untaxed_usd)*ail.dnk_price_subtotal_usd*ai.untaxed_percent
                ELSE (aml_apr.amount_currency/ai.dnk_amount_untaxed_usd)*ail.dnk_price_subtotal_usd*ai.untaxed_percent
                END AS prorated_payment_amount
        """
        return select_str


    def _from(self):
        from_str = """
                FROM (SELECT *, CASE WHEN amount_tax < 0 THEN amount_untaxed/amount_untaxed WHEN amount_tax >= 0 THEN amount_untaxed/(amount_untaxed+amount_tax) END AS untaxed_percent FROM account_invoice) ai
                INNER JOIN account_invoice_line ail ON ai.id = ail.invoice_id
                INNER JOIN account_invoice_account_move_line_rel ai_aml_rel ON ai.id = ai_aml_rel.account_invoice_id
                INNER JOIN account_move_line aml ON ai_aml_rel.account_move_line_id = aml.id
                INNER JOIN account_move am ON ai.move_id = am.id
                INNER JOIN (SELECT apr.id, aml.move_id, apr.credit_move_id, apr.amount, apr.amount_currency, rc.name AS currency_name
                FROM account_move_line aml
                INNER JOIN account_partial_reconcile apr ON aml.id = apr.debit_move_id
                LEFT JOIN res_currency rc ON apr.currency_id = rc.id
                ) aml_apr ON am.id = aml_apr.move_id AND aml_apr.credit_move_id = aml.id
                INNER JOIN account_payment ap ON aml.payment_id = ap.id
                LEFT JOIN product_product pp ON ail.product_id = pp.id
                LEFT JOIN product_template pt ON pp.product_tmpl_id = pt.id
                LEFT JOIN product_category subfamily ON pt.categ_id = subfamily.id
                LEFT JOIN product_category family ON subfamily.parent_id = family.id
                LEFT JOIN product_category color ON family.parent_id = color.id
        """
        return from_str


    def _where(self):
        where_str = """
                WHERE aml.reconciled = True
                ORDER BY aml.date DESC, ail.sequence;
        """
        where_str = ""
        return where_str


    @api.model_cr
    def init(self):
        # self._table = account_invoice_payment_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
                %s %s %s
        )""" % (
                self._table,
                self._select(), self._from(), self._where()))
