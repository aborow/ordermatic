# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class ResPartner(models.Model):

	_inherit = "res.partner"

	warranty_information = fields.One2many('warranty.information','partner_id','Warranty Information')