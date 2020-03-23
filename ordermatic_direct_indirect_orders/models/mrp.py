# -*- coding: utf-8 -*-
# Part of AktivSoftware See LICENSE file for full
# copyright and licensing details.

from odoo import models, fields, api, _

class MrpProduction(models.Model):

	_inherit = 'mrp.production'

	mrp_direct_order_id = fields .Many2one('mrp.production',string='Direct Production',store=True)
	mrp_indirect_order_id = fields.Many2one('mrp.production',string='Indirect Production',store=True)
	direct_mo_orders = fields.One2many('mrp.production','mrp_direct_order_id',string='Direct Orders',compute='_add_direct_orders')
	indirect_mo_orders = fields.One2many('mrp.production','mrp_indirect_order_id',string='Indirect Orders(MO)',compute='_add_indirect_orders_mo')
	indirect_po_orders = fields.One2many('purchase.order','mrp_production_id',string='Indirect Orders(PO)',compute='_add_indirect_orders_po')
	direct_orders_origin = fields.Char('Direct Orders')
	indirect_orders_origin_mo = fields.Char('Indirect Orders MO')
	indirect_orders_origin_po = fields.Char('Indirect Orders PO')
	indirect_orders_origin_po = fields.Char('Indirect Orders PO')
	
	@api.one
	@api.depends('origin')
	def _add_direct_orders(self):
		if self.state not in ('done','cancel'):
			direct_orders = self.search([('origin','=',self.name)])
			if direct_orders:
				self.direct_mo_orders = [(6, 0, direct_orders.ids)]
				self.mrp_direct_order_id = self.id
				if self.direct_mo_orders:
					prepare_string = ''
					for direct in self.direct_mo_orders:
						if not prepare_string:
							prepare_string = str(direct.id)
						else:
							prepare_string = prepare_string + ',' + str(direct.id)
					self.env['mrp.production'].browse(self.id).sudo().write({'direct_orders_origin': prepare_string}) 
		else:
			final_direct_orders = []
			if self.direct_orders_origin:
				split_string = self.direct_orders_origin.split(',')
				for order_id in self.direct_orders_origin.split(','):
					final_direct_orders.append(int(order_id))
				self.direct_mo_orders = [(6, 0, final_direct_orders)]

	@api.multi
	@api.depends('origin')
	def _add_indirect_orders_mo(self):
		indirect_orders_mo_list = []
		for order in self:
			if order.bom_id:
				for bom_line in order.bom_id.bom_line_ids:
					indirect_orders_mo = self.env['mrp.production'].search([('product_tmpl_id','=',bom_line.product_id.product_tmpl_id.id),('state','=','confirmed')])
					[indirect_orders_mo_list.append(order.id) for order in indirect_orders_mo if 'OP' in order.origin]
		final_indirect_orders_mo = self.env['mrp.production'].browse(indirect_orders_mo_list)
		if self.state not in ('done','cancel'):
			if final_indirect_orders_mo:
				self.update({'indirect_mo_orders': [(6, 0, final_indirect_orders_mo.ids)]})
				self.mrp_indirect_order_id = self.id
				if self.indirect_mo_orders:
					prepare_string = ''
					for indirect in self.indirect_mo_orders:
						if not prepare_string:
							prepare_string = str(indirect.id)
						else:
							prepare_string = prepare_string + ',' + str(indirect.id)
						self.env['mrp.production'].browse(self.id).sudo().write({'indirect_orders_origin_mo': prepare_string})
		else:
			final_indirect_orders = []
			if self.indirect_orders_origin_mo:
				split_string = self.indirect_orders_origin_mo.split(',')
				for order_id in self.indirect_orders_origin_mo.split(','):
					final_indirect_orders.append(int(order_id))
				self.indirect_mo_orders = [(6, 0, final_indirect_orders)]

	@api.multi
	@api.depends('origin')
	def _add_indirect_orders_po(self):
		indirect_orders_po_list = []
		for order in self:
			if order.bom_id and order.state not in ('done','cancel'):
				for bom_line in order.bom_id.bom_line_ids:
					indirect_orders_po = self.env['purchase.order.line'].search([('product_id','=',bom_line.product_id.id),('state','=','purchase')])
					[indirect_orders_po_list.append(line.order_id.id) for line in indirect_orders_po if line.order_id.origin and 'OP' in  line.order_id.origin]
		final_indirect_orders_po = self.env['purchase.order'].browse(indirect_orders_po_list)
		if self.state not in ('done','cancel'):
			if final_indirect_orders_po:
				self.update({'indirect_po_orders': [(6, 0, final_indirect_orders_po.ids)]})
				self.mrp_production_id = self.id
				if self.indirect_po_orders:
					prepare_string = ''
					for indirect_po in self.indirect_po_orders:
						if not prepare_string:
							prepare_string = str(indirect_po.id)
						else:
							prepare_string = prepare_string + ',' + str(indirect_po.id)
						self.env['mrp.production'].browse(self.id).sudo().write({'indirect_orders_origin_po': prepare_string})
		else:
			final_indirect_orders_po_list = []
			if self.indirect_orders_origin_po:
				split_string = self.indirect_orders_origin_po.split(',')
				for order_id in self.indirect_orders_origin_po.split(','):
					final_indirect_orders_po_list.append(int(order_id))
				self.indirect_po_orders = [(6, 0, final_indirect_orders_po_list)]


class PurchaseOrder(models.Model):

	_inherit = 'purchase.order'

	mrp_production_id = fields.Many2one('mrp.production',string='Manufacturing Order')