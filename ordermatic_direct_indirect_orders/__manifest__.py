# -*- coding: utf-8 -*-
# Part of AktivSoftware See LICENSE file for full
# copyright and licensing details.
{
    'name': "Ordermatic - Direct Indirect Orders",

    'summary': """
        This Module is use for adding the direct and indirect orders to the manufacturing oder's form view.""",

    'description': """
        OMC-254 = Manufacturing Report (Direct and Indirect MOs)
    """,

    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'category': 'Manufacturing',
    'version': '12.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['mrp','purchase'],

    # always loaded
    'data': [
        'views/mrp_production_view.xml',
    ],

    'auto_install': False,
    'installable': True,
    'application': False
    # only loaded in demonstration mode
}