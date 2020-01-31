# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class PurchaseOrderLine(models.Model):

	_inherit = "purchase.order.line"

	vendor_product_code = fields.Char('Vendor Product Code')

	@api.onchange('product_id')
	def onchange_product_id(self):
		res = super(PurchaseOrderLine, self).onchange_product_id()
		product_supplier_info_id = self.env['product.supplierinfo'].search([('name','=',self.order_id.partner_id.id),('product_tmpl_id','=',self.product_id.product_tmpl_id.id),('product_code','!=',False)],limit=1)
		if product_supplier_info_id:
			self.vendor_product_code = product_supplier_info_id.product_code
			self.name = str("[" + self.product_id.default_code + "]"+ " " + self.product_id.name)
		else:
			self.vendor_product_code = False
		return res