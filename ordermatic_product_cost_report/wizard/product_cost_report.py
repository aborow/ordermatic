#-*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields,api, _
from datetime import datetime
from odoo.exceptions import ValidationError
from odoo.tools.misc import formatLang
import base64
import io
import xlsxwriter
import logging
_logger = logging.getLogger(__name__)

class ProductCostReport(models.TransientModel):

	_name = "product.cost.report"
	_description = "Product Cost Report"

	product_ids = fields.Many2many('product.template',string="Products")

	@api.multi
	def get_domain(self):
		"""Method will filter record based on domain."""
		domain = [('product_tmpl_id.sale_ok', '=', True),('product_tmpl_id.bom_ids','!=',False)]
		if self.product_ids:
			domain.append(('product_tmpl_id','in',self.product_ids.ids))
		return domain

	@api.multi
	def get_bom_data(self):
		domain = self.get_domain()
		bom_ids = self.env['mrp.bom'].search(domain)
		return bom_ids

	@api.multi
	def print_xls(self):
		"""Method will print the XLS report."""
		bom_ids = self.get_bom_data()
		if not bom_ids:
			raise ValidationError(_('No records found for this product.'))
		fp = io.BytesIO()
		workbook = xlsxwriter.Workbook(fp)
		worksheet = workbook.add_worksheet('Product Cost Report')
		data_format = workbook.add_format({'align': 'center'})
		report_header_format = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 18})
		header_format = workbook.add_format({'bold': True})
		parent_product_format = workbook.add_format({'color':'black','bg_color':'#D7DBDD'})
		# child_product_format = workbook.add_format({'align': 'center'})
		bold = workbook.add_format({'bold': True})
		worksheet.set_column('A:A', 30)
		worksheet.set_column('B:B', 25)
		worksheet.set_column('C:C', 15)
		worksheet.set_column('D:D', 15)
		worksheet.set_column('E:E', 15)
		worksheet.set_column('F:F', 15)
		worksheet.set_column('G:G', 15)
		worksheet.set_column('H:H', 15)
		worksheet.set_column('I:I', 15)
		not_exist = workbook.add_format({'bold': True, 'font_color': 'red'})
		row = 0
		colm = 0
		currency_id= self.env.user.company_id.currency_id
		if bom_ids:
			_logger.info("BOM IDS------------------------------------- %s" % bom_ids)
			for bom in bom_ids:
				bom_costs = bom._update_bom_cost(bom)
				if bom_costs:
					_logger.info("bom_costs-----------------@@@@@@@@@@-------------------- %s" % bom_costs)
					row += 0
					worksheet.write(row, 0, 'Product Name', header_format)
					worksheet.write(row, 1, 'Internal Reference', header_format)
					worksheet.write(row, 2, 'Product Cost', header_format)
					worksheet.write(row, 3, 'BOM Cost', header_format)
					worksheet.write(row, 4, 'Cost For Qty 1', header_format)
					worksheet.write(row, 5, 'Cost For Qty 2', header_format)
					worksheet.write(row, 6, 'Cost For Qty 4', header_format)
					worksheet.write(row, 7, 'Cost For Qty 6', header_format)
					worksheet.write(row, 8, 'Cost For Qty 10', header_format)
					# colm = 0	
					row += 1
					worksheet.write(row, 0, bom.product_tmpl_id.name, parent_product_format)
					worksheet.write(row, 1, bom.product_tmpl_id.default_code, parent_product_format)
					worksheet.write(row, 2, formatLang(self.env, bom.product_cost, currency_obj=currency_id), parent_product_format)
					worksheet.write(row, 3, formatLang(self.env, bom.bom_cost, currency_obj=currency_id), parent_product_format)
					worksheet.write(row, 4, formatLang(self.env, bom_costs[0], currency_obj=currency_id), parent_product_format)
					worksheet.write(row, 5, formatLang(self.env, bom_costs[1], currency_obj=currency_id), parent_product_format)
					worksheet.write(row, 6, formatLang(self.env, bom_costs[2], currency_obj=currency_id), parent_product_format)
					worksheet.write(row, 7, formatLang(self.env, bom_costs[3], currency_obj=currency_id), parent_product_format)
					worksheet.write(row, 8, formatLang(self.env, bom_costs[4], currency_obj=currency_id), parent_product_format)
					# colm = 0
					row += 1
					for bom_line in bom.bom_line_ids:
						bom_line_costs = bom._get_bom_line_cost(bom,bom_line)
						worksheet.write(row, 0, bom_line.product_id.name)
						worksheet.write(row, 1, bom_line.product_id.default_code)
						worksheet.write(row, 2, formatLang(self.env,bom_line.product_cost, currency_obj=currency_id))
						worksheet.write(row, 3, formatLang(self.env,bom_line.bom_cost, currency_obj=currency_id))
						worksheet.write(row, 4, bom_line_costs[0])
						worksheet.write(row, 5, bom_line_costs[1])
						worksheet.write(row, 6, bom_line_costs[2])
						worksheet.write(row, 7, bom_line_costs[3])
						worksheet.write(row, 8, bom_line_costs[4])
						colm = 0
						row += 1
					row += 1
					worksheet.write(row, 0, 'Total',header_format)
					worksheet.write(row, 2, formatLang(self.env,bom.product_cost, currency_obj=currency_id), header_format)
					worksheet.write(row, 3, formatLang(self.env,bom.bom_cost, currency_obj=currency_id), header_format)
					worksheet.write(row, 4, formatLang(self.env,bom_costs[0], currency_obj=currency_id), header_format)
					worksheet.write(row, 5, formatLang(self.env,bom_costs[1], currency_obj=currency_id), header_format)
					worksheet.write(row, 6, formatLang(self.env,bom_costs[2], currency_obj=currency_id), header_format)
					worksheet.write(row, 7, formatLang(self.env,bom_costs[3], currency_obj=currency_id), header_format)
					worksheet.write(row, 8, formatLang(self.env,bom_costs[4], currency_obj=currency_id), header_format)
					row += 2
		workbook.close()
		fp.seek(0)
		result = base64.b64encode(fp.read())
		attachment_obj = self.env['ir.attachment']
		attachment_id = attachment_obj.create(
			{'name': 'product_cost_report.xlsx', 'datas_fname': 'Product Cost Report.xlsx', 'datas': result})
		download_url = '/web/content/' + \
			str(attachment_id.id) + '?download=True'
		base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
		return {
			"type": "ir.actions.act_url",
			"url": str(base_url) + str(download_url),
			"target": "new"
		}