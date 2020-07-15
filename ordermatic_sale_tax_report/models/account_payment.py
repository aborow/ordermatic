# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _	

class AccountInvoiceLine(models.Model):

	_inherit = "account.invoice.line"

	index_no = fields.Integer('Index',default=0)