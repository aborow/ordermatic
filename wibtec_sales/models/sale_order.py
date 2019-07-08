# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class SaleOrder(models.Model):

	_inherit = "sale.order"

	expected_install_date = fields.Date('Expected Install Date')
	actual_install_date = fields.Date('Actual Install Date')