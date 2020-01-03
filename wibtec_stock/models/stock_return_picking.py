# -*- coding: utf-8 -*-

from odoo import fields, models, api, tools

class StockReturnPicking(models.TransientModel):

	_inherit = 'stock.return.picking.line'
	
	to_refund = fields.Boolean(string="To Return", help='Trigger a decrease of the delivered/received quantity in the associated Sale Order/Purchase Order')