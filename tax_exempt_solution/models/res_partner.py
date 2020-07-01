# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class ResPartner(models.Model):

	_inherit = "res.partner"

	is_tax_exempt = fields.Boolean('Is Tax Exempt')
	exemption_number = fields.Char('Exemption Number')
	exemption_code_id = fields.Many2one('exemption.code',string="Exemption Code")
	tax_exempt_certificate = fields.Binary('Tax Exempt Certificate')