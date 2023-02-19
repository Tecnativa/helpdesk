# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _get_fields_for_new_lot(self):
        return [
            "fao_fishing_area_id",
            "fao_fishing_technique_id",
            "fishing_ship_id",
            "quality",
            # "packaging_date",
            "presentation_id",
            "harvesting_id",
            "country_id",
        ]

    def _get_value_production_lot(self):
        res = super()._get_value_production_lot()
        # 1 - Search last product lot for this supplier
        if self.picking_id.partner_id:
            last_sml_purchased = self.env["stock.move.line"].search(
                [
                    ("product_id", "=", self.product_id.id),
                    ("lot_id", "!=", False),
                    ("picking_id.partner_id", "=", self.picking_id.partner_id.id),
                    ("picking_id.picking_type_code", "=", "incoming"),
                    ("location_id.usage", "=", "supplier"),
                ],
                order="date DESC",
                limit=1,
            )
            if last_sml_purchased:
                for field in self._get_fields_for_new_lot():
                    if isinstance(last_sml_purchased.lot_id[field], models.BaseModel):
                        value = last_sml_purchased.lot_id[field].id
                    else:
                        value = last_sml_purchased.lot_id[field]
                    res[field] = value
        return res
