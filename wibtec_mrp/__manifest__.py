# -*- coding: utf-8 -*-
# Part of AktivSoftware See LICENSE file for full
# copyright and licensing details.
{
    'name': "Wibtec Manufacturing",

    'summary': """
        	This Module is used to add custom changes on MRP. """,

    'description': """
        OMC-117 = Work order kanban card colors
    """,
    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'category': 'Manufacturing',
    'version': '12.0.1.0.3',
    # any module necessary for this one to work correctly
    'depends': [
                'mrp',
                #'mrp_workorder'
                ],
    # always loaded
    'data': [
        'views/mrp_workorder_view.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False
    # only loaded in demonstration mode
}
