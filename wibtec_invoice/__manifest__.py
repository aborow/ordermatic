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
        OMC-261 = Invoice is cutting off the name of the company
        OMC-246 = Add Tracking Numbers to invoices
        OMC-264 = Grammar Error (Quick Change to Production Please)
        OMC-266 = Add Amount Due to Invoice Print Out
        OMC-275 = Tracking Number Issue while accesing Invoices
        OMC-245 = Setup Terms and Conditions for both Sales Orders and Invoices
        OMC-267 = Header is overlapping Terms and Conditions section
        OMC-283 = Bug - Batch Payments
    """,
    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'category': 'Invoice',
    'version': '12.0.1.0.21',
    # any module necessary for this one to work correctly
    'depends': ['account','l10n_us_check_printing', 'sale_management','sale'],
    # always loaded
    'data': [   
        'views/res_partner_view.xml',
        'views/account_invoice_view.xml',
        'views/report_check_bottom_view.xml',
        'views/report_account_invoice_template.xml',
        'views/reports_views.xml',
        'views/sale_order_view.xml',
        'views/res_config_settings_view.xml'
    ],
    'auto_install': False,
    'installable': True,
    'application': False
    # only loaded in demonstration mode
}
