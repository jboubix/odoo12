# -*- coding: utf-8 -*-
from odoo import models, fields, api


class DnkRestrictPurchaseOrdersLines(models.Model):
    _inherit = "purchase.order.line"

    @api.multi
    def _check_purchase_group(self):
        for rec in self:
            if self.env.user.has_group('dnk_purchase_restrict_orders_lines.dnk_purchase_orders_lines_admin') :
                rec.dnk_mod_purchase_line_ids = True
            else :
                rec.dnk_mod_purchase_line_ids = False

    dnk_mod_purchase_line_ids = fields.Boolean(String='- Edit Purchase Lines', compute='_check_purchase_group', store=False)
