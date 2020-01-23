# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HelpdeskTicket(models.Model):

    _inherit = "helpdesk.ticket"

    due_date = fields.Date("Due Date")
