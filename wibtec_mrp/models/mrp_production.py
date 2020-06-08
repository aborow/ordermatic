# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class MrpProduction(models.Model):

	_inherit = "mrp.production"

	delivery_lead_time_vendor = fields.Integer('Vendor Delivery Lead Time',default=0) 
	lead_time_from_stock_rule = fields.Integer('Reordering Rule Lead Time',default=0)
	manufacturing_lead_time_product = fields.Float('Product Manufacturing Lead Time',default=0.0)
	manufacturing_lead_time_company = fields.Float('Company Manufacturing Lead Time',default=0.0)
	lead_type_from_stock_rule = fields.Selection([
		('net', 'Day(s) to get the products'), 
		('supplier', 'Day(s) to purchase')], 'Lead Type')

	@api.model
	def create(self,vals):
		res = super(MrpProduction,self).create(vals)
		product_supplier_info_id = res.product_id._select_seller()
		res.delivery_lead_time_vendor = product_supplier_info_id.delay or 0.0
		res.manufacturing_lead_time_product = res.product_id.produce_delay or 0.0
		res.manufacturing_lead_time_company = res.company_id.manufacturing_lead or 0.0
		return res
				
	@api.onchange('routing_id')
	def onchange_routing_id(self):	
		"""Value will be assigned based on the routing's location."""
		if self.routing_id.finished_products_location_id.id:
			self.location_dest_id = self.routing_id.finished_products_location_id.id

class StockMove(models.Model):

	_inherit = "stock.move"

	onhand_qty = fields.Float('On Hand',related='product_id.onhand_qty')

class StockRule(models.Model):

	_inherit = "stock.rule"

	def _prepare_mo_vals(self, product_id, product_qty, product_uom, location_id, name, origin, values, bom):
		return {
			'origin': origin,
			'product_id': product_id.id,
			'product_qty': product_qty,
			'product_uom_id': product_uom.id,
			'location_src_id': self.location_src_id.id or self.picking_type_id.default_location_src_id.id or location_id.id,
			'location_dest_id': location_id.id,
			'bom_id': bom.id,
			'date_planned_start': fields.Datetime.to_string(self._get_date_planned(product_id, values)),
			'date_planned_finished': values['date_planned'],
			'procurement_group_id': False,
			'propagate': self.propagate,
			'picking_type_id': self.picking_type_id.id or values['warehouse_id'].manu_type_id.id,
			'company_id': values['company_id'].id,
			'move_dest_ids': values.get('move_dest_ids') and [(4, x.id) for x in values['move_dest_ids']] or False,
			'lead_time_from_stock_rule':values.get('orderpoint_id').lead_days or 0.0,
			'lead_type_from_stock_rule':values.get('orderpoint_id').lead_type or 'supplier'
		}