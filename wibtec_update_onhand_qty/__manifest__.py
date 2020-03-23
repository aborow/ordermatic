# -*- coding: utf-8 -*-
{
    'name': "Wibtec Update Quantity OnHand",

    'summary': """
        This module will update quantity on hand based on sheet which format you can see below.""",

    'description': """
        OMC-79 Update Onhand Quantity based on sheet.
        OMC-192 Need to Change locations of products in Parallel
    """,
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'category': 'product',
    'version': '12.0.1.1.0',

    # any module necessary for this one to work correctly
    'depends': ['product','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'wizard/update_qty_onhand_view.xml',
        'wizard/update_locations_view.xml'
    ],
    'auto_install': False,
    'installable': True,
    'application': False
}