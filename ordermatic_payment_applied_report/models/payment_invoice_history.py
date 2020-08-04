#-*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields,api, _

class PaymentInvoiceHistory(models.Model):

	_name = "payment.invoice.history"

	invoice_id = fields.Many2one('account.invoice',string="Invoice")
	payment_id = fields.Many2one('account.payment',string="Payment")
	amount_applied = fields.Float(string='Amount Applied')
	amount_unapplied = fields.Float(string='Amount Unapplied')