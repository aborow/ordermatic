# -*- coding: utf-8 -*-
{
    'name': "Wibtec Stock",
    'summary': """
            This Module is used to create reordering rule for all the products. """,

    'description': """
        OMC-115 : Add location as a Group BY option on the Inventory Valuation report.
	OMC-118 : update delivery slip and packing slip
    """,
    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'category': 'Stock',
    'version': '12.0.1.0.2',
    # any module necessary for this one to work correctly
    'depends': ['stock','stock_account'],
    # always loaded
    'data': [
        # 'views/stock_quant_view.xml',
        'views/report_delivery_slip_template.xml',
        'views/report_packing_slip_template.xml',
        'views/reports_views.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False
    # only loaded in demonstration mode
}
