# -*- coding: utf-8 -*-
# Part of AktivSoftware See LICENSE file for full
# copyright and licensing details.
{
    'name': "Tax Exempt Solution for Customers",

    'summary': """
        	This Module is used to add Tax Exempt Solution for Customers. """,

    'description': """
        OMC-141 = Accounting: Tax Exempt Solution for Customers
        OMC-271 = Sales Tax exemption for Credit Notes
        OMC-268 = Tax Cloud issue with API
    """,
    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'category': 'Contacts',
    'version': '12.0.1.2.0',
    # any module necessary for this one to work correctly
    'depends': ['base','sale','sale_account_taxcloud','account_taxcloud'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/taxable_sales_upload_report_view.xml',
        'views/res_partner_view.xml'
    ],
    'auto_install': False,
    'installable': True,
    'application': False
    # only loaded in demonstration mode
}