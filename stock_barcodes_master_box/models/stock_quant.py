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
        force_secondary_qty_to_reserve = self.env.context.get(
            "force_secondary_qty_to_reserve", None
        )
        if (
            force_minimal_qty_to_reserve is not None
            and force_secondary_qty_to_reserve is not None
        ):
            tolerance_percent = 10
            quants_to_return = self.browse()
            mb_count = 0
            available_master_boxes = self.env["stock.quant.master.box"].browse()
            for quant in quants:
                if quant.package_id.master_box_id not in available_master_boxes:
                    available_master_boxes += quant.package_id.master_box_id
            for master_box in available_master_boxes:
                quants_in_mb = quants.filtered(
                    lambda q: q.package_id.master_box_id == master_box
                )
                quantity_in_mb = sum(quants_in_mb.mapped("quantity"))
                if quantity_in_mb > (
                    force_minimal_qty_to_reserve
                    - force_minimal_qty_to_reserve * tolerance_percent / 100
                ) and quantity_in_mb < (
                    force_minimal_qty_to_reserve
                    + force_minimal_qty_to_reserve * tolerance_percent / 100
                ):
                    quants_to_return += quants_in_mb
                    mb_count += 1
                    if mb_count >= force_secondary_qty_to_reserve:
                        return quants_to_return
            quants = quants_to_return + (
                quants.filtered("package_id.master_box_id") - quants_to_return
            )
        return quants
