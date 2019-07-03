# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.tools import append_content_to_html, DEFAULT_SERVER_DATE_FORMAT

class report_account_followup_report(models.AbstractModel):
    _inherit = "account.followup.report"

    @api.model
    def send_email(self, options):
        partner = self.env['res.partner'].browse(options.get('partner_id'))
        # José Candelas
        # original = email = self.env['res.partner'].browse(partner.address_get(['invoice'])['invoice']).email
        email = partner.email
        if email and email.strip():
            body_html = self.with_context(print_mode=True, mail=True, keep_summary=True).get_html(options)
            msg = self.get_post_message(options)
            msg += '<br>' + body_html.decode('utf-8')
            msg_id = partner.message_post(body=msg, subtype='account_reports.followup_logged_action')
            email = self.env['mail.mail'].create({
                'mail_message_id': msg_id.id,
                'subject': _('%s Payment Reminder') % (self.env.user.company_id.name) + ' - ' + partner.name,
                'body_html': append_content_to_html(body_html, self.env.user.signature or '', plaintext=False),
                'email_from': self.env.user.email or '',
                'email_to': email,
                'body': msg,
            })
            return True
        raise UserError(_('Could not send mail to partner because it does not have any email address defined'))
