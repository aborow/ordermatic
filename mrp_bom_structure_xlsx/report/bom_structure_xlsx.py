# Copyright 2017 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
from odoo import models
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class BomStructureXlsx(models.AbstractModel):
    _name = 'report.mrp_bom_structure_xlsx.bom_structure_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def print_bom_children(self, ch, sheet, row, level):
      i, j = row, level
      j += 1
      # sheet.write(i, 1, '> '*j)
      sheet.write(i, j, ch.product_id.default_code or '')
      sheet.write(i, 11, ch.product_id.default_code or '')
      sheet.write(i, 12, ch.product_id.display_name or '')
      sheet.write(i, 13, ch.product_uom_id._compute_quantity(
          ch.product_qty, ch.product_id.uom_id) or '')
      sheet.write(i, 14, ch.product_id.uom_id.name or '')
      sheet.write(i, 15, ch.bom_id.code or '')
      i += 1
      for child in ch.child_line_ids:
        if j >=10:
          j = 9
        i = self.print_bom_children(child, sheet, i, j)
      j -= 1
      return i

    def generate_xlsx_report(self, workbook, data, objects):
        workbook.set_properties({
            'comments': 'Created with Python and XlsxWriter from Odoo 12.0'})
        sheet = workbook.add_worksheet(_('BOM Structure'))
        sheet.set_landscape()
        sheet.fit_to_pages(1, 0)
        sheet.set_zoom(80)
        sheet.set_column(0, 0, 40)
        sheet.set_column(1, 6, 20)
        sheet.set_column(2, 6, 20)
        sheet.set_column(3, 6, 40)
        sheet.set_column(4, 6, 20)
        sheet.set_column(5, 6, 20)
        sheet.set_column(6, 6, 20)
        sheet.set_column(7, 6, 20)
        sheet.set_column(8, 6, 20)
        sheet.set_column(9, 6, 20)
        sheet.set_column(10, 6, 20)
        sheet.set_column(11, 6, 20)
        sheet.set_column(12, 6, 20)
        sheet.set_column(13, 6, 20)
        sheet.set_column(14, 6, 20)
        sheet.set_column(15, 6, 20)
        sheet.set_column(16, 6, 20)
        bold = workbook.add_format({'bold': True})
        title_style = workbook.add_format({'bold': True,
                                           'bg_color': '#FFFFCC',
                                           'bottom': 1})
        sheet_title = [_('BOM Name'),
                       _('Level1'),
                       _('Level2'),
                       _('Level3'),
                       _('Level4'),
                       _('Level5'),
                       _('Level6'),
                       _('Level7'),
                       _('Level8'),
                       _('Level9'),
                       _('Level10'),
                       _('Product Reference'),
                       _('Product Name'),
                       _('Quantity'),
                       _('Unit of Measure'),
                       _('Reference')
                       ]
        sheet.set_row(0, None, None, {'collapsed': 1})
        sheet.write_row(1, 0, sheet_title, title_style)
        sheet.freeze_panes(2, 0)
        i = 2
        for o in objects:
            sheet.write(i, 0, o.product_tmpl_id.name or o.default_code or '', bold)
            # sheet.write(i, 1, '', bold)
            sheet.write(i, 11, o.product_id.default_code or '', bold)
            sheet.write(i, 12, o.product_id.name or '', bold)
            sheet.write(i, 13, o.product_qty, bold)
            sheet.write(i, 14, o.product_uom_id.name or '', bold)
            sheet.write(i, 15, o.code or '', bold)
            i += 1
            j = 0
            for ch in o.bom_line_ids:
                i = self.print_bom_children(ch, sheet, i, j)