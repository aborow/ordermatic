#-*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields,api, _
from datetime import datetime
from odoo.exceptions import ValidationError
import base64
import io
import xlsxwriter

class PaymentAppliedReport(models.TransientModel):

	_name = "payment.applied.report"
	_description = "Payment Applied Report"

	from_date = fields.Date('From Date')
	to_date = fields.Date('To Date')
	
	@api.multi
	@api.constrains('from_date', 'to_date')
	def check_date(self):
		""" This method is used to check constrains on dates."""
		if self.from_date and self.to_date and (self.from_date > self.to_date):
			raise ValidationError(_('To Date should be greater than From Date.'))

	@api.multi
	def get_date_domain(self):
		"""Method will filter record based on domain."""
		domain = [
			('payment_date', '>=', self.from_date),
			('payment_date', '<=', self.to_date),
			('state','in',['posted','sent']),
			('partner_type','=','customer'),
			('payment_type','=','inbound')
			]
		return domain

	@api.multi
	def get_account_payments(self):
		"""Method will filter invoices based on domain and returns it."""
		domain = self.get_date_domain()
		payments = self.env['account.payment'].search(domain)
		return payments

	@api.multi
	def find_journal_item(self,partner,invoice):
		"""Method will find journal item based on domain and returns it."""
		account_move_line_id = self.env['account.move.line'].search([
			('invoice_id','=',invoice.id),
			('debit','!=',0.0)],order='id asc',limit=1)
		return account_move_line_id

	@api.multi
	def print_xls(self):
		"""Method will print the XLS report."""
		payments = self.get_account_payments()
		if not payments:
			raise ValidationError(
				_('No records found.'))
		fp = io.BytesIO()
		workbook = xlsxwriter.Workbook(fp)
		worksheet = workbook.add_worksheet('Payment Applied Report')
		data_format = workbook.add_format({'align': 'center'})
		report_header_format = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 18})
		header_format = workbook.add_format({'bold': True, 'align': 'center','color':'white','bg_color':'navy'})
		bold = workbook.add_format({'bold': True})
		worksheet.set_column('A:A', 20)
		worksheet.set_column('B:B', 20)
		worksheet.set_column('C:C', 23)
		worksheet.set_column('D:D', 20)
		worksheet.set_column('E:E', 20)
		worksheet.set_column('F:F', 20)
		worksheet.set_column('G:G', 20)
		worksheet.set_column('H:H', 20)
		worksheet.set_column('I:I', 22)
		worksheet.set_column('J:J', 20)
		worksheet.set_column('K:K', 20)
		not_exist = workbook.add_format({'bold': True, 'font_color': 'red'})
		row = 0
		colm = 0
		if payments:
			row += 0
			worksheet.write(row, colm, 'Payment Name', header_format)
			colm += 1
			worksheet.write(row, colm, 'Payment Journal', header_format)
			colm += 1
			worksheet.write(row, colm, 'Payment Method Type', header_format)
			colm += 1
			worksheet.write(row, colm, 'Customer', header_format)
			colm += 1
			worksheet.write(row, colm, 'Payment Date', header_format)
			colm += 1
			worksheet.write(row, colm, 'Invoice Amount', header_format)
			colm += 1
			worksheet.write(row, colm, 'Status', header_format)
			colm += 1
			worksheet.write(row, colm, 'Associated Invoice', header_format)
			colm += 1
			worksheet.write(row, colm, 'Payment Applied Date', header_format)
			colm += 1
			worksheet.write(row, colm, 'Amount Applied', header_format)
			colm += 1
			worksheet.write(row, colm, 'Amount UnApplied', header_format)
			colm += 1
			for payment in payments:
				amount_paid = 0.0
				invoice_ids = self.env['account.invoice'].search([('payment_ids','in',payment.id)],order = "id asc")
				for invoice in invoice_ids:
					account_move_line_id = self.find_journal_item(payment.partner_id,invoice)
					colm = 0	
					row += 1
					if payment.name:
						worksheet.write(row, colm,payment.name, data_format)
					else:
						worksheet.write(row, colm,' ', data_format)
					colm += 1
					if payment.journal_id:
						worksheet.write(row, colm,payment.journal_id.name, data_format)
					else:
						worksheet.write(row, colm,' ', data_format)
					colm += 1
					if payment.payment_method_id:
						worksheet.write(row, colm,payment.payment_method_id.name, data_format)
					else:
						worksheet.write(row, colm,' ', data_format)
					colm += 1	
					if payment.partner_id:
						if payment.partner_id.parent_id:
							worksheet.write(row, colm,payment.partner_id.parent_id.name, data_format)
						else:
							worksheet.write(row, colm,payment.partner_id.name, data_format)
					else:
						worksheet.write(row, colm,' ', data_format)
					colm += 1
					if payment.payment_date:
						worksheet.write(row, colm,datetime.strptime(str(payment.payment_date),'%Y-%m-%d').strftime('%Y/%m/%d'), data_format)
					else:
						worksheet.write(row, colm,' ', data_format)
					colm += 1
					if payment.amount:
						worksheet.write(row, colm,payment.amount, data_format)
					else:
						worksheet.write(row, colm,' ', data_format)
					colm += 1
					if payment.state:
						if payment.state == 'posted':
							worksheet.write(row, colm,'Posted', data_format)
						elif payment.state == 'sent':
							worksheet.write(row, colm,'Sent', data_format)
					else:
						worksheet.write(row, colm,' ', data_format)
					colm += 1
					if invoice:
						worksheet.write(row, colm,invoice.number, data_format)
					else:
						worksheet.write(row, colm,' ', data_format)
					colm += 1
					if account_move_line_id:
						worksheet.write(row, colm,datetime.strptime(str(account_move_line_id.date),'%Y-%m-%d').strftime('%Y/%m/%d'), data_format)
					else:
						worksheet.write(row, colm,' ', data_format)
					colm += 1
					if account_move_line_id:
						amount_paid += account_move_line_id.debit
						worksheet.write(row, colm,account_move_line_id.debit, data_format)
					else:
						worksheet.write(row, colm,' ', data_format)
					colm += 1
					if account_move_line_id:
						remaining_amount = payment.amount - amount_paid
						worksheet.write(row, colm,round(remaining_amount,3), data_format)
					else:
						worksheet.write(row, colm,' ', data_format)
					colm += 1
		workbook.close()
		fp.seek(0)
		result = base64.b64encode(fp.read())
		attachment_obj = self.env['ir.attachment']
		attachment_id = attachment_obj.create(
			{'name': 'payment_applied_report.xlsx', 'datas_fname': 'Payment Applied Report.xlsx', 'datas': result})
		download_url = '/web/content/' + \
			str(attachment_id.id) + '?download=True'
		base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
		return {
			"type": "ir.actions.act_url",
			"url": str(base_url) + str(download_url),
			"target": "new"
		}