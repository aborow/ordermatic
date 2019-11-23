# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class UpdatePartnerAddress(models.TransientModel):

	_name = "update.partner.address"

	@api.multi
	def update_partner_address(self):
		# Method is used to change value of partner's address based on child address.
		domain = [('parent_id','!=',False)]
		child_partner_ids = self.env['res.partner'].search(domain)
		parent_partner_ids = [partner.parent_id for partner in child_partner_ids if not partner.parent_id.street and not partner.parent_id.street2 and not partner.parent_id.city and not partner.parent_id.city and not partner.parent_id.state_id and not partner.parent_id.zip and not partner.parent_id.country_id]
		for parent_partner_id in parent_partner_ids:
			for child_partner_id in child_partner_ids:
				if child_partner_id.parent_id.id == parent_partner_id.id:
					if child_partner_id.street or child_partner_id.street2 or child_partner_id.city or child_partner_id.state_id or child_partner_id.zip or child_partner_id.country_id:
						parent_partner_id.write({
							'street':child_partner_id.street,
							'street2':child_partner_id.street2,
							'city':child_partner_id.city,
							'state_id':child_partner_id.state_id.id,
							'zip':child_partner_id.zip,
							'country_id':child_partner_id.country_id.id
							})