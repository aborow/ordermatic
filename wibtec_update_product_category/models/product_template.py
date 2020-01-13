# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class ProductTemplate(models.Model):

	_inherit = "product.template"

	is_tax_added = fields.Boolean(string='Is Tax Added',default=False)
	is_duplicate = fields.Boolean(string="Is Duplicate",default=False)
	is_cost_added = fields.Boolean(string="Is Cost Added",default=False)
	inv_qty = fields.Float(string="Inventory Quantity",default=0.0)
	inv_val = fields.Float(string="Inventory Valuation",default=0.0)

class ProductProduct(models.Model):

	_inherit = "product.product"

	is_duplicate = fields.Boolean(string="Is Duplicate",default=False)	