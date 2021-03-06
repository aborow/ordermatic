# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models, _
from odoo.tools.translate import _
import odoo.addons.decimal_precision as dp
from datetime import datetime
from odoo.exceptions import UserError,ValidationError
from odoo.addons import decimal_precision as dp
from functools import partial
from odoo.tools.misc import formatLang


_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):

	_inherit = "sale.order"

	def _amount_by_group(self):
		for order in self:
			currency = order.currency_id or order.company_id.currency_id
			fmt = partial(formatLang, self.with_context(lang=order.partner_id.lang).env, currency_obj=currency)
			res = {}
			for line in order.order_line:
				price_reduce = line.price_unit * (1.0 - line.discount / 100.0)
				taxes = line.tax_id.compute_all(price_reduce, quantity=line.product_uom_qty, product=line.product_id, partner=order.partner_shipping_id)['taxes']
				for tax in line.tax_id:
					group = tax.tax_group_id
					res.setdefault(group, {'amount': 0.0, 'base': 0.0})
					for t in taxes:
						if t['id'] == tax.id or t['id'] in tax.children_tax_ids.ids:
							if tax.is_avatax == True:
								res[group]['amount'] += line.tax_amt
							else:
								res[group]['amount'] += t['amount']
							res[group]['base'] += t['base']
			res = sorted(res.items(), key=lambda l: l[0].sequence)
			order.amount_by_group = [(
				l[0].name, l[1]['amount'], l[1]['base'],
				fmt(l[1]['amount']), fmt(l[1]['base']),
				len(res),
			) for l in res]

	def calculate_tax_on_sales_order(self):
		self.compute_tax()

	def get_25_chara_exemption_number(self, exemption_number):
		final_exemption_number = ''
		if exemption_number and len(exemption_number) > 25:
			for partner_exemption in exemption_number.split(','):
				current_exempltio_len = len(
					final_exemption_number) + len(partner_exemption) + 2
				if current_exempltio_len <= 25:
					if not final_exemption_number:
						final_exemption_number = partner_exemption
					else:
						final_exemption_number = final_exemption_number + ', ' + partner_exemption
				elif current_exempltio_len > 25:
					break
		return final_exemption_number

	@api.onchange('partner_id')
	def onchange_partner_id(self):
		"""Override method to add new fields values.
		@param part- update vals with partner exemption number and code, 
		also check address validation by avalara  
		"""
		res = super(SaleOrder, self).onchange_partner_id()
		self.exemption_code = self.partner_id.exemption_number
		self.exemption_code_id = self.partner_id.exemption_code_id
		self.tax_add_shipping = True
		self.tax_add_id = self.partner_shipping_id.id
		if self.partner_id.validation_method:
			self.is_add_validate = True
		else:
			self.is_add_validate = False
		return res

	@api.model
	def create(self, vals):
		ship_add_id = False

		if 'tax_add_default' in vals and vals['tax_add_default']:
			ship_add_id = vals['partner_id']
		elif 'tax_add_invoice' in vals and vals['tax_add_invoice']:
			ship_add_id = vals['partner_invoice_id']
		elif 'tax_add_shipping' in vals and vals['tax_add_shipping']:
			ship_add_id = vals['partner_shipping_id']
		if ship_add_id:
			vals['tax_add_id'] = ship_add_id
		return super(SaleOrder, self).create(vals)

	@api.multi
	def copy(self, default=None):
		res = super(SaleOrder, self).copy(default)
		res.onchange_partner_id()
		return res

	@api.multi
	def _prepare_invoice(self):
		invoice_vals = super(SaleOrder, self)._prepare_invoice()
		invoice_vals.update({
			'exemption_code': self.exemption_code or self.partner_id.exemption_number or None,
			'exemption_code_id': self.exemption_code_id.id or self.partner_id.exemption_code_id.id or None,
			'tax_add_default': self.tax_add_default,
			'tax_add_invoice': self.tax_add_invoice,
			'tax_add_shipping': self.tax_add_shipping,
			'shipping_add_id': self.tax_add_id.id,
			'shipping_address': self.tax_address,
			'location_code': self.location_code or '',
		})
		return invoice_vals

	@api.depends('order_line.price_total', 'order_line.tax_id')
	def _amount_all(self):
		"""
		Compute the total amounts of the SO.
		Ovverride This function for solving issue of Without saving SO if Confirm
		SO then Avatax is not calculate so solve this issue
		"""
		for order in self:
			if order.state not in ['draft', 'sent']:
				order.compute_tax()
			amount_untaxed = amount_tax = 0.0
			for line in order.order_line:
				amount_untaxed += line.price_subtotal
				amount_tax += line.price_tax
			amount_tax += order.tax_amount           
			order.update({
				'amount_untaxed': amount_untaxed,
				'amount_tax': amount_tax,
				'amount_total': amount_untaxed + amount_tax,
			})

	@api.onchange('tax_add_default', 'partner_id')
	def default_tax_address(self):
		if self.tax_add_default and self.partner_id:
			self.tax_add_id = self.partner_id.id
			self.tax_add_default = True
			self.tax_add_invoice = self.tax_add_shipping = False

	@api.onchange('tax_add_invoice', 'partner_invoice_id', 'partner_id')
	def invoice_tax_address(self):
		if (self.tax_add_invoice and self.partner_invoice_id) or (self.tax_add_invoice and self.partner_id):
			self.tax_add_id = self.partner_invoice_id.id or self.partner_id.id
			self.tax_add_default = self.tax_add_shipping = False
			self.tax_add_invoice = True

	@api.onchange('tax_add_shipping', 'partner_shipping_id', 'partner_id')
	def delivery_tax_address(self):
		if (self.tax_add_shipping and self.partner_shipping_id) or (self.tax_add_shipping and self.partner_id):
			self.tax_add_id = self.partner_shipping_id.id or self.partner_id.id
			self.tax_add_default = self.tax_add_invoice = False
			self.tax_add_shipping = True

	exemption_code = fields.Char(
		'Exemption Number', help="It show the customer exemption number")
	is_add_validate = fields.Boolean('Address validated')
	exemption_code_id = fields.Many2one(
		'exemption.code', 'Exemption Code', help="It show the customer exemption code")
	amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True,
									 readonly=True, compute='_amount_all', track_visibility='always')
	amount_tax = fields.Monetary(
		string='Taxes', store=True, readonly=True, compute='_amount_all', track_visibility='always')
	amount_total = fields.Monetary(
		string='Total', store=True, readonly=True, compute='_amount_all', track_visibility='always')
	tax_amount = fields.Float(
		'Tax Code Amount', digits=dp.get_precision('Sale Price'))
	tax_add_default = fields.Boolean('Tax Default Address (AVATAX)')
	tax_add_invoice = fields.Boolean('Tax Invoice Address (AVATAX)')
	tax_add_shipping = fields.Boolean('Tax Delivery Address (AVATAX)', default=True, states={
									  'draft': [('readonly', False)]})
	tax_add_id = fields.Many2one('res.partner', 'Tax Partner Address (AVATAX)')
	tax_address = fields.Text('Tax Address (AVATAX)')
	location_code = fields.Char('Location Code', help='Origin address location code')
	avalara_tax_amount = fields.Char('Avalara Tax Amount', 
			default=0.0,
			help='It will display the amount after calculation of tax from avalara.')

	@api.model
	def create_lines(self, order_lines):
		""" Tax line creation for calculating tax amount using avalara tax code. """
		lines = []
		for line in order_lines:
			# If Avatax Tax is added then only Calculate Avatax in line
			if line.product_id and line.product_id.tax_apply and any(tax for tax in line.tax_id if tax.is_avatax):
				tax_code = (
					line.product_id.tax_code_id and line.product_id.tax_code_id.name) or None
				lines.append({
					'qty': line.product_uom_qty,
					'itemcode': line.product_id and line.product_id.default_code or None,
					'description': line.product_id.description or None,
					'amount': line.price_unit * (1-(line.discount or 0.0)/100.0) * line.product_uom_qty,
					'tax_code': tax_code,
					'id': line,
					'tax_id': line.tax_id,
				})
		return lines

	@api.model
	def compute_tax(self):
		""" Create and update tax amount for each and every order line and shipping line.
		@param order_line: send sub_total of each line and get tax amount
		@param shiiping_line: send shipping amount of each ship line and get ship tax amount  
		"""
		avatax_config_obj = self.env['avalara.salestax']
		account_tax_obj = self.env['account.tax']
		avatax_config = avatax_config_obj._get_avatax_config_company()

		# Make sure Avatax is configured
		if not avatax_config:
			raise UserError(_('Your Avatax Countries settings are not configured. You need a country code in the Countries section.  \nIf you have a multi-company installation, you must add settings for each company.  \n\nYou can update settings in Avatax->Avatax API.'))

		tax_amount = o_tax_amt = 0.0

		# ship from Address / Origin Address either warehouse or company if none
		if self.warehouse_id and self.warehouse_id.partner_id:
			ship_from_address_id = self.warehouse_id.partner_id
		else:
			ship_from_address_id = self.company_id.partner_id
		if avatax_config and not avatax_config.disable_tax_calculation:
			ava_tax = account_tax_obj.search(
				[('is_avatax', '=', True),
				 ('type_tax_use', 'in', ['sale', 'all']),
				 ('company_id', '=', self.company_id.id)])

			shipping_add_id = self.tax_add_id

			lines = self.create_lines(self.order_line)
			# If Avatax Tax is added Avatax tax and also used greater than 0.00% Tax in line then display warning
			if any(tax for lines in self.order_line for tax in lines.tax_id if tax.is_avatax):
				tax_greater_0 = any(
					tax for lines in self.order_line for tax in lines.tax_id if not tax.amount == 0)
				if tax_greater_0:
					raise UserError(
						_('This sales order is using a Non Avatax sales tax rate greater than 0%.  Please select AVATAX on the sales order line.'))
			order_date = str(self.date_order).split(' ')[0]
			order_date = datetime.strptime(order_date, "%Y-%m-%d").date()
			if lines:
				exemption_code = self.exemption_code or self.partner_id.exemption_number or None
				exemption_code_id = self.exemption_code_id or self.partner_id.exemption_code_id or None
				if avatax_config.on_line:
					# Line level tax calculation
					# tax based on individual order line
					tax_id = []
					for line in lines:
						tax_id = line['tax_id'] and [
							tax.id for tax in line['tax_id']] or []
						if ava_tax and ava_tax[0].id not in tax_id:
							tax_id.append(ava_tax[0].id)
						ol_tax_amt = account_tax_obj._get_compute_tax(avatax_config, order_date,
																	  self.name, 'SalesOrder', self.partner_id, ship_from_address_id,
																	  shipping_add_id, [
																		  line], self.user_id, exemption_code, exemption_code_id.name if exemption_code_id else None,
																	  ).TotalTax
						o_tax_amt += ol_tax_amt  # tax amount based on total order line total
						line['id'].write({'tax_amt': ol_tax_amt})

					tax_amount = o_tax_amt
				elif avatax_config.on_order:
					tax_amount = account_tax_obj._get_compute_tax(avatax_config, order_date,
																  self.name, 'SalesOrder', self.partner_id, ship_from_address_id,
																  shipping_add_id, lines, self.user_id, exemption_code, exemption_code_id.name if exemption_code_id else None,
																  ).TotalTax

					for o_line in self.order_line:
						o_line.write({'tax_amt': 0.0, })
				else:
					raise UserError(
						_('Please select system calls in Avatax API Configuration'))
			else:
				for o_line in self.order_line:
					o_line.write({'tax_amt': 0.0, })

		else:
			for o_line in self.order_line:
				o_line.write({'tax_amt': 0.0, })
		self.update({
			'tax_amount': tax_amount,
			'order_line': [],
			'avalara_tax_amount':round(tax_amount,2)
		})
		return tax_amount

	@api.multi
	def button_dummy(self):
		""" It used to called manually calculation method of avalara and get tax amount"""
		self.compute_tax()
		return super(SaleOrder, self).button_dummy()

	@api.multi
	def action_confirm(self):
		self.compute_tax()
		self._amount_all()
		return super(SaleOrder, self).action_confirm()


class SaleOrderLine(models.Model):

	_inherit = "sale.order.line"

	@api.onchange('tax_id')
	def onchange_invoice_line_tax_ids(self):
		tax_id = self.env['account.tax'].search([('name','=','AVATAX'),('type_tax_use','=','sale')])
		if self.product_id and self.order_id.partner_id and self.order_id.partner_id.tax_exempt == True:
			if tax_id in self.tax_id:
				self.tax_id = [(6, 0, tax_id.ids)]
			else:
				raise ValidationError("Before updating tax here please make sure to disable the customer's tax-exempt setting.!")


	tax_amt = fields.Float('Avalara Tax', help="tax calculate by avalara")


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: