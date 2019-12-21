# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class PurchaseOrder(models.Model):

	_inherit = "purchase.order"

	@api.multi
	@api.onchange('partner_id')
	def onchange_partner_id_warning(self):
		res = super(PurchaseOrder, self).onchange_partner_id_warning()
		if self.partner_id and self.partner_id.is_tax_exempt == True:
			tax_id = self.env['account.tax'].search([('name','=','Tax Exempt-Purchases'),('type_tax_use','=','purchase')])
			if tax_id:
				[line.write({'taxes_id': [(6, 0, tax_id.ids)]}) for line in self.order_line]
		elif self.partner_id and self.partner_id.is_tax_exempt == False:
			[line.write({'taxes_id': [(6, 0, line.product_id.supplier_taxes_id.ids)]}) for line in self.order_line]
		return res

class PurchaseOrderLine(models.Model):

	_inherit = "purchase.order.line"

	@api.multi
	@api.onchange('product_id')
	def onchange_product_id(self):
		res = super(PurchaseOrderLine, self).onchange_product_id()
		if self.product_id and self.order_id.partner_id.is_tax_exempt == True:
			tax_id = self.env['account.tax'].search([('name','=','Tax Exempt-Purchases'),('type_tax_use','=','purchase')])
			if tax_id:
				self.update({'taxes_id': [(6, 0, tax_id.ids)]})
		return res