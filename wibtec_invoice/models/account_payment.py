# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _
from odoo.tools.misc import formatLang, format_date

INV_LINES_PER_STUB = 9

class AccountPayment(models.Model):

	_inherit = "account.payment"

	def _check_make_stub_line(self, invoice):
		res = super(AccountPayment, self)._check_make_stub_line(invoice)
		if invoice.type in ['in_invoice', 'out_refund']:
			invoice_sign = 1
			invoice_payment_reconcile = invoice.move_id.line_ids.mapped('matched_debit_ids').filtered(lambda r: r.debit_move_id in self.move_line_ids)
		else:
			invoice_sign = -1
			invoice_payment_reconcile = invoice.move_id.line_ids.mapped('matched_credit_ids').filtered(lambda r: r.credit_move_id in self.move_line_ids)

		if self.currency_id != self.journal_id.company_id.currency_id:
			amount_paid = abs(sum(invoice_payment_reconcile.mapped('amount_currency')))
		else:
			amount_paid = abs(sum(invoice_payment_reconcile.mapped('amount')))
			
		amount_residual = invoice_sign * invoice.residual
		return {
			'due_date': format_date(self.env, invoice.date_due),
			'invoice_date': format_date(self.env,invoice.date_invoice),
			'reference': invoice.reference,
			'amount_discount': formatLang(self.env,invoice.amount_discount, currency_obj=invoice.currency_id) if invoice.amount_discount != 0 else '',
			'number': invoice.reference and invoice.number + ' - ' + invoice.reference or invoice.number,
			'amount_total': formatLang(self.env, invoice_sign * invoice.amount_total, currency_obj=invoice.currency_id),
			'amount_residual': formatLang(self.env, amount_residual, currency_obj=invoice.currency_id) if amount_residual * 10**4 != 0 else '-',
			'amount_paid': formatLang(self.env, invoice_sign * amount_paid, currency_obj=invoice.currency_id),
			'currency': invoice.currency_id,
			'origin': invoice.origin or invoice.reference or False,
		}

	def find_invoice_address_partner(self,partner_id):
		partner_invoice_ids = self.env['res.partner'].search([('parent_id','=',partner_id.id),('type','=','invoice')])
		if partner_invoice_ids:
			return partner_invoice_ids[-1]
		else:
			return False

	def _check_build_page_info(self, i, p):
		res = super(AccountPayment, self)._check_build_page_info(i,p)
		partner_invoice_id = self.find_invoice_address_partner(self.partner_id)
		category_id=False
		multi_stub = self.company_id.account_check_printing_multi_stub
		if self.partner_id.category_id.id:
			category_id = self.env['res.partner.category'].search([('id','=',self.partner_id.category_id.id)],limit=1)
		else:
			category_id = False
		return {
			'account_no': category_id.name if (category_id != False) else False,
			'sequence_number': self.check_number if (self.check_number != 0) else False,
			'payment_date': format_date(self.env, self.payment_date),
			'partner_id': partner_invoice_id or self.partner_id,
			'partner_name': self.partner_id.name,
			'currency': self.currency_id,
			'state': self.state,
			'amount': formatLang(self.env, self.amount, currency_obj=self.currency_id) if i == 0 else 'VOID',
			'amount_in_word': self._check_fill_line(self.check_amount_in_words) if i == 0 else 'VOID',
			'memo': self.communication,
			'print_check_as':self.partner_id.print_check_as or self.partner_id.name,
			'stub_cropped': not multi_stub and len(self.invoice_ids) > INV_LINES_PER_STUB,
			# If the payment does not reference an invoice, there is no stub line to display
			'stub_lines': p,
		}