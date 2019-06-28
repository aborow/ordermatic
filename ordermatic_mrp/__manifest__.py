#! -*- encoding: utf-8 -*-
{
    'name': 'Ordermatic - changes to MRP',
    'version': '1.0',
    'license': 'OPL-1',
    'category': 'Extra Tools',
    'summary': 'Changes to MRP',
    'description': """

- adds a connection between work orders and shipments

    """,
    'author': 'Wibtec',
    'website': 'http://www.wibtec.com',
    'depends': ['mrp'],
    'data': [
            'views/mrp_view.xml',
            ],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
