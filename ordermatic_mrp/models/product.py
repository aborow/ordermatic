#! -*- encoding: utf-8 -*-
from odoo import models, fields, api, _

class Product(models.Model):
    _inherit = 'product.product'

    location_dest_id = fields.Many2one(
                                        'stock.location',
                                        'Finished Products Location',
                                        help='Default finished goods location'
                                        )
