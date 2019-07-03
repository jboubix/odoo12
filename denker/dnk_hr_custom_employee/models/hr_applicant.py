
# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Applicant(models.Model):
    _inherit = 'hr.applicant'

    @api.one
    @api.depends('partner_name', 'job_id')
    def _compute_name(self):
        if self.partner_name and self.job_id:
            self.name = self.job_id.name + ' - ' + self.partner_name


    name = fields.Char(
        string="Subject / Application Name", required=True,
        compute='_compute_name', store=True, readonly=True)
    job_id = fields.Many2one('hr.job', "Applied Job", required=True)
    partner_name = fields.Char("Applicant's Name", required=True)
    reference = fields.Many2one('hr.employee',
                                string='Referred By', copy=False,
                                help='Persona quién recomendó a este empleado')


    @api.model
    def create(self, vals):
        vals_append = {
            'name': str(vals.get('job_id')) + ' - ' + vals.get('partner_name'),
        }
        vals.update(vals_append)

        return super(Applicant, self.with_context(mail_create_nolog=True)).create(vals)


    @api.multi
    def create_employee_from_applicant(self):
        res = super(Applicant, self).create_employee_from_applicant()
        employee_obj =  self.env['hr.employee']
        employee = employee_obj.search([('id', '=', res['res_id'])], limit =1)
        employee.active = False
        return res
