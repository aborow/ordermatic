# -*- coding: utf-8 -*-
{
    'name': 'Avalara Extend',
    'category': 'Sale',
    'author': "WIB Technologies, Inc",
    'website': "http://www.wibtec.com",
    'version': '12.0.1.0.1',
    'summary': "Miscelaneous changes to products and customer related to avalara",
    'description': """OMC-276 : Integrate Avalara""",
    'depends': ['wibtec_avatax_connector','base'],
    'data': [
        "wizard/update_product_customer_tax.xml",
        #"wizard/validate_customer_address.xml",
       
    ],
    # 'images': [
    #     'static/description/icon.png',
    # ],
}
