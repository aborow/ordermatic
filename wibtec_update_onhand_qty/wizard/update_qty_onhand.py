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


class UpdateQuantityOnhand(models.TransientModel):

    _name = 'update.quantity.onhand'

    file = fields.Binary('Upload File')

    @api.multi
    @api.constrains('file')
    def _check_file(self):
        # Constrains for file if file is not uploaded 
        if not self.file:
            raise ValidationError(_('Please upload CSV formatted file.'))

    @api.multi
    def update_onhand_qty(self):
        # Method is used to fetch all data from selected csv file
        if not self.file:
            raise Warning(_('Please Select CSV File.'))
        else:
            keys = ['StockCode','Warehouse','OnHand']
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
                    if values['StockCode'] == 'StockCode':
                        continue
                    res=self.create_stock_iventory(values)
                    _logger.info("res:::::::::::::::::::::::::::::: %s" % res)
            return res

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
        product_id = self.env['product.product'].search(['|',('default_code','=',product),('name','=',product)],limit=1)
        if product_id:
            return product_id
        else:
            raise Warning(_('Product %s is not Available in System.') % product)

    @api.multi
    def find_inventory(self,location):
        # Method will find product from inventory if product will found then it will return product else it will return warning 
        location_id = self.find_location(location)
        inventory_id = self.env['stock.inventory'].search([('location_id','=',location_id.id),('filter','=','partial')],limit=1)
        if inventory_id:
            return inventory_id
        else:
            inventory_id = self.env['stock.inventory'].create({
                    'company_id':1,
                    'date': datetime.today(),
                    'filter':'partial',
                    'location_id':location_id.id,
                    'name':location_id.name
                })
            return inventory_id

    @api.multi
    def find_stock_inventory_line(self,inventory_id,product_id,location_id,onhand_qty):
        # Find stock from inventory if exist then returns else creates new one
        product_id = self.find_product(product_id)
        location_id = self.find_location(location_id)
        stock_inventory_line_id = self.env['stock.inventory.line'].search([
                ('inventory_id','=',inventory_id.id),
                ('product_id','=',product_id.id),
                ('location_id','=',location_id.id)],limit=1)
        if stock_inventory_line_id:
            stock_inventory_line_id.write({'product_qty':stock_inventory_line_id.product_qty + float(onhand_qty)})
        else:
            stock_inventory_line_id = self.env['stock.inventory.line'].create({
                'location_id':location_id.id,
                'product_id':product_id.id,
                'product_uom_id':product_id.uom_id.id,
                'inventory_id':inventory_id.id,
                'product_qty':onhand_qty
            })
            return stock_inventory_line_id

    @api.multi
    def create_stock_iventory(self,values):
        # Create stock Inventory
        inventory_id = self.find_inventory(values.get('Warehouse'))
        stock_inventory_line_id = self.find_stock_inventory_line(inventory_id,values.get('StockCode'),values.get('Warehouse'),values.get('OnHand'))