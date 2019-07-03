# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError

class PurchaseOrderFile(models.Model):
    _inherit = ['sale.order']


    @api.multi
    @api.onchange('dnk_purchase_order_name')
    def update_client_order_ref(self):
        for sale in self:
            if sale.dnk_purchase_order_name:
                sale.client_order_ref = sale.dnk_purchase_order_name.lower().replace('.pdf','').upper()

    dnk_purchase_order_name = fields.Char('- Purchase Order Name')
    dnk_purchase_order_file = fields.Binary('- Purchase Order File', store=True)

    @api.model
    def action_confirm(self):
        if self.partner_id.dnk_purchase_order_required and not self.dnk_purchase_order_name :
            raise ValidationError(_('The settings for this client requires a purchase order file.'))
        res =super(PurchaseOrderFile, self).action_confirm()
        return res
