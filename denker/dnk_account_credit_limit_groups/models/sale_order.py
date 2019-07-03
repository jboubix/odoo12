# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools


class DnkSaleOrder (models.Model):
    _inherit = "sale.order"

    @api.multi
    def _get_accounting_edit_form(self):

        for rec in self:
            if self.env.user.has_group('dnk_account_credit_limit_groups.dnk_account_credit_limit_group') :
                rec.dnk_edit_accounting_fields = True
            else :
                rec.dnk_edit_accounting_fields = False

    dnk_edit_accounting_fields = fields.Boolean('- Edit Accounting Fields?', compute='_get_accounting_edit_form', store=False)


    @api.multi
    @api.depends('permitted_credit_limit')
    @api.onchange('permitted_credit_limit')
    def udpate_allow_stock_moves(self):
        for sale in self._origin:
            if (sale.permitted_credit_limit):
                for stock_picking in sale.picking_ids:
                    stock_picking.write({'allow_delivery':False})
            else:
                for stock_picking in sale.picking_ids:
                    stock_picking.write({'allow_delivery':True})
