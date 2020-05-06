# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class AccountBatchPayment(models.Model):

	_inherit = "account.batch.payment"

	@api.one
	def normalize_payments(self):
		# Since a batch payment has no confirmation step (it can be used to select payments in a bank reconciliation
		# as long as state != reconciled), its payments need to be posted
		self.payment_ids.filtered(lambda r: r.state == 'sent').post()


	def validate_batch(self):
		records = self.filtered(lambda x: x.state == 'draft')
		for record in records:
			record.payment_ids.post()
			record.payment_ids.write({'state':'sent', 'payment_reference': record.name})
		records.write({'state': 'sent'})

		records = self.filtered(lambda x: x.file_generation_enabled)
		if records:
			return self.export_batch_payment()