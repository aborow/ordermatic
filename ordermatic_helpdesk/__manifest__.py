#! -*- encoding: utf-8 -*-
{
    'name': 'Ordermatic - changes to helpdesk',
    'version': '1.0',
    'license': 'OPL-1',
    'category': 'Extra Tools',
    'summary': 'Changes to helpdesk',
    'description': """

Helpdesk ticket form view:
- new "vendor_id" field
- new "estimated costs" field

Helpdesk ticket tree view:
- show tag field
- show estimated costs field

    """,
    'author': 'Wibtec',
    'website': 'http://www.wibtec.com',
    'depends': ['helpdesk'],
    'data': [
            'views/helpdesk_view.xml',
            ],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
