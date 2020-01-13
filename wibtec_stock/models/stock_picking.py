# -*- coding: utf-8 -*-

from odoo import fields, models, api, tools

class StockPicking(models.Model):

    _inherit = 'stock.picking'

    @api.multi
    def _check_delivery_installed(self):
        self.ensure_one()
        module_obj = self.env['ir.module.module'].sudo()
        delivery_installed = module_obj.search([('name', '=', 'delivery'),('state', '=', 'installed')])
        res = {}
        if delivery_installed:
            return True
        return False