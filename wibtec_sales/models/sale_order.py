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

class SaleReport(models.Model):

	_inherit='sale.report'

	omc_projected_shipping_date = fields.Date('OMC Projected Shipping Date',readonly=True)
	omc_actual_delivery_date = fields.Date('OMC Actual Delivery Date',readonly=True)

	def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
		fields['omc_projected_shipping_date'] = ", s.omc_projected_shipping_date as omc_projected_shipping_date"
		fields['omc_actual_delivery_date'] = ", s.omc_actual_delivery_date as omc_actual_delivery_date"
		groupby += ', s.omc_projected_shipping_date'
		groupby += ', s.omc_actual_delivery_date'
		return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)