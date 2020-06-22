# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import datetime

class StockPicking(models.Model):

	_inherit = "stock.picking"

	@api.multi
	def create_warranty_information(self):
		if self.state == 'done':
			if self.picking_type_id.code == 'outgoing':
				sale_id = self.env['sale.order'].search([('name','=',self.origin)],limit=1)
				if sale_id:
					for move in self.move_ids_without_package:
						move_line_ids = self.env['stock.move.line'].search([('product_id','=',move.product_id.id),('move_id','=',move.id)])
						for move_line in move_line_ids:
							if move.product_id.tracking == 'serial':
								warranty_information_id = self.env['warranty.information'].create({
										'partner_id':sale_id.partner_id.id,
										'customer_ID':sale_id.partner_id.category_id[0].name if sale_id.partner_id.category_id else '',
										'product_id':move.product_id.id,
										'description':move.product_id.long_desc,
										'street':sale_id.partner_id.street,
										'street2':sale_id.partner_id.street2,
										'city':sale_id.partner_id.city,
										'state_id':sale_id.partner_id.state_id.id,
										'zip': sale_id.partner_id.zip,
										'country_id':sale_id.partner_id.country_id.id,
										'serial_number':move_line.lot_id.name if move_line.lot_id else False,
										'sale_date':datetime.datetime.strptime(str(sale_id.confirmation_date),'%Y-%m-%d %H:%M:%S').date(),
										'delivery_date': datetime.datetime.strptime(str(self.date_done),'%Y-%m-%d %H:%M:%S').date(),
										'stock_move_line_id':move_line.id
										})
		return True

	@api.multi
	def button_validate(self):
		res = super(StockPicking, self).button_validate()
		self.create_warranty_information()
		return res