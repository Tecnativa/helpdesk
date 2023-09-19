# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    def _gather(
        self,
        product_id,
        location_id,
        lot_id=None,
        package_id=None,
        owner_id=None,
        strict=False,
    ):
        quants = super()._gather(
            product_id, location_id, lot_id, package_id, owner_id, strict
        )
        force_minimal_qty_to_reserve = self.env.context.get(
            "force_minimal_qty_to_reserve", None
        )
        if force_minimal_qty_to_reserve is not None:
            quants = quants.filtered("package_id.master_box_id")
        return quants
