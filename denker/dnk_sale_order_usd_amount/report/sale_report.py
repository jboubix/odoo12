# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = 'sale.report'

    dnk_price_subtotal_usd = fields.Float('- Untaxed Total USD')
    dnk_family =fields.Char('- Family')
    dnk_subfamily =fields.Char('- Subfamily')
    dnk_color =fields.Char('- Color')

    def _select(self):
        select_subtotal_usd = ",sum(l.dnk_price_subtotal_usd) as dnk_price_subtotal_usd "
        select_family_color = ",pc.family as dnk_family, pc.color as dnk_color, pc.subfamily as dnk_subfamily"
        return super(SaleReport, self)._select() + select_subtotal_usd + select_family_color

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
            AS pc ON pc.id = t.categ_id
        """
        return super(SaleReport, self)._from() + select_add_family

    def _group_by(self):
        dnk_group_by = ",pc.family, pc.color, pc.subfamily"
        return super(SaleReport, self)._group_by() + dnk_group_by
