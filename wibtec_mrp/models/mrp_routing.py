# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class MrpRouting(models.Model):

	_inherit = "mrp.routing"
				
	finished_products_location_id = fields.Many2one('stock.location',string="Finished Products Location")