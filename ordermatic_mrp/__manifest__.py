#! -*- encoding: utf-8 -*-
{
    'name': 'Ordermatic - changes to MRP',
    'version': '1.0',
    'license': 'OPL-1',
    'category': 'Extra Tools',
    'summary': 'Changes to MRP',
    'description': """
- adds a connection between work orders and shipments
#- adds a connection between purchase order lines and MO
- allows to set a 'Default finished goods location' in a product
    """,
    'author': 'Wibtec',
    'website': 'http://www.wibtec.com',
    'depends': ['purchase_mrp','sale_purchase','sale_mrp'],
    'data': [
            'views/mrp_view.xml',
            'views/product_view.xml',
            #'views/purchase_view.xml',
            ],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
