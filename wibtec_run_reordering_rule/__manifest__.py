# -*- coding: utf-8 -*-
{
    'name': "Run Re-ordering Rule",

    'summary': """
        OMC-200 : Seperate Reorder rule execution from Scheduler (issue with reserving parts of non planned MOs.""",
    'description': """
    """,
    'category': 'Stock',
    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'version': '12.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['stock'],

    # always loaded
    'data': [
        'security/access_scheduler_security.xml',
        'view/procurement_orderpoint_compute_views.xml',
    ],

}
