#! -*- encoding: utf-8 -*-
import logging

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

class WorkOrder(models.Model):
    _inherit = 'mrp.workorder'

    employee_id = fields.Many2one('hr.employee', 'Assigned to',
                                    help='Employee who should be responsible for this work order')
