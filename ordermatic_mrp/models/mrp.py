#! -*- encoding: utf-8 -*-
import logging
from odoo import models, fields, api, _
_logger = logging.getLogger(__name__)


class WorkOrder(models.Model):
    _inherit = 'mrp.workorder'

    picking_ids = fields.Many2many(
                                    comodel_name='stock.picking',
                                    relation='workorder_picking_rel',
                                    column1='picking_id',
                                    column2='workorder_id',
                                    string='Shipments'
                                    )
