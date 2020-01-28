# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class PurchaseOrder(models.Model):

	_inherit = 'purchase.order'

	receipt_status = fields.Selection([
		('full', "Fully Delivered"),
		('partial', "Partially Delivered"),
		('not', "Not Delivered"),
	], string="Receipt Status",compute='update_receipt_status',store=True)
	
	@api.multi
	@api.depends('order_line.product_qty','order_line.qty_received')
	def update_receipt_status(self):
		for order in self:
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
				order.delivery_status = 'partial'