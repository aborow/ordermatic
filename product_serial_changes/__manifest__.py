#! -*- encoding: utf-8 -*-
{
    'name': 'Serial number changes',
    'version': '1.0',
    'license': 'OPL-1',
    'category': 'Extra Tools',
    'summary': 'Changes to serial numbers',
    'description': """

- In the lot/serials list, adds the column quantity

- Allows for a purchased product to also get serials from the serial sequence (adds a button)

- On producing a product, the lot/serial number dropdown will not allow create/edit (just read)

- On producing a product, the subcomponents serial number dropdown will not allow create/edit (just read)

- No selection of Serial Number while producing. The serial will be crated automatically on starting production.

    """,
    'author': 'Wibtec',
    'website': 'http://www.wibtec.com',
    'depends': ['purchase_stock'],
    'data': [
            'views/stock_production_lot_view.xml',
            'views/stock_move_view.xml',
            'views/mrp_view.xml',
            ],
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
