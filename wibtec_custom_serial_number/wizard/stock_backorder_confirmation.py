# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import datetime
import logging

_logger = logging.getLogger(__name__)


class StockBackorderConfirmation(models.TransientModel):

    _inherit = 'stock.backorder.confirmation'

    @api.multi
    def create_warranty_information(self, picking_id, order_id):
        if picking_id and order_id:
            for move in picking_id.move_ids_without_package:
                move_line_ids = self.env['stock.move.line'].search(
                    [('product_id', '=', move.product_id.id), ('move_id', '=', move.id)])
                for move_line in move_line_ids:
                    if move.product_id.tracking == 'serial':
                        warranty_information_id = self.env['warranty.information'].create({
                            'partner_id': order_id.partner_id.id,
                            'customer_ID': order_id.partner_id.category_id.name,
                            'product_id': move.product_id.id,
                            'description': move.product_id.long_desc,
                            'street': order_id.partner_id.street,
                            'street2': order_id.partner_id.street2,
                            'city': order_id.partner_id.city,
                            'state_id': order_id.partner_id.state_id.id,
                            'zip': order_id.partner_id.zip,
                            'country_id': order_id.partner_id.country_id.id,
                            'serial_number': move_line.lot_id.name if move_line.lot_id else False,
                            'sale_date': datetime.datetime.strptime(str(order_id.confirmation_date), '%Y-%m-%d %H:%M:%S').date(),
                            'delivery_date': datetime.datetime.strptime(str(picking_id.date_done), '%Y-%m-%d %H:%M:%S').date(),
                            'stock_move_line_id': move_line.id
                        })

    def process(self):
        res = super(StockBackorderConfirmation, self)._process()
        picking_id, order_id = self.return_pickings()
        if picking_id:
            self.create_warranty_information(picking_id, order_id)
        return res

    def process_cancel_backorder(self):
        res = super(StockBackorderConfirmation, self)._process()
        picking_id, order_id = self.return_pickings()
        if picking_id:
            self.create_warranty_information(picking_id, order_id)
        return res

    def return_pickings(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids') or []
        picking_id = False
        order_id = False
        _logger.info("Picking First %s: " % (picking_id,))
        _logger.info("order_id First %s: " % (order_id,))
        if context.get('active_model') == 'sale.order':
            order_id = self.env['sale.order'].browse(active_ids)
            picking_id = self.env['stock.picking'].search(
                [('origin', '=', order_id.name), ('state', '=', 'done')])
        elif context.get('active_model') == 'stock.picking':
            picking_id = self.env['stock.picking'].browse(active_ids)
            order_id = self.env['sale.order'].search(
                [('name', '=', picking_id.origin)])
        _logger.info("Context %s: " % (self._context,))
        _logger.info("Picking Secondddd %s: " % (picking_id,))
        _logger.info("order_id Secondddd  %s: " % (order_id,))
        return picking_id, order_id
