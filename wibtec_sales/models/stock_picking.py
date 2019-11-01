# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import datetime

class StockPicking(models.Model):

	_inherit = 'stock.picking'

	def action_done(self):
		res = super(StockPicking, self).action_done()
		if self.picking_type_id.code == 'outgoing':
			order_id = self.env['sale.order'].search([('name', '=', self.origin)],limit=1)
			if order_id:
				order_id.write({'omc_actual_delivery_date':datetime.datetime.strptime(str(self.date_done), '%Y-%m-%d %H:%M:%S').date()})
		return res