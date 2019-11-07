# -*- coding: utf-8 -*-
# Part of AktivSoftware See LICENSE file for full
# copyright and licensing details.
{
    'name': "Wibtec Sales",

    'summary': """
<<<<<<< HEAD
        	This Module is used to add dates in sale order from. """,
=======
        	This Module is used to add dates in sale order from.  """,
>>>>>>> fdf4abbe422768f00683639b78680c02b8dd441a

    'description': """
        OMC-33 = "New fields for Sales Order Form"
        OMC-126 = "Add new field "Order Contact"
        OMC-135 = "Remove Create / Edit product from Sales Order line popup."
        OMC-136 = "Quote and Sales Order Forms (Delivery Dates)"
        OMC-151 = "Add OMC Project Delivery Date and OMC Actual Delivery Date to Sales Analysis Report"
        OMC-152 = "Move Fields on Quote / Sales Order Form"
        OMC-144 = "Sales & MFG: Update OMC Actual Delivery Date with Delivery Order DONE date"
<<<<<<< HEAD
=======

        OMC-161 = Delivery scheduled date comes from SO 'OMC Projected Delivery Date' (once the SO is confirmed)
>>>>>>> fdf4abbe422768f00683639b78680c02b8dd441a
    """,
    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'category': 'Sales',
    'version': '12.0.1.0.9',
    # any module necessary for this one to work correctly
<<<<<<< HEAD
    'depends': ['sale','delivery','sale_enterprise'],
=======
    'depends': ['sale','delivery','sale_enterprise','sale_stock'],
>>>>>>> fdf4abbe422768f00683639b78680c02b8dd441a
    # always loaded
    'data': [
        'views/sale_order_view.xml',
        'views/report_sale_order.xml',
        'views/product_template_view.xml'
    ],
    'auto_install': False,
    'installable': True,
    'application': False
    # only loaded in demonstration mode
}
