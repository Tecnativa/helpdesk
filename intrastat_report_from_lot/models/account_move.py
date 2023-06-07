# Copyright 2023 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_intrastat_line_vals(self, line):
        """Take product origin country from lot."""
        vals = super()._get_intrastat_line_vals(line)
        lot_country = line.move_line_ids.lot_ids.country_id[:1].country_id
        if lot_country:
            lot_country_code = self.env["res.partner"]._get_intrastat_country_code(
                lot_country
            )
            vals.update(
                product_origin_country_id=lot_country.id,
                product_origin_country_code=lot_country_code,
            )
        return vals
