# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)

class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    cycle_count_rule_ids = fields.Many2many(
        comodel_name='stock.cycle.count.rule',
        relation='warehouse_cycle_count_'
                 'rule_rel',
        column1='warehouse_id',
        column2='rule_id',
        string='Cycle Count Rules')
    cycle_count_planning_horizon = fields.Integer(
        string='Cycle Count Planning Horizon (in days)',
        help='Cycle Count planning horizon in days. Only the counts inside '
             'the horizon will be created.')
    counts_for_accuracy_qty = fields.Integer(
        string='Inventories for location accuracy calculation',
        default=1,
        help='Number of latest inventories used to calculate location '
             'accuracy')

    @api.one
    def get_horizon_date(self):
        date = datetime.today()
        delta = timedelta(self.cycle_count_planning_horizon)
        date_horizon = date + delta
        return date_horizon


    # Rui Franco 20190516
    @api.model
    def get_locations_under(self, loc, res):
        Location = self.env['stock.location']
        child_locations = Location.search([('location_id','=',loc)])
        for cl in child_locations:
            res.append(cl.id)
            self.get_locations_under(cl.id, res)
        return res

    @api.model
    def _get_cycle_count_locations_search_domain(self, parent):
        # Rui Franco 20190516 - parent_left/right don't exist in v12
        # We need to get all locations under this one...
        locations = self.get_locations_under(self.id, [])
        domain = [
                    ('id', 'in', locations),
                    ('cycle_count_disabled', '=', False)
                ]
        return domain

    @api.model
    def _search_cycle_count_locations(self, rule):
        locations = self.env['stock.location']
        if rule.apply_in == 'warehouse':
            locations = self.env['stock.location'].search(
                self._get_cycle_count_locations_search_domain(
                    self.view_location_id))
        elif rule.apply_in == 'location':
            for loc in rule.location_ids:
                locations += self.env['stock.location'].search(
                    self._get_cycle_count_locations_search_domain(loc))
        return locations

    @api.model
    def _cycle_count_rules_to_compute(self):
        rules = self.cycle_count_rule_ids.search([
            ('rule_type', '!=', 'zero'), ('warehouse_ids', '=', self.id)])
        return rules

    @api.one
    def action_compute_cycle_count_rules(self):
        #_logger.info("****************************")
        #_logger.info("action_compute_cycle_count_rules")

        ''' Apply the rule in all the sublocations of a given warehouse(s) and
        returns a list with required dates for the cycle count of each
        location '''
        proposed_cycle_counts = []
        rules = self._cycle_count_rules_to_compute()

        #_logger.info("rules: %s" % rules)

        for rule in rules:
            locations = self._search_cycle_count_locations(rule)
            if locations:
                proposed_cycle_counts.extend(rule.compute_rule(locations))

        #_logger.info("proposed_cycle_counts: %s" % proposed_cycle_counts)

        if proposed_cycle_counts:
            locations = list(set([d['location'] for d in
                                  proposed_cycle_counts]))
            for loc in locations:
                proposed_for_loc = list(filter(lambda x: x['location'] == loc,
                                          proposed_cycle_counts))
                earliest_date = min([d['date'] for d in proposed_for_loc])
                cycle_count_proposed = list(filter(lambda x: x['date'] ==
                                              earliest_date,
                                              proposed_for_loc))[0]
                domain = [('location_id', '=', loc.id),
                          ('state', 'in', ['draft'])]

                #_logger.info("domain: %s" % domain)

                existing_cycle_counts = self.env['stock.cycle.count'].search(
                    domain)

                #_logger.info("existing_cycle_counts: %s" % existing_cycle_counts)

                if existing_cycle_counts:
                    existing_earliest_date = sorted(
                        existing_cycle_counts.mapped('date_deadline'))[0]

                    # Rui Franco 20190516
                    cycle_count_proposed_date = datetime.strptime(
                                                    cycle_count_proposed['date'],
                                                    DEFAULT_SERVER_DATETIME_FORMAT
                                                    ).date()

                    if cycle_count_proposed_date < existing_earliest_date:
                        cc_to_update = existing_cycle_counts.search([
                            ('date_deadline', '=', existing_earliest_date)])
                        cc_to_update.write({
                            'date_deadline': cycle_count_proposed_date,
                            'cycle_count_rule_id': cycle_count_proposed[
                                'rule_type'].id,
                        })
                delta = datetime.strptime(
                    cycle_count_proposed['date'],
                    DEFAULT_SERVER_DATETIME_FORMAT) - datetime.today()

                #_logger.info("delta.days: %s" % delta.days)
                #_logger.info("self.cycle_count_planning_horizon: %s" % self.cycle_count_planning_horizon)

                if not existing_cycle_counts and \
                        delta.days < self.cycle_count_planning_horizon:
                    self.env['stock.cycle.count'].create({
                        'date_deadline': cycle_count_proposed['date'],
                        'location_id': cycle_count_proposed['location'].id,
                        'cycle_count_rule_id': cycle_count_proposed[
                            'rule_type'].id,
                        'state': 'draft'
                    })

    @api.model
    def cron_cycle_count(self):
        whs = self.search([])
        whs.action_compute_cycle_count_rules()
        return True
