# -*- coding: utf-8 -*-
# Part of AktivSoftware See LICENSE file for full
# copyright and licensing details.
{
    'name': "Product Cost Report",

    'summary': """
        	This Module is used to export the record of products with the bom cost and product cost. """,

    'description': """
        OMC-298 : Product Cost Report
    """,
    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'category': 'Sales',
    'version': '12.0.1.0.0',
    # any module necessary for this one to work correctly
    'depends': ['base','sale'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/product_cost_report_view.xml'
        # 'wizard/product_cost_report_view.xml',
        # 'views/account_payment_view.xml'
    ],
    'auto_install': False,
    'installable': True,
    'application': False
    # only loaded in demonstration mode
}