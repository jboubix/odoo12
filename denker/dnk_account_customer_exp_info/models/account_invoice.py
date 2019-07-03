# -*- encoding: utf-8 -*-
from odoo import api, fields, models, _

class DnkAccountInvoice(models.Model):
    _inherit = "account.invoice"

    dnk_customer_exp_info = fields.Text('- Export Information', help="Campo que estará en el formato PDF de la factura si el campo de 'External Trade' está marcado")

    #Redefino el campo para quital el default que tenía la función _default_comment. BC
    comment = fields.Text()

    def _default_comment(self):
        #invoice_type = self.env.context.get('type', 'out_invoice')
        #if invoice_type == 'out_invoice' and self.env['ir.config_parameter'].sudo().get_param('sale.use_sale_note'):
            #return self.env.user.company_id.sale_note
        return ""
