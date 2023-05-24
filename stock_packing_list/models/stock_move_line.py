# Copyright 2023 Tecnativa - Sergio Teruel
# Copyright 2023 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def action_put_into_packing_list_box(self):
        packing_packing_list_item_id = self.env.context.get(
            "packing_list_item_id", False
        )
        vals_list = []
        for sml in self:
            vals_list.append(
                {
                    "packing_list_item_id": packing_packing_list_item_id,
                    "stock_move_line_id": sml.id,
                    "qty": sml.qty_done * (sml.product_id.weight or 1.0),
                }
            )
        self.env["stock.packing.list.detail"].create(vals_list)
