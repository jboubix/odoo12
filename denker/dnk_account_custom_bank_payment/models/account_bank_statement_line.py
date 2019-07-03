
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    def process_reconciliation(self, counterpart_aml_dicts=None,
                               payment_aml_rec=None, new_aml_dicts=None):
        res = super(AccountBankStatementLine, self).process_reconciliation(
            counterpart_aml_dicts=counterpart_aml_dicts,
            payment_aml_rec=payment_aml_rec, new_aml_dicts=new_aml_dicts)
        payments = res.mapped('line_ids.payment_id')

        for payment in payments:
            payment_type = payment.payment_type
            partner_type = payment.partner_type
            xml_file_name = payment.l10n_mx_edi_cfdi_name

            # Use the right sequence to set the name
            if payment_type == 'transfer':
                sequence_code = 'account.payment.transfer'
            else:
                if partner_type == 'customer':
                    if payment_type == 'inbound':
                        sequence_code = 'account.payment.customer.invoice'
                    if payment_type == 'outbound':
                        sequence_code = 'account.payment.customer.refund'
                if partner_type == 'supplier':
                    if payment_type == 'inbound':
                        sequence_code = 'account.payment.supplier.refund'
                    if payment_type == 'outbound':
                        sequence_code = 'account.payment.supplier.invoice'
            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print(payment_type)
            print(partner_type)
            print(sequence_code)
            name = self.env['ir.sequence'].with_context(ir_sequence_date=self.date).next_by_code(sequence_code)

            # Falta hacer la corrección del archivo xml como lo hace el script: fixmovename.py
            model = "account.payment"
            journal_code = payment.journal_id.code

            attachments = self.env['ir.attachment'].search([('res_model','=',model),('res_id','=',payment.id)])
            base_file_name = journal_code + "-" + name + "-MX-Payment-10."

            for attachment in attachments:
                file_extension = attachment['datas_fname'][-3:]
                current_file_name = base_file_name + file_extension
                if current_file_name != attachment.datas_fname:
                    # Si es que está incorrecto es el archivo xml, también corregir el campo: l10n_mx_edi_cfdi_name del account.payment
                    if file_extension == 'xml':
                        xml_file_name = current_file_name
                        # Corregir los campos: name, datas_fname y res_name del Attachment
                        vals_attachment = {
                            'name': current_file_name,
                            'datas_fname': current_file_name,
                            'res_name': payment.name,
                        }
                        attachment.write(vals_attachment)
                        break

            """if partner_type == 'supplier':
                payment.write({
                    'l10n_mx_edi_cfdi_name': xml_file_name,
                })
            else:
                payment.write({
                    # 'l10n_mx_edi_partner_bank_id': self.bank_account_id,
                    'name': name,
                    'l10n_mx_edi_cfdi_name': xml_file_name,
                })"""
            payment.write({
                # 'l10n_mx_edi_partner_bank_id': self.bank_account_id,
                'name': name,
                'l10n_mx_edi_cfdi_name': xml_file_name,
            })
        return res
