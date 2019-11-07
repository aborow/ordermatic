# -*- coding: utf-8 -*-
# Part of AktivSoftware See LICENSE file for full
# copyright and licensing details.
{
    'name': "Custom Import BOM",

    'summary': """
        This Module is used to import BOMs. """,

    'description': """
        OMC-64 = BOM Custom Import
    """,
    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'category': 'product',
    'version': '12.0.1.0.0',
    # any module necessary for this one to work correctly
    'depends': ['mrp'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/import_bom_views.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False
    # only loaded in demonstration mode
}