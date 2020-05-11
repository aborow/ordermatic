# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    use_invoice_note = fields.Boolean(string='Default Terms & Conditions',config_parameter='invoice.use_invoice_note')
    invoice_note = fields.Text(related='company_id.invoice_note', string="Terms & Conditions", readonly=False)