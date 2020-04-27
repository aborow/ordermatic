# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    @api.onchange('group_mrp_routings')
    def _onchange_group_mrp_routings(self):
        res = super(ResConfigSettings,self)._onchange_group_mrp_routings()
        # If we activate 'MRP Work Orders', it means that we need to install 'mrp_workorder'.
        # The opposite is not always true: other modules (such as 'quality_mrp_workorder') may
        # depend on 'mrp_workorder', so we should not automatically uninstall the module if 'MRP
        # Work Orders' is deactivated.
        # Long story short: if 'mrp_workorder' is already installed, we don't uninstall it based on
        # group_mrp_routings
        if self.group_mrp_routings:
            self.module_mrp_workorder = False
        elif not self.env['ir.module.module'].search([('name', '=', 'mrp_workorder'), ('state', '=', 'installed')]):
            self.module_mrp_workorder = False