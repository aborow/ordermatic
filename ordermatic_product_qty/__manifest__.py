# -*- coding: utf-8 -*-
# Part of AktivSoftware See LICENSE file for full
# copyright and licensing details.
{
    'name': "Qty Available Smart Button",

    'summary': """
        	This Module is used to Show qty a smart button on the product view that shows the quantity available (ON Hand minus RESERVED).
Add the MOs and Sales Orders to a list when clicking on the smart button so it is easy to find those orders that are reserving the product.""",

    'description': """
        OMC-352 : QTY Available Smart button
        
    """,
    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'category': 'Sales',
    'version': '12.0.1.2.4',
    # any module necessary for this one to work correctly
    'depends': ['stock'],
    # always loaded
    'data': [
            # 'views/product_product_views.xml'
    ],
    'auto_install': False,
    'installable': True,
    'application': False
    # only loaded in demonstration mode
}