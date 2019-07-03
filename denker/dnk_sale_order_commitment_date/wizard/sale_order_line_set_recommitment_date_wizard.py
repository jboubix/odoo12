# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
import unicodedata

# 2:  imports of openerp
from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class StockPickingPrintLabelWizard(models.TransientModel):
    _name = 'sale.order.line.set.recommitment.date.wizard'
    _description = "Sale Order Line Set Recommitment Date Wizard"

    dnk_recommitment_date = fields.Datetime(string='- Recommitment Date', store=True,
                                    help="Date by which the products are sure to be delivered. This is "
                                         "a date that you can promise to the customer, based on the "
                                         "Product Lead Times.")


    def set_recommitment_date(self):
        line = self.env['sale.order.line'].browse(self.env.context.get('active_id'))
        line.write({'dnk_recommitment_date': self.dnk_recommitment_date, 'dnk_final_commitment_date': self.dnk_recommitment_date, 'dnk_recommitment_date_changed': True})
        #line.dnk_recommitment_date = self.dnk_recommitment_date
        #line.dnk_recommitment_date_changed = True

        dates_list = []
        for order_line in line.order_id.order_line:
            if order_line.order_id.state in ('sale', 'done'):
                if order_line.dnk_recommitment_date:
                    dates_list.append(order_line.dnk_recommitment_date)

        line.order_id.dnk_longest_recommitment_date = max(dates_list)

        # Ya no es necesario enviarlo, al hacer "write" se envía el correo
        """if line.order_id.state in ('sale', 'done') and line.order_id.partner_id.dnk_recommitment_notification:
            # Enviar correo al cliente informándole el cambio en la Fecha Compromiso
            template_obj = self.env['mail.template'].search([('name','=','Dnk - Commitment Date - Send by Email')], limit=1)
            body = self.env['mail.template'].render_template(template_obj.body_html, 'sale.order.line', line.id)
            if template_obj:
                mail_values = {
                    'subject': self.env['mail.template'].render_template(template_obj.subject, 'sale.order.line', line.id),
                    'body_html': body,
                    'email_to': line.order_id.partner_id.email,
                    'email_from': self.env['mail.template'].render_template(template_obj.email_from, 'sale.order.line', line.id),
                    'res_id': line.id,
                    'model': 'sale.order.line',
                    'body': body,
                }
                create_and_send_email = self.env['mail.mail'].create(mail_values).send()"""
