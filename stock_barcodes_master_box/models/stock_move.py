# Copyright 2023 Tecnativa - Carlos Dauden
# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    is_master_box = fields.Boolean(related="secondary_uom_id.is_master_box")

    def _get_available_quantity(
        self,
        location_id,
        lot_id=None,
        package_id=None,
        owner_id=None,
        strict=False,
        allow_negative=False,
    ):
        self.ensure_one()
        if self.is_master_box:
            self = self.with_context(
                force_minimal_qty_to_reserve=self.secondary_uom_id.factor,
                force_secondary_qty_to_reserve=self.secondary_uom_qty,
            )
        return super(StockMove, self)._get_available_quantity(
            location_id,
            lot_id=lot_id,
            package_id=package_id,
            owner_id=owner_id,
            strict=strict,
            allow_negative=allow_negative,
        )

    def _update_reserved_quantity(
        self,
        need,
        available_quantity,
        location_id,
        lot_id=None,
        package_id=None,
        owner_id=None,
        strict=True,
    ):
        self.ensure_one()
        if self.is_master_box:
            self = self.with_context(
                force_minimal_qty_to_reserve=self.secondary_uom_id.factor,
                force_secondary_qty_to_reserve=self.secondary_uom_qty,
            )
        return super(StockMove, self)._update_reserved_quantity(
            need, available_quantity, location_id, lot_id, package_id, owner_id, strict
        )
