# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends('partner_id')
    def _dnk_compute_partner_id(self):
        for sale in self:
            # Supondré que siempre inicio una Sale Order desde una oportunidad.
            # por lo tanto sólo podré seleccionar contactos del cliente de la oportunidad
            if sale :
                sale.dnk_temp_partner_id = sale.opportunity_id.partner_id.id



    dnk_temp_partner_id = fields.Integer(string="- Id de Partner", compute="_dnk_compute_partner_id", store=False, readonly=True)
