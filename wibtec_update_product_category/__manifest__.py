# -*- coding: utf-8 -*-
# Part of AktivSoftware See LICENSE file for full
# copyright and licensing details.
{
    'name': "Product Update Category",

    'summary': """
        This Module is use for change product category base on list of given csv file.""",

    'description': """
        OMC-80 = Product Update Category
    	OMC-82 = Product UOM Update
    	OMC-84 = Remove Customer Tax from Product
        OMC-96 = Please updates all products that are Make to Order to also have Manufacture route
        OMC-88 = Update UOMs
        OMC-104 = Remove MTO from all products
        OMC-107 = Buy parts are not reflected in Odoo properly
        OMC-105 = Set default Tax rates on products
        OMC-120 = add Long Description Field to Products
        OMC-121 = Make VENDOR Tax default to Tax Exempt
        OMC-173 = Update COST price from SYSPRO's inventory valuation report
        OMC-175 = Duplicate products in parallel1 DB
    """,

    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'category': 'product',
    'version': '12.0.1.11.2',

    # any module necessary for this one to work correctly
    'depends': ['product','sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/product_update_category_view.xml',
    ],

    'auto_install': False,
    'installable': True,
    'application': False
    # only loaded in demonstration mode
}