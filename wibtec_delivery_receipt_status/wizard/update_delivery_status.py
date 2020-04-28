# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class UpdateDeliveryStatus(models.TransientModel):

    _name = "update.delivery.status"

    @api.multi
    def update_delivery_status(self):
        # Method is used to update deliery status to the flag.
        sale_recs = self.env['sale.order'].search([])
        if sale_recs:
            for order in sale_recs:
                fully_delivered = [line for line in order.order_line if line.product_uom_qty ==  line.qty_delivered]
                partial_delivered = [line for line in order.order_line if line.qty_delivered <  line.product_uom_qty and line.qty_delivered !=  0.0]
                partial_delivered_with_zero_qty = [line for line in order.order_line if line.qty_delivered <  line.product_uom_qty and line.qty_delivered ==  0.0]
                not_delivered = [line for line in order.order_line if line.qty_delivered == 0.0]
                if len(order.order_line) == len(fully_delivered):
                    order.delivery_status = 'full'
                elif len(partial_delivered) > 0:
                    order.delivery_status = 'partial'
                elif len(order.order_line) == len(not_delivered):
                    order.delivery_status = 'not'
                elif len(partial_delivered_with_zero_qty) > 0:
                    order.delivery_status = 'partial'
        purchase_recs = self.env['purchase.order'].search([])
        if purchase_recs:
            for order in purchase_recs:
                fully_delivered = [line for line in order.order_line if line.product_qty ==  line.qty_received]
                partial_delivered = [line for line in order.order_line if line.qty_received <  line.product_qty and line.qty_received !=  0.0]
                partial_delivered_with_zero_qty = [line for line in order.order_line if line.qty_received <  line.product_uom_qty and line.qty_received ==  0.0]
                not_delivered = [line for line in order.order_line if line.qty_received == 0.0]
                if len(order.order_line) == len(fully_delivered):
                    order.receipt_status = 'full'
                elif len(partial_delivered) > 0:
                    order.receipt_status = 'partial'
                elif len(order.order_line) == len(not_delivered):
                    order.receipt_status = 'not'
                elif len(partial_delivered_with_zero_qty) > 0:
                    order.receipt_status = 'partial'