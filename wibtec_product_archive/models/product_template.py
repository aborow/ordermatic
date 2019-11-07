# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields,models, _

class ProductTemplate(models.Model):

	_inherit = "product.template"

	is_active_custom = fields.Boolean('Is Active',default=False)