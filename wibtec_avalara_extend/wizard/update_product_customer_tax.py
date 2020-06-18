# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models


class UpdateProductCustomerTax(models.TransientModel):
    _name = "update.product.customer.tax.wizard"

    replace_account_tax_id = fields.Many2one(
        'account.tax', 'Replace Tax With', required=True)

    @api.multi
    def action_update_product_customer_tax(self):
        if self.replace_account_tax_id:
            product_ids = self.env['product.template'].search([('active','=',True),('sale_ok','=',True)])
            [product.write({'taxes_id': [(6, 0, [self.replace_account_tax_id.id])]}) for product in product_ids]