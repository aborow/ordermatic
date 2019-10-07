#! -*- encoding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = 'stock.move'

    # Method to allow adding serial numbers to all the lines that still
    # don't have one
    @api.multi
    def add_serial_numbers(self):
        self.ensure_one()
        ProductionLot = self.env['stock.production.lot']
        for l in self.move_line_ids:
            if self.has_tracking == 'serial':
                if not l.lot_name:
                    # Create a new serial and add it to the record
                    serial = self.env['ir.sequence']\
                                    .next_by_code('stock.lot.serial')
                    serial_id = ProductionLot.create({
                                                'name': serial,
                                                'product_id': self.product_id.id
                                                })
                    l.update({
                            'lot_id': serial_id.id,
                            'lot_name': serial_id.name
                            })


"""
class ProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    @api.model
    def check_production_lot_count(self, lot):
        count = 0
        if lot:
            count = self.env['stock.production.lot']\
                        .search_count([('name', 'like', lot)])
        return count


    @api.constrains('name')
    def check_production_lot(self):
        self.ensure_one()
        try:
            original = self._origin.name
        except Exception as e:
            original = self.name
            pass
        if self.check_production_lot_count(original)>1:
            raise ValidationError(
                        'Lot/Serial number %s is already being used' % lot
                        )
"""
