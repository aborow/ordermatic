# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    note_of_invoice = fields.Text("Notes for Invoice")

    @api.multi
    def _prepare_invoice(self):
        result = super(SaleOrder, self)._prepare_invoice()
        if self.note_of_invoice:
            result.update({'note_of_invoice': self.note_of_invoice})
        return result
