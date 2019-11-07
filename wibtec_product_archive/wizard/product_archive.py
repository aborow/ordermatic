# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import Warning
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

class ProductArchive(models.TransientModel):

	_name = "product.archive"

	file = fields.Binary('Select File')
			
	@api.multi
	def update_product(self):
		# Method is used to fetch all data from selected csv file
		self.archive_products()
		self.archive_boms()
		if not self.file:
			raise Warning(_('Please Select CSV File.'))
		else:
			keys = ['Reference','Name','Type']
			data = base64.b64decode(self.file)
			file_input = io.StringIO(data.decode("utf-8"))
			file_input.seek(0)
			reader_info = []
			reader = csv.reader(file_input, delimiter=',')
			try:
				reader_info.extend(reader)
			except Exception:
				raise exceptions.Warning(_("Not a valid file!"))
			values = {}
			for i in range(len(reader_info)):
				field = map(str, reader_info[i])
				values = dict(zip(keys, field))
				if values:
					if values['Reference'] == 'Reference':
						continue
					res=self.update_product_archive(values)
					_logger.info("res:::::::::::::::::::::::::::::: %s" % res)
			self.product_tmpl_active_from_product()
			return res

	@api.multi
	def update_product_archive(self,values):
		# Method is used to change value of active field product based on condition.
		product_id = self.find_product(values.get('Name'),values.get('Reference'))
		if values.get('Type') == 'bom':
			bom_id = self.find_bom(product_id)
			bom_id.write({'active':True})
			_logger.info("res::::::::::::bom_id:::::::::::::::::: %s" % bom_id)
			self.unarchive_bom(bom_id)
		product_id.write({'active':True})
		return product_id
		

	@api.multi
	def find_bom(self,product_id):
		# Method is will return BOM if condition will fulfill else return warning.
		bom_id = self.env['mrp.bom'].search(['|',('active','=',True),('active','=',False),('product_tmpl_id','=',product_id.id)])
		if bom_id:
			return bom_id
		else:
			raise Warning(_('BOM "%s" is not Available in System.') % product_id.name)

	@api.multi
	def find_product(self,name,reference):
		# Method is will return Product if condition will fulfill else return warning.
		product_template_obj=self.env['product.template'].search([('name','=',name),('default_code','=',reference),('active','=',False)])
		if product_template_obj:
			return product_template_obj
		else:
			if not reference:
				raise Warning(_('Product Reference "%s" is not Available in System.') % reference)
			else:
				raise Warning(_('Product "%s" is not Available in System.') % name)

	@api.multi
	def archive_products(self):
		# Method will archive all products
		product_template_obj=self.env['product.template'].search([])
		[product.write({'active':False,'is_active_custom':False}) for product in product_template_obj]
			

	@api.multi
	def archive_boms(self):
		# Method will archive all bom
		mrp_boms=self.env['mrp.bom'].search([])
		[bom.write({'active':False}) for bom in mrp_boms]

	@api.multi
	def unarchive_bom(self,bom_ids):
		# Method will unarchive products which are bom components
		for bom in bom_ids:
			for line in bom.bom_line_ids:
				boms = self.env['mrp.bom'].search(['|',('active','=',True),('active','=',False),('product_tmpl_id','=',line.product_id.product_tmpl_id.id)])
				_logger.info("res::::::::::::bomsbomsbomsboms:::::::::::::::::: %s" % boms)
				for bom in boms:
					bom.write({'active':True})
		[line.product_id.write({'active':True}) for bom in bom_ids for line in bom.bom_line_ids]

	@api.multi
	def product_tmpl_active_from_product(self):
		product_ids = self.env['product.product'].search([('active','=',True)],limit=5000)
		for product in product_ids:
			if product.product_tmpl_id.is_active_custom == False:
				product.product_tmpl_id.write({'active':True,'is_active_custom':True})