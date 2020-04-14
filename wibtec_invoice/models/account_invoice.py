# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import odoo
from odoo import api, fields, models, _
import datetime
from odoo.tools.misc import formatLang
from odoo.tools import float_is_zero, float_compare

class AccountInvoice(models.Model):

    _inherit = "account.invoice"

    amount_discount = fields.Float('Discount Amount',compute='compute_amount_discount')
    note_of_invoice = fields.Text("Notes For Invoice")
    name = fields.Char(string='PO/Customer Reference', index=True,
                       readonly=True, states={'draft': [('readonly', False)]}, copy=False,
                       help='The name that will be used on account move lines')
    tracking_numbers = fields.Char("Tracking Numbers",compute='_add_tracking_numbers')

    @api.multi
    @api.depends('origin')
    def _add_tracking_numbers(self):
        for invoice in self:
            self.env.cr.execute("SELECT order_line_id FROM sale_order_line_invoice_rel WHERE invoice_line_id in %s", (tuple(
                invoice.invoice_line_ids.ids),))
            rows = self.env.cr.dictfetchall()
            sale_line_ids = [x['order_line_id'] for x in rows]
            if sale_line_ids:
                sale_order_recs = self.env['sale.order.line'].browse(sale_line_ids).mapped('order_id')
                tracking_numbers = ''
                for sale_id in sale_order_recs:
                    for picking in sale_id.picking_ids:
                        if picking.carrier_tracking_ref and picking.sale_id:
                            if not invoice.tracking_numbers:
                                tracking_numbers = picking.carrier_tracking_ref
                                invoice.update({'tracking_numbers':tracking_numbers})
                            else:
                                tracking_numbers = tracking_numbers + ',' + picking.carrier_tracking_ref
                                invoice.update({'tracking_numbers':tracking_numbers})

    @api.one
    @api.depends('invoice_line_ids.discount_amount')
    def compute_amount_discount(self):
        self.amount_discount = sum(line.discount_amount for line in self.invoice_line_ids)
                
    @api.multi
    # Returns the origin date
    def _get_origin_date(self,origin):
        sale_order = self.env['sale.order'].search([('name','=',origin)],limit=1)
        if sale_order.confirmation_date:
            confirmation_date = datetime.datetime.strptime(str(sale_order.confirmation_date),'%Y-%m-%d %H:%M:%S').date()
            return confirmation_date
        else:
            return 

    @api.multi
    # Returns the origin date
    def _get_order_contact(self,origin):
        sale_order = self.env['sale.order'].search([('name','=',origin)],limit=1)
        if sale_order.order_contact:
            return sale_order.order_contact
        else:
            return 

    @api.multi
    def _get_shipping_date(self,origin):
        # Returns the shipping date
        stock_picking = self.env['stock.picking'].search([('origin','=',origin)],limit=1)
        if stock_picking.date_done:
            date_done = datetime.datetime.strptime(str(stock_picking.date_done),'%Y-%m-%d %H:%M:%S').date()
            return date_done
        else:
            return

    @api.multi
    def _get_tax_amount(self, amount,payment=None):
        # Returns the tax amount
        self.ensure_one()
        res = {}
        currency = self.currency_id or self.company_id.currency_id
        res = formatLang(self.env, amount, currency_obj=currency)
        #for payment in self.payment_move_line_ids:
        if payment != None:
            if self.type in ('out_invoice', 'in_refund'):
                amount = sum([p.amount for p in payment.matched_debit_ids if p.debit_move_id in self.move_id.line_ids])
                amount_currency = sum([p.amount_currency for p in payment.matched_debit_ids if p.debit_move_id in self.move_id.line_ids])
            elif self.type in ('in_invoice', 'out_refund'):
                amount = sum([p.amount for p in payment.matched_credit_ids if p.credit_move_id in self.move_id.line_ids])
                amount_currency = sum([p.amount_currency for p in payment.matched_credit_ids if p.credit_move_id in self.move_id.line_ids])
            # get the payment value in invoice currency
            if payment.currency_id and payment.currency_id == self.currency_id:
                amount_to_show = amount_currency
            else:
                amount_to_show = payment.company_id.currency_id.with_context(date=payment.date).compute(amount, self.currency_id)
            if float_is_zero(amount_to_show, precision_rounding=self.currency_id.rounding):
                return res
            res = formatLang(self.env, amount_to_show, currency_obj=currency)
        return res


class AccountInvoiceLine(models.Model):

    _inherit = "account.invoice.line"

    discount_amount = fields.Float('Discount Amount',compute='compute_discount_amount')

    @api.multi
    @api.depends('discount')
    def compute_discount_amount(self):
        for invoice in self:
            if invoice.discount:
                price = invoice.price_unit * invoice.quantity
                invoice.discount_amount = round(price - invoice.price_subtotal,2)
            else:
                invoice.discount_amount = 0.0