# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class Product(models.Model):
	_inherit = "product.product"

	@api.multi
	@api.depends('stock_move_ids.product_qty', 'stock_move_ids.state', 'stock_move_ids.remaining_value', 'product_tmpl_id.cost_method', 'product_tmpl_id.standard_price', 'product_tmpl_id.property_valuation', 'product_tmpl_id.categ_id.property_valuation')
	def _compute_stock_value(self):
		return super(Product,self)._compute_stock_value()

class StockQuants(models.Model):

	_inherit = "stock.quant"

	stock_value = fields.Float(string='Stock Value')

	@api.model
	def create(self,vals):
		print ("\n Create custom************************************************")
		res = super(StockQuants,self).create(vals)
		print ("\n res---------------------------",res)
		print ("\n vals*****************888888*****************",vals)
		stock_quants = self.search([('product_id','=',res.product_id.id)])
		print ("\n stock_quants*********************",stock_quants)
		[quant.update({'stock_value':0.0}) for quant in stock_quants]
		res.product_id.update({'is_added_in_stock':False})
		return res
	
	@api.multi
	def compute_stock_quant_value(self):
		print ("\n compute_stock_quant_value*********************************")
		for quant in self:
			print ("\n quant---------------------------------------",quant)
			stock_quants = self.search([('product_id','=',quant.product_id.id)])
			print ("\n stock_quants*********************",stock_quants)
			print("\n\n\n\n\n\n quant.product_id:::::::::::::: ::::::::::: ", quant.product_id)
			quant_prod = quant.product_id._compute_stock_value()
			print("\n\n\n\n\n quant+++++++++++++++++++++++++++", quant_prod)
			if quant and quant.product_id:
				print ("\n quant------------------------",quant)
				print ("\n compute_stock_quant_value++++++++++++++++++++++++++++++++++")
				if quant.product_id.is_added_in_stock == False:
					print ("\n in if*************************************************")
					if stock_quants:
						test = [stock_quant.write({'stock_value':quant.product_id.stock_value/len(stock_quants) or 0.0}) for stock_quant in stock_quants]
						print ("\n quant------------1-----------------",test)
					else:
						test = quant.write({'stock_value':quant.product_id.stock_value or 0.0})
						print ("\n quant--------------2---------------",test)
					quant.product_id.update({'is_added_in_stock':True})

	
class StockQuantityHistory(models.TransientModel):

	_inherit = 'stock.quantity.history'

	def open_table_with_updated_values(self):
		quant_ids = self.env['stock.quant'].sudo().search([])
		[quant.compute_stock_quant_value() for quant in quant_ids]
		self.ensure_one()
		if self.compute_at_date:
			tree_view_id = self.env.ref('stock.view_stock_product_tree').id
			form_view_id = self.env.ref('stock.product_form_view_procurement_button').id
			# We pass `to_date` in the context so that `qty_available` will be computed across
			# moves until date.
			action = {
				'type': 'ir.actions.act_window',
				'views': [(tree_view_id, 'tree'), (form_view_id, 'form')],
				'view_mode': 'tree,form',
				'name': _('Products'),
				'res_model': 'product.product',
				'context': dict(self.env.context, to_date=self.date),
			}
			return action
		else:
			self.env['stock.quant']._merge_quants()
			self.env['stock.quant']._unlink_zero_quants()
			return self.env.ref('stock.quantsact').read()[0]