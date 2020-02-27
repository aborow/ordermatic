# -*- coding: utf-8 -*-
# Part of AktivSoftware See LICENSE file for full
# copyright and licensing details.
{
    'name': "Wibtec Invoice",

    'summary': """
        	This Module is used to add format of invoice into qweb report of invoice added. """,

    'description': """
        OMC-114 = Update Invoice look and feel
        OMC-133 = Default Sales Tax Payable
        OMC-134 = Check Format Customizations
        OMC-166 = Print Check As
        OMC-167 = Pay to the order of address field change
        OMC-239 = Tax Account defaults
        OMC-243 = Notes for Invoices
        OMC-244 = Update Customer Reference Field
    """,
    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'category': 'Invoice',
    'version': '12.0.1.0.8',
    # any module necessary for this one to work correctly
    'depends': ['account','l10n_us_check_printing', 'sale_management'],
    # always loaded
    'data': [   
        'views/res_partner_view.xml',
        'views/account_invoice_view.xml',
        'views/report_check_bottom_view.xml',
        'views/report_account_invoice_template.xml',
        'views/reports_views.xml',
        'views/sale_order_view.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False
    # only loaded in demonstration mode
}
