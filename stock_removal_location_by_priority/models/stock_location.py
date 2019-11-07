# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models , api , _
from odoo.exceptions import UserError


class StockLocation(models.Model):
    _inherit = 'stock.location'

    removal_priority = fields.Integer(help="This priority applies when "
                                           "removing stock and incoming dates "
                                           "are equal.",
                                      string="SO Priority", default=10)
