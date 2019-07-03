# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _

class DnkProductCategory(models.Model):

    _inherit = "product.category"

    dnk_pd_form_type = fields.Selection([('diseno','Diseño'),('personalizado','Personalizado'),('bolsa','Bolsa')],string="- Tipo de Desarrollo de Productos")
