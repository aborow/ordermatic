# -*- coding: utf-8 -*-
# Part of AktivSoftware See LICENSE file for full
# copyright and licensing details.
{
    'name': "Wibtec Sales",

    'summary': """
        	This Module is used to add dates in sale order from. """,

    'description': """
        OMC-64 = BOM Custom Import
    """,
    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'category': 'Sales',
    'version': '12.0.1.0.2',
    # any module necessary for this one to work correctly
    'depends': ['sale','delivery'],
    # always loaded
    'data': [
        'views/sale_order_view.xml',
        'views/product_template_view.xml'
    ],
    'auto_install': False,
    'installable': True,
    'application': False
    # only loaded in demonstration mode
}
