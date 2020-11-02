# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.service import security
from odoo.addons.web.controllers.main import Home

class LoginAs(Home):
    
    @http.route('/web/login_as/<int:user_id>', type='http', auth='user', sitemap=False)
    def switch_to_user(self, user_id, **kwargs):  # @UnusedVariable
        user = request.env.user # @UndefinedVariable
        uid = user.id  
        login_as_type = None
        
        if user._is_system():
            login_as_type = 'system'
        
        elif user.has_group('oi_login_as.group_login_as'):
            employee_id = request.env['hr.employee'].search([('user_id', '=', user_id)], limit = 1)
            if request.env['hr.employee'].search([('id', '=', employee_id.id), ('id', 'child_of', user.employee_ids.ids)], count = True):
                login_as_type = 'user'        

        if login_as_type:  # @UndefinedVariable
            request.session.impersonate_uid = uid
            request.session.readonly = login_as_type == 'user'
            uid = request.session.uid = user_id
            request.env['res.users']._invalidate_session_cache()
            request.session.session_token = security.compute_session_token(request.session, request.env)

        return http.local_redirect(self._login_redirect(uid), keep_hash=True, forward_debug = False)

    @http.route('/web/login_back', type='http', auth='user', sitemap=False)
    def switch_back(self, **kwargs):  # @UnusedVariable
        uid = request.env.user.id  # @UndefinedVariable
        query = None
        if request.session.impersonate_uid:  # @UndefinedVariable
            uid = request.session.uid = request.session.impersonate_uid  # @UndefinedVariable
            request.session.impersonate_uid = False
            request.session.readonly = False
            request.env['res.users']._invalidate_session_cache()
            request.session.session_token = security.compute_session_token(request.session, request.env)  
            if uid in [1,2]:           
                query={'debug':1}           

        return http.local_redirect(self._login_redirect(uid), query=query, keep_hash=True, forward_debug = query and True or False)
