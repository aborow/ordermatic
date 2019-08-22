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


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.onchange('product_id', 'picking_type_id', 'company_id')
    def onchange_product_id(self):
        """ Finds UoM of changed product. """
        if not self.product_id:
            self.bom_id = False
        else:
            bom = self.env['mrp.bom']._bom_find(product=self.product_id, picking_type=self.picking_type_id, company_id=self.company_id.id)
            if bom.type == 'normal':
                self.bom_id = bom.id
                self.product_qty = self.bom_id.product_qty
                self.product_uom_id = self.bom_id.product_uom_id.id
            else:
                self.bom_id = False
                self.product_uom_id = self.product_id.uom_id.id

            return_values = {'domain': {'product_uom_id': [('category_id', '=', self.product_id.uom_id.category_id.id)]}}
            # Load default production location from the product
            if self.product_id and self.product_id.location_dest_id:
                return_values['value'] = {'location_dest_id': self.product_id.location_dest_id.id}
            return return_values
