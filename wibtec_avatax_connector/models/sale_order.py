# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models, _
from odoo.tools.translate import _
import odoo.addons.decimal_precision as dp
from datetime import datetime
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def get_25_chara_exemption_number(self, exemption_number):
        final_exemption_number = ''
        if exemption_number and len(exemption_number) > 25:
            for partner_exemption in exemption_number.split(','):
                current_exempltio_len = len(
                    final_exemption_number) + len(partner_exemption) + 2
                if current_exempltio_len <= 25:
                    if not final_exemption_number:
                        final_exemption_number = partner_exemption
                    else:
                        final_exemption_number = final_exemption_number + ', ' + partner_exemption
                elif current_exempltio_len > 25:
                    break
        return final_exemption_number

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        """Override method to add new fields values.
        @param part- update vals with partner exemption number and code, 
        also check address validation by avalara  
        """
        res = super(SaleOrder, self).onchange_partner_id()
#        addr = self.partner_shipping_id
        # self.exemption_code = self.partner_id.exemption_number or ''
        self.exemption_code = self.get_25_chara_exemption_number(
            self.partner_id.exemption_number)
        self.exemption_code_id = self.partner_id.exemption_code_id.id or None
        self.tax_add_shipping = True
#        self.tax_address = str((addr.name  or '')+ '\n'+(addr.street or '')+ '\n'+(addr.city and addr.city+', ' or ' ')+(addr.state_id and addr.state_id.name or '')+ ' '+(addr.zip or '')+'\n'+(addr.country_id and addr.country_id.name or ''))
        self.tax_add_id = self.partner_shipping_id.id
        if self.partner_id.validation_method:
            self.is_add_validate = True
        else:
            self.is_add_validate = False
        return res

    @api.model
    def create(self, vals):
        #        if vals['partner_id']:
        #            vals['tax_add_id'] = vals['partner_id']
        ship_add_id = False

        if 'tax_add_default' in vals and vals['tax_add_default']:
            ship_add_id = vals['partner_id']
        elif 'tax_add_invoice' in vals and vals['tax_add_invoice']:
            ship_add_id = vals['partner_invoice_id']
        elif 'tax_add_shipping' in vals and vals['tax_add_shipping']:
            ship_add_id = vals['partner_shipping_id']
#        else:
#            ship_add_id = vals['partner_id']
        if ship_add_id:
            vals['tax_add_id'] = ship_add_id
#            vals['tax_address'] = str(ship_add_id.name+ '\n'+(ship_add_id.street or '')+ '\n'+(ship_add_id.city and ship_add_id.city+', ' or ' ')+(ship_add_id.state_id and ship_add_id.state_id.name or '')+ ' '+(ship_add_id.zip or '')+'\n'+(ship_add_id.country_id and ship_add_id.country_id.name or ''))
        return super(SaleOrder, self).create(vals)

    @api.multi
    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        # _logger.info("\n\n\n\n::::::WRITEEE::SO <%s>", vals)
    #     if 'tax_add_default' in vals or 'tax_add_invoice' in vals \
    #             or 'tax_add_shipping' in vals:
    #         for self_obj in self:
    #             ship_add_id = False
    #             if 'tax_add_default' in vals and vals['tax_add_default']:
    #                 ship_add_id = self_obj.partner_id
    #             elif 'tax_add_invoice' in vals and vals['tax_add_invoice']:
    #                 ship_add_id = self_obj.partner_invoice_id or self_obj.partner_id
    #             elif 'tax_add_shipping' in vals and vals['tax_add_shipping']:
    #                 ship_add_id = self_obj.partner_shipping_id or self_obj.partner_id
    # #            else:
    # #                ship_add_id = self.partner_id
    #             if ship_add_id:
    #                 vals['tax_add_id'] = ship_add_id.id
    #                vals['tax_address'] = str(ship_add_id.name+ '\n'+(ship_add_id.street or '')+ '\n'+(ship_add_id.city and ship_add_id.city+', ' or ' ')+(ship_add_id.state_id and ship_add_id.state_id.name or '')+ ' '+(ship_add_id.zip or '')+'\n'+(ship_add_id.country_id and ship_add_id.country_id.name or ''))
        # print (ll)
        return res

    @api.multi
    def copy(self, default=None):
        res = super(SaleOrder, self).copy(default)
        res.onchange_partner_id()
        return res

    @api.multi
    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals.update({
            'exemption_code': self.exemption_code or '',
            'exemption_code_id': self.exemption_code_id.id or False,
            'tax_add_default': self.tax_add_default,
            'tax_add_invoice': self.tax_add_invoice,
            'tax_add_shipping': self.tax_add_shipping,
            'shipping_add_id': self.tax_add_id.id,
            'shipping_address': self.tax_address,
            'location_code': self.location_code or '',
        })
        return invoice_vals

    # @api.onchange('order_line.tax_id')
    # def onchange_tax_id(self):
    #     """
    #     Compute the total amounts of the SO.
    #     """
    #     for sale in self:
    #         sale.compute_tax()

    # @api.depends('order_line.price_total', 'order_line.tax_id')
    # def _amount_all(self):
    #     """
    #     Compute the total amounts of the SO. OLD Method
    #     """
    #     res = super(SaleOrder, self)._amount_all()
    #     for order in self:
    #         _logger.info(
    #             "\n\n\n Order @@##@@ line.price_tax::: <%s>", order.state)
    #         # if order.order_line:
    #         amount_tax = 0.0

    #         if order.state not in ['draft', 'sent']:
    #             _logger.info("\n\n\n _amount_all CALLLLLLLLLLLLLL::")
    #             amount_tax = order.compute_tax()
    #         _logger.info(
    #             "\n\n\n Order ???????? amount_tax::: <%s>", amount_tax)
    #         _logger.info("\n\n\n Order ::: order.order_lin@!!!!!<%s>(%s)(%s)(%s)",
    #                      order, order.state, order.amount_untaxed, order.order_line)
    #         for line in order.order_line:
    #             _logger.info(
    #                 "\n\n\n Order @@##@@ line.price_tax::: <%s>", line.price_tax)
    #             amount_tax += line.price_tax
    #         _logger.info(
    #             "\n\n\n Order 1111 amount_tax::: <%s>", amount_tax)
    #         amount_tax += order.tax_amount
    #         _logger.info(
    #             "\n\n\n Order 22222 amount_tax::: <%s>", amount_tax)
    #         order.update({
    #             'amount_tax': order.pricelist_id.currency_id.round(amount_tax),
    #             'amount_total': order.amount_untaxed + amount_tax,
    #         })
    #         _logger.info(" order ::: order@@@@ <%s>(%s)",
    #                      order.amount_tax, order.amount_untaxed)
    #     return res

    @api.depends('order_line.price_total', 'order_line.tax_id')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        Ovverride This function for solving issue of Without saving SO if Confirm
        SO then Avatax is not calculate so solve this issue
        """
        for order in self:
            # _logger.info("\n\n\n _amount_all CALLLLLLLLLLLLLL::")
            if order.state not in ['draft', 'sent']:
                order.compute_tax()
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                # _logger.info(" order ::: order@@@@ <%s>(%s)",
                #              line.price_subtotal, line.price_tax)
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            # if order.tax_amount:
            amount_tax += order.tax_amount
            # print("\n\n\n\n:::::::amount_tax::::::", amount_tax)
            # _logger.info(" order ::: 22222222222@@@@ <%s>(%s)",
            #              order.amount_tax, order.tax_amount)
            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_total': amount_untaxed + amount_tax,
            })

    @api.onchange('tax_add_default', 'partner_id')
    def default_tax_address(self):
        if self.tax_add_default and self.partner_id:
            self.tax_add_id = self.partner_id.id
#            self.tax_address = str(addr.name+ '\n'+(addr.street or '')+ '\n'+(addr.city and addr.city+', ' or ' ')+(addr.state_id and addr.state_id.name or '')+ ' '+(addr.zip or '')+'\n'+(addr.country_id and addr.country_id.name or ''))
            self.tax_add_default = True
            self.tax_add_invoice = self.tax_add_shipping = False

    @api.onchange('tax_add_invoice', 'partner_invoice_id', 'partner_id')
    def invoice_tax_address(self):
        if (self.tax_add_invoice and self.partner_invoice_id) or (self.tax_add_invoice and self.partner_id):
            self.tax_add_id = self.partner_invoice_id.id or self.partner_id.id
#            self.tax_address = str(addr.name+ '\n'+(addr.street or '')+ '\n'+(addr.city and addr.city+', ' or ' ')+(addr.state_id and addr.state_id.name or '')+ ' '+(addr.zip or '')+'\n'+(addr.country_id and addr.country_id.name or ''))
            self.tax_add_default = self.tax_add_shipping = False
            self.tax_add_invoice = True

    @api.onchange('tax_add_shipping', 'partner_shipping_id', 'partner_id')
    def delivery_tax_address(self):
        if (self.tax_add_shipping and self.partner_shipping_id) or (self.tax_add_shipping and self.partner_id):
            self.tax_add_id = self.partner_shipping_id.id or self.partner_id.id
           # self.tax_address = str(addr.name+ '\n'+(addr.street or '')+ '\n'+(addr.city and addr.city+', ' or ' ')+(addr.state_id and addr.state_id.name or '')+ ' '+(addr.zip or '')+'\n'+(addr.country_id and addr.country_id.name or ''))
            self.tax_add_default = self.tax_add_invoice = False
            self.tax_add_shipping = True

    exemption_code = fields.Char(
        'Exemption Number', help="It show the customer exemption number")
    is_add_validate = fields.Boolean('Address validated')
    exemption_code_id = fields.Many2one(
        'exemption.code', 'Exemption Code', help="It show the customer exemption code")
    amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True,
                                     readonly=True, compute='_amount_all', track_visibility='always')
    amount_tax = fields.Monetary(
        string='Taxes', store=True, readonly=True, compute='_amount_all', track_visibility='always')
    amount_total = fields.Monetary(
        string='Total', store=True, readonly=True, compute='_amount_all', track_visibility='always')
    tax_amount = fields.Float(
        'Tax Code Amount', digits=dp.get_precision('Sale Price'))
    tax_add_default = fields.Boolean('Tax Default Address (AVATAX)')
    tax_add_invoice = fields.Boolean('Tax Invoice Address (AVATAX)')
    tax_add_shipping = fields.Boolean('Tax Delivery Address (AVATAX)', default=True, states={
                                      'draft': [('readonly', False)]})
    tax_add_id = fields.Many2one('res.partner', 'Tax Partner Address (AVATAX)')
    tax_address = fields.Text('Tax Address (AVATAX)')
    # 'location_code = fields.related('shop_id', 'location_code', type="char", string="Location Code", store=True, readonly=True, help="Origin address location code"),
    location_code = fields.Char(
        'Location Code', help='Origin address location code')

    @api.model
    def create_lines(self, order_lines):
        """ Tax line creation for calculating tax amount using avalara tax code. """
        lines = []
        for line in order_lines:
            # If Avatax Tax is added then only Calculate Avatax in line
            if line.product_id and line.product_id.tax_apply and any(tax for tax in line.tax_id if tax.is_avatax):
                tax_code = (
                    line.product_id.tax_code_id and line.product_id.tax_code_id.name) or None
                lines.append({
                    'qty': line.product_uom_qty,
                    'itemcode': line.product_id and line.product_id.default_code or None,
                    'description': line.product_id.description or None,
                    'amount': line.price_unit * (1-(line.discount or 0.0)/100.0) * line.product_uom_qty,
                    'tax_code': tax_code,
                    'id': line,
                    'tax_id': line.tax_id,
                })
        return lines

    @api.model
    def compute_tax(self):
        """ Create and update tax amount for each and every order line and shipping line.
        @param order_line: send sub_total of each line and get tax amount
        @param shiiping_line: send shipping amount of each ship line and get ship tax amount  
        """
        _logger.info("\n\n\n compute_tax ::::::::CALLLLLLLLLLLLLL::")
        avatax_config_obj = self.env['avalara.salestax']
        account_tax_obj = self.env['account.tax']
        avatax_config = avatax_config_obj._get_avatax_config_company()

        # Make sure Avatax is configured
        if not avatax_config:
            raise UserError(_('Your Avatax Countries settings are not configured. You need a country code in the Countries section.  \nIf you have a multi-company installation, you must add settings for each company.  \n\nYou can update settings in Avatax->Avatax API.'))

        tax_amount = o_tax_amt = 0.0

        # ship from Address / Origin Address either warehouse or company if none
        if self.warehouse_id and self.warehouse_id.partner_id:
            ship_from_address_id = self.warehouse_id.partner_id
        else:
            ship_from_address_id = self.company_id.partner_id
        # _logger.info("\n\n\n Order ship_from_address_id:: <%s>",
        #              ship_from_address_id)
        if avatax_config and not avatax_config.disable_tax_calculation:
            ava_tax = account_tax_obj.search(
                [('is_avatax', '=', True),
                 ('type_tax_use', 'in', ['sale', 'all']),
                 ('company_id', '=', self.company_id.id)])

            shipping_add_id = self.tax_add_id

            lines = self.create_lines(self.order_line)
            # If Avatax Tax is added Avatax tax and also used greater than 0.00% Tax in line then display warning
            if any(tax for lines in self.order_line for tax in lines.tax_id if tax.is_avatax):
                tax_greater_0 = any(
                    tax for lines in self.order_line for tax in lines.tax_id if not tax.amount == 0)
                if tax_greater_0:
                    raise UserError(
                        _('This sales order is using a Non Avatax sales tax rate greater than 0%.  Please select AVATAX on the sales order line.'))
            order_date = str(self.date_order).split(' ')[0]
            order_date = datetime.strptime(order_date, "%Y-%m-%d").date()
            if lines:
                if avatax_config.on_line:
                    # Line level tax calculation
                    # tax based on individual order line
                    tax_id = []
                    for line in lines:
                        tax_id = line['tax_id'] and [
                            tax.id for tax in line['tax_id']] or []
                        if ava_tax and ava_tax[0].id not in tax_id:
                            tax_id.append(ava_tax[0].id)
                        ol_tax_amt = account_tax_obj._get_compute_tax(avatax_config, order_date,
                                                                      self.name, 'SalesOrder', self.partner_id, ship_from_address_id,
                                                                      shipping_add_id, [
                                                                          line], self.user_id, self.exemption_code or None, self.exemption_code_id.code or None,
                                                                      ).TotalTax
                        o_tax_amt += ol_tax_amt  # tax amount based on total order line total
                        # line['id'].write({'tax_amt': ol_tax_amt, 'tax_id': [(6,0, tax_id)]})
                        line['id'].write({'tax_amt': ol_tax_amt})

                    tax_amount = o_tax_amt
                    # _logger.info(
                    #     "\n\n\n Order IFFFFFFFFFFF:: tax_amount <%s>", tax_amount)
                elif avatax_config.on_order:
                    # Order level tax calculation
                    #                lines1.extend(lines2)

                    tax_amount = account_tax_obj._get_compute_tax(avatax_config, order_date,
                                                                  self.name, 'SalesOrder', self.partner_id, ship_from_address_id,
                                                                  shipping_add_id, lines, self.user_id, self.exemption_code or None, self.exemption_code_id.code or None,
                                                                  ).TotalTax

                    for o_line in self.order_line:
                        o_line.write({'tax_amt': 0.0, })
                else:
                    raise UserError(
                        _('Please select system calls in Avatax API Configuration'))
            else:
                for o_line in self.order_line:
                    o_line.write({'tax_amt': 0.0, })

        else:
            for o_line in self.order_line:
                o_line.write({'tax_amt': 0.0, })
#            for s_line in order.shipping_lines:
#               ship_order_line.write(cr, uid, [s_line.id], {'tax_amt': 0.0,})

        # Need to put in comments because if Sale order id is like NewID then occure Traceback
        # so as a solution self.update is working

        # self.write({'tax_amount': tax_amount, 'order_line' : []})
        self.update({
            'tax_amount': tax_amount,
            'order_line': [],
        })
        print("\n\n\n::tax_amount::::::", tax_amount)
        _logger.info(" computeeeeeee ::: tax_amount <%s>", tax_amount)
        return tax_amount

    @api.multi
    def button_dummy(self):
        """ It used to called manually calculation method of avalara and get tax amount"""
        self.compute_tax()
        return super(SaleOrder, self).button_dummy()

    @api.multi
    def action_confirm(self):
        self.compute_tax()
        self._amount_all()
        return super(SaleOrder, self).action_confirm()


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    tax_amt = fields.Float('Avalara Tax', help="tax calculate by avalara")


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
