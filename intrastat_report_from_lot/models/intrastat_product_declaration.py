# Copyright 2023 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class IntrastatProductDeclaration(models.Model):
    _inherit = "intrastat.product.declaration"

    def _gather_invoices(self, notedict):
        """Take product origin country from lot."""
        lines = super()._gather_invoices(notedict)
        for line_vals in lines:
            inv_line = self.env["account.move.line"].browse(
                line_vals["invoice_line_id"]
            )
            invoice = inv_line.move_id
            inv_intrastat_line = invoice.intrastat_line_ids.filtered(
                lambda r: r.invoice_line_id == inv_line
            )
            if not inv_intrastat_line:
                lot_country = inv_line.move_line_ids.lot_ids.country_id[:1].country_id
                if lot_country:
                    lot_country_code = self._get_product_origin_country_code(
                        inv_line, lot_country, notedict
                    )
                    line_vals.update(
                        product_origin_country_id=lot_country.id,
                        product_origin_country_code=lot_country_code,
                    )
        return lines
