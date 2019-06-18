#! -*- encoding: utf-8 -*-
import logging

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

class StockMove(models.Model):
    _inherit = 'stock.move'

    product_active = fields.Boolean('Active product', related='product_id.active')

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    product_active = fields.Boolean('Active product', related='product_id.active')
