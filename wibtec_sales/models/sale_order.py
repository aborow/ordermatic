# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):

	_inherit = "sale.order"

	requested_delivery_date = fields.Date('Requested Delivery Date')
	expected_delivery_date = fields.Date('Expected Delivery Date')
	actual_delivery_date = fields.Date('Actual Delivery Date')
	order_contact = fields.Char('Order Contact')

	@api.multi
	def action_confirm(self):
		res = super(SaleOrder, self).action_confirm()
		if not self.order_contact:
			raise ValidationError(_('Please enter value for "Order Contact" to confirm the quotation.'))
		return res