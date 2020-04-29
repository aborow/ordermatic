# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, _

class SaleSubscription(models.Model):

	_inherit = "sale.subscription"

	internal_reference = fields.Char('Internal Reference',related='partner_id.ref')