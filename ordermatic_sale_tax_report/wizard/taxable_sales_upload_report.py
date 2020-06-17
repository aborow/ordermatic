#-*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields,api, _
from datetime import datetime
from odoo.exceptions import ValidationError
import base64
import io
import xlsxwriter
import datetime
import os
import csv
import base64

class TaxableSalesUploadReport(models.TransientModel):

	_name = "taxable.sales.upload.report"
	_description = "Taxable Sales Upload Report"

	# @api.model
	# def get_states(self):
	# 	state_ids = self.env['res.country.state'].search([('country_id','=',self.env.user.company_id.country_id.id)])
	# 	return state_ids

	from_date = fields.Date('From Date')
	to_date = fields.Date('To Date')
	country_id = fields.Many2one('res.country','Country',default=lambda self: self.env.user.company_id.country_id)
	state_ids = fields.Many2many('res.country.state',string='State')

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
			('date_invoice', '>=', self.from_date),
			('date_invoice', '<=', self.to_date),
			('type','in',['out_invoice','out_refund']),
			('state','not in',['draft','cancel']),
			]
		if self.state_ids:
			domain.append(('partner_shipping_id.state_id', 'in', self.state_ids.ids))
		return domain

	@api.multi
	def get_account_invoices(self):
		"""Method will filter invoices based on domain and returns it."""
		domain = self.get_date_domain()
		invoices = self.env['account.invoice'].search(domain)
		return invoices

	@api.multi
	def _get_tic_category_id(self):
		tic_category_id = self.env['ir.default'].get('res.config.settings', 'tic_category_id')
		return tic_category_id

	@api.multi
	def calculate_index(self,invoice):
		if invoice.invoice_line_ids:
			for index in range(0,len(invoice.invoice_line_ids)-1):
				for line in invoice.invoice_line_ids:
					line.write({'index_no': index})
					index += 1
	@api.multi
	def find_internal_reference(self,partner_id):
		if partner_id.ref:
			return partner_id.ref
		elif not partner_id.ref:
			if partner_id.parent_id and partner_id.parent_id.ref:
				return partner_id.parent_id.ref
			else:
				return partner_id.id

	@api.multi
	def find_partner_name(self,partner_id):
		if partner_id.parent_id:
			partner_name = str(partner_id.parent_id.name)+ ' ' + str(partner_id.name)
			partner = partner_name.replace(',', '')
			return partner
		else:
			partner = str(partner_id.name).replace(',', '')
			return partner

	@api.multi
	def get_taxes_percentage(self,line):
		tax_percentage = 0.0
		for tax in line.invoice_line_tax_ids:
			tax_percentage = tax_percentage + tax.amount
		return tax_percentage

	@api.multi
	def get_state(self,invoice):
		state = ''
		if invoice.state == 'open':
			state = 'Open'
		elif invoice.state == 'in_payment':
			state = 'In Payment'
		elif invoice.state == 'paid':
			state = 'Paid'
		return state 

	@api.multi
	def print_csv_report(self):
		invoices = self.get_account_invoices()
		if not invoices:
			raise ValidationError(
				_('No records found.'))

		with open(os.path.join("/tmp", "taxable_sales_upload_report.csv"), 'w', newline='') as csvfile:

			# specify delimiter to csv file
			spamwriter = csv.writer(csvfile, delimiter=',',quotechar='\'', quoting=csv.QUOTE_MINIMAL)
			# Add label in header
	
			spamwriter.writerow(['OrderID'] + ['Partner Name'] + ['CustomerID'] + 
								['TransactionDate'] + ['DeliveredBySeller'] + 
								['ShipFromAddr1'] + ['ShipFromAddr2'] + ['ShipFromCity'] +
								['ShipFromState'] + ['ShipFromZip5'] + ['ShipFromZip4'] +
								['ShipToAddr1'] + ['ShipToAddr2'] + ['ShipToAddr2'] + ['ShipToState'] + ['ShipToZip5'] +
								['ShipToZip4'] + ['Invoice Payment Status'] + ['CartItemIndex'] + ['CartItem'] +
								['Account'] + ['CartItemTIC'] + ['CartItemPrice'] +
								['CartItemQty'] + ['CartItemTaxRate'] + ['CartItemTaxAmount'] + ['Discount(%)'] + ['Subtotal'])

			# Removed old attachment if any
			existing_attachment = self.env['ir.attachment'].search(
				[('datas_fname', '=', 'taxable_sales_upload_report.csv')])
			if existing_attachment:
				existing_attachment.unlink()
			current_date = fields.Date.today()
			for invoice in invoices:
				self.calculate_index(invoice)
				state = self.get_state(invoice)
				# tic_category_id = self._get_tic_category_id()
				# tic_category = self.env['product.tic.category'].browse(tic_category_id)
				partner_ref = self.find_internal_reference(invoice.partner_id)
				partner_name = self.find_partner_name(invoice.partner_id)
				
				# Add lines in csv
				for line in invoice.invoice_line_ids:
					tax_percentage = self.get_taxes_percentage(line)
					spamwriter.writerow([
										invoice.number if invoice.number else '',
										partner_name or '',
										partner_ref or '',
										datetime.datetime.strptime(str(invoice.date_invoice),'%Y-%m-%d').strftime('%Y%m%d') if invoice.date_invoice else '',
										0 if invoice.id else '',
										invoice.company_id.partner_id.street.replace(",", " ") if invoice.company_id.partner_id.street else '',
										invoice.company_id.partner_id.street2.replace(",", " ") if invoice.company_id.partner_id.street2 else '',
										invoice.company_id.partner_id.city or '',
										invoice.company_id.partner_id.state_id.code or '',
										invoice.company_id.partner_id.zip or '',
										'',
										invoice.partner_shipping_id.street.replace(",", " ") if invoice.partner_shipping_id.street else '',
										invoice.partner_shipping_id.street2.replace(",", " ") if invoice.partner_shipping_id.street2 else '',
										invoice.partner_shipping_id.city or '',
										invoice.partner_shipping_id.state_id.code or '',
										invoice.partner_shipping_id.zip or '',
										'',
										state or '',
										line.index_no if line.index_no > 0 else 0,
										line.product_id.id or '',
										line.account_id.code + ' ' + line.account_id.name if line.account_id.code and line.account_id.name else line.account_id.name,
										# tic_category.code or 0,
										line.price_unit or '',
										line.quantity or '',
										tax_percentage or '',
										line.price_tax or '',
										line.discount or '',
										line.price_subtotal or ''
										])
			# closed connection
			csvfile.close()

			# open file in read mode
			f_read = open(os.path.join("/tmp", "taxable_sales_upload_report.csv"), "r")
			file_string = f_read.read()
			f_read.close()
			os.remove(os.path.join("/tmp", "taxable_sales_upload_report.csv"))
			values = {
				'name': "Taxable Sales Upload Report.csv",
				'datas_fname': 'taxable_sales_upload_report.csv',
				'res_model': 'ir.ui.view',
				'res_id': False,
				'type': 'binary',
				'public': True,
				'datas': base64.b64encode(bytes(file_string, 'utf-8'))
			}
			#Create attachment for download
			attachment_id = self.env['ir.attachment'].sudo().create(values)
			download_url = '/web/content/' + \
				str(attachment_id.id) + '?download=True'
			base_url = self.env['ir.config_parameter'].sudo().get_param(
				'web.base.url')
			return {
				"type": "ir.actions.act_url",
				"url": str(base_url) + str(download_url),
				"target": "new",
			}

	@api.multi
	def print_xls(self):
		"""Method will print the XLS report."""
		invoices = self.get_account_invoices()
		if not invoices:
			raise ValidationError(
				_('No records found.'))
		fp = io.BytesIO()
		workbook = xlsxwriter.Workbook(fp)
		worksheet = workbook.add_worksheet('Taxable Sales Upload Report')
		data_format = workbook.add_format({'align': 'center'})
		report_header_format = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 18})
		header_format = workbook.add_format({'bold': True, 'align': 'center','color':'white','bg_color':'navy'})
		bold = workbook.add_format({'bold': True})
		worksheet.set_column('A:A', 20)
		worksheet.set_column('B:B', 20)
		worksheet.set_column('C:C', 20)
		worksheet.set_column('D:D', 20)
		worksheet.set_column('E:E', 20)
		worksheet.set_column('F:F', 20)
		worksheet.set_column('G:G', 20)
		worksheet.set_column('H:H', 20)
		worksheet.set_column('I:I', 20)
		worksheet.set_column('J:J', 20)
		worksheet.set_column('K:K', 20)
		worksheet.set_column('L:L', 20)
		worksheet.set_column('M:M', 20)
		worksheet.set_column('N:N', 20)
		worksheet.set_column('O:O', 20)
		worksheet.set_column('P:P', 20)
		worksheet.set_column('Q:Q', 20)
		worksheet.set_column('R:R', 20)
		worksheet.set_column('S:S', 20)
		worksheet.set_column('T:T', 20)
		worksheet.set_column('U:U', 20)
		worksheet.set_column('V:V', 20)
		worksheet.set_column('W:W', 20)
		worksheet.set_column('X:X', 20)
		worksheet.set_column('Y:Y', 20)
		not_exist = workbook.add_format({'bold': True, 'font_color': 'red'})
		row = 0
		colm = 0
		if invoices:
			row += 0
			worksheet.write(row, colm, 'OrderID', header_format)
			colm += 1
			worksheet.write(row, colm, 'CustomerID', header_format)
			colm += 1
			worksheet.write(row, colm, 'TransactionDate', header_format)
			colm += 1
			worksheet.write(row, colm, 'AuthorizedDate', header_format)
			colm += 1
			worksheet.write(row, colm, 'CapturedDate', header_format)
			colm += 1
			worksheet.write(row, colm, 'DeliveredBySeller', header_format)
			colm += 1
			worksheet.write(row, colm, 'ShipFromAddr1', header_format)
			colm += 1
			worksheet.write(row, colm, 'ShipFromAddr2', header_format)
			colm += 1
			worksheet.write(row, colm, 'ShipFromCity', header_format)
			colm += 1
			worksheet.write(row, colm, 'ShipFromState', header_format)
			colm += 1
			worksheet.write(row, colm, 'ShipFromZip5', header_format)
			colm += 1
			worksheet.write(row, colm, 'ShipFromZip4', header_format)
			colm += 1
			worksheet.write(row, colm, 'ShipToAddr1', header_format)
			colm += 1
			worksheet.write(row, colm, 'ShipToAddr2', header_format)
			colm += 1
			worksheet.write(row, colm, 'ShipToCity', header_format)
			colm += 1
			worksheet.write(row, colm, 'ShipToState', header_format)
			colm += 1
			worksheet.write(row, colm, 'ShipToZip5', header_format)
			colm += 1
			worksheet.write(row, colm, 'ShipToZip4', header_format)
			colm += 1
			worksheet.write(row, colm, 'CartItemIndex', header_format)
			colm += 1
			worksheet.write(row, colm, 'CartItem', header_format)
			colm += 1
			worksheet.write(row, colm, 'CartItemTIC', header_format)
			colm += 1
			worksheet.write(row, colm, 'CartItemPrice', header_format)
			colm += 1
			worksheet.write(row, colm, 'CartItemQty', header_format)
			colm += 1
			worksheet.write(row, colm, 'CartItemTaxRate', header_format)
			colm += 1
			worksheet.write(row, colm, 'CartItemTaxAmount', header_format)
			for invoice in invoices:
				for line in invoice.invoice_line_ids:
					colm = 0
					row += 1
					if invoice.id:
						worksheet.write(row, colm,invoice.id, data_format)
					else:
						worksheet.write(row, colm,' ', data_format)
					colm += 1
					if invoice.partner_id:
						worksheet.write(row, colm,invoice.partner_id.id, data_format)
					else:
						worksheet.write(row, colm,' ', data_format)
					colm += 1
					if invoice.create_date:
						worksheet.write(row, colm,datetime.datetime.strptime(str(invoice.create_date),'%Y-%m-%d %H:%M:%S.%f').strftime('%Y%m%d'), data_format)
					else:
						worksheet.write(row, colm,' ', data_format)
					colm += 1
					current_date = fields.Date.today()
					worksheet.write(row, colm,datetime.datetime.strptime(str(current_date),'%Y-%m-%d').strftime('%Y%m%d'), data_format)
					colm += 1
					worksheet.write(row, colm,datetime.datetime.strptime(str(current_date),'%Y-%m-%d').strftime('%Y%m%d'), data_format)
					colm += 1
					if invoice.id:
						worksheet.write(row, colm,0, data_format)
					else:
						worksheet.write(row, colm,' ', data_format)
					colm += 1
					if invoice.company_id.partner_id:
						worksheet.write(row, colm,str(invoice.company_id.partner_id.street), data_format)
					else:
						worksheet.write(row, colm,' ', data_format)
					colm += 1
					if invoice.company_id.partner_id:
						worksheet.write(row, colm,str(invoice.company_id.partner_id.street2), data_format)
					else:
						worksheet.write(row, colm,' ', data_format)
					colm += 1
					if invoice.company_id.partner_id:
						worksheet.write(row, colm,str(invoice.company_id.partner_id.city), data_format)
					else:
						worksheet.write(row, colm,' ', data_format)
					colm += 1
					if invoice.company_id.partner_id:
						worksheet.write(row, colm,str(invoice.company_id.partner_id.state_id.code), data_format)
					else:
						worksheet.write(row, colm,' ', data_format)
					colm += 1
					if invoice.company_id.partner_id:
						worksheet.write(row, colm,str(invoice.company_id.partner_id.zip), data_format)
					else:
						worksheet.write(row, colm,' ', data_format)
					colm += 1
					worksheet.write(row, colm,' ', data_format)
					colm += 1
					if invoice.partner_shipping_id:
						worksheet.write(row, colm,str(invoice.partner_shipping_id.street), data_format)
					else:
						worksheet.write(row, colm,' ', data_format)
					colm += 1
					if invoice.partner_shipping_id:
						worksheet.write(row, colm,str(invoice.partner_shipping_id.street2), data_format)
					else:
						worksheet.write(row, colm,' ', data_format)
					colm += 1
					if invoice.partner_shipping_id:
						worksheet.write(row, colm,str(invoice.partner_shipping_id.city), data_format)
					else:
						worksheet.write(row, colm,' ', data_format)
					colm += 1
					if invoice.partner_shipping_id:
						worksheet.write(row, colm,str(invoice.partner_shipping_id.state_id.code), data_format)
					else:
						worksheet.write(row, colm,' ', data_format)
					colm += 1
					if invoice.partner_shipping_id:
						worksheet.write(row, colm,str(invoice.partner_shipping_id.zip), data_format)
					else:
						worksheet.write(row, colm,' ', data_format)
					colm += 1
					worksheet.write(row, colm,' ', data_format)
					colm += 1
					line_index = 0
					if line:
						self.calculate_index(invoice)
						worksheet.write(row, colm,str(line.index_no), data_format)
					else:
						worksheet.write(row, colm,' ', data_format)
					colm += 1
					if line.product_id:
						worksheet.write(row, colm,str(line.product_id.id), data_format)
					else:
						worksheet.write(row, colm,' ', data_format)
					colm += 1
					tic_category_id = self._get_tic_category_id()
					if tic_category_id:
						tic_category = self.env['product.tic.category'].browse(tic_category_id)
						worksheet.write(row, colm,tic_category.code, data_format)
					else:
						worksheet.write(row, colm,1, data_format)
					colm += 1
					if line.price_unit:
						worksheet.write(row, colm,line.price_unit, data_format)
					else:
						worksheet.write(row, colm, ' ', data_format)
					colm += 1
					if line.quantity:
						worksheet.write(row, colm,line.quantity, data_format)
					else:
						worksheet.write(row, colm, ' ', data_format)
					colm += 1
					if line.invoice_line_tax_ids:
						worksheet.write(row, colm,line.invoice_line_tax_ids.amount, data_format)
					else:
						worksheet.write(row, colm, ' ', data_format)
					colm += 1
					if line.price_tax:
						worksheet.write(row, colm,line.price_tax, data_format)
					else:
						worksheet.write(row, colm, ' ', data_format)
					colm += 1
		workbook.close()
		fp.seek(0)
		result = base64.b64encode(fp.read())
		attachment_obj = self.env['ir.attachment']
		attachment_id = attachment_obj.create(
			{'name': 'taxable_sales_upload_report.xlsx', 'datas_fname': 'Taxable Sales Upload Report.xlsx', 'datas': result})
		download_url = '/web/content/' + \
			str(attachment_id.id) + '?download=True'
		base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
		return {
			"type": "ir.actions.act_url",
			"url": str(base_url) + str(download_url),
			"target": "new"
		}