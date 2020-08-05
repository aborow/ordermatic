# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import timedelta

class MrpProduction(models.Model):

	_inherit = "mrp.production"

	delivery_lead_time_vendor = fields.Integer('Vendor Delivery Lead Time',default=0) 
	lead_time_from_stock_rule = fields.Integer('Reordering Rule Lead Time',default=0)
	manufacturing_lead_time_product = fields.Float('Product Manufacturing Lead Time',default=0.0)
	manufacturing_lead_time_company = fields.Float('Company Manufacturing Lead Time',default=0.0)
	lead_type_from_stock_rule = fields.Selection([
		('net', 'Day(s) to get the products'), 
		('supplier', 'Day(s) to purchase')], 'Lead Type')
	sale_orders = fields.Many2many('sale.order','sale_manufacturing_orders_rel_data',
		'mrp_production_id' , 'order_id',string="Sale Orders", compute='_add_associated_sales_orders')
	order_history = fields.One2many('order.history','mrp_production_id',string="Order History")
	expected_duration = fields.Float(string='Expected Duration')
	expected_duration_details = fields.Char(string='Expected Duration',compute='compute_expected_duration')

	@api.multi
	def compute_expected_duration(self):
		for mo in self:
			if mo.workorder_ids:
				for wo in mo.workorder_ids:
					mo.expected_duration += wo.duration_expected
			duration_min = timedelta(minutes=mo.expected_duration)
			duration = self.convert_timedelta(duration_min)
			mo.expected_duration_details = duration
			
	def convert_timedelta(self,timedelta_object):
		days = timedelta_object.days 
		hours = timedelta_object.seconds//3600
		minutes = (timedelta_object.seconds % 3600) // 60
		if days > 0:
			duration = str(days) + ' ' + 'days' + ' ' + str(hours)+ ' ' + 'hours' + ' ' + str(minutes) + ' ' + 'minutes'
		elif hours > 0:
			duration = str(hours)+ ' ' + 'hours' + ' ' + str(minutes) + ' ' + 'minutes'
		elif minutes > 0:
			duration = str(minutes) + ' ' + 'minutes'
		else:
			duration = 0
		return duration

	@api.multi
	def refresh_sale_orders(self):
		self.order_history = [(5,)]
		self._add_associated_order_history(self.sale_orders)

	@api.multi
	def _add_associated_order_history(self,sale_orders):
		if sale_orders:
			for mo in self:
				for order in sale_orders:
					ordered_qty = 0.0
					delivery_lead_times = 0.0
					sale_order_line = self.env['sale.order.line'].search([('order_id','=',order.id),('product_id','=',mo.product_id.id)])
					if sale_order_line:
						for line in sale_order_line:
							ordered_qty += line.product_uom_qty
							delivery_lead_times += line.customer_lead
					order_history_id = self.env['order.history'].search([('sale_order_id','=',order.id),('mrp_production_id','=',mo.id)])
					if not order_history_id:
						total_lead_time = mo.delivery_lead_time_vendor + mo.lead_time_from_stock_rule + mo.manufacturing_lead_time_product + mo.manufacturing_lead_time_company + delivery_lead_times
						order_history_id = mo.order_history.create({
								'mrp_production_id' : mo.id,
								'sale_order_id' : order.id,
								'commitment_date': order.commitment_date,
								'quantity' : ordered_qty,
								'delivery_lead_times': delivery_lead_times,
								'total_lead_time' : total_lead_time,
								'suggested_deadline': self.calculate_deadline_date(order.commitment_date,total_lead_time)
							})
					else:
						pass
		else:
			pass

	@api.multi
	def calculate_deadline_date(self,commitment_date,days):
		if commitment_date and days:
			deadline_date = commitment_date - timedelta(days=days)
			return deadline_date

	@api.multi
	def _add_associated_sales_orders(self):
		for mo in self:
			sale_orders = self.env['sale.order'].sudo().search([
				('order_line.product_id','=',mo.product_id.id),
				('state','=','sale'),
				('confirmation_date','<=',mo.create_date),
				])
			final_sale_orders = [order.id for order in sale_orders for line in order.order_line if line.qty_delivered <  line.product_uom_qty and order.delivery_status != 'full' and line.product_id == mo.product_id]
			mo.update({'sale_orders':[(6, 0, final_sale_orders)]})
			mo.refresh_sale_orders()

	@api.model
	def create(self,vals):
		res = super(MrpProduction,self).create(vals)
		product_supplier_info_id = res.product_id._select_seller()
		res.delivery_lead_time_vendor = product_supplier_info_id.delay if product_supplier_info_id else 0.0
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
			'lead_time_from_stock_rule':values.get('orderpoint_id').lead_days if values.get('orderpoint_id') else 0.0,
			'lead_type_from_stock_rule':values.get('orderpoint_id').lead_type if values.get('orderpoint_id') else 'supplier'
		}