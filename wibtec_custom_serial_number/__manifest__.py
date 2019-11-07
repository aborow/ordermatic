# -*- coding: utf-8 -*-
# Part of AktivSoftware See LICENSE file for full
# copyright and licensing details.
{
    'name': "Custom Serial Number",

    'summary': """
        This Module is used to search warranty information of the product from the serial number itself.""",

    'description': """
        OMC-90 = Create custom Serial Number Module && imports the warranty information.
    """,
    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'category': 'product',
<<<<<<< HEAD
    'version': '12.0.1.0.1',
=======
    'version': '12.0.1.0.2',
>>>>>>> fdf4abbe422768f00683639b78680c02b8dd441a
    # any module necessary for this one to work correctly
    'depends': ['product','sale','stock','contacts'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/warranty_information_view.xml',
        'views/res_partner_view.xml',
        'wizard/import_warranty_information_view.xml'
    ],
    'auto_install': False,
    'installable': True,
    'application': False
    # only loaded in demonstration mode
}