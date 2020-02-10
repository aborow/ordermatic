# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class PurchaseOrder(models.Model):

	_inherit = 'purchase.order'

	shipping_address_id = fields.Many2one('res.partner',string='Address')

	@api.onchange('partner_id')
	def onchange_partner(self):
		#onchange of partner will set the shipping address default.
		partner_id = self.env['res.partner'].search([('parent_id','=',self.company_id.partner_id.id),('type','=','delivery')])
		if partner_id:
			self.shipping_address_id = partner_id.id
		else:
			self.shipping_address_id = False
	
class PurchaseOrderLine(models.Model):

	_inherit = "purchase.order.line"

	vendor_product_code = fields.Char('Vendor Product Code',compute='return_vendor_product_code')

	@api.depends('product_id')
	def return_vendor_product_code(self):
		for line in self:
			product_supplier_info_id = self.env['product.supplierinfo'].search([('name','=',line.order_id.partner_id.id),('product_tmpl_id','=',line.product_id.product_tmpl_id.id),('product_code','!=',False)],limit=1)
			if product_supplier_info_id:
				line.vendor_product_code = product_supplier_info_id.product_code
				if line.product_id.default_code and line.product_id.name:
					line.name = str("[" + line.product_id.default_code + "]"+ " " + line.product_id.name)
				elif line.product_id.default_code and not line.product_id.name:
					line.name = str(line.product_id.default_code)
				elif line.product_id.name and not line.product_id.default_code:
					line.name = str(line.product_id.name)
			else:
				line.vendor_product_code = False