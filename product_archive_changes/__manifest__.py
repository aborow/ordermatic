#! -*- encoding: utf-8 -*-
{
    'name': 'Changes to product archival',
    'version': '1.0',
    'license': 'OPL-1',
    'category': 'Extra Tools',
    'summary': 'Changes to product archival',
    'description': """

- A group is created and only members from this group will be able to archive products
    This is just about showing the 'archive' button and no changes are done to python code

- Members of the NON-archive group will not be able to read archived products
- OMC-351 Getting permission error when trying to pull up sales module

- Unarchive a BoM should unarchive all its components

    """,
    'author': 'Wibtec',
    'website': 'http://www.wibtec.com',
    'depends': ['mrp'],
    'data': [
            'security/groups.xml',
            'security/ir_rule.xml',
            'views/product_view.xml',
            'views/mrp_view.xml',
            ],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
