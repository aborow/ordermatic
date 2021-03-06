# -*- coding: utf-8 -*-
# Copyright 2018 Openinside co. W.L.L.
{
    "name": "Login as another user",
    "summary": "Login as/impersonate another user",
    "version": "12.0.1.1.12",
    'category': 'Extra Tools',
    "website": "https://www.open-inside.com",
	"description": """
		 * allow administrator to login as/impersonate normal user
		 * allow administrator to login as/impersonate portal user
		 * login back to administrator		 
		 
    """,
	'images':[
        'static/description/cover.png'
	],
    "author": "Openinside",
    "license": "OPL-1",
    "price" : 29.99,
    "currency": 'EUR',
    "installable": True,
    "depends": [
        'web', 'hr'
    ],
    "data": [
        'security/res_groups.xml',
        'view/login_as.xml',
        'view/action.xml',
        'view/web_assets.xml'
    ],
    'qweb' : [
        'static/src/xml/templates.xml'
    ],
    'external_dependencies' : {
        
    },    
    'installable': True,
    'auto_install': True,    
    'odoo-apps' : True,
    'images':[
        'static/description/cover.png'
    ],      
}

