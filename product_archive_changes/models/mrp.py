#! -*- encoding: utf-8 -*-
import logging

from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)

class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    @api.multi
    def write(self, vals):
        res = super(MrpBom, self.sudo()).write(vals)
        if vals.get('active'):
            for s in self:
                _logger.info("UNARCHIVING BoM %s" % s)
                # Unarchiving a BoM should mean unarchiving all its components
                # Archiving a BoM SHOULD NOT mean archiving its components
                for l in s.sudo().bom_line_ids:
                    if not l.product_id.active:
                        _logger.info("UNARCHIVING PRODUCT %s" % l.product_id)
                        l.product_id.active = True
        return res


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    product_active = fields.Boolean('Active product', related='product_id.active')
