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
			if tax.is_avatax == True:
				tax_percentage = line.tax_amt / line.price_subtotal
			else:
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
								['Account'] + ['CartItemPrice'] +
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
										line.price_unit or '',
										line.quantity or '',
										tax_percentage or '',
										line.tax_amt or '',
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