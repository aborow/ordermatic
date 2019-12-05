# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

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