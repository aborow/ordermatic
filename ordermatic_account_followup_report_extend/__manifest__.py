# -*- coding: utf-8 -*-
# Part of AktivSoftware See LICENSE file for full
# copyright and licensing details.
{
    'name': "OrderMatic Account Followup Report",

    'summary': """This Module is used to change the customer statement report. """,

    'description': """
        OMC-235 = "Customer Statement Change"
    """,
    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'category': 'Accounts',
    'version': '12.0.1.0.2',
    # any module necessary for this one to work correctly
    'depends': ['account_reports'],
    # always loaded
    'data': [
       'views/account_followup_report.xml'
    ],
    'auto_install': False,
    'installable': True,
    'application': False
    # only loaded in demonstration mode
}