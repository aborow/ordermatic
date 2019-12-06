# -*- coding: utf-8 -*-
# Part of AktivSoftware See LICENSE file for full
# copyright and licensing details.
{
    'name': "Wibtec Manufacturing",

    'summary': """
        	This Module is used to add custom changes on MRP. """,

    'description': """
        OMC-117 = Work order kanban card colors
        OMC-197 = Add Default Finished Good location to the Routing
    """,
    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'category': 'Manufacturing',
    'version': '12.0.1.0.4',
    # any module necessary for this one to work correctly
    'depends': [
                'mrp',
                #'mrp_workorder'
                ],
    # always loaded
    'data': [
        'views/mrp_workorder_view.xml',
        'views/mrp_routing_view.xml'
    ],
    'auto_install': False,
    'installable': True,
    'application': False
    # only loaded in demonstration mode
}
