# Copyright 2017 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
from odoo import models
from odoo.tools.translate import _
from odoo.tools.misc import formatLang

_logger = logging.getLogger(__name__)


class BomStructureXlsx(models.AbstractModel):
	_name = 'report.mrp_bom_structure_xlsx.bom_structure_xlsx'
	_inherit = 'report.report_xlsx.abstract'

	def print_bom_children(self, ch, sheet, row, level):
		currency_id= self.env.user.company_id.currency_id
		workcenters = self.find_workcenters(ch.bom_id.routing_id)
		product_id = ch.product_id or ch.product_tmpl_id.product_variant_ids
		bom = self.env['mrp.bom']._bom_find(product=product_id)
		i, j = row, level
		j += 1
		# sheet.write(i, 1, '> '*j)
		sheet.write(i, j, ch.product_id.default_code or '')
		sheet.write(i, 11, ch.product_id.default_code or '')
		sheet.write(i, 12, ch.bom_id.code or '')
		sheet.write(i, 13, ch.product_id.display_name or '')
		sheet.write(i, 14, ch.product_uom_id._compute_quantity(ch.product_qty, ch.product_id.uom_id) or '')
		sheet.write(i, 15, ch.product_id.uom_id.name or '')
		sheet.write(i, 16, formatLang(self.env, round(ch.product_id.standard_price,2), currency_obj=currency_id) or '')
		sheet.write(i, 17, formatLang(self.env, ch.product_cost, currency_obj=currency_id) or '')
		sheet.write(i, 18, formatLang(self.env, ch.bom_cost, currency_obj=currency_id) or '')
		# workcenters = self.find_workcenters(bom.routing_id)
		# if workcenters:
		# 	if bom:
		# 		operation_details = self.find_operation_line_details(bom)
		# 		i += 1
		# 		for od in operation_details:
		# 			duration_minutes = '%02d:%02d' % (int(float(od.quantity)), float(od.quantity) % 1 * 60)
		# 			wc_name = od.operation_id.name + " " + '-' + " " + od.operation_id.workcenter_id.name if od.operation_id.workcenter_id else od.operation_id.name
		# 			sheet.write(i, j, wc_name   or '')
		# 			sheet.write(i, 14, duration_minutes)
		# 			sheet.write(i, 15, 'Minutes')
		# 			sheet.write(i, 16, '')
		# 			sheet.write(i, 17, formatLang(self.env, od.bom_cost, currency_obj=currency_id) or '')
		# 			i += 1
		i += 1
		len_child = ch.child_line_ids
		list_child_ids = ch.child_line_ids.ids
		if list_child_ids:
			last_bom = list_child_ids[::-1][0]
		for child in ch.child_line_ids:
			child._update_cost(child)
			# child.bom_id.compute_parent_bom_costs(child.bom_id)
			if j >=10:
			  j = 9
			i = self.print_bom_children(child, sheet, i, j)
			if child.id == last_bom: 
				if workcenters:
					if bom:
						operation_details = self.find_operation_line_details(bom)
						# i += 1
						for od in operation_details:
							duration_minutes = '%02d:%02d' % (int(float(od.quantity)), float(od.quantity) % 1 * 60)
							wc_name = od.operation_id.name + " " + '-' + " " + od.operation_id.workcenter_id.name if od.operation_id.workcenter_id else od.operation_id.name
							sheet.write(i, j+1, wc_name   or '')
							sheet.write(i, 14, duration_minutes)
							sheet.write(i, 15, 'Minutes')
							sheet.write(i, 16, '')
							sheet.write(i, 17, formatLang(self.env, od.bom_cost, currency_obj=currency_id) or '')
							i += 1
				j -= 1
		return i

	def generate_xlsx_report(self, workbook, data, objects):
		currency_id= self.env.user.company_id.currency_id
		workbook.set_properties({
			'comments': 'Created with Python and XlsxWriter from Odoo 12.0'})
		sheet = workbook.add_worksheet(_('BOM Structure'))
		sheet.set_landscape()
		sheet.fit_to_pages(1, 0)
		sheet.set_zoom(80)
		sheet.set_column(0, 0, 40)
		sheet.set_column(1, 6, 20)
		sheet.set_column(2, 6, 20)
		sheet.set_column(3, 6, 40)
		sheet.set_column(4, 6, 20)
		sheet.set_column(5, 6, 20)
		sheet.set_column(6, 6, 20)
		sheet.set_column(7, 6, 20)
		sheet.set_column(8, 6, 20)
		sheet.set_column(9, 6, 20)
		sheet.set_column(10, 6, 20)
		sheet.set_column(11, 6, 20)
		sheet.set_column(12, 6, 20)
		sheet.set_column(13, 6, 20)
		sheet.set_column(14, 6, 20)
		sheet.set_column(15, 6, 20)
		sheet.set_column(16, 6, 20)
		sheet.set_column(17, 6, 20)
		sheet.set_column(18, 6, 20)
		bold = workbook.add_format({'bold': True})
		align = workbook.add_format({'align': 'left'})
		title_style = workbook.add_format({'bold': True,
										   'bg_color': '#FFFFCC',
										   'bottom': 1})
		sheet_title = [_('BOM Name'),
					   _('Level1'),
					   _('Level2'),
					   _('Level3'),
					   _('Level4'),
					   _('Level5'),
					   _('Level6'),
					   _('Level7'),
					   _('Level8'),
					   _('Level9'),
					   _('Level10'),
					   _('Product Reference'),
					   _('Reference'),
					   _('Product Name'),
					   _('Quantity'),
					   _('Unit of Measure'),
					   _('Unit Cost'),
					   _('Material Cost'),
					   _('BOM Cost')
					   ]
		sheet.set_row(0, None, None, {'collapsed': 1})
		sheet.write_row(1, 0, sheet_title, title_style)
		sheet.freeze_panes(2, 0)
		i = 2
		for o in objects:
			workcenters = self.find_workcenters(o.routing_id)
			o._update_cost(o)
			sheet.write(i, 0, o.product_tmpl_id.name or o.default_code or '', bold)
			sheet.write(i, 11, o.product_tmpl_id.default_code or '', bold)
			sheet.write(i, 12, o.code or '', bold)
			sheet.write(i, 13, o.product_tmpl_id.name or '', bold)
			sheet.write(i, 14, o.product_qty, bold)
			sheet.write(i, 15, o.product_uom_id.name or '', bold)
			sheet.write(i, 16, formatLang(self.env, round(o.product_id.standard_price,2), currency_obj=currency_id) or '', bold)
			sheet.write(i, 17, formatLang(self.env, o.product_cost, currency_obj=currency_id) or '', bold)
			sheet.write(i, 18, formatLang(self.env, o.bom_cost, currency_obj=currency_id) or '', bold)
			if workcenters:
				operation_details = self.find_operation_details(o)
				i += 1
				for od in operation_details:
					duration_minutes = '%02d:%02d' % (int(float(od.quantity)), float(od.quantity) % 1 * 60)
					wc_name = od.operation_id.name + " " + '-' + " " + od.operation_id.workcenter_id.name if od.operation_id.workcenter_id else od.operation_id.name
					sheet.write(i, 1, wc_name   or '', bold)
					sheet.write(i, 14, duration_minutes, bold)
					sheet.write(i, 15, 'Minutes', bold)
					sheet.write(i, 16,'')
					sheet.write(i, 17,formatLang(self.env, od.bom_cost, currency_obj=currency_id) or '', bold)
					i += 1
			j = 0
			for ch in o.bom_line_ids:
				ch._update_cost(ch)
				i = self.print_bom_children(ch, sheet, i, j)

	def find_workcenters(self,routing_id):
		if routing_id:
			workcenters = self.env['mrp.routing.workcenter'].search([('routing_id','=',routing_id.id)])
			return workcenters
		else:
			return False	
 
	def find_operation_details(self,bom_id):
		if bom_id:
			operation_details = self.env['operations.details'].search([('bom_id','=',bom_id.id)])
			return operation_details
		else:
			return False
	
	def find_operation_line_details(self,bom_id):
		if bom_id:
			operation_line_details = self.env['operations.line.details'].search([('bom_id','=',bom_id.id)])
			return operation_line_details
		else:
			return False