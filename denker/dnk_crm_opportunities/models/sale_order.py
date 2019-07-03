# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class DnkCRMSaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def get_dnk_final_customer_id(self):
            self.dnk_final_customer_id = self.opportunity_id.dnk_final_customer_id or False
    dnk_final_customer_id = fields.Many2one("res.partner", compute="get_dnk_final_customer_id", string='- Final Customer')


    @api.multi
    def get_dnk_opportunity_id(self):
            self.dnk_opportunity_id = self.opportunity_id.id or False

    #No pude mostrar el  puto opportunity_id desde el xml, entonces la copié, ALV
    dnk_opportunity_id = fields.Many2one("crm.lead", compute="get_dnk_opportunity_id", string='- Opportunity')
