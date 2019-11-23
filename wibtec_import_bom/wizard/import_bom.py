# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import Warning,ValidationError
import logging
_logger = logging.getLogger(__name__)
import io
try:
	import csv
except ImportError:
	_logger.debug('Cannot `import csv`.')
try:
	import StringIO
except ImportError:
	_logger.debug('Cannot `import StringIO`.')
try:
	import base64
except ImportError:
	_logger.debug('Cannot `import base64`.')

class ImportBOM(models.TransientModel):

	_name = "import.bom"

	file = fields.Binary('Select File')

	@api.multi
	@api.constrains('file')
	def _check_file(self):
		# Constrains for file if file is not uploaded 
		if not self.file:
			raise ValidationError(_('Please upload CSV formatted file to import BOM.'))

	@api.multi
	def import_bom(self):
		# Method will import BOM
		keys = ['Product Template','BoM Type', 'Quantity', 'Product', 'Product Quantity']
		try:
			data = base64.b64decode(self.file)
			file_input = io.StringIO(data.decode("utf-8"))
			file_input.seek(0)
			reader = csv.reader(file_input, delimiter=',')
		except ValueError:  
			raise ValidationError(_('Not a Valid File!'))
		reader_info = []
		reader_info.extend(reader)
		values = {}
		for i in range(len(reader_info)):
			field = map(str, reader_info[i])
			values = dict(zip(keys, field))
			if values:
				if values['Product Template'] == 'Product Template':
					continue
				res=self.create_bom(values)
		return res

	@api.multi
	def create_bom(self,values):
		# Method will create BOM with values from CSV file
		product_template_id = self.find_product_template(values.get('Product Template'))
		bom_obj_id = self.env['mrp.bom'].search([('product_tmpl_id','=',product_template_id.id),('product_qty','=',values.get('Quantity')),('type','=',values.get('BoM Type'))],limit=1)
		if bom_obj_id:
			lines = self.create_bom_line(values, bom_obj_id)
			return lines
		else:
			bom_id = self.env['mrp.bom'].create({
										'product_tmpl_id' : product_template_id.id,
										'product_qty' : values.get('Quantity'),
										'type':values.get('BoM Type'),
										'product_uom_id': product_template_id.uom_id.id,
										'company_id':1
										})
			lines = self.create_bom_line(values, bom_id)
			return lines

	@api.multi
	def create_bom_line(self,values,bom_id):
		# Method will create BOM line for passed arguement(BOM)
		product_id = self.find_product_product(values.get('Product'))
		bom_line_id  = self.env['mrp.bom.line'].create({
				'product_id' : product_id.id,
				'product_qty' : values.get('Product Quantity'),
				'product_uom_id' : product_id.uom_id.id,
				'bom_id' : bom_id.id
				})

	@api.multi
	def find_product_template(self,product_template):
		# Method will find product from product templates if product will found then it will return product else it will return warning
		product_temp_obj_search=self.env['product.template'].search(['|',('default_code','=',product_template),('name','=',product_template)],limit=1)
		if product_temp_obj_search:
			return product_temp_obj_search
		else:
			raise Warning(_('Product %s is not Available in System.') % product_template)

	@api.multi
	def find_product_product(self,product_product):
		# Method will find product from product product if product will found then it will return product else it will return warning
		product_product_obj_search=self.env['product.product'].search(['|',('default_code','=',product_product),('name','=',product_product)],limit=1)
		if product_product_obj_search:
			return product_product_obj_search
		else:
			raise Warning(_('Product %s is not Available in System.') % product_product)    