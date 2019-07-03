# -*- encoding: utf-8 -*-
from odoo import api, fields, models, _

class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.multi
    def dnk_stock_journal_items(self):
        move_lines = self.env['account.move.line'].search([('ref','=',self.name)])
        res = [line.id for line in move_lines]
        return {
                'domain': "[('id','in',[" + ','.join(map(str, list(res))) + "])]",
                'name'      : _('- Journal Items'),
                'view_mode': 'tree,form',
                'view_type': 'form',
                'res_model': 'account.move.line',
                'type': 'ir.actions.act_window',
            }

    @api.multi
    def dnk_stock_journal_entries(self):
        move_lines = self.env['account.move'].search([('ref','=',self.name)])
        res = [line.id for line in move_lines]
        return {
                'domain': "[('id','in',[" + ','.join(map(str, list(res))) + "])]",
                'name'      : _('- Journal Entries'),
                'view_mode': 'tree,form',
                'view_type': 'form',
                'res_model': 'account.move.line',
                'type': 'ir.actions.act_window',
            }
