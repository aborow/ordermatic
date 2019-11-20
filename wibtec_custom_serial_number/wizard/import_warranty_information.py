# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import Warning,ValidationError
import datetime
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

class ImportWarrantyInformation(models.TransientModel):

	_name = "import.warranty.information"
	_description = "Import Warranty Information"

	file = fields.Binary('Select File')

	@api.multi
	@api.constrains('file')
	def _check_file(self):
		# Constrains for file if file is not uploaded 
		if not self.file:
			raise ValidationError(_('Please upload CSV formatted file to import BOM.'))

	@api.multi
	def import_warranty_information(self):
		# Method will import BOM
		keys = ['Serial Number','Product','Partner','Sales Date']
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
				if values['Serial Number'] == 'Serial Number':
					continue
				res=self.create_warranty_information(values)
		return res

	@api.multi
	def create_warranty_information(self,values):
		# Method will create BOM with values from CSV file
		product_id = self.find_product(values.get('Product'))
		partner_id = self.find_partner(values.get('Partner'))
		if product_id.active == False:
			product_id.write({'is_used_in_warranty':True})
		warranty_information_id = self.env['warranty.information'].create({
			'partner_id': partner_id.id if partner_id else False,
			'customer_ID':values.get('Partner'),
			'product_id':product_id.id if product_id else False,
			'description':product_id.long_desc if product_id else False,
			'street':partner_id.street if partner_id else False,
			'street2':partner_id.street2 if partner_id else False,
			'city':partner_id.city if partner_id else False,
			'state_id':partner_id.state_id.id if partner_id else False,
			'zip': partner_id.zip if partner_id else False,
			'country_id': partner_id.country_id.id if partner_id else False,
			'serial_number':values.get('Serial Number') if values.get('Serial Number') else False,
			'sale_date':datetime.datetime.strptime(values.get('Sales Date'),'%Y-%m-%d').date() if values.get('Sales Date') else False
			})
		return warranty_information_id

	@api.multi
	def find_product(self,product):
		# Method will find product from product templates if product will found then it will return product else it will return warning
		product_obj_search=self.env['product.product'].search(['|',
																('active','=',True),
																('active','=',False),
																('default_code','=',product)],limit=1)
		if product_obj_search:
			return product_obj_search
		else:
			raise Warning(_('Product %s is not Available in System.') % product)
			# return False

	@api.multi
	def find_tags_partner(self,tag_name):
		# Method will find tag from product partner if partner will found then it will return partner else it will return warning
		tag_id =self.env['res.partner.category'].search(['|',('active','=',True),
														('active','=',False),
														('name','=',tag_name)],limit=1)
		if tag_id:
			return tag_id
		else:
			# return False
			raise Warning(_('Tag %s is not Available in System.') % tag_name)

	@api.multi
	def find_partner(self,tag_name):
		# Method will find partner from partner if partner will found then it will return partner else it will return warning
		tag_id = self.find_tags_partner(tag_name)
		if tag_id:
			partner_id =self.env['res.partner'].search(['|',('active','=',True),
														('active','=',False),
														('category_id','=',tag_id.id)],limit=1)
			if partner_id:
				return partner_id
			else:
				# return False
				raise Warning(_('Partner %s is not Available in System.') % tag_name)