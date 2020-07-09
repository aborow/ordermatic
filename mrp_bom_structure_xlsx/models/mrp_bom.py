#-*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields,api, _

class MrpBom(models.Model):

	_inherit = "mrp.bom"

	bom_cost = fields.Float(string='Bom Cost')
	product_cost = fields.Float(string='Product Cost')

	@api.multi
	def _update_cost(self,parent_bom):
		product_id = parent_bom.product_id or parent_bom.product_tmpl_id.product_variant_ids
		bom = self.env['mrp.bom']._bom_find(product=product_id)
		if bom:
			bom_structure_obj = self.env['report.mrp.report_bom_structure']
			lines = bom_structure_obj._get_bom(bom.id, product_id=product_id, line_qty=bom.product_qty, level=1)
			bom.bom_cost =  lines.get('total')
			bom.product_cost = lines.get('price')
			if lines.get('components') and bom.bom_line_ids:
				for line in bom.bom_line_ids:
					bom = self.env['mrp.bom']._bom_find(product=line.product_id)
					for component in lines.get('components'):
						if component.get('prod_id') == line.product_id.id:
							line.write({'bom_cost':component.get('total')})
							line.write({'product_cost':component.get('prod_cost')})					

class MrpBomLine(models.Model):

	_inherit = "mrp.bom.line"

	bom_cost = fields.Float(string='Bom Cost')
	product_cost = fields.Float(string='Product Cost')

	@api.multi
	def _update_cost(self,child_bom):
		product_id = child_bom.product_id or child_bom.product_tmpl_id.product_variant_ids
		bom = self.env['mrp.bom']._bom_find(product=product_id)
		if bom:
			bom_structure_obj = self.env['report.mrp.report_bom_structure']
			lines = bom_structure_obj._get_bom(bom.id, product_id=product_id, line_qty=bom.product_qty, level=1)
			bom.bom_cost =  lines.get('total')
			bom.product_cost = lines.get('price')
			if lines.get('components') and bom.bom_line_ids:
				for line in bom.bom_line_ids:
					bom = self.env['mrp.bom']._bom_find(product=line.product_id)
					for component in lines.get('components'):
						if component.get('prod_id') == line.product_id.id:
							line.write({'bom_cost':component.get('total')})
							line.write({'product_cost':component.get('prod_cost')})