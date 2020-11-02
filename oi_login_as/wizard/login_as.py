'''
Created on May 13, 2019

@author: Zuhair Hammadi
'''
from odoo import models, fields, api

class LoginAs(models.TransientModel):
    _name = 'login.as'
    _description = _name
    
    @api.model
    def _employee_domain(self):
        domain = [('user_id', '!=', False), ('user_id', '!=', self.env.user.id)]
        if self.env.user._is_system():
            domain.append(('id', 'child_of', self.env.user.employee_ids.ids))
        return domain
        
    group_id = fields.Many2one('res.groups')
    user_id = fields.Many2one('res.users', required = True)
    
    group_ids = fields.Many2many('res.groups', compute = '_calc_group_ids', string = 'User Groups')
    company_id = fields.Many2one(related='user_id.company_id', readonly=True)
    company_ids = fields.Many2many(related='user_id.company_ids', readonly=True)
    
    employee_id = fields.Many2one('hr.employee', domain = _employee_domain)
    
    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            self.user_id = self.employee_id.user_id
    
    @api.multi
    def switch_to_user(self):
        assert self.env.user._is_system() or self.env.user.has_group('oi_login_as.group_login_as')
        return {
            'type' : 'ir.actions.act_url',
            'url' : '/web/login_as/%d' % self.user_id.id,
            'target' : 'self'
            }
        
    @api.onchange('group_id')
    def _onchange_group_id(self):
        if self.group_id and self.group_id not in self.user_id.groups_id:
            self.user_id = False
    
    @api.depends('user_id')
    def _calc_group_ids(self):
        for record in self:
            record.group_ids = record.user_id.groups_id.filtered(lambda group : group.category_id.visible).sorted('full_name')        