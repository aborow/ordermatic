# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _
import base64
import csv
# from io import StringIO
from odoo.exceptions import Warning as UserError

class ValidateCustomerAddress(models.TransientModel):
    _name = "validate.customer.address.wizard"

    name = fields.Char('Name')
    is_failed = fields.Boolean('Is Fail Validate')
    start = fields.Integer('Start Range')
    end = fields.Integer('End Range')
    customer_name = fields.Text('Customer Name')
    last_partner_id = fields.Char('Last partner')

    @api.multi
    def action_customer_validate(self):
        print ("\n action_customer_validate============================")
        domain=[('customer','=', True),('is_address_validate','=',False)]
        print ("\n domain======================",domain)
        partner_recs = self.env['res.partner'].search(domain,limit=200,order='id asc')
        print ("\n partner_recs=====================",partner_recs)
        if partner_recs:
            for partner in partner_recs:
                name =''
                print ("\n partner==================",partner)
                demo = partner.script_varify_address_validatation()
                self.last_partner_id=partner.id
                if demo == 'Failed':
                    self.is_failed = True
                    if partner.name:
                        name = partner.name
                    else:
                        name = str(partner.id)
                    if self.customer_name:
                        self.customer_name = self.customer_name + ' , ' + name
                    else:
                        self.customer_name = str(partner.name)
                partner.is_address_validate = True

            result = {
                        "type": "ir.actions.act_window",
                        'view_type': 'form',
                        'view_mode': 'form',
                        'res_model': 'validate.customer.address.wizard',
                        'views': [(False, 'form')],
                        "res_id": self.id,
                        "target": 'new'
                    }
            return result
        else:
            raise UserError(_('No data to process.'))


