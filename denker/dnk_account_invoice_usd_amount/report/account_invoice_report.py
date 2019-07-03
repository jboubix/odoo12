# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    dnk_price_subtotal_usd = fields.Float('- Total WOT USD')
    dnk_residual_usd = fields.Float('- Total Residual USD')
    dnk_subfamily =fields.Char('- Subfamily')
    dnk_family =fields.Char('- Family')
    dnk_color =fields.Char('- Color')
    dnk_invoice_number = fields.Char('- Invoice Number')
    dnk_invoice_origin = fields.Char('- Invoice Origin')

    def _from(self):
        select_add_family = """
            LEFT JOIN
                (SELECT subfamily.id, subfamily.name AS  subfamily, family.name AS family, color.name AS color FROM product_category subfamily
			LEFT JOIN
			(SELECT pc2.id, pc2.name, pc2.parent_id FROM product_category pc2 WHERE pc2.parent_id IN
                (SELECT id FROM product_category WHERE parent_id IS NULL)) family  ON family.id = subfamily.parent_id
			LEFT JOIN
			(SELECT pc3.id,pc3.name FROM product_category pc3 WHERE pc3.parent_id IS NULL) color ON family.parent_id = color.id
				WHERE subfamily.parent_id IS NOT NULL AND subfamily.parent_id NOT IN (SELECT id FROM product_category WHERE parent_id IS NULL))
            AS pc ON pc.id = pt.categ_id
        """
        return super(AccountInvoiceReport, self)._from() + select_add_family

    def _select(self):
        select_subtotal_usd = ",sub.dnk_price_subtotal_usd * (CASE WHEN sub.price_total < 0 THEN -1	ELSE 1 END) AS dnk_price_subtotal_usd"
        select_residual_usd = ",sub.dnk_residual_usd as dnk_residual_usd"
        select_family_color = ",sub.subfamily as dnk_subfamily ,sub.family as dnk_family , sub.color as dnk_color "
        select_account_number = ",sub.dnk_invoice_number AS dnk_invoice_number"
        select_account_origin = ",sub.dnk_invoice_origin AS dnk_invoice_origin"

        return super(AccountInvoiceReport, self)._select() + select_subtotal_usd + select_residual_usd + select_family_color + select_account_number + select_account_origin


    def _sub_select(self):
        string_subtotal_usd = ",SUM(ail.dnk_price_subtotal_usd * invoice_type.sign) AS dnk_price_subtotal_usd"
        string_residual_usd = ",ai.dnk_residual_usd / (SELECT count(*) FROM account_invoice_line l2 where invoice_id = ai.id) * count(*) * invoice_type.sign AS dnk_residual_usd"
        string_family_color = ",pc.subfamily,pc.family, pc.color"
        string_account_number = ",ai.number AS dnk_invoice_number"
        string_account_origin = ",ai.origin AS dnk_invoice_origin"
        return super(AccountInvoiceReport, self)._sub_select() + string_subtotal_usd + string_residual_usd + string_family_color + string_account_number + string_account_origin

    def _group_by(self):
        group_family_color = ",pc.subfamily, pc.family, pc.color, ai.number, ai.origin"
        return super(AccountInvoiceReport, self)._group_by() + group_family_color
