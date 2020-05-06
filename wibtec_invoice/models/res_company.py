# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ResCompany(models.Model):

    _inherit = "res.company"

    invoice_note = fields.Text(string='Default Terms and Conditions', translate=True)