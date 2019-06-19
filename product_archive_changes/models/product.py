#! -*- encoding: utf-8 -*-
import logging
from odoo import models, fields, api, _
_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def write(self, vals):
        res = super(ProductProduct, self.sudo()).write(vals)
        if vals.get('active'):
            for s in self:
                _logger.info("UNARCHIVING PRODUCT %s" % s)
                # If the product is to be created out of a BoM, then, all the
                # products in it should be brought back to life
                for bom in s.sudo().bom_ids:
                    _logger.info("CHECKING BoM %s" % bom)
                    if bom.active:
                        for line in bom.sudo().bom_line_ids:
                            _logger.info("UNARCHIVING PRODUCT %s" % line.product_id)
                            line.product_id.active = True
        return res
