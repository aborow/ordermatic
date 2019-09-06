# -*- coding: utf-8 -*-
{
    'name': "Wibtec Helpdesk",

    'summary': """
        This module will help to add customizations in helpdesk.""",

    'description': """
        OMC-92 = Add Due Date to Helpdesk tickets
    """,

    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'category': 'Sales',
    'version': '12.0.1.0.0',
    # any module necessary for this one to work correctly
    'depends': ['helpdesk'],
    # always loaded
    'data': [
        'views/helpdesk_ticket_views.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False
}