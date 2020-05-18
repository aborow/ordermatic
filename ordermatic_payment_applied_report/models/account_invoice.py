#-*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields,api, _
import json
from odoo.tools import date_utils

class AccountInvoice(models.Model):

	_inherit = "account.invoice"


	@api.one
	@api.depends('payment_move_line_ids.amount_residual')
	def _get_payment_info_JSON(self):
		self.payments_widget = json.dumps(False)
		if self.payment_move_line_ids:
			info = {'title': _('Less Payment'), 'outstanding': False, 'content': self._get_payments_vals()}
			self.payments_widget = json.dumps(info, default=date_utils.json_default)
			self.create_payment_history()

	@api.multi
	def create_payment_history(self):
		payment_vals = self._get_payments_vals()
		account_payment = self.env['account.payment']
		for payment in payment_vals:
			payment_history_id = self.env['payment.invoice.history'].search([
					('invoice_id','=',self.id),
					('payment_id','=',account_payment.browse(payment.get('account_payment_id')).id),
					('amount_applied','=',payment.get('amount'))
				])
			if not payment_history_id and account_payment.browse(payment.get('account_payment_id')).partner_type == 'customer':
				payment_history_id = self.env['payment.invoice.history'].create({
						'invoice_id' : self.id,
						'payment_id' : account_payment.browse(payment.get('account_payment_id')).id,
						'amount_applied' : payment.get('amount'),
					})
			self.payment_ids._calculate_amount_unapplied(account_payment.browse(payment.get('account_payment_id')).id)

class AccountPayment(models.Model):

	_inherit = "account.payment"

	payment_history_ids = fields.One2many('payment.invoice.history','payment_id',string='Payment History')

	@api.multi
	def _calculate_amount_unapplied(self,payment):
		amount_paid = 0.0
		if payment:
			invoice_ids = self.env['account.invoice'].search([('payment_ids','in',payment)],order = "id asc")
			if invoice_ids:
				for invoice in invoice_ids:
					payment_history_id = self.env['payment.invoice.history'].search([
						('invoice_id','=',invoice.id),
						('payment_id','=',payment)],limit=1)
					amount_paid += payment_history_id.amount_applied
					remaining_amount = self.browse(payment).amount - amount_paid
					payment_history_id.write({'amount_unapplied':remaining_amount})