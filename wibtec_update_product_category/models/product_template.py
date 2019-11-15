# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class ProductTemplate(models.Model):

	_inherit = "product.template"

	is_tax_added = fields.Boolean(string='Is Tax Added',default=False)
	is_duplicate = fields.Boolean(string="Is Duplicate",default=False)

class ProductProduct(models.Model):

	_inherit = "product.product"

	is_duplicate = fields.Boolean(string="Is Duplicate",default=False)	