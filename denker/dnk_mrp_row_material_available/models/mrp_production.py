from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.osv.query import Query
from odoo.models import BaseModel
from odoo.exceptions import AccessError
import logging

_logger = logging.getLogger(__name__)


class MrpProduction(models.Model):
    """ Manufacturing Orders """
    _inherit = 'mrp.production'


    @api.multi
    def button_mark_done(self):
        _logger.info('XXX - Enter to button_mark_done method: uid: %s, model: %s, id: %s, ',
            self._uid, self._name, self.id)

        self.ensure_one()

        _logger.info('XXX - Iterate on Work Orders: uid: %s, model: %s, id: %s',
            self._uid, self._name, self.id)
        for wo in self.workorder_ids:
            if wo.time_ids.filtered(lambda x: (not x.date_end) and (x.loss_type in ('productive', 'performance'))):
                raise UserError(_('Work order %s is still running') % wo.name)

        _logger.info('XXX - Call post_inventory method: uid: %s, model: %s, id: %s',
            self._uid, self._name, self.id)
        self.post_inventory()
        moves_to_cancel = (self.move_raw_ids | self.move_finished_ids).filtered(lambda x: x.state not in ('done', 'cancel'))

        _logger.info('XXX - Moves to cancel: uid: %s, model: %s, id: %s, moves %s',
            self._uid, self._name, self.id, moves_to_cancel)

        moves_to_cancel._action_cancel()

        _logger.info('XXX - Moves already canceled: uid: %s, model: %s, id: %s, moves %s',
            self._uid, self._name, self.id, moves_to_cancel)

        self.write({'state': 'done', 'date_finished': fields.Datetime.now()})

        _logger.info('XXX - Mark MO as Done: uid: %s, model: %s, id: %s',
            self._uid, self._name, self.id)

        return self.write({'state': 'done'})
