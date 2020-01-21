# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class MrpProduction(models.Model):

	_inherit = "mrp.production"	
				
	@api.onchange('routing_id')
	def onchange_routing_id(self):	
		"""Value will be assigned based on the routing's location."""
		if self.routing_id.finished_products_location_id.id:
			self.location_dest_id = self.routing_id.finished_products_location_id.id

class StockMove(models.Model):

	_inherit = "stock.move"

	onhand_qty = fields.Float('Available',related='product_id.onhand_qty')