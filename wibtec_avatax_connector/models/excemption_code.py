# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class exemption_code(models.Model):
	
    _name = 'exemption.code'
    _description = 'Exemption Code'
    
    name = fields.Char('Name')
    code = fields.Char('Code')

    @api.multi
    @api.depends('name', 'code')
    def name_get(self):
        return [(r.id, ('(' + r.code + ')' + ' ' + r.name)) for r in self]