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
        OMC-237 = Create an Expand ALL button in BOM > Structure and Cost screen
        OMC-269 = Update Work Order with correct Time
        OMC-205 = Insllation MRP II automatic(this issue was known whilw woking on OMC-245)
        OMC-297 = Production Scheduling Issue
    """,
    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'category': 'Manufacturing',
    'version': '12.0.1.0.12',
    # any module necessary for this one to work correctly
    'depends': [
                'mrp','sale'
                ],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/mrp_workorder_view.xml',
        'views/mrp_routing_view.xml',
        'views/mrp_bom_view.xml',
        'views/mrp_production_view.xml'
    ],
    'qweb': ['static/src/xml/mrp.xml'],
    'auto_install': False,
    'installable': True,
    'application': False
    # only loaded in demonstration mode
}