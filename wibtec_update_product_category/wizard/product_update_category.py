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


class ProductUpdateCategory(models.TransientModel):

	_name = "product.update.category"

	file = fields.Binary('Upload Category File')
	file_long_desc = fields.Binary('Upload Long Description File')
	file_uom = fields.Binary('Upload UOM File')
	file_route = fields.Binary('Upload Route File')
	options = fields.Selection([('remove','Remove'),('update','Update')],string="Options",default='remove',required=True)
	update_options = fields.Selection([('category','Product Category'),('uom','UOM'),('route','Route'),('tax','Tax'),('long_desc','Long Description')],string="Update Options",required=True,default='category')

	@api.multi
	def update_tax_vlaues(self):
		product_ids = self.env['product.template'].search(['|',('active','=',False),('active','=',True),('is_tax_added','=',False),('type','=','product')],limit=6000)
		# customer_tax_id = self.env['account.tax'].search([('name','=','Tax Cloud'),
		# 												('type_tax_use','=','sale')])
		supplier_taxes_id = self.env['account.tax'].search([('name','=','Tax Exempt'),
														('type_tax_use','=','purchase')])
		supplier_taxes = [supplier_taxes_id.id]
		# vendor_tax_id = self.env['account.tax'].search([('name','=','Tax 8.25%'),
		# 												('type_tax_use','=','purchase'),
		# 												('amount','=',8.2500)])
		# vendor_tax_list = [vendor_tax_id.id]
		# tic_category_id = self.env['product.tic.category'].search([('code','=',0),('description','=','Uncategorized')])
		[product.write({'supplier_taxes_id': [(6, 0, supplier_taxes)],'is_tax_added':True}) for product in product_ids]
		

	@api.multi
	def remove_value(self):
		product_ids = self.env['product.template'].search([('taxes_id','!=',False)])
		[product.write({'taxes_id':[(5,)]}) for product in product_ids if product_ids]

	@api.multi
	def update_product_uom(self):
		if not self.file_uom:
			raise Warning(_('Please Select CSV File.'))
		else:
			keys = ['To Replace','With Replace']
			try:
				data = base64.b64decode(self.file_uom)
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
					if values['To Replace'] == 'To Replace':
						continue
					res=self.update_uoms(values)
			return res

	@api.multi
	def update_uoms(self,values):
		# Update Uoms
		old_uom_id = self.find_uom(values.get('To Replace'))
		new_uom_id = self.find_uom(values.get('With Replace'))
		product_ids = self.find_products(old_uom_id)
		[product.write({'uom_id':new_uom_id.id,'uom_po_id':new_uom_id.id}) for product in product_ids if product_ids]
		self.find_and_update_bom_uom()
		self.find_and_update_bom_line_uom()

	@api.multi
	def find_and_update_bom_uom(self):
		# Method will find BOM and uupdate them with currently set uom of product.
		boms_ids = self.env['mrp.bom'].search([])
		[bom.write({'product_uom_id':bom.product_tmpl_id.uom_id.id}) for bom in boms_ids]
			

	@api.multi
	def find_and_update_bom_line_uom(self):
		# Method will find BOM and uupdate them with currently set uom of product.
		boms_line_ids = self.env['mrp.bom.line'].search([])
		[line.write({'product_uom_id':line.product_id.uom_id.id}) for line in boms_line_ids]
			

	@api.multi
	def find_products(self,uom):
		product_ids=self.env['product.template'].search([('uom_id','=',uom.id)])
		if product_ids:
			return product_ids
		else:
			raise Warning(_('No Products are there with this "%s".') % uom.name)

	@api.multi
	def find_uom(self,uom):
		product_uom_id=self.env['uom.uom'].search([('name','=',uom)],limit=1)
		if product_uom_id:
			return product_uom_id
		else:
			raise Warning(_('UOM "%s" is not Available in System.') % uom)


	@api.multi
	@api.constrains('file')
	def _check_file(self):
		# Constrains for file if file is not uploaded
		if self.options == 'update':
			if self.update_options == 'uom':
				if not self.file_uom:
					raise ValidationError(_('Please upload CSV formatted file to update.'))
			elif self.update_options == 'category':
				if not self.file:
					raise ValidationError(_('Please upload CSV formatted file to update.'))
			elif self.update_options == 'route':
				if not self.file_route:
					raise ValidationError(_('Please upload CSV formatted file to update.'))
			elif self.update_options == 'long_desc':
				if not self.file_long_desc:
					raise ValidationError(_('Please upload CSV formatted file to update.'))
			
	@api.multi
	def update_product(self):
		# Method is used to fetch all data from selected csv file
		if not self.file:
			raise Warning(_('Please Select CSV File.'))
		else:
			keys = ['Reference','Product Category']
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
					if values['Reference'] == 'Reference':
						continue
					res=self.update_category_to_products(values)
			return res

	@api.multi
	def update_category_to_products(self,values):
		# Method is used to change value of product category field of product based on condition.
		product_id = self.find_product(values.get('Reference'))
		product_category_id = self.find_product_category(values.get('Product Category'))
		if product_id and product_category_id:
			product_id.write({'categ_id':product_category_id.id})

	@api.multi
	def find_product_category(self,category):
		# Method will return category of product if condition will fulfill else return warning.
		product_category_obj = self.env['product.category'].search([('complete_name','=',category)],limit=1)
		if product_category_obj:
			return product_category_obj
		else:
			raise Warning(_('Product Category "%s" is not Available in System.') % category)
		

	@api.multi
	def find_product(self,reference):
		# Method is will return Product if condition will fulfill else return warning.
		product_template_obj=self.env['product.template'].search(['|',('active','=',False),('active','=',True),('default_code','=',reference)],limit=1)
		if product_template_obj:
			return product_template_obj
		else:
			raise Warning(_('Product "%s" is not Available in System.') % reference)

	@api.multi
	def update_route(self):
		# Method to set route for all products
		# route_mto_id = self.env['stock.location.route'].search([('name','=','Make To Order')])
		route_man_id = self.env['stock.location.route'].search([('name','=','Manufacture')])
		updated_route_list = [route_man_id.id]
		product_template_obj=self.env['product.template'].search([('active','=',True)])
		# updated_route_list = [route_mto_id.id,route_man_id.id]
		# product_template_obj=self.env['product.template'].search(['|',
		# 	('active','=',False),
		# 	('active','=',True),
		# 	('route_ids','=',route_mto_id.id)
		# 	])
		# [product.update({'route_ids': [(6, 0, updated_route_list)]}) for product in product_template_obj if product_template_obj]
		[product.update({'route_ids': [(6, 0, updated_route_list)]}) for product in product_template_obj if product_template_obj]

	@api.multi
	def update_bom_product_route(self):
		# Method is used to fetch all data from selected csv file
		if not self.file_route:
			raise Warning(_('Please Select CSV File.'))
		else:
			keys = ['Product','Route']
			try:
				data = base64.b64decode(self.file_route)
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
					res=self.update_product_route(values)
			return res

	@api.multi
	def update_product_route(self,values):
		# Method will find route from system and product from sheet and update route to that product
		route_buy_id = self.env['stock.location.route'].search([('name','=','Buy')])
		updated_route_list = [route_buy_id.id]
		product =self.env['product.template'].search(['|',
										('active','=',True),
										('active','=',False),
										('default_code','=',values.get('Product'))],limit=1)
		if product and route_buy_id:
			product.update({'route_ids': [(6, 0, updated_route_list)]})

	@api.multi
	def update_long_desc(self):
		# Method is used to fetch all data from selected csv file
		if not self.file_long_desc:
			raise Warning(_('Please Select CSV File.'))
		else:
			keys = ['Internal Reference','Long Description']
			try:
				data = base64.b64decode(self.file_long_desc)
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
					if values['Internal Reference'] == 'Internal Reference':
						continue
					res=self.update_long_desc_to_products(values)
			return res

	@api.multi
	def update_long_desc_to_products(self,values):
		product_id = self.find_product(values.get('Internal Reference'))
		if product_id:
			product_id.write({'long_desc':values.get('Long Description')})