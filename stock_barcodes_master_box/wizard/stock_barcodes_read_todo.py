# Copyright 2023 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class WizStockBarcodesReadTodo(models.TransientModel):
    _inherit = "wiz.stock.barcodes.read.todo"

    def _group_key(self, wiz, line):
        key = super()._group_key(wiz, line)
        if wiz.option_group_id.group_key_for_todo_records:
            return key
        if (
            wiz.option_group_id.source_pending_moves == "move_line_ids"
            and line.secondary_uom_id.is_master_box
        ):
            return (line.location_id, line.product_id, line.lot_id, line.master_box_id)
        return key

    def todo_values_after_hook(self, todo_vals):
        for elem in todo_vals.values():
            secondary_uom_id = elem.get("secondary_uom_id", False)
            if secondary_uom_id:
                secondary_uom = self.env["product.secondary.unit"].browse(
                    secondary_uom_id
                )
                if secondary_uom.is_master_box:
                    elem["secondary_uom_qty"] = (
                        elem["product_uom_qty"] / secondary_uom.factor or 1.0
                    )
        return todo_vals
