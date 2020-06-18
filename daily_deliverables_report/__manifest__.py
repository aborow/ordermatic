# -*- coding: utf-8 -*-
{
    'name': "Wibtec Daily Deliverables Report",
    'summary': """
            This Module is used to print report in excel report with all data of sale orders""",
    'description': """
        OMC-159 : Custom Sales Report
        OMC-257 : Update Daily Delivery Report
        OMC-259 : Daily Deliverable Report Error
    """,
    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'category': 'Stock',
    'version': '12.0.1.0.8',
    # any module necessary for this one to work correctly
    'depends': ['sale'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/daily_deliverables_report_view.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False
    # only loaded in demonstration mode
}