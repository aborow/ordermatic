# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import datetime

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools import float_compare, float_round

from .taxcloud_request import TaxCloudRequest

class AccountInvoice(models.Model):

	_inherit = 'account.invoice'

	@api.multi
	def calculate_index(self):
		for invoice in self:
			if invoice.invoice_line_ids:
				for index in range(0,len(invoice.invoice_line_ids)-1):
					for line in invoice.invoice_line_ids:
						line.write({'index_no': index})
						index += 1

	@api.multi
	@api.onchange('partner_id')
	def onchange_partner_id(self):
		res = super(AccountInvoice, self)._onchange_partner_id()
		if self.partner_id and self.partner_id.is_tax_exempt == True:
			tax_id = self.env['account.tax'].search([('name','=','Tax Exempt-Sales'),('type_tax_use','=','sale')])
			if tax_id:
				[line.write({'invoice_line_tax_ids': [(6, 0, tax_id.ids)]}) for line in self.invoice_line_ids]
		elif self.partner_id and self.partner_id.is_tax_exempt == False:
			[line.write({'invoice_line_tax_ids': [(6, 0, line.product_id.taxes_id.ids)]}) for line in self.invoice_line_ids]
		return res

	@api.multi
	def validate_taxes_on_invoice(self):
		company = self.company_id
		Param = self.env['ir.config_parameter']
		api_id = Param.sudo().get_param('account_taxcloud.taxcloud_api_id_{}'.format(company.id)) or Param.sudo().get_param('account_taxcloud.taxcloud_api_id')
		api_key = Param.sudo().get_param('account_taxcloud.taxcloud_api_key_{}'.format(company.id)) or Param.sudo().get_param('account_taxcloud.taxcloud_api_key')
		request = TaxCloudRequest(api_id, api_key)

		shipper = self.company_id or self.env.user.company_id
		request.set_location_origin_detail(shipper)
		request.set_location_destination_detail(self._get_partner())

		request.set_invoice_items_detail(self)

		response = request.get_all_taxes_values()

		if response.get('error_message'):
			raise ValidationError(_('Unable to retrieve taxes from TaxCloud: ')+'\n'+response['error_message']+'\n\n'+_('The configuration of TaxCloud is in the Accounting app, Settings menu.'))

		tax_values = response['values']

		raise_warning = False
		for index, line in enumerate(self.invoice_line_ids):
			if line.price_unit >= 0.0 and line.quantity >= 0.0:
				price = line.price_unit * (1 - (line.discount or 0.0) / 100.0) * line.quantity
				if not price:
					tax_rate = 0.0
				else:
					tax_rate = tax_values[index] / price * 100
				if len(line.invoice_line_tax_ids) != 1 or float_compare(line.invoice_line_tax_ids.amount, tax_rate, precision_digits=3):
					raise_warning = True
					tax_id = self.env['account.tax'].search([('name','=','Tax Exempt-Sales'),('type_tax_use','=','sale')])
					if tax_id.id in line.invoice_line_tax_ids.ids:
						line.invoice_line_tax_ids = tax_id
					elif not line.invoice_line_tax_ids:
						pass
					else:
						tax_rate = float_round(tax_rate, precision_digits=3)
						tax = self.env['account.tax'].sudo().search([
							('amount', '=', tax_rate),
							('amount_type', '=', 'percent'),
							('type_tax_use', '=', 'sale'),
							('company_id', '=', company.id),
						], limit=1)
						if not tax:
							tax = self.env['account.tax'].sudo().create({
								'name': 'Tax %.3f %%' % (tax_rate),
								'amount': tax_rate,
								'amount_type': 'percent',
								'type_tax_use': 'sale',
								'description': 'Sales Tax',
								'company_id': company.id,
							})
						line.invoice_line_tax_ids = tax

		self._onchange_invoice_line_ids()

		if self.env.context.get('taxcloud_authorize_transaction'):
			current_date = fields.Datetime.context_timestamp(self, datetime.datetime.now())

			if self.type == 'out_invoice':
				if self.state == 'open':
					request.client.service.AuthorizedWithCapture(
						request.api_login_id,
						request.api_key,
						request.customer_id,
						request.cart_id,
						self.id,
						current_date,  # DateAuthorized
						current_date,  # DateCaptured
					)
			elif self.type == 'out_refund':
				request.set_invoice_items_detail(self)
				origin_invoice = self.env['account.invoice'].search([('number', '=', self.origin)], limit=1)
				if origin_invoice:
					request.client.service.Returned(
						request.api_login_id,
						request.api_key,
						origin_invoice.id,
						request.cart_items,
						fields.Datetime.from_string(self.date_invoice)
					)
				else:
					_logger.warning(_("The source document on the refund is not valid and thus the refunded cart won't be logged on your taxcloud account"))

		if raise_warning:
			return {'warning': _('The tax rates have been updated, you may want to check it before validation')}
		else:
			return True

class AccountInvoiceLine(models.Model):

	_inherit = "account.invoice.line"

	index_no = fields.Integer('Index',default=0)

	@api.multi
	@api.onchange('product_id')
	def _onchange_product_id(self):
		res = super(AccountInvoiceLine, self)._onchange_product_id()
		if self.product_id and self.invoice_id.partner_id.is_tax_exempt == True:
			tax_id = self.env['account.tax'].search([('name','=','Tax Exempt-Sales'),('type_tax_use','=','sale')])
			if tax_id:
				self.update({'invoice_line_tax_ids': [(6, 0, tax_id.ids)]})
		return res