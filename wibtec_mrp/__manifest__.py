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
        OMC-169 = Update BOM view to show 150 records instead of 40 records
        OMC-198 = Material Availability Change
    """,
    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'category': 'Manufacturing',
    'version': '12.0.1.0.6',
    # any module necessary for this one to work correctly
    'depends': [
                'mrp',
                ],
    # always loaded
    'data': [
        'views/mrp_workorder_view.xml',
        'views/mrp_routing_view.xml',
        'views/mrp_bom_view.xml',
        'views/mrp_production_view.xml'
    ],
    'auto_install': False,
    'installable': True,
    'application': False
    # only loaded in demonstration mode
}