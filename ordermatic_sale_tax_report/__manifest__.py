# -*- coding: utf-8 -*-
# Part of AktivSoftware See LICENSE file for full
# copyright and licensing details.
{
    'name': "Sales Tax Report",

    'summary': """
        	This Module is used to export the record of invoices into the proper format. """,

    'description': """
        OMC-268 : Tax Cloud issue with API
        OMC-272 = Create Sales Tax Report
    """,
    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'category': 'Sales',
    'version': '12.0.1.2.1',
    # any module necessary for this one to work correctly
    'depends': ['base'],
    # always loaded
    'data': [
        'wizard/taxable_sales_upload_report_view.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False
    # only loaded in demonstration mode
}