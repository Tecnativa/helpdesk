# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    @api.model
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

    def _compute_fao_fishing(self):
        picking_id = self.env.context.get("active_picking_id", False)
        if not picking_id:
            return super()._compute_fao_fishing()
        picking = self.env["stock.picking"].browse(picking_id)
        processed_lots = self.browse()
        for lot in self:
            last_lot = lot._get_last_lot_purchased(picking)
            if not last_lot:
                continue
            for field_name in self._get_fields_for_new_lot():
                lot[field_name] = last_lot[field_name]
            processed_lots += lot
        return super(StockProductionLot, self - processed_lots)._compute_fao_fishing()

    def _get_last_lot_purchased(self, picking):
        last_sml_purchased = self.env["stock.move.line"]
        if picking.partner_id:
            last_sml_purchased = self.env["stock.move.line"].search(
                [
                    ("picking_id", "!=", picking.id),
                    ("product_id", "=", self.product_id.id),
                    ("lot_id", "!=", False),
                    ("picking_id.partner_id", "=", picking.partner_id.id),
                    ("picking_id.picking_type_code", "=", "incoming"),
                    ("location_id.usage", "=", "supplier"),
                ],
                order="date DESC",
                limit=1,
            )
        return last_sml_purchased.lot_id
