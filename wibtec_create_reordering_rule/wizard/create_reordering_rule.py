# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CreateReorderingRule(models.TransientModel):

	_name = 'create.reordering.rule'

	@api.multi
	def create_reordering_rule(self):
		# Method creates reordering rule
		product_ids = self.env['product.product'].search([])
		rule_ids = self.env['stock.warehouse.orderpoint'].search([])
		product_rules_list = [rule.product_id.id for rule in rule_ids]
		for product in product_ids:
			if product.id not in product_rules_list:
				location_id = self.find_location()
				warehouse_id = self.find_warehouse()
				rule_id = self.env['stock.warehouse.orderpoint'].create({
					'company_id':1,
					'lead_type':'supplier',
					'location_id':location_id.id,
					'name':self.env['ir.sequence'].next_by_code('stock.orderpoint'),
					'product_id':product.id,
					'product_max_qty':1,
					'product_min_qty':0,
					'product_uom':product.uom_id.id,
					'qty_multiple':1,
					'warehouse_id':warehouse_id.id,
					'active':True
					})

	@api.multi
	def find_location(self):
		# Method will returns location if exists
		location_id = self.env['stock.location'].search([('location_name','=','WH/Stock')])
		if location_id:
			return location_id

	@api.multi
	def find_warehouse(self):
		# Method will returns warehouse if exists
		warehouse_id = self.env['stock.warehouse'].search([('name','=','My Company')])
		if warehouse_id:
			return warehouse_id