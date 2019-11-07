#! -*- encoding: utf-8 -*-
{
    'name': 'Ordermatic - changes to permissions on tags',
    'version': '1.0',
    'license': 'OPL-1',
    'category': 'Extra Tools',
    'summary': 'Changes to permissions on tags',
    'description': """

- creates a group to create partner tags
- remmoves create/edit/delete permissions from existing groups

    """,
    'author': 'Wibtec',
    'website': 'http://www.wibtec.com',
    'depends': [
                'contacts',
                'sale',
                'crm',
                'helpdesk',
                ],
    'data': [
            'security/security.xml',
            ],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
