#! -*- encoding: utf-8 -*-
import logging
from odoo import models, fields, api, _
_logger = logging.getLogger(__name__)


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    vendor_id = fields.Many2one('res.partner', 'Vendor', domain=[('supplier','=',True)])
    product_id = fields.Many2one('product.product', 'Product', domain=[('sale_ok','=',True)])
    estimated_costs = fields.Float('Estimated costs')

    @api.multi
    def _get_team(self):
        for s in self:
            is_maintenance_team = False
            is_product_change_team = False
            if s.team_id:
                if 'campus maintenance' in s.team_id.name.lower():
                    is_maintenance_team = True
                if 'product change' in s.team_id.name.lower():
                    is_product_change_team = True
            s.is_maintenance_team = is_maintenance_team
            s.is_product_change_team = is_product_change_team

    is_maintenance_team = fields.Boolean('Is maintenance team', compute='_get_team')
    is_product_change_team = fields.Boolean('Is product change team', compute='_get_team')
