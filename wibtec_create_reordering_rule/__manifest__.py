# -*- coding: utf-8 -*-
# Part of AktivSoftware See LICENSE file for full
# copyright and licensing details.
{
    'name': "Wibtec Create Reordering Rule",

    'summary': """
            This Module is used to create reordering rule for all the products. """,

    'description': """
        OMC-111 : Add default reorder rule
    """,
    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'category': 'Sales',
    'version': '12.0.1.0.1',
    # any module necessary for this one to work correctly
    'depends': ['stock'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/create_reordering_rule_view.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False
    # only loaded in demonstration mode
}
