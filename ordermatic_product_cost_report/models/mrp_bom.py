#-*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields,api, _
from odoo.tools.misc import formatLang


class MrpBom(models.Model):

	_inherit = "mrp.bom"

	bom_cost = fields.Float(string='Bom Cost')
	product_cost = fields.Float(string='Product Cost')

	@api.multi
	def _update_bom_cost(self,parent_bom):
		product_id = parent_bom.product_id or parent_bom.product_tmpl_id.product_variant_ids
		bom = self.env['mrp.bom']._bom_find(product=product_id)
		list_total = []
		if bom:
			bom_structure_obj = self.env['report.mrp.report_bom_structure']
			lines = bom_structure_obj._get_bom(bom.id, product_id=product_id, line_qty=bom.product_qty, level=1)
			lines_1 = bom_structure_obj._get_bom(bom.id, product_id=product_id, line_qty=1, level=1)
			lines_2 = bom_structure_obj._get_bom(bom.id, product_id=product_id, line_qty=2, level=1)
			lines_4 = bom_structure_obj._get_bom(bom.id, product_id=product_id, line_qty=4, level=1)
			lines_6 = bom_structure_obj._get_bom(bom.id, product_id=product_id, line_qty=6, level=1)
			lines_10 = bom_structure_obj._get_bom(bom.id, product_id=product_id, line_qty=10, level=1)
			list_total.append(round(lines_1.get('total'),2))
			list_total.append(round(lines_2.get('total'),2))
			list_total.append(round(lines_4.get('total'),2))
			list_total.append(round(lines_6.get('total'),2))
			list_total.append(round(lines_10.get('total'),2))
			bom.bom_cost =  round(lines.get('total'),2) 
			bom.product_cost = round(lines.get('price'),2)
		return list_total

	@api.multi
	def _get_bom_line_cost(self,parent_bom,bom_line):
		product_id = parent_bom.product_id or parent_bom.product_tmpl_id.product_variant_ids
		bom = self.env['mrp.bom']._bom_find(product=product_id)
		list_line_total = []
		if bom:
			currency_id= self.env.user.company_id.currency_id
			bom_structure_obj = self.env['report.mrp.report_bom_structure']
			lines_1 = bom_structure_obj._get_bom(bom.id, product_id=product_id, line_qty=1, level=1)
			lines_2 = bom_structure_obj._get_bom(bom.id, product_id=product_id, line_qty=2, level=1)
			lines_4 = bom_structure_obj._get_bom(bom.id, product_id=product_id, line_qty=4, level=1)
			lines_6 = bom_structure_obj._get_bom(bom.id, product_id=product_id, line_qty=6, level=1)
			lines_10 = bom_structure_obj._get_bom(bom.id, product_id=product_id, line_qty=10, level=1)
			components_1 = self._get_bom_cost(lines_1.get('components'),bom_line)
			components_2 = self._get_bom_cost(lines_2.get('components'),bom_line)
			components_4 = self._get_bom_cost(lines_4.get('components'),bom_line)
			components_6 = self._get_bom_cost(lines_6.get('components'),bom_line)
			components_10 = self._get_bom_cost(lines_10.get('components'),bom_line)
			list_line_total.append(formatLang(self.env, components_1, currency_obj=currency_id))
			list_line_total.append(formatLang(self.env, components_2, currency_obj=currency_id))
			list_line_total.append(formatLang(self.env, components_4, currency_obj=currency_id))
			list_line_total.append(formatLang(self.env, components_6, currency_obj=currency_id))
			list_line_total.append(formatLang(self.env, components_10, currency_obj=currency_id))
		return list_line_total

	@api.multi
	def _get_bom_cost(self,components,bom_line):
		for component in components:
			if component.get('line_id') == bom_line.id:
				bom_cost = round(component.get('total'),2)
		return bom_cost

class MrpBomLine(models.Model):

	_inherit = "mrp.bom.line"

	bom_cost = fields.Float(string='Bom Cost')
	product_cost = fields.Float(string='Product Cost')

	@api.multi
	def _update_bom_line_cost(self,child_bom):
		product_id = child_bom.product_id or child_bom.product_tmpl_id.product_variant_ids
		bom = self.env['mrp.bom']._bom_find(product=product_id)
		if bom:
			bom_structure_obj = self.env['report.mrp.report_bom_structure']
			bom.bom_cost =  lines.get('total')
			bom.product_cost = lines.get('price')
			if lines.get('components') and bom.bom_line_ids:
				for line in bom.bom_line_ids:
					bom = self.env['mrp.bom']._bom_find(product=line.product_id)
					for component in lines.get('components'):
						if component.get('prod_id') == line.product_id.id:
							line.write({'bom_cost': round(component.get('total'),2)})
							line.write({'product_cost': round(component.get('prod_cost'),2)})