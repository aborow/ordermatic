# -*- coding: utf-8 -*-

# from datetime import datetime

from odoo import fields, models


class ResPartner(models.Model):
	
    _inherit = "res.partner"

    is_address_validate = fields.Boolean('Is Address Validate?',default=False)