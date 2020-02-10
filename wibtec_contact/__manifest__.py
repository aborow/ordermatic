# -*- coding: utf-8 -*-
# Part of AktivSoftware See LICENSE file for full
# copyright and licensing details.
{
    'name': "Wibtec Contacts",

    'summary': """
        	This Module is used to add customization in contacts. """,

    'description': """
        OMC-123 = Internal Notes need to show up on the Company's landing page not under a tab
        OMC-124 = Need to be able to search by Street address and/or City
        OMC-221 = Move internal reference field
    """,
    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'category': 'Contacts',
    'version': '12.0.1.0.2',
    # any module necessary for this one to work correctly
    'depends': ['base'],
    # always loaded
    'data': [
        'views/res_partner_view.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False
    # only loaded in demonstration mode
}
