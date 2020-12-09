# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _compute_omc_qty_available(self):
        for record in self:
            record.omc_qty_available = record.qty_available - record.outgoing_qty

    omc_qty_available = fields.Float(string="Qty Available", compute="_compute_omc_qty_available")

    def omc_action_open_quants(self):
        sale_order_lines = self.env['sale.order.line'].search([
            ('product_id', '=', self.id), ('state', '=', 'sale')
        ])
        if sale_order_lines:
            sale_order = sale_order_lines.mapped('order_id')
        action = self.env.ref(
            'sale.action_orders').read()[0]
        action["context"] = {"create": False}
        if len(sale_order) > 1:
            action['domain'] = [('id', 'in', sale_order.ids)]
        elif len(sale_order) == 1:
            form_view = [(self.env.ref('sale.view_order_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [
                    (state, view)
                    for state, view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = sale_order.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
