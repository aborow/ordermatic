# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class SaleOrder(models.Model):

	_inherit = "sale.order"

	requested_delivery_date = fields.Date('Requested Delivery Date')
	expected_delivery_date = fields.Date('Expected Delivery Date')
	actual_delivery_date = fields.Date('Actual Delivery Date')
	order_contact = fields.Char('Order Contact')