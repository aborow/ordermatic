# -*- coding: utf-8 -*-
# Part of AktivSoftware See LICENSE file for full
# copyright and licensing details.
{
    'name': "Update Inventory Details",

    'summary': """
        This Module is used to update Inventory Details. """,

    'description': """
        OMC-79 = Update Inventory Details
    """,
    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'category': 'Stock',
    'version': '12.0.1.1.0',
    # any module necessary for this one to work correctly
    'depends': ['stock'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/update_stock_inventory_line_view.xml',
        'views/stock_inventory_view.xml'
    ],
    'auto_install': False,
    'installable': True,
    'application': False
    # only loaded in demonstration mode
}