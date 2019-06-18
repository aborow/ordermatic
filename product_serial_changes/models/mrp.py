#! -*- encoding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class MrpProductProduce(models.TransientModel):
    _inherit = 'mrp.product.produce'

    force_serial = fields.Char('Force serial',
                                help='Leave blank to create the serial number automatically')

    @api.multi
    def do_produce(self):
        if self.product_tracking == 'serial':
            if self.force_serial:
                try:
                    ProductionLot = self.env['stock.production.lot']
                    if not ProductionLot.search([('name','=',self.force_serial)]):
                        serial_id = ProductionLot.create({
                                                        'name': self.force_serial,
                                                        'product_id': self.product_id.id
                                                        })
                        self.lot_id = serial_id.id
                    else:
                        raise Exception('The serial number is alreay being used')
                except Exception as e:
                    raise ValidationError(_('The serial could not be created:\n%s') % e)
            else:
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
