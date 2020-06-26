# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT,DEFAULT_SERVER_DATE_FORMAT
from odoo.exceptions import UserError
from odoo.addons.wibtec_avatax_connector.models.avalara_api import AvaTaxService, BaseAddress
import logging, tempfile

class AccountTax(models.Model):

    """Inherit to implement the tax using avatax API"""

    _inherit = "account.tax"
    
    is_avatax = fields.Boolean('Is Avatax')

    @api.model
    def _get_compute_tax(self, avatax_config, doc_date, doc_code, doc_type, partner, ship_from_address, shipping_address,
                          lines, user=None, exemption_number=None, exemption_code_name=None, commit=False, invoice_date=False, reference_code=False, location_code=False, context=None):
        currency_code = self.env.user.company_id.currency_id.name
        if not partner.customer_code:
            if not avatax_config.auto_generate_customer_code:
                raise UserError(_('Customer Code for customer %s not defined.\n\n  You can edit the Customer Code in customer profile. You can fix by clicking "Generate Customer Code" button in the customer contact information"'% (partner.name)))
            else:
                partner.generate_cust_code() 
                        
        if not shipping_address:
            raise UserError(_('There is no shipping address defined for the partner.'))        
        
        if not ship_from_address:
            raise UserError(_('There is no company address defined.'))

        #this condition is required, in case user select force address validation on AvaTax API Configuration
        if not avatax_config.address_validation:
            if avatax_config.force_address_validation:
                if not shipping_address.date_validation:
                    raise UserError(_('Please validate the shipping address for the partner %s.'
                                % (partner.name)))

            if not ship_from_address.date_validation:
                raise UserError(_('Please validate the company address.'))

        #For check credential
        avalara_obj = AvaTaxService(avatax_config.account_number, avatax_config.license_key,
                                 avatax_config.service_url, avatax_config.request_timeout, avatax_config.logging)
        avalara_obj.create_tax_service()
        addSvc = avalara_obj.create_address_service().addressSvc
        origin = BaseAddress(addSvc, ship_from_address.street or None,
                             ship_from_address.street2 or None,
                             ship_from_address.city, ship_from_address.zip,
                             ship_from_address.state_id and ship_from_address.state_id.code or None,
                             ship_from_address.country_id and ship_from_address.country_id.code or None, 0).data
        destination = BaseAddress(addSvc, shipping_address.street or None,
                                  shipping_address.street2 or None,
                                  shipping_address.city, shipping_address.zip,
                                  shipping_address.state_id and shipping_address.state_id.code or None,
                                  shipping_address.country_id and shipping_address.country_id.code or None, 1).data
        
        invoice_date = str(invoice_date).split(' ')[0] if invoice_date else False
        partner_ref = self.partner_name(partner)
        # partner_ref = partner.ref if partner.ref else partner.name
        result = avalara_obj.get_tax(avatax_config.company_code, doc_date, doc_type,
                                 partner_ref, doc_code, origin, destination,
                                 lines, exemption_number,
                                 exemption_code_name,
                                 user and user.name or None, commit, invoice_date, reference_code, location_code, currency_code, partner.vat_id or None)
        
        return result

    @api.model
    def cancel_tax(self, avatax_config, doc_code, doc_type, cancel_code):
         """Sometimes we have not need to tax calculation, then method is used to cancel taxation"""
         avalara_obj = AvaTaxService(avatax_config.account_number, avatax_config.license_key,
                                  avatax_config.service_url, avatax_config.request_timeout,
                                  avatax_config.logging)
         avalara_obj.create_tax_service()
         try:
             result = avalara_obj.get_tax_history(avatax_config.company_code, doc_code, doc_type)
         except:
             return True
        
         result = avalara_obj.cancel_tax(avatax_config.company_code, doc_code, doc_type, cancel_code)
         return result

    @api.model
    def partner_name(self,partner_id):
        if partner_id.ref:
            return partner_id.ref
        else:
            if partner_id.parent_id:
                partner_name = str(partner_id.parent_id.name)+ ' ' + str(partner_id.name)
                partner = partner_name.replace(',', '')
                return partner
            else:
                partner = str(partner_id.name).replace(',', '')
                return partner

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: