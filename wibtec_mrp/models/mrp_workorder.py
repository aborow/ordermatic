# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from dateutil.relativedelta import relativedelta
from datetime import datetime

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
	duration_remaining = fields.Float('Remaining Duration',compute='_compute_duration_remaining')
	duration_expected_for_single_qty = fields.Float('Duration Expected Single Quantity',compute='_compute_duration_remaining')

	@api.multi
	@api.depends('duration_expected', 'qty_produced')
	def _compute_duration_remaining(self):
		for wo in self:
			wo.duration_expected_for_single_qty = wo.duration_expected / wo.qty_production
			if wo.qty_produced > 0.0 and wo.qty_producing > 0.0:
				test = wo.qty_production - wo.qty_produced
				wo.duration_remaining = wo.duration_expected_for_single_qty * (wo.qty_production - wo.qty_produced)
			elif wo.qty_produced == 0.0:
				wo.duration_remaining = wo.duration_expected

	@api.multi 
	def update_duration(self):
		duration = 0.0
		time_lines = self.env['mrp.workcenter.productivity'].search([('workorder_id','=',self.id)])
		if time_lines:
			for time in time_lines:
				duration += time.duration
			routing_workcenter_id = self.env['mrp.routing.workcenter'].search([('routing_id','=',self.production_id.routing_id.id),('id','=',self.operation_id.id)],limit=1)
			if routing_workcenter_id and routing_workcenter_id.time_mode == 'manual':
				if self.qty_producing == 0.0 and self.qty_produced == self.qty_production:
					if round(duration) != self.duration_expected and round(duration) < self.duration_expected:
						time_line_id = time_lines[0]
						time_line_id.write({'duration':time_line_id.duration + self.duration_expected - duration})
						end_date = fields.Datetime.from_string(time_line_id.date_start) + relativedelta(minutes=time_line_id.duration)
						time_line_id.write({'date_end':end_date})
		return True

	@api.multi
	def button_finish(self):
		self.ensure_one()
		self.end_all()
		self.update_duration()
		return self.write({'state': 'done', 'date_finished': self.time_ids[0].date_end if self.time_ids else fields.Datetime.now()})