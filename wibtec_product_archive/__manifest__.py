# -*- coding: utf-8 -*-
# Part of AktivSoftware See LICENSE file for full
# copyright and licensing details.
{
    'name': "Product Archive",

    'summary': """
        This Module is use for change product active status base on list of given csv file. """,

    'description': """
        OMC-63 = Product Archive Script
    """,

    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'category': 'product',
    'version': '12.0.1.3.0',

    # any module necessary for this one to work correctly
    'depends': ['product','mrp'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'wizard/product_archive_view.xml',
    ],

    'auto_install': False,
    'installable': True,
    'application': False
    # only loaded in demonstration mode
}