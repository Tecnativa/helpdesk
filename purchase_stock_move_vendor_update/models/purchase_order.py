# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def write(self, vals):
        res = super().write(vals)
        if "partner_id" not in vals:
            return res
        for purchase in self:
            purchase.order_line.order_id = purchase
        return res


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    def write(self, vals):
        res = super().write(vals)
        if "order_id" not in vals:
            return res
        # TODO: Improve performance extracting search from loop
        StockMove = self.env["stock.move"]
        for line in self:
            all_moves_ids = False
            if line.state in ["draft", "sent", "to approve"]:
                move = StockMove.search([("created_purchase_line_id", "=", line.id)])
                all_moves_ids = move._rollup_move_dests({move.id})
            if line.state in ["purchase", "done"]:
                all_moves_ids = line.move_dest_ids._rollup_move_dests(
                    set(line.move_dest_ids.ids)
                )
            if all_moves_ids:
                all_moves = StockMove.browse(all_moves_ids)
                all_moves = all_moves.filtered(
                    lambda ln: ln.vendor_id != line.order_id.partner_id
                )
                all_moves.vendor_id = line.order_id.partner_id
        return res
