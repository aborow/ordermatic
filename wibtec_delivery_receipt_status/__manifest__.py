# -*- coding: utf-8 -*-
# Part of AktivSoftware See LICENSE file for full
# copyright and licensing details.
{
    'name': "Wibtec Delivery/Receipt Status",

    'summary': """This Module is used to update the delivery and receipt status for SO and PO.""",

    'description': """
        OMC-213:New Delivery Status Flag in Sales Orders and Receipt Status Flag in Purchase Orders
    """,
    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'category': 'Inventory',
    'version': '12.0.1.0.0',
    # any module necessary for this one to work correctly
    'depends': ['sale','purchase'],
    # always loaded
    'data': [
        'wizard/update_delivery_status_view.xml',
        'views/sale_order_view.xml',
        'views/purchase_order_view.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False
    # only loaded in demonstration mode
}