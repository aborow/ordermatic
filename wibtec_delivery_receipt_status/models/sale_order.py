# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class SaleOrder(models.Model):

	_inherit = "sale.order"

	delivery_status = fields.Selection([
		('full', "Fully Delivered"),
		('partial', "Partially Delivered"),
		('not', "Not Delivered"),
	], string="Delivery Status" ,compute='update_delivery_status',store=True)

	@api.multi
	@api.depends('order_line.qty_delivered','order_line.product_uom_qty')
	def update_delivery_status(self):
		for order in self:
			fully_delivered = [line for line in order.order_line if line.product_uom_qty ==  line.qty_delivered]
			partial_delivered = [line for line in order.order_line if line.qty_delivered <  line.product_uom_qty and line.qty_delivered !=  0.0]
			partial_delivered_with_zero_qty = [line for line in order.order_line if line.qty_delivered <  line.product_uom_qty and line.qty_delivered ==  0.0]
			not_delivered = [line for line in order.order_line if line.qty_delivered == 0.0]
			if len(order.order_line) == len(fully_delivered):
				order.delivery_status = 'full'
			elif len(partial_delivered) > 0:
				order.delivery_status = 'partial'
			elif len(partial_delivered_with_zero_qty) > 0:
				order.delivery_status = 'partial'
			elif len(order.order_line) == len(not_delivered):
				order.delivery_status = 'not'