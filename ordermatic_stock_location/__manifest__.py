# -*- coding: utf-8 -*-
{
    'name': "Ordermatic - stock by location",
    'summary': "Allow members from a group to consult stock by location",
    'description': "OMC-188 : Allow members from a group to consult stock by location",
    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'category': 'Inventory',
    'version': '12.0.1.0.1',
    'depends': ['stock'],
    'data': [
            'data/res_groups_data.xml',
            'views/stock_view.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False
}
