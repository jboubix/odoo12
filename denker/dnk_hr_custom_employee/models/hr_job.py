
# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class HrJob(models.Model):
    _inherit = 'hr.job'

    # register/deregister an employee
    employee_register_ids = fields.One2many(comodel_name='hr.employee.register',
                                inverse_name='job_id',
                                string='- Employee register',
                                help='Employee register history for statistic use.')

    employee_deregister_ids = fields.One2many(comodel_name='hr.employee.register',
                                inverse_name='job_id',
                                string='- Employee deregister',
                                help='Employee deregister history for statistic use.')


class EmployeeRecruitmentHistory(models.Model):
    _name = 'hr.employee.register'
    _description = 'Employee register'
    _order = 'register_date'

    name = fields.Char(tring='Employee', required=True, size=32)
    job_id = fields.Many2one('hr.job', 'Job', required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True)
    register_date = fields.Date(string='Fecha', required=True)
    leave_cause_id = fields.Many2one(
        'hr.employee.leave.cause',
        string='Motivo de Baja',
        required=False)


class EmployeeLeaveCause(models.Model):
    _name = 'hr.employee.leave.cause'
    _description = 'Employee leave cause'

    name = fields.Char(tring='Leave Cause', required=True, size=32)
