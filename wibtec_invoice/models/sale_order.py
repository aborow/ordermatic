# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SaleOrder(models.Model):
	_inherit = "sale.order"

	note_of_invoice = fields.Text("Notes for Invoice")
	tracking_numbers = fields.Char("Tracking Numbers",compute='_add_tracking_numbers')

	@api.multi
	def _prepare_invoice(self):
		result = super(SaleOrder, self)._prepare_invoice()
		if self.note_of_invoice:
			result.update({'note_of_invoice': self.note_of_invoice,'tracking_numbers':self.tracking_numbers})
		return result


	@api.multi
	@api.depends('picking_ids')
	def _add_tracking_numbers(self):
		tracking_numbers = ''
		for picking in self.picking_ids:
			if picking.carrier_tracking_ref and picking.sale_id:
				if not picking.sale_id.tracking_numbers:
					tracking_numbers = picking.carrier_tracking_ref
					self.update({'tracking_numbers':tracking_numbers})
				else:
					tracking_numbers = tracking_numbers + ',' + picking.carrier_tracking_ref
					self.update({'tracking_numbers':tracking_numbers})
