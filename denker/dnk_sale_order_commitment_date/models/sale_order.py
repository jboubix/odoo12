# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta
from odoo import api, fields, models, _
from .functions import add_business_days, next_business_day
from openerp.exceptions import ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta, datetime, time
from odoo import api, fields, models, _


class SaleOrder(models.Model):
    """Add several date fields to Sales Orders, computed or user-entered"""
    _inherit = 'sale.order'

    # Eliminar del siguiente campo el parámetro: compute='_compute_commitment_date',
    dnk_longest_commitment_date = fields.Datetime(string='- Longest Commitment Date', store=True,
                                    help="The longest Commitment Date of the Order Lines",
                                    readonly=True)
    dnk_longest_recommitment_date = fields.Datetime(string='- Longest Recommitment Date', store=True,
                                    help="The longest Recommitment Date of the Order Lines",
                                    readonly=True)


    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            confirmation_date = fields.Datetime.from_string(order.confirmation_date)
            # Colocar la bandera de Cambio de Fecha Compromiso en Falso, ya que
            # sólo me interesan los cambios a partir de que el pedido fue confirmado
            max_commitment_date = False
            for line in order.order_line:
                # Si la Fecha Solicitada no está establecida, calcularla
                if line.dnk_commitment_date == False:
                    line.dnk_commitment_date = next_business_day(confirmation_date + timedelta(days=line.customer_lead or 0.0) + timedelta(days=line.order_id.team_id.dnk_transit_days or 0.0))
                    #line.dnk_commitment_date = add_business_days(commitment_date, line.customer_lead or 0.0)
                else:
                    # Si la Fecha Solicitada está establecida verificar si es mayor a la "Fecha Calculada" de Entrega
                    calculated_lead_time = next_business_day(confirmation_date + timedelta(days=line.customer_lead or 0.0) + timedelta(days=line.order_id.team_id.dnk_transit_days or 0.0))
                    # calculated_lead_time = add_business_days(commitment_date, line.customer_lead or 0.0)
                    line_commitment_date = fields.Datetime.from_string(line.dnk_commitment_date)

                    # Si la fecha de compromiso es sábado o domingo enviar mensaje de error
                    if line_commitment_date.weekday() >= 5:
                        # Enviar mensaje de Error
                        raise ValidationError(_('You cannot delivering on Saturday nither Sunday.\n')
                                            + _("Please modify the Commitment Date of \"[" + line.product_id.default_code + "] " + line.product_id.name + "\" product."))

                    # print("calculated_lead_time", type(calculated_lead_time), calculated_lead_time)
                    # print("line_commitment_date", type(line_commitment_date), line_commitment_date)
                    if calculated_lead_time > line_commitment_date:
                        # Enviar mensaje de Error
                        raise ValidationError(_('You cannot delivering before the Product Lead Time plus Transit Days of the Sales Channel.\n')
                                            + _("Please modify the Commitment Date of \"[" + line.product_id.default_code + "] " + line.product_id.name + "\" product."))

                line.dnk_final_commitment_date = line.dnk_commitment_date

                if max_commitment_date == False:
                    max_commitment_date = line.dnk_commitment_date
                elif max_commitment_date<line.dnk_commitment_date:
                    max_commitment_date = line.dnk_commitment_date

            order.dnk_longest_commitment_date = max_commitment_date
        return res


    # Si se cancela el pedido, hacer todas las fechas nulas
    @api.multi
    def action_cancel(self):
        res = super(SaleOrder, self).action_cancel()
        for order in self:
            order.dnk_longest_commitment_date = False
            order.dnk_longest_recommitment_date = False
            for line in order.order_line:
                line.dnk_commitment_date = False
                line.dnk_final_commitment_date = False
                line.dnk_recommitment_date = False
                line.dnk_recommitment_date_changed = False
        return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    dnk_commitment_date = fields.Datetime(string="- Initial Commitment Date",
                                    help="It is the \"Commitment Date\" in which the client will receive the product, "
                                         "is calculated with the \"Customer Lead Time\" of the product plus the \"Transit Days\". of the Sales Channel.")
    dnk_final_commitment_date = fields.Datetime(string='- Final Commitment Date', store=True,
                                    help="Is equal to \"Commitment Date\" but if the Line have \"Recommitment Date\", "
                                         "then this date is equal to \"Recommitment Date\".")
    dnk_recommitment_date = fields.Datetime(string='- Recommitment Date', store=True,
                                    help="Date by which the products are sure to be delivered. This is "
                                         "a date that you can promise to the customer, based on the "
                                         "Product Lead Times.", invisible=True)
    dnk_recommitment_date_changed = fields.Boolean(string='- Recommitment Date Changed?',
                                    default=False, copy=False, store=True, invisible=True)


    # Configurar la Fecha Planeada de las entregas del pedido
    @api.multi
    def _prepare_procurement_values(self, group_id=False):
        vals = super(SaleOrderLine, self)._prepare_procurement_values(group_id=group_id)
        for line in self:
            if line.dnk_commitment_date:
                # FIX buscar la función original
                date_planned = fields.Datetime.from_string(line.dnk_commitment_date) - timedelta(days=line.order_id.company_id.security_lead or 0.0)
            else:
                if line.order_id.team_id:
                    transit_days = line.order_id.team_id.dnk_transit_days
                else:
                    transit_days = 0
                # fields.date.today().strftime(DEFAULT_SERVER_DATE_FORMAT)
                date_planned = fields.date.today() + \
                               timedelta(days=line.customer_lead or 0.0) + \
                               timedelta(days=transit_days or 0.0) - \
                               timedelta(days=line.order_id.company_id.security_lead or 0.0)
                date_planned = next_business_day(date_planned)
            vals.update({
                'date_planned': fields.Datetime.to_string(date_planned),
            })
        return vals

    # Recalcular el campo "customer_lead" al cambiar de Equipo de Ventas
    #@api.multi
    #@api.onchange('team_id')
    #def _onchange_team_id_set_customer_lead(self):
    #    for order in self:
    #        for line in order.order_line:
    #            line.customer_lead = line.product_id.sale_delay + order.team_id.dnk_transit_days


    # Sumar los días de tránsito a los días de entrega de la línea del pedido
    #@api.onchange('product_id')
    #def _onchange_product_id_set_customer_lead(self):
    #    self.customer_lead = self.product_id.sale_delay + self.order_id.team_id.dnk_transit_days


    # Si el usuario cambia el campo "Fecha Reconfirmación", avisar al usuario que el cliente será notificado con un correo
    @api.multi
    @api.depends('dnk_recommitment_date')
    def send_warning_message(self):
        max_last_recommitment_date = False
        for line in self:
            if line.order_id.state in ('sale', 'done') and line.dnk_recommitment_date != line.dnk_commitment_date:
                # TO DO: Reprogramar entregas
                # Cuando sea posible, reprogramar las entregas y la órden de producción
                # for move in line.move_ids:
                #    pass move.date

                # Levantar la bandera para saber que el campo dnk_recommitment_date ha cambiado
                line.dnk_recommitment_date_changed = True
                line.dnk_final_commitment_date = line.dnk_recommitment_date
                warning = {}
                title = _('Commitment date has been changed!')
                message = _('The Commitment Date has been changed. The customer is going to be notified automatically at saving the Order.')
                warning = {
                        'title': title,
                        'message': message,
                }
                if warning:
                    return {'warning': warning}

                if max_last_recommitment_date == False:
                    max_last_recommitment_date = line.dnk_recommitment_date
                elif max_last_recommitment_date<line.dnk_recommitment_date:
                    max_last_recommitment_date = line.dnk_recommitment_date

                line.order_id.dnk_longest_recommitment_date = max_last_recommitment_date


    # Al crear el registro, escribir el nuevo campo 'dnk_commitment_date'
    @api.model
    def create(self, vals):
        res = super(SaleOrderLine, self).create(vals)
        if not res.dnk_commitment_date:
            res.write({
                'dnk_commitment_date': res.dnk_commitment_date,
                'dnk_recommitment_date': res.dnk_recommitment_date,
                'dnk_recommitment_date_changed': res.dnk_recommitment_date_changed,
            })
        return res


    # Escribir el nuevo campo 'dnk_commitment_date'
    @api.multi
    def write(self, vals):
        res = super(SaleOrderLine, self).write(vals)

        for line in self:
            commitment_date_changed = line.dnk_recommitment_date_changed
            if commitment_date_changed:
                line.dnk_recommitment_date_changed = False
                if line.order_id.partner_id.parent_id:
                    recommitment_notification = line.order_id.partner_id.parent_id.dnk_recommitment_notification
                else:
                    recommitment_notification = line.order_id.partner_id.dnk_recommitment_notification
                if line.order_id.state in ('sale', 'done') and recommitment_notification:
                    # Env iar correo al cliente informándole el cambio en la Fecha Compromiso
                    template_obj = self.env['mail.template'].search([('name','=','Dnk - Commitment Date - Send by Email')], limit=1)
                    body = self.env['mail.template'].render_template(template_obj.body_html, 'sale.order.line', line.id)
                    if template_obj:
                        mail_values = {
                            'subject': self.env['mail.template'].render_template(template_obj.subject, 'sale.order.line', line.id),
                            'body_html': body,
                            'email_to': line.order_id.partner_id.email,
                            'email_from': self.env.user.email and '%s <%s>' % (self.env.user.name, self.env.user.email) or '',
                            'reply_to': self.env.user.email or '',
                            'res_id': line.id,
                            'model': 'sale.order.line',
                            'body': body,
                        }
                        create_and_send_email = self.env['mail.mail'].create(mail_values).send()
                        # TO DO: Registrar en el LOG que se envió un correo por cambio de recommitment_date

        return res


    # Si el usuario cambia el campo "Fecha Reconfirmación", avisar al usuario que
    # la fecha de Reconfimación no debe ser menor a la Fecha de Confirmación
    @api.onchange('dnk_commitment_date')
    def onchange_commitment_date(self):
        """Warn if the requested dates is sooner than the commitment date"""
        # Si el pedido no está confirmado tomar la fecha actual, si no, la Fecha de Confirmación
        calculated_lead_time = next_business_day(fields.date.today() + timedelta(days=self.customer_lead or 0.0) + timedelta(days=self.order_id.team_id.dnk_transit_days or 0.0))
        calculated_lead_time = datetime.combine(calculated_lead_time, time(0, 0))
        if (self.dnk_commitment_date and fields.Datetime.from_string(self.dnk_commitment_date) < calculated_lead_time):
            return {'warning': {
                'title': _('Commitment date is too soon!'),
                'message': _("The commitment date is "
                             "sooner than the product sale delay plus plus transit days. You may be "
                             "unable to customer's delivery on time.")
                }
            }
        if self.dnk_commitment_date:
            if fields.Datetime.from_string(self.dnk_commitment_date).weekday() >= 5:
                return {'warning': {
                    'title': _('Commitment date is weekend!'),
                    'message': _("The commitment date is "
                                 "weekend (Saturday or Sunday. You may be "
                                 "unable to delivery on weekend. Please change the Commitment Date.")
                    }
                }
