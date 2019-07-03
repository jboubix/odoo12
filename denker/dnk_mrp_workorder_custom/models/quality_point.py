# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta
from odoo import api, fields, models, _


class QualityPoint(models.Model):
    _inherit = "quality.point"

    note = fields.Html(string='Note', sanitize=False, sanitize_tags=False, sanitize_attributes=False)
