# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

#
# Order Point Method:
#    - Order if the virtual stock of today is bellow the min of the defined order point
#

from odoo import api, models, tools

import logging
import threading

_logger = logging.getLogger(__name__)

class ProcurementOrderpointConfirm(models.TransientModel):
    _name = 'procurement.orderpoint.compute'
    _description = 'Compute Minimum Stock Rules'

    def _procure_calculation_orderpoint(self):
        with api.Environment.manage():
            # As this function is in a new thread, I need to open a new cursor, because the old one may be closed
            new_cr = self.pool.cursor()
            self = self.with_env(self.env(cr=new_cr))
            scheduler_cron = self.sudo().env.ref('stock.ir_cron_scheduler_action')
            # Avoid to run the scheduler multiple times in the same time
            try:
                with tools.mute_logger('odoo.sql_db'):
                    self._cr.execute("SELECT id FROM ir_cron WHERE id = %s FOR UPDATE NOWAIT", (scheduler_cron.id,))
            except Exception:
                _logger.info('Attempt to run procurement scheduler aborted, as already running')
                self._cr.rollback()
                self._cr.close()
                return {}

            self.env['procurement.group']._procure_orderpoint_confirm(
                use_new_cursor=new_cr.dbname,
                company_id=self.env.user.company_id.id)
            new_cr.close()
            return {}

    def procure_calculation(self):
        threaded_calculation = threading.Thread(target=self._procure_calculation_orderpoint, args=())
        threaded_calculation.start()
        return {'type': 'ir.actions.act_window_close'}