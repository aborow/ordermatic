# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import odoo
from odoo import api, fields, models, _

class AccountTax(models.Model):

	_inherit = 'account.tax'

	@api.onchange('type_tax_use')
	def onchange_type_tax_use(self):
		if self.type_tax_use != 'sale':
			self.account_id = False

	@api.model
	def _default_tax_account(self):
		account_id =  self.env['account.account'].search([('name','=','Sales Tax Payable'),('code','=','111202')], limit=1)
		if account_id:
			return account_id

	account_id = fields.Many2one('account.account', domain=[('deprecated', '=', False)], string='Tax Account', ondelete='restrict',
		help="Account that will be set on invoice tax lines for invoices. Leave empty to use the expense account.", oldname='account_collected_id',default=_default_tax_account)