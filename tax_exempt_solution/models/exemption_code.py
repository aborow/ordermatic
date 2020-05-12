# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class ExemptionCode(models.Model):

	_name = "exemption.code"
	_description = "Exemption Code"

	name = fields.Char('Name')