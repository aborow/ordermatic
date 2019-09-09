# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class MrpWorkorder(models.Model):

	_inherit = "mrp.workorder"

	@api.multi
	def change_color_on_kanban(self): 
		for record in self:
			color = 0
			if record.state == 'progress':
				record.color = 8
			elif record.state == 'ready':
				record.color = 4
			elif record.state == 'pending':
				record.color = 3
			elif record.state == 'done':
				record.color = 10
				
	color = fields.Integer('Color Index', compute="change_color_on_kanban")