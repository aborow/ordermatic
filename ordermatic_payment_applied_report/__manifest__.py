# -*- coding: utf-8 -*-
# Part of AktivSoftware See LICENSE file for full
# copyright and licensing details.
{
    'name': "Payment Applied Report",

    'summary': """
        	This Module is used to export the record of payment into the proper format. """,

    'description': """
        OMC-282 : Payment Applied Report
    """,
    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'category': 'Sales',
    'version': '12.0.1.0.1',
    # any module necessary for this one to work correctly
    'depends': ['base','account'],
    # always loaded
    'data': [
        'wizard/payment_applied_report_view.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False
    # only loaded in demonstration mode
}