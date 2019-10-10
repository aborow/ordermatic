# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class WarrantyInformation(models.Model):

	_name = "warranty.information"
	_description = "Warranty Information"
	_rec_name = 'partner_id'

	product_id = fields.Many2one('product.product','Product',required=True)
	description = fields.Char('Product Description')
	sale_date = fields.Date('Sales Date',required=True)
	delivery_date = fields.Date('Delivery Date',required=True)
	sales_notes = fields.Text('Sales Notes')
	serial_number = fields.Char('Serial Number',required=True)
	partner_id = fields.Many2one('res.partner','Customer',required=True)
	company_id = fields.Many2one('res.company',related='partner_id.company_id')
	customer_ID = fields.Char('Customer ID')
	street = fields.Char()
	street2 = fields.Char()
	zip = fields.Char(change_default=True)
	city = fields.Char()
	state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', domain="[('country_id', '=?', country_id)]")
	country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
	stock_move_line_id = fields.Many2one('stock.move.line',string="Associated Stock Move Line")