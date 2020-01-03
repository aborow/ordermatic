# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import datetime

class StockMoveLines(models.Model):

	_inherit = "stock.move.line"

	@api.multi
	def write(self,vals):
		val = {}
		if 'lot_id' in vals:
			warranty_information_id = self.env['warranty.information'].search([('stock_move_line_id','=',self.id)])
			if warranty_information_id and not self._context.get('demo'):
				ctx = {}
				ctx = self._context.copy()
				ctx.update({'demo': True})
				val = {}
				lot_id = self.env['stock.production.lot'].browse(vals.get('lot_id'))
				val = {'serial_number':lot_id.name}
				warranty_information_id.with_context(ctx).write(val)
		return super(StockMoveLines, self).write(vals)