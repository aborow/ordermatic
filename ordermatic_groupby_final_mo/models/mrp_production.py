# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.osv import expression
import datetime

class MrpProduction(models.Model):

	_inherit = "mrp.production"

	def _search_manufacturing_sequence(self, operator, value):
		recs = self.search([]).filtered(lambda x : str(x.manufacturing_seq) in value)
		if recs:
			return [('id', 'in', [x.id for x in recs])]
				
	parent_product_id = fields.Many2one('product.product',string="Reference Part")
	parent_mrp_id = fields.Many2one('mrp.production',string="Final MO")
	manufacturing_seq = fields.Char(string="MO Sequence",compute='_calculate_sequence',search='_search_manufacturing_sequence')
	sequence = fields.Char(string="Sequence",compute='_calculate_sequence')
	final_product_id = fields.Many2one('product.product',string="Final Product")

	@api.multi
	@api.depends('parent_product_id','origin')
	def _calculate_sequence(self):
		for mo in self:
			if mo.origin and 'MO' in mo.origin:
				manufacturing_id = mo.search([('name','=',mo.origin)],limit=1)
				stock_move_id = self.env['stock.move'].search([('raw_material_production_id','=',manufacturing_id.id),('product_id','=',mo.product_id.id)],limit=1)
				mo.sequence = stock_move_id.mo_sequence
				date = datetime.datetime.strptime(str(mo.create_date),'%Y-%m-%d %H:%M:%S.%f').date()
				create_date = date.strftime("%Y%m%d")
				if manufacturing_id.sequence:
					mo.manufacturing_seq = str(manufacturing_id.manufacturing_seq)+ '_' + str(mo.sequence)
				else:
					mo.manufacturing_seq = str(create_date)+ '_' + str(mo.sequence)
				
	@api.model
	def create(self, vals):
		res = super(MrpProduction, self).create(vals)
		sequence = 0
		if res.move_raw_ids:
			for move in res.move_raw_ids:
				move.write({'mo_sequence': sequence + 1})
				sequence += 1
		if res.origin:
			manufacturing_id = self.search([('name','=',res.origin)],limit=1)
			if manufacturing_id and manufacturing_id.origin and 'MO' in manufacturing_id.origin:
				main_origin = manufacturing_id.origin
				while main_origin:
					parent_mrp = self.search([('name','=',main_origin)],limit=1)
					if not parent_mrp and 'OP' in main_origin:
						ro_mrp_id = self.search([('origin','=', main_origin)],limit=1)
						res.final_product_id = ro_mrp_id.product_id.id
						res.update({'final_product_id' : ro_mrp_id.product_id.id,
								'parent_mrp_id' : ro_mrp_id.id})
						main_origin = False
					elif not parent_mrp and 'SO' in main_origin:
						so_mrp_id = self.search([('origin','=', main_origin)],limit=1)
						res.final_product_id = so_mrp_id.product_id.id
						res.update({'final_product_id' : so_mrp_id.product_id.id,
								'parent_mrp_id' : so_mrp_id.id})
						main_origin = False
					elif parent_mrp and not parent_mrp.origin:
						res.update({'final_product_id' : parent_mrp.product_id.id,
								'parent_mrp_id' : parent_mrp.id})
						main_origin = False
					else:
						main_origin = parent_mrp.origin
						res.update({'final_product_id' : parent_mrp.product_id.id,
								'parent_mrp_id' : parent_mrp.id})
				res.update({'parent_product_id': manufacturing_id.product_id.id})
			elif manufacturing_id:
				res.update({'final_product_id' : manufacturing_id.product_id.id,
							'parent_mrp_id' : manufacturing_id.id,
							'parent_product_id': manufacturing_id.product_id.id})
		return res

class StockMove(models.Model):

	_inherit = "stock.move"

	mo_sequence = fields.Char(string="MO Sequence",store=True)