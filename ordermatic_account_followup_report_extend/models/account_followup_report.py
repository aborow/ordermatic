# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.tools.misc import formatLang, format_date
from datetime import datetime


class AccountFollowupReport(models.AbstractModel):

    _inherit = "account.followup.report"

    def _get_columns_name(self, options):
        """
        Override
        Return the name of the columns of the follow-ups report
        """
        headers = [{},
                   {'name': _('Date'), 'class': 'date', 'style': 'text-align:center; white-space:nowrap;'},
                   {'name': _('Due Date'), 'class': 'date', 'style': 'text-align:center; white-space:nowrap;'},
                   {'name': _('Source Document'), 'style': 'text-align:center; white-space:nowrap;'},
                   {'name': _('Amount'), 'style': 'text-align:right; white-space:nowrap;'},
                   {'name': _('Paid/Credit'), 'style': 'text-align:right; white-space:nowrap;'},
                   {'name': _('Communication'), 'style': 'text-align:center; white-space:nowrap;'},
                   {'name': _('Expected Date'), 'class': 'date', 'style': 'white-space:nowrap;'},
                   {'name': _('Excluded'), 'class': 'date', 'style': 'white-space:nowrap;'},
                   {'name': _('Total Due'), 'class': 'number o_price_total', 'style': 'text-align:right; white-space:nowrap;'}
                  ]
        if self.env.context.get('print_mode'):
            headers = headers[:7] + headers[9:]  # Remove the 'Expected Date' and 'Excluded' columns
        return headers

    def _get_lines(self, options, line_id=None):
        """
        Override
        Compute and return the lines of the columns of the follow-ups report.
        """
        # Get date format for the lang
        partner = options.get('partner_id') and self.env['res.partner'].browse(options['partner_id']) or False
        if not partner:
            return []
        lang_code = partner.lang or self.env.user.lang or 'en_US'

        lines = []
        res = {}
        today = fields.Date.today()
        line_num = 0
        for l in partner.unreconciled_aml_ids.filtered(lambda l: l.company_id == self.env.user.company_id):
            if l.company_id == self.env.user.company_id:
                if self.env.context.get('print_mode') and l.blocked:
                    continue
                currency = l.currency_id or l.company_id.currency_id
                if currency not in res:
                    res[currency] = []
                res[currency].append(l)
        for currency, aml_recs in res.items():
            total = 0
            total_issued = 0
            for aml in aml_recs:
                amount = aml.amount_residual_currency if aml.currency_id else aml.amount_residual
                date_due = format_date(self.env, aml.date_maturity or aml.date, lang_code=lang_code)
                total += not aml.blocked and amount or 0
                is_overdue = today > aml.date_maturity if aml.date_maturity else today > aml.date
                is_payment = aml.payment_id
                if is_overdue or is_payment:
                    total_issued += not aml.blocked and amount or 0
                if is_overdue:
                    date_due = {'name': date_due, 'class': 'color-red date', 'style': 'white-space:nowrap;text-align:center;color: red;'}
                if is_payment:
                    date_due = ''
                move_line_name = aml.invoice_id.name or aml.name
                if self.env.context.get('print_mode'):
                    move_line_name = {'name': move_line_name, 'style': 'text-align:center; white-space:normal;'}
                amount = formatLang(self.env, amount, currency_obj=currency)
                line_num += 1
                expected_pay_date = format_date(self.env, aml.expected_pay_date, lang_code=lang_code) if aml.expected_pay_date else ''
                paid_total_amount = aml.invoice_id.amount_total - aml.invoice_id.residual
                paid_amount = formatLang(self.env, paid_total_amount, currency_obj=currency)
                total_amount = formatLang(self.env, aml.invoice_id.amount_total, currency_obj=currency)
                columns = [
                    format_date(self.env, aml.date, lang_code=lang_code),
                    date_due,
                    aml.invoice_id.origin,
                    total_amount,
                    paid_amount if paid_total_amount > 0.0 else ' ',
                    move_line_name,
                    expected_pay_date + ' ' + (aml.internal_note or ''),
                    {'name': aml.blocked, 'blocked': aml.blocked},
                    amount,
                ]
                if self.env.context.get('print_mode'):
                    columns = columns[:6] + columns[8:]
                lines.append({
                    'id': aml.id,
                    'invoice_id': aml.invoice_id.id,
                    'view_invoice_id': self.env['ir.model.data'].get_object_reference('account', 'invoice_form')[1],
                    'account_move': aml.move_id,
                    'name': aml.move_id.name,
                    'caret_options': 'followup',
                    'move_id': aml.move_id.id,
                    'type': is_payment and 'payment' or 'unreconciled_aml',
                    'unfoldable': False,
                    'has_invoice': bool(aml.invoice_id),
                    'columns': [type(v) == dict and v or {'name': v} for v in columns],
                })
            total_due = formatLang(self.env, total, currency_obj=currency)
            line_num += 1
            lines.append({
                'id': line_num,
                'name': '',
                'class': 'total',
                'unfoldable': False,
                'level': 0,
                'columns': [{'name': v} for v in [''] * (5 if self.env.context.get('print_mode') else 7) + [total >= 0 and _('Total Due') or '', total_due]],
            })
            if total_issued > 0:
                total_issued = formatLang(self.env, total_issued, currency_obj=currency)
                line_num += 1
                lines.append({
                    'id': line_num,
                    'name': '',
                    'class': 'total',
                    'unfoldable': False,
                    'level': 0,
                    'columns': [{'name': v} for v in [''] * (5 if self.env.context.get('print_mode') else 7) + [_('Total Overdue'), total_issued]],
                })
            # Add an empty line after the total to make a space between two currencies
            line_num += 1
            lines.append({
                    'id': line_num,
                    'name': 'Balance Details',
                    'style': 'text-align:left; white-space:nowrap;',
                    'unfoldable': False,
                    'level': 0,
                    'columns': [{'name': v} for v in [''] * (7 if self.env.context.get('print_mode') else 9)],
                })
            line_num += 1
            column_aged_rec = [
                    'Balance',
                    'Current',
                    '0-30 Days',
                    '30-60 Days',
                    '60-90 Days',
                    '90-120 Days',
                    'Over 120-Days',
                ]
            lines.append({
                'id': line_num,
                'name': '',
                'style': 'text-align:right;white-space:nowrap;border:0px;background-color: white;',
                'unfoldable': False,
                'level': 1,
                'columns': [type(v) == dict and v or {'name': v} for v in column_aged_rec],
            })
            balance_list = self._find_values(aml_recs,currency)
            line_num += 1
            lines.append({
                'id': line_num,
                'name': '',
                'style': 'text-align:right; white-space:nowrap;border:0px;background-color: white;',
                'unfoldable': False,
                'level': -1,
                'columns': [type(v) == dict and v or {'name': v} for v in balance_list if balance_list],
            })
            lines.append({
                'id': line_num,
                'name': '',
                'style': 'text-align:center; white-space:nowrap;border:0px;background-color: white;',
                'class': '',
                'unfoldable': False,
                'level': 0,
                'columns': [{} for col in columns],
            })
        # Remove the last empty line
        if lines:
            lines.pop()
        return lines

    @api.multi
    def _find_values(self,aml_recs,currency):
        balance_list = [0,0,0,0,0,0,0]
        new_balance_list = []
        for aml in aml_recs:
            days = self.calculate_days(aml.date_maturity)
            if days < 0:
                balance_list[1] += aml.invoice_id.residual
            if days >= 0 and days <= 30:
                balance_list[2] += aml.invoice_id.residual
            elif days >= 30 and days <= 60:
                balance_list[3] += aml.invoice_id.residual
            elif days >= 60 and days <= 90:
                balance_list[4] += aml.invoice_id.residual
            elif days >= 90 and days <= 120:
                balance_list[5] += aml.invoice_id.residual
            elif days >= 120:
                balance_list[6] += aml.invoice_id.residual
        balance_list[0] = balance_list[1]+balance_list[2]+balance_list[3]+balance_list[4]+balance_list[5]+balance_list[6]
        new_balance_list.append(formatLang(self.env, balance_list[0], currency_obj=currency))
        new_balance_list.append(formatLang(self.env, balance_list[1], currency_obj=currency))
        new_balance_list.append(formatLang(self.env, balance_list[2], currency_obj=currency))
        new_balance_list.append(formatLang(self.env, balance_list[3], currency_obj=currency))
        new_balance_list.append(formatLang(self.env, balance_list[4], currency_obj=currency))
        new_balance_list.append(formatLang(self.env, balance_list[5], currency_obj=currency))
        new_balance_list.append(formatLang(self.env, balance_list[6], currency_obj=currency))
        return new_balance_list

    @api.multi
    def calculate_days(self,date_maturity):
        today_date = datetime.strptime(str(datetime.today()),'%Y-%m-%d %H:%M:%S.%f').date()
        delta = today_date - date_maturity
        return delta.days