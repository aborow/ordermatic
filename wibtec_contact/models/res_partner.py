# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class ResPartner(models.Model):

	_inherit = "res.partner"

	opt_out = fields.Boolean(string='Opt Out')
	is_w9_file = fields.Boolean(string="W9 on file?")
