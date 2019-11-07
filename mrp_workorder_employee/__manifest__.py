#! -*- encoding: utf-8 -*-
{
    'name': 'Work order responsible',
    'version': '1.0',
    'license': 'OPL-1',
    'category': 'Extra Tools',
    'summary': 'Assign an employee as responsible for a work order',
    'description': """

- Adds a field to the work order
- Adds a kanban view

    """,
    'author': 'Wibtec',
    'website': 'http://www.wibtec.com',
    'depends': ['mrp', 'hr'],
    'data': [
            'views/mrp_workorder_view.xml',
            ],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
