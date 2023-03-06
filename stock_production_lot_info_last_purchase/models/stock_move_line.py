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

    def _mapped_field_values(self, lot, as_default=False):
        field_values = {}
        for field in self._get_fields_for_new_lot():
            if isinstance(lot[field], models.BaseModel):
                value = lot[field].id
            else:
                value = lot[field]
            field_values.update(
                {("default_{}" if as_default else "{}").format(field): value}
            )
        return field_values

    def _get_value_production_lot(self):
        res = super()._get_value_production_lot()
        # 1 - Search last product lot for this supplier
        if self.picking_id.partner_id:
            last_lot_purchased = self.env[
                "stock.production.lot"
            ]._get_last_lot_purchased(self.picking_id.partner_id, self.product_id)
            if last_lot_purchased:
                res.update(self._mapped_field_values(last_lot_purchased))
        return res

    def action_generate_lot(self):
        self.ensure_one()
        last_lot_purchased = self.env["stock.production.lot"]._get_last_lot_purchased(
            self.picking_id.partner_id, self.product_id
        )
        ctx = self.env.context.copy()
        ctx.update(self._mapped_field_values(last_lot_purchased, as_default=True))
        new_lot = self.env["ir.sequence"].next_by_code("stock.lot.serial")
        self.lot_id = (
            self.env["stock.production.lot"]
            .with_context(**ctx)
            .create(
                {
                    "product_id": self.product_id.id,
                    "company_id": self.company_id.id,
                    "name": new_lot,
                }
            )
        )
