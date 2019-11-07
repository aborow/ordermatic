#! -*- encoding: utf-8 -*-
"""
import logging

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

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
