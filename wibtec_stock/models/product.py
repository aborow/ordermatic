# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class Product(models.Model):

	_inherit = "product.product"

	is_added_in_stock = fields.Boolean(string='Is Added in Stock',default=False)