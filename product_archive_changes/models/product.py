#! -*- encoding: utf-8 -*-
import logging

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

"""
class MrpProductProduce(models.TransientModel):
    _inherit = 'mrp.product.produce'


    @api.multi
    def do_produce(self):
        if self.product_tracking == 'serial':
            self.create_serial_number()
        return super(MrpProductProduce, self).do_produce()


    @api.multi
    def create_serial_number(self):
        self.ensure_one()
        ProductionLot = self.env['stock.production.lot']
        serial = self.env['ir.sequence']\
                        .next_by_code('stock.lot.serial')
        serial_id = ProductionLot.create({
                                        'name': serial,
                                        'product_id': self.product_id.id
                                        })
        if serial_id:
            self.lot_id = serial_id.id
"""
