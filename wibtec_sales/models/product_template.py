# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class ProductTemplate(models.Model):

	_inherit = "product.template"

	long_desc = fields.Char('Long Description')

	@api.multi
	def write(self,vals):
		res = super(ProductTemplate, self).write(vals)
		if 'active' in vals and vals.get('active') == False:
			if self.sale_ok == True:
				self.update({'sale_ok':False})
		return res