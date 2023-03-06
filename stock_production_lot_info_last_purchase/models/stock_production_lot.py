# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    @api.model
    def _get_last_lot_purchased(self, supplier, product):
        last_sml_purchased = self.env["stock.move.line"]
        if supplier:
            last_sml_purchased = self.env["stock.move.line"].search(
                [
                    ("product_id", "=", product.id),
                    ("lot_id", "!=", False),
                    ("picking_id.partner_id", "=", supplier.id),
                    ("picking_id.picking_type_code", "=", "incoming"),
                    ("location_id.usage", "=", "supplier"),
                ],
                order="date DESC",
                limit=1,
            )
        return last_sml_purchased.lot_id
