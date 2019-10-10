# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import odoo
from odoo import api, fields, models, _
import datetime
from odoo.tools.misc import formatLang
from odoo.tools import float_is_zero, float_compare


class AccountInvoice(models.Model):

	_inherit = "account.invoice"
				
	@api.multi
	# Returns the origin date
	def _get_origin_date(self,origin):
		sale_order = self.env['sale.order'].search([('name','=',origin)],limit=1)
		if sale_order.confirmation_date:
			confirmation_date = datetime.datetime.strptime(str(sale_order.confirmation_date),'%Y-%m-%d %H:%M:%S').date()
			return confirmation_date
		else:
			return 

	@api.multi
	# Returns the origin date
	def _get_order_contact(self,origin):
		sale_order = self.env['sale.order'].search([('name','=',origin)],limit=1)
		if sale_order.order_contact:
			return sale_order.order_contact
		else:
			return 

	@api.multi
	def _get_shipping_date(self,origin):
		# Returns the shipping date
		stock_picking = self.env['stock.picking'].search([('origin','=',origin)],limit=1)
		if stock_picking.date_done:
			date_done = datetime.datetime.strptime(str(stock_picking.date_done),'%Y-%m-%d %H:%M:%S').date()
			return date_done
		else:
			return

	@api.multi
	def _get_tax_amount(self, amount,payment=None):
		# Returns the tax amount
		self.ensure_one()
		res = {}
		currency = self.currency_id or self.company_id.currency_id
		res = formatLang(self.env, amount, currency_obj=currency)
		#for payment in self.payment_move_line_ids:
		if payment != None:
			if self.type in ('out_invoice', 'in_refund'):
				amount = sum([p.amount for p in payment.matched_debit_ids if p.debit_move_id in self.move_id.line_ids])
				amount_currency = sum([p.amount_currency for p in payment.matched_debit_ids if p.debit_move_id in self.move_id.line_ids])
			elif self.type in ('in_invoice', 'out_refund'):
				amount = sum([p.amount for p in payment.matched_credit_ids if p.credit_move_id in self.move_id.line_ids])
				amount_currency = sum([p.amount_currency for p in payment.matched_credit_ids if p.credit_move_id in self.move_id.line_ids])
			# get the payment value in invoice currency
			if payment.currency_id and payment.currency_id == self.currency_id:
				amount_to_show = amount_currency
			else:
				amount_to_show = payment.company_id.currency_id.with_context(date=payment.date).compute(amount, self.currency_id)
			if float_is_zero(amount_to_show, precision_rounding=self.currency_id.rounding):
				return res
			res = formatLang(self.env, amount_to_show, currency_obj=currency)
		return res