# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions,_
from datetime import datetime, date, time, timedelta
import calendar

class SaleConfigSettings(models.Model):
    _inherit = "res.company"

    inmediate_payment = fields.Many2one('account.payment.term',string="Término de pago inmediato")


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    inmediate_payment = fields.Many2one('account.payment.term',string="Término de pago inmediato", related='company_id.inmediate_payment')

class CreditLimitAlertSaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    permitted_credit_limit = fields.Boolean('Límite de crédito excedido permitido', default=False)
    paid_sale_order = fields.Boolean('Pedido Pagado', default=False)

    @api.one
    @api.multi
    def action_confirm(self):
        current_date = date.today() - timedelta(days=15)
        cr = self.env.cr

        sql = ""

        if self.partner_id.parent_id:
            sql = "SELECT COALESCE(SUM(1),0) FROM account_invoice WHERE type='out_invoice' AND state='open' AND date_due<='"+str(current_date)+"' AND partner_id NOT IN (SELECT partner_id FROM res_company) AND (partner_id='"+str(self.partner_id.id)+"' OR partner_id='"+str(self.partner_id.parent_id.id)+"')"
        else:
            sql = "SELECT COALESCE(SUM(1),0) FROM account_invoice WHERE type='out_invoice' AND state='open' AND date_due<='"+str(current_date)+"' AND partner_id NOT IN (SELECT partner_id FROM res_company) AND partner_id='"+str(self.partner_id.id)+"'"

        cr.execute(sql)
        facturas_vencidas = cr.fetchone()
        fac = max(facturas_vencidas)
        pago_in = self.company_id.inmediate_payment.id

        if self.partner_id.block_sales==True:
            raise exceptions.ValidationError('El cliente tiene bloqueadas las ventas')

        if self.partner_id.parent_id.block_sales==True:
            raise exceptions.ValidationError('La compañía del cliente tiene bloqueadas las ventas')

        if not self.payment_term_id:
            raise exceptions.ValidationError('Necesita seleccionar un plazo de pago.')

        if (self.payment_term_id.id==pago_in and self.paid_sale_order!=True):
            raise exceptions.ValidationError('Si el pago es inmediato, necesita validar que esta orden esté pagada')

        if (fac >= 1 and self.payment_term_id.id != pago_in and self.permitted_credit_limit is not True):
            raise exceptions.ValidationError('Este cliente o la empresa a la que pertenece tiene facturas vencidas.')
        else:

            if self.partner_id.credit_limit != 0:
                credit = self.env['res.currency']._compute(self.company_id.currency_id,self.currency_id,self.partner_id.credit)
                credit_limit = self.env['res.currency']._compute(self.company_id.currency_id,self.currency_id,self.partner_id.credit_limit)
                c_credit = self.env['res.currency']._compute(self.company_id.currency_id,self.currency_id,self.partner_id.parent_id.credit)
                c_credit_limit = self.env['res.currency']._compute(self.company_id.currency_id,self.currency_id,self.partner_id.credit_limit)


                if credit + self.amount_total > credit_limit:
                    if self.payment_term_id.id != pago_in:
                        if self.permitted_credit_limit is not True:
                            self.avisado = True
                            raise exceptions.ValidationError('Este cliente ha exedido el Límite de Crédito. Su límite actual es: '
                                                             + str(self.partner_id.credit_limit) +', actualmente tiene una deuda de: '
                                                             + str(self.partner_id.credit) + ' y disponible tiene '
                                                             + str(self.partner_id.credit_available)
                                                             + ', debe de autorizar el Límite de Crédito excedido' )

                if c_credit + self.amount_total > c_credit_limit:
                    if self.payment_term_id.id != pago_in:
                        if self.permitted_credit_limit is not True:
                            self.avisado = True
                            raise exceptions.ValidationError('La compañía del cliente ha exedido el Límite de Crédito. Su límite actual es: '
                                                             + str(self.partner_id.parent_id.credit_limit) +', actualmente tiene una deuda de: '
                                                             + str(self.partner_id.parent_id.credit) + ' y disponible tiene '
                                                             + str(self.partner_id.parent_id.credit_available)
                                                             + ', debe de autorizar el Límite de Crédito excedido' )


            res = super(CreditLimitAlertSaleOrder, self).action_confirm()

            return res

class CreditLimitAlertStockPicking(models.Model):
    _name = "stock.picking"
    _inherit = 'stock.picking'


    allow_delivery = fields.Boolean('Permitir entrega con facturas vencidas', default=False)

    @api.multi
    def button_validate(self):
        self.ensure_one()
        if self.partner_id:
            if self.picking_type_code == 'outgoing':
                current_date = date.today() - timedelta(days=15)
                cr = self.env.cr

                sql = ""

                if self.partner_id.parent_id:
                    sql = "SELECT COALESCE(SUM(1),0) FROM account_invoice WHERE type='out_invoice' AND state='open' AND date_due<='"+str(current_date)+"' AND partner_id NOT IN (SELECT partner_id FROM res_company) AND (partner_id='"+str(self.partner_id.id)+"' OR partner_id='"+str(self.partner_id.parent_id.id)+"')"
                else:
                    sql = "SELECT COALESCE(SUM(1),0) FROM account_invoice WHERE type='out_invoice' AND state='open' AND date_due<='"+str(current_date)+"' AND partner_id NOT IN (SELECT partner_id FROM res_company) AND partner_id='"+str(self.partner_id.id)+"'"

                cr.execute(sql)
                facturas_vencidas = cr.fetchone()
                fac = max(facturas_vencidas)
                if fac >= 1 and self.allow_delivery is not True:
                    raise exceptions.ValidationError('Este cliente o la empresa a la que pertenece tiene facturas vencidas.')
                else:
                    res = super(CreditLimitAlertStockPicking, self).button_validate()
                    return res
            else:
                res = super(CreditLimitAlertStockPicking, self).button_validate()
                return res

        else:
            res = super(CreditLimitAlertStockPicking, self).button_validate()
            return res
