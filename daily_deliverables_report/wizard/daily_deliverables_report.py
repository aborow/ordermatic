#-*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields,api, _
from datetime import datetime
from odoo.exceptions import ValidationError
import base64
import io
import xlsxwriter
import datetime

class DailyDeliverablesReport(models.TransientModel):

    _name = "daily.deliverables.report"
    _description = "Daily Deliverables Report"

    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')

    @api.multi
    @api.constrains('from_date', 'to_date')
    def check_date(self):
        """ This method is used to check constrains on dates."""
        if self.from_date and self.to_date and (self.from_date > self.to_date):
            raise ValidationError(_('To Date should be greater than From Date.'))

    @api.multi
    def get_date_domain(self):
        """Method will filter record based on domain."""
        domain = [
            ('omc_projected_shipping_date', '>=', self.from_date),
            ('omc_projected_shipping_date', '<=', self.to_date),
            ('state','in',('sale','done'))]
        return domain

    @api.multi
    def get_sale_orders(self):
        """Method will filter sale order based on domain and returns it."""
        domain = self.get_date_domain()
        sale_orders = self.env['sale.order'].search(domain)
        return sale_orders

    @api.multi
    def calculate_days(self,omc_projected_shipping_date,date_order):
        date_order = datetime.datetime.strptime(str(date_order),'%Y-%m-%d %H:%M:%S').date()
        delta = omc_projected_shipping_date - date_order
        return delta.days

    @api.multi
    def print_xls(self):
        """Method will print the XLS report."""
        sale_orders = self.get_sale_orders()
        if not sale_orders:
            raise ValidationError(
                _('No records found.'))
        fp = io.BytesIO()
        workbook = xlsxwriter.Workbook(fp)
        worksheet = workbook.add_worksheet('Daily Deliverables Report')
        data_format = workbook.add_format({'align': 'center'})
        report_header_format = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 18})
        header_format = workbook.add_format({'bold': True, 'align': 'center','color':'white','bg_color':'navy'})
        bold = workbook.add_format({'bold': True})
        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:C', 20)
        worksheet.set_column('D:D', 20)
        worksheet.set_column('E:E', 25)
        worksheet.set_column('F:F', 35)
        worksheet.set_column('G:G', 15)
        worksheet.set_column('H:H', 35)
        worksheet.set_column('I:I', 20)
        worksheet.set_column('J:J', 25)
        worksheet.set_column('K:K', 35)
        worksheet.set_column('L:L', 20)
        worksheet.set_column('M:M', 20)
        worksheet.set_column('N:N', 20)
        worksheet.set_column('O:O', 20)
        worksheet.set_column('P:P', 20)
        not_exist = workbook.add_format({'bold': True, 'font_color': 'red'})
        row = 0
        colm = 0
        header_string = 'Daily Deliverables Report From ' + \
            str(self.from_date) + ' to ' + str(self.to_date)
        worksheet.merge_range(
            'A1:P2', header_string, report_header_format)
        sale_orders = self.get_sale_orders()
        if sale_orders:
            row += 3
            worksheet.write(row, colm, 'Order Date', header_format)
            colm += 1
            worksheet.write(row, colm, 'Salesperson', header_format)
            colm += 1
            worksheet.write(row, colm, 'Order Contact', header_format)
            colm += 1
            worksheet.write(row, colm, 'Order Reference', header_format)
            colm += 1
            worksheet.write(row, colm, 'Customer', header_format)
            colm += 1
            worksheet.write(row, colm, 'Customer Requested Delivery Date', header_format)
            colm += 1
            worksheet.write(row, colm, 'Status', header_format)
            colm += 1
            worksheet.write(row, colm, 'Order Lines', header_format)
            colm += 1
            worksheet.write(row, colm, 'Product Category', header_format)
            colm += 1
            worksheet.write(row, colm, 'Projected Lead Time', header_format)
            colm += 1
            worksheet.write(row, colm, 'OMC Projected Shipping Date', header_format)
            colm += 1
            worksheet.write(row, colm, 'Internal Reference', header_format)
            colm += 1
            worksheet.write(row, colm, 'Qty Ordered', header_format)
            colm += 1
            worksheet.write(row, colm, 'UoM', header_format)
            colm += 1
            worksheet.write(row, colm, 'Qty Delivered ', header_format)
            colm += 1
            worksheet.write(row, colm, 'Order Line Status', header_format)
            for order in sale_orders:
                for line in order.order_line:
                    colm = 0
                    row += 1
                    if order.date_order:
                        worksheet.write(row, colm,datetime.datetime.strptime(str(order.date_order),'%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S'), data_format)
                    else:
                        worksheet.write(row, colm,'-', data_format)
                    colm += 1
                    if order.user_id:
                        worksheet.write(row, colm, order.user_id.name, data_format)
                    else:
                        worksheet.write(row, colm,'-', data_format)
                    colm += 1
                    if order.order_contact:
                        worksheet.write(row, colm, order.order_contact, data_format)
                    else:
                        worksheet.write(row, colm,'-', data_format)
                    colm += 1
                    if order.name:
                        worksheet.write(row, colm, order.name, data_format)
                    else:
                        worksheet.write(row, colm,'-', data_format)
                    colm += 1
                    if order.partner_id:
                        worksheet.write(row, colm, order.partner_id.name, data_format)
                    else:
                        worksheet.write(row, colm,'-', data_format)
                    colm += 1
                    if order.customer_requested_delivery_date:
                        worksheet.write(row, colm, datetime.datetime.strptime(str(order.customer_requested_delivery_date),'%Y-%m-%d').strftime('%Y-%m-%d'), data_format)
                    else:
                        worksheet.write(row, colm,'-', data_format)
                    colm += 1
                    if order.state:
                        worksheet.write(row, colm, str(order.state).capitalize(), data_format)
                    else:
                        worksheet.write(row, colm,'-', data_format)
                    colm += 1
                    if line.product_id:
                        worksheet.write(row, colm, line.product_id.name, data_format)
                    elif line.display_type == 'line_note':
                        worksheet.write(row, colm, line.name, data_format)
                    else:
                        worksheet.write(row, colm,'-', data_format)
                    colm += 1
                    if line.product_id.categ_id:
                        worksheet.write(row, colm, line.product_id.categ_id.complete_name, data_format)
                    else:
                        worksheet.write(row, colm,'-', data_format)
                    colm += 1
                    if order.omc_projected_shipping_date and order.date_order:
                        days = self.calculate_days(order.omc_projected_shipping_date,order.date_order)
                        worksheet.write(row, colm, days, data_format)
                    else:
                        worksheet.write(row, colm,'-', data_format)
                    colm += 1
                    if order.omc_projected_shipping_date:
                        worksheet.write(row, colm, datetime.datetime.strptime(str(order.omc_projected_shipping_date),'%Y-%m-%d').strftime('%Y-%m-%d'), data_format)
                    else:
                        worksheet.write(row, colm,'-', data_format)
                    colm += 1
                    if line.product_id.default_code:
                        worksheet.write(row, colm, line.product_id.default_code, data_format)
                    else:
                        worksheet.write(row, colm,'-', data_format)
                    colm += 1
                    if line.product_uom_qty:
                        worksheet.write(row, colm, line.product_uom_qty, data_format)
                    else:
                        worksheet.write(row, colm,'-', data_format)
                    colm += 1
                    if line.product_uom:
                        worksheet.write(row, colm, line.product_uom.name, data_format)
                    else:
                        worksheet.write(row, colm,'-', data_format)
                    colm += 1
                    if line.qty_delivered:
                        worksheet.write(row, colm, line.qty_delivered, data_format)
                    else:
                        worksheet.write(row, colm,'-', data_format)  
                    colm += 1
                    if line.product_uom_qty < line.qty_delivered:
                        worksheet.write(row, colm, 'Open', data_format)
                    elif line.product_uom_qty <= line.qty_delivered:
                        worksheet.write(row, colm, 'Closed', data_format)
                    else:
                        worksheet.write(row, colm, '-', data_format)
                    colm += 1
        workbook.close()
        fp.seek(0)
        result = base64.b64encode(fp.read())
        attachment_obj = self.env['ir.attachment']
        attachment_id = attachment_obj.create(
            {'name': 'daily_deliverables_report.xlsx', 'datas_fname': 'Daily Deliverables Report.xlsx', 'datas': result})
        download_url = '/web/content/' + \
            str(attachment_id.id) + '?download=True'
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return {
            "type": "ir.actions.act_url",
            "url": str(base_url) + str(download_url),
            "target": "new"
        }