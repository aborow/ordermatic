# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class StockLocation(models.Model):

	_inherit = "stock.location"

	location_name = fields.Char("Location Name",related='display_name',store=True)