# -*- coding: utf-8 -*-
# Part of AktivSoftware See LICENSE file for full
# copyright and licensing details.
{
    'name': "Ordermatic Manufacturing Groupby",

    'summary': """
        	This Module is used to add parent product and sequence on MO based on hierarchy. """,

    'description': """
        OMC-143 : Add MO functionality to group by Final Product
    """,
    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'category': 'Manufacturing',
    'version': '12.0.1.0.1',
    # any module necessary for this one to work correctly
    'depends': ['mrp'],
    # always loaded
    'data': [
        'views/mrp_production_view.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False
    # only loaded in demonstration mode
}
