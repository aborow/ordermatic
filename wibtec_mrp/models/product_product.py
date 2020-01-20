# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class ProductProduct(models.Model):

	_inherit = "product.product"

	onhand_qty = fields.Float('On Hand',related='product_tmpl_id.qty_available')