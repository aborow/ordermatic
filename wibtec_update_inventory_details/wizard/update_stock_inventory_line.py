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

class updateStockInventoryLine(models.TransientModel):

	_name = "update.stock.inventory.line"
	_description = "Update Stock Inventory Line"

	file = fields.Binary('Select File')
	stock_inventory_id = fields.Many2one('stock.inventory',string="Stock Inventory",readonly=True) 

	@api.multi
	@api.constrains('file')
	def _check_file(self):
		# Constrains for file if file is not uploaded 
		if not self.file:
			raise ValidationError(_('Please upload CSV formatted file to update Quantity.'))

	@api.multi
	def update_inventory_details(self):
		# Method will update inventory lines
		keys = ['Product','Location','Real Quantity']
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
				if values['Product'] == 'Product':
					continue
				res=self.create_stock_iventory_line(values)
		return res

	@api.multi
	def create_stock_iventory_line(self,values):
		# Method will update inventory lines
		product_id = self.find_product(values.get('Product'))
		location_id = self.find_location(values.get('Location'))
		if self.stock_inventory_id:
			self.env['stock.inventory.line'].create({
				'location_id':location_id.id,
				'product_id':product_id.id,
				'product_uom_id':product_id.uom_id.id,
				'inventory_id':self.stock_inventory_id.id,
				'product_qty':values.get('Real Quantity')
			})
		# stock_inventory_line_id = self.env['stock.inventory.line'].search([('product_id','=',product_id.id),('location_id','=',location_id.id),('inventory_id','=',self.stock_inventory_id.id)])
		# if stock_inventory_line_id:
		#   stock_inventory_line_id.write({
		#       'product_qty' : values.get('Real Quantity')
		#       })
		# else:
		#   raise Warning(_('No Lines Found to Update!'))    

	@api.multi
	def find_location(self,location):
		# Method will find location if location will found then it will return location else it will return warning
		location_id = self.env['stock.location'].search([('location_name','=',location)],limit=1)
		if location_id:
			return location_id
		else:
			raise Warning(_('Location %s is not Found in System.') % location)    

	@api.multi
	def find_product(self,product):
		# Method will find product from product product if product will found then it will return product else it will return warning
		product_id = self.env['product.product'].search(['|',('default_code','=',product),('name','=',product)],limit=1)
		if product_id:
			return product_id
		else:
			raise Warning(_('Product %s is not Available in System.') % product)    