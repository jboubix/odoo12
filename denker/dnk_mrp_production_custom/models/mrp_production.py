# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta
from odoo import api, fields, models, _
import string


"""
 * Get color (black/white) depending on bgColor so it would be clearly seen.
 * @param bgColor
 * @returns {string}
 """
def getColorByBgColor(bgColor):
    if not bgColor:
        return '#000000'
    if bgColor[0] == '#':
        bgColor = bgColor[1:]
    return '#000000' if (int(bgColor, 16) > 8388607) else '#FFFFFF'


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.depends('product_id')
    def _dnk_compute_attribute_color(self):
        for production in self:
            production.dnk_attribute_color = "#313131"
            for attribute_value in production.product_id.attribute_value_ids:
                if 'attribute_value' in  attribute_value and attribute_value.html_color != False:
                    production.dnk_attribute_color = attribute_value.html_color
                    production.dnk_attribute_color_name = attribute_value.name
                    if all(c in string.hexdigits for c in attribute_value.html_color[1:]):
                        production.dnk_attribute_inverse_color = getColorByBgColor(attribute_value.html_color)
                    break


    # Sólo agregar al campo original: track_visibility='onchange'
    date_planned_start = fields.Datetime(
        'Deadline Start', copy=False, default=fields.Datetime.now,
        index=True, required=True,
        states={'confirmed': [('readonly', False)]}, oldname="date_planned", track_visibility='onchange')

    dnk_subfamily = fields.Many2one('product.category', string='- Subfamily', related='product_id.product_tmpl_id.categ_id', store=True)
    dnk_family = fields.Many2one('product.category', string='- Family', related='dnk_subfamily.parent_id', store=True)
    dnk_color = fields.Many2one('product.category', string='- Color', related='dnk_family.parent_id', store=True)
    dnk_product_default_code = fields.Char(string='- Product Internal Reference', compute='_get_product_default_code', store=True)

    workorder_ready = fields.Char(
        '- Work Order',
        readonly=True)
    workorder_ready_state = fields.Selection([
        ('pending', 'Pending'),
        ('ready', 'Ready'),
        ('progress', 'In Progress'),
        ('done', 'Finished'),
        ('cancel', 'Cancelled')], string='- WO Status',
        readonly=True)

    dnk_attribute_color = fields.Char(string='- Color', store=True, default="#313131",
                                      compute="_dnk_compute_attribute_color", readonly=True,
                                      help="HTML Color Attribute of the Product.")
    dnk_attribute_inverse_color =fields.Char(string='- Inverse Color', store=True, default="#313131",
                                      compute="_dnk_compute_attribute_color", readonly=True,
                                      help="HTML Color Attribute of the Product.")
    dnk_attribute_color_name = fields.Char(string='- Color Name', store=True,
                                      compute="_dnk_compute_attribute_color", readonly=True,
                                      help="Name Color Attribute of the Product.")


    @api.multi
    @api.depends('product_id', 'product_id.default_code')
    def _get_product_default_code(self):
        for production in self:
            production.dnk_product_default_code = production.product_id.default_code


    @api.multi
    @api.depends('workorder_ids.state')
    def _compute_workorder_done_count(self):
        data = self.env['mrp.workorder'].read_group([
            ('production_id', 'in', self.ids),
            ('state', '=', 'done')], ['production_id'], ['production_id'])
        count_data = dict((item['production_id'][0], item['production_id_count']) for item in data)
        for production in self:
            production.workorder_done_count = count_data.get(production.id, 0)
            for workorder in production.workorder_ids:
                if workorder.state in ('ready', 'progress'):
                    production.write({'workorder_ready': workorder.name, 'workorder_ready_state': workorder.state})
                    break
