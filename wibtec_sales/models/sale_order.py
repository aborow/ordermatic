# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):

	_inherit = "sale.order"

	customer_requested_delivery_date = fields.Date('Customer Requested Delivery Date')
	omc_projected_shipping_date = fields.Date('OMC Projected Shipping Date')
	omc_actual_delivery_date = fields.Date('OMC Actual Delivery Date')
	order_contact = fields.Char('Order Contact')

	@api.multi
	def action_confirm(self):
		res = super(SaleOrder, self).action_confirm()
		if not self.order_contact:
			raise ValidationError(_('Please enter value for "Order Contact" to confirm the quotation.'))
		return res