# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from lxml import etree
from odoo.exceptions import UserError, RedirectWarning, ValidationError

class CRMLead(models.Model):
    _inherit = "crm.lead"


    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(CRMLead, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        doc = etree.XML(res['arch'])
        for node in doc.xpath("//field[@name='dnk_family_id']"):
            colors = self.env['product.category'].search([('parent_id','=',False)])
            if colors:
                parent_categ = []
                for color in colors:
                    if color:
                        parent_categ.append(color.id)
                if parent_categ:
                    node.set('domain', "[('parent_id', 'in', "+str(parent_categ)+")]")
        res['arch'] = etree.tostring(doc)
        return res


    @api.multi
    @api.onchange('dnk_price', 'dnk_pieces')
    @api.depends('dnk_price', 'dnk_pieces')
    def _get_revenue(self):
        for lead in self:
            lead.planned_revenue = lead.dnk_price * lead.dnk_pieces


    @api.multi
    def write(self, vals):
        res = super(CRMLead, self).write(vals)
        if  self.type == ('opportunity')  and (self.dnk_price <= 0 or self.dnk_pieces <= 0):
            raise ValidationError(_('The Price and Pieces must be greater than 0.'))
        return res


    dnk_final_customer_id = fields.Many2one('res.partner','- Final Customer')
    dnk_is_vendor = fields.Boolean('- Is Vendor?')
    dnk_family_id = fields.Many2one('product.category', '- Family', required=False)
    dnk_subfamily_id = fields.Many2one('product.category','- SubFamily')
    dnk_product_id = fields.Many2one('product.product','- Product')
    dnk_price = fields.Float("- Price")
    dnk_pieces = fields.Integer("- Pieces")
