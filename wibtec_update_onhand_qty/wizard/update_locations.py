# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import Warning,ValidationError
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)
import io
try:
    import csv
except ImportError:
    _logger.debug('Cannot `import csv`.')
try:
    import StringIO
except ImportError:
    _logger.debug('Cannot `import StringIO`.')
try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')


class UpdateLocations(models.TransientModel):

    _name = 'update.locations'

    file = fields.Binary('Upload File')

    @api.multi
    @api.constrains('file')
    def _check_file(self):
        # Constrains for file if file is not uploaded 
        if not self.file:
            raise ValidationError(_('Please upload CSV formatted file.'))

    @api.multi
    def update_locations(self):
        # Method is used to fetch all data from selected csv file
        if not self.file:
            raise Warning(_('Please Select CSV File.'))
        else:
            keys = ['Locations','Product']
            data = base64.b64decode(self.file)
            file_input = io.StringIO(data.decode("utf-8"))
            file_input.seek(0)
            reader_info = []
            reader = csv.reader(file_input, delimiter=',')
            try:
                reader_info.extend(reader)
            except Exception:
                raise exceptions.Warning(_("Not a valid file!"))
            values = {}
            for i in range(len(reader_info)):
                field = map(str, reader_info[i])
                values = dict(zip(keys, field))
                if values:
                    if values['Locations'] == 'Locations':
                        continue
                    res=self.update_locations_with_correct_location(values)
                    _logger.info("res:::::::::::::::::::::::::::::: %s" % res)
            return res

    @api.multi
    def update_locations_with_correct_location(self,values):
        # Update locations
        product_id = self.find_product(values.get('Product'))
        location_id = self.find_location(values.get('Locations'))
        self.find_and_update_stock_moves(product_id,location_id)

    @api.multi
    def find_and_update_stock_moves(self,product,location_id):
        location_name = 'Virtual Locations/Inventory adjustment'
        from_location_id = self.find_location(location_name)
        product_move = self.env['stock.move.line'].search([('product_id','=',product.id),('location_id','=',from_location_id.id),('state','=','done')],limit=1)
        product_move.write({'location_dest_id':location_id.id})
        product_move.move_id.write({'location_dest_id':location_id.id})

    @api.multi
    def update_stock_quant(self,product_move):
        domain = [
            ('product_id', '=', product_move.product_id.id),
            ('location_id', '=', product_move.location_id.id),
            ('lot_id', '=', self.lot_id.id),
            '|',
                ('package_id', '=', self.package_id.id),
                ('result_package_id', '=', self.package_id.id),
        ]
        stock_quant = self.env['stock.quant'].search(domain,limit=1)


    @api.multi
    def find_location(self,location):
        # Method will find location if location will found then it will return location else it will return warning
        location_id = self.env['stock.location'].search([('location_name','=',location)],limit=1)
        if location_id:
            return location_id
        else:
            raise Warning(_('Location %s is not Found in System.') % location)

    @api.multi
    def find_product(self,product):
        # Method will find product from product product if product will found then it will return product else it will return warning
        product_id = self.env['product.product'].search([('default_code','=',product)],limit=1)
        if product_id:
            return product_id
        else:
            raise Warning(_('Product %s is not Available in System.') % product)