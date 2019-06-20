#! -*- encoding: utf-8 -*-
import logging
from odoo import models, fields, api, _
_logger = logging.getLogger(__name__)


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    vendor_id = fields.Many2one('res.partner', 'Vendor', domain=[('supplier','=',True)])
    estimated_costs = fields.Float('Estimated costs')
