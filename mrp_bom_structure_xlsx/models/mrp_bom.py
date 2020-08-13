#-*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields,api, _

class MrpBom(models.Model):

	_inherit = "mrp.bom"

	bom_cost = fields.Float(string='Bom Cost')
	product_cost = fields.Float(string='Product Cost')
	operation_details = fields.One2many('operations.details','bom_id',string='Operation Details')

	@api.multi
	def _update_cost(self,parent_bom):
		product_id = parent_bom.product_id or parent_bom.product_tmpl_id.product_variant_ids
		bom = self.env['mrp.bom']._bom_find(product=product_id)
		if bom:
			bom_structure_obj = self.env['report.mrp.report_bom_structure']
			lines = bom_structure_obj._get_bom(bom.id, product_id=product_id, line_qty=bom.product_qty, level=1)
			bom.bom_cost =  round(lines.get('total'),2)
			bom.product_cost = round(lines.get('price'),2)
			if lines.get('operations'):
				for operations_details in lines.get('operations'):
					operation_detail = self.find_operation_details(bom,operations_details.get('operation'))
					if operation_detail:
						operation_detail.update({
							'quantity' : operations_details.get('duration_expected'),
							'bom_cost' : round(operations_details.get('total'),2),
							'operation_id': operations_details.get('operation').id,
						})
					else:
						operation_detail = self.env['operations.details'].create({
							'bom_id' : self.id,
							'quantity' : operations_details.get('duration_expected'),
							'bom_cost' : operations_details.get('total'),
							'operation_id': operations_details.get('operation').id,
						})
			if lines.get('components') and bom.bom_line_ids:
				for line in bom.bom_line_ids:
					bom = self.env['mrp.bom']._bom_find(product=line.product_id)
					for component in lines.get('components'):
						if component.get('prod_id') == line.product_id.id:
							line.write({'bom_cost':round(component.get('total'),2)})
							line.write({'product_cost':round(component.get('prod_cost'),2)})


	def find_operation_details(self,bom_id,operation):
		if bom_id and operation:
			operation_details = self.env['operations.details'].search([('bom_id','=',bom_id.id),('operation_id','=',operation.id)])
			return operation_details
		else:
			return False					

class MrpBomLine(models.Model):

	_inherit = "mrp.bom.line"

	bom_cost = fields.Float(string='Bom Cost')
	product_cost = fields.Float(string='Product Cost')
	operation_line_details = fields.One2many('operations.line.details','bom_line_id',string='Operation Line Details')

	@api.multi
	def _update_cost(self,child_bom):
		product_id = child_bom.product_id or child_bom.product_tmpl_id.product_variant_ids
		bom = self.env['mrp.bom']._bom_find(product=product_id)
		if bom:
			bom_structure_obj = self.env['report.mrp.report_bom_structure']
			lines = bom_structure_obj._get_bom(bom.id, product_id=product_id, line_qty = self.product_qty, line_id=self.id, level=1)
			bom.bom_cost =  lines.get('total')
			bom.product_cost = lines.get('price')
			if lines.get('operations'):
				for operations_details in lines.get('operations'):
					operation_line_detail = self.find_operation_details(bom,operations_details.get('operation'))
					if operation_line_detail:
						operation_line_detail.update({
							'quantity' : operations_details.get('duration_expected'),
							'bom_cost' : round(operations_details.get('total'),2),
							'operation_id': operations_details.get('operation').id,
							'bom_id':bom.id if bom else False
						})
					else:
						operation_line_detail = self.env['operations.line.details'].create({
							'bom_id':bom.id if bom else False,
							'bom_line_id' : self.id,
							'quantity' : operations_details.get('duration_expected'),
							'bom_cost' : round(operations_details.get('total'),2),
							'operation_id': operations_details.get('operation').id,
						})
			if lines.get('components') and bom.bom_line_ids:
				for line in bom.bom_line_ids:
					bom = self.env['mrp.bom']._bom_find(product=line.product_id)
					for component in lines.get('components'):
						if component.get('prod_id') == line.product_id.id:
							line.write({'bom_cost':round(component.get('total'),2)})
							line.write({'product_cost':round(component.get('prod_cost'),2)})

	def find_operation_details(self,bom_id,operation):
		if bom_id and operation:
			operation_details = self.env['operations.line.details'].search([('bom_id','=',bom_id.id),('operation_id','=',operation.id)])
			return operation_details
		else:
			return False


class OperationsDetails(models.Model):

	_name = "operations.details"

	bom_id = fields.Many2one('mrp.bom',string="BOM")
	operation_id = fields.Many2one('mrp.routing.workcenter',string="Operation")
	quantity = fields.Float('Quantity')
	uom_id = fields.Many2one('uom.uom',string='Unit Of Measure')
	bom_cost = fields.Float('BOM Cost')

class OperationsLinesDetails(models.Model):

	_name = "operations.line.details"

	bom_id = fields.Many2one('mrp.bom',string="BOM")
	bom_line_id = fields.Many2one('mrp.bom.line',string="BOM")
	operation_id = fields.Many2one('mrp.routing.workcenter',string="Operation")
	quantity = fields.Float('Quantity')
	uom_id = fields.Many2one('uom.uom',string='Unit Of Measure')
	bom_cost = fields.Float('BOM Cost')