# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
from PIL import Image
import base64


class ProofOfDelivery(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def _get_image(self):
        return dict((p.id, tools.image_get_resized_images(p.dnk_img_tmp_proof_of_delivery)) for p in self)

    @api.one
    def _set_image(self):
        for record in self:
            if record.dnk_img_proof_of_delivery == record.dnk_img_tmp_proof_of_delivery: continue
            self.dnk_img_tmp_proof_of_delivery = tools.image_resize_image_big(self.dnk_img_proof_of_delivery.encode())
            self.dnk_img_proof_of_delivery = self.dnk_img_tmp_proof_of_delivery
        return

    dnk_img_tmp_proof_of_delivery = fields.Binary("- Temporal Proof Of Delivery",
                     help="This field holds the proof of delivery image", store=False)
    dnk_img_proof_of_delivery = fields.Binary(string="- Proof Of Delivery", store=True, inverse="_set_image",
                            help="Medium-sized of proof of delivery image. It is automatically " \
                                 "resized, with aspect ratio preserved.", copy=False)
    dnk_img_proof_of_delivery_name = fields.Char('- Proof Of Delivery File Name', copy=False)
