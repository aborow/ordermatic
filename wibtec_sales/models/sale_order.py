# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import datetime
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
		# The creation of a delivery order when a SO is confirmed is not such a
		# straightforward thing as there are two steps involved. So, in order not
		# to fall into any sort of caveat, the update of the delivery scheduled date
		# is delayed a bit. We do this with a scheduled task
		if self.omc_projected_shipping_date:
			res_model_id = self.env['ir.model'].search([('model','=','sale.order')]).id
			cron_id = self.env['ir.cron'].sudo().create({
												'name': 'Update delivery date',
												'model_id': res_model_id,
												'state': 'code',
												'code': "model.update_delivery_date(%s)" % (self.id),
												'interval_number': 1,
												'interval_type': 'minutes',
												'nextcall': datetime.datetime.now() \
																+ datetime.timedelta(minutes = 1),
												'numbercall': 1,
												'doall': True
												})
		return res


	def update_delivery_date(self, sale_id):
		pick = self.env['stock.picking'].search(
												[('sale_id','=',sale_id)],
												order='id ASC',
												limit=1
												)
		if pick:
			pick.scheduled_date = datetime.datetime.combine(
													pick.sale_id.omc_projected_shipping_date,
													pick.scheduled_date.time()
													)

	@api.onchange('omc_projected_shipping_date')
	def _onchange_omc_projected_shipping_date(self):
		#Onchange of omc_projected_shipping_date
		if self.omc_projected_shipping_date:
			current_date_time = datetime.datetime.now()
			self.commitment_date = datetime.datetime.combine(self.omc_projected_shipping_date,current_date_time.time())