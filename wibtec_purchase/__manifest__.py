# -*- coding: utf-8 -*-
# Part of AktivSoftware See LICENSE file for full
# copyright and licensing details.
{
    'name': "Wibtec Purchase",

    'summary': """This Module is used to add column in purchase order report. """,

    'description': """
        OMC-228 = "Add Vendor Product Code to Purchase Order Printout"
    """,
    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'category': 'Sales',
    'version': '12.0.1.0.0',
    # any module necessary for this one to work correctly
    'depends': ['purchase'],
    # always loaded
    'data': [
        'views/purchase_order_report_view.xml',
        'views/purchase_order_view.xml'
    ],
    'auto_install': False,
    'installable': True,
    'application': False
    # only loaded in demonstration mode
}