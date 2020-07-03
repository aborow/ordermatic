# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models


class UpdateProductCustomerTax(models.TransientModel):
	_name = "update.product.customer.tax.wizard"

	replace_account_tax_id = fields.Many2one(
		'account.tax', 'Replace Tax With', required=True)

	@api.multi
	def action_update_product_customer_tax(self):
		if self.replace_account_tax_id:
			product_ids = self.env['product.template'].search(['|',('active','=',True),('active','=',False)])
			[product.write({'taxes_id': [(6, 0, [self.replace_account_tax_id.id])]}) for product in product_ids]

	@api.multi
	def action_add_parent_ref_to_child(self):
		child_partners = self.env['res.partner'].search([('parent_id','!=',False)])
		if child_partners:
			for child_partner in child_partners:
				if 'Accounts Payable' or 'Account Payable' in child_partner.name and child_partner.parent_id:
					child_partner.write({'ref': child_partner.parent_id.ref})