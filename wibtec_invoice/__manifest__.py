# -*- coding: utf-8 -*-
# Part of AktivSoftware See LICENSE file for full
# copyright and licensing details.
{
    'name': "Wibtec Invoice",

    'summary': """
        	This Module is used to add format of invoice into qweb report of invoice.""",

    'description': """
        OMC-114 = Update Invoice look and feel
        OMC-133 = Default Sales Tax Payable
    """,
    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'category': 'Invoice',
    'version': '12.0.1.0.3',
    # any module necessary for this one to work correctly
    'depends': ['account'],
    # always loaded
    'data': [
        'views/report_account_invoice_template.xml',
        'views/reports_views.xml'
    ],
    'auto_install': False,
    'installable': True,
    'application': False
    # only loaded in demonstration mode
}