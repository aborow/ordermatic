# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class OrderHistory(models.Model):

	_name = "order.history"
	_desc = "Order History"

	mrp_production_id = fields.Many2one('mrp.production',string='Manufacturin Order')
	sale_order_id = fields.Many2one('sale.order',string="Sale Order #")
	quantity = fields.Float('Quantity')
	total_lead_time = fields.Float('Total Lead Time(in Days)')
	commitment_date = fields.Datetime('Commitment Date')
	suggested_deadline = fields.Datetime('Suggested Deadline')
	delivery_lead_times = fields.Float('Delivery Lead Times(in Days)')