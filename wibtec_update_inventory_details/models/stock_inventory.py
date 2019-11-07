# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class StockInventory(models.Model):

    _inherit = "stock.inventory"

    @api.multi
    def open_wizard(self):
        # Method will open wizard
        return {
                'name': _('update Inventory Details'),
                'type': 'ir.actions.act_window',
                'res_model': 'update.stock.inventory.line',
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'new',
                'context': {'default_stock_inventory_id': self.id}
            }

    @api.multi
    def set_qty(self):
        # Method will set qty to 100 for every line
        [line.write({'product_qty':100}) for inventory in self for line in inventory.line_ids if line]