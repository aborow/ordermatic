#! -*- encoding: utf-8 -*-
import logging
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        group = self.env.ref('product_archive_changes.nok_archive_products')
        if group and group.users and self.env.user.id in group.users.ids:
            domain.append(['active', '=', True])
            return super(ProductProduct, self).search_read(domain, fields, offset, limit, order)
        return super(ProductProduct, self).search_read(domain, fields, offset, limit, order)

    @api.multi
    def write(self, vals):
        _logger.info('product.py')
        res = super(ProductProduct, self.sudo()).write(vals)
        if vals.get('active'):
            for s in self:
                _logger.info("UNARCHIVING PRODUCT %s" % s)
                # If the product is to be created out of a BoM, then, all the
                # products in it should be brought back to life
                # 20190805 - Ordermatic also want to unarchive BoM
                for bom in self.env['mrp.bom'].sudo().search([
                    '|',
                    ('active', '=', True),
                    ('active', '=', False),
                    ('product_tmpl_id', '=', s.product_tmpl_id.id),
                ]):
                    _logger.info("CHECKING BoM %s" % bom)
                    if not bom.active:
                        bom.write({'active': True})
                    for line in bom.sudo().bom_line_ids:
                        if not line.product_id.active:
                            _logger.info("UNARCHIVING PRODUCT %s" % line.product_id)
                            line.product_id.active = True

                """
                for bom in s.sudo().bom_ids:
                    _logger.info("CHECKING BoM %s" % bom)
                    if bom.active:
                        for line in bom.sudo().bom_line_ids:
                            _logger.info("UNARCHIVING PRODUCT %s" % line.product_id)
                            line.product_id.active = True
                """
        return res
