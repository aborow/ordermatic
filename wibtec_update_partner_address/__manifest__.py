# -*- coding: utf-8 -*-
# Part of AktivSoftware See LICENSE file for full
# copyright and licensing details.
{
    'name': "Update Partner Address",

    'summary': """
        This Module is use to update partner's address. """,

    'description': """
        OMC-75 = Update Partner Address

        Module will update parent partner's address with child partner if child partner exists and parent partner's address is not available.
    """,

    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'category': 'Contacts',
    'version': '12.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['contacts'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/update_partner_address_view.xml',
    ],

    'auto_install': False,
    'installable': True,
    'application': False
    # only loaded in demonstration mode
}