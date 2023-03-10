# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from collections import defaultdict

from odoo import models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def _create_and_assign_production_lot(self):
        res = super(StockMoveLine, self)._create_and_assign_production_lot()
        picking_dic = defaultdict(lambda: self.browse())
        for sml in self:
            picking_dic[sml.picking_id.id] += sml
        for picking_id, move_lines in picking_dic.items():
            move_lines.mapped("lot_id").with_context(
                active_picking_id=picking_id
            )._compute_fao_fishing()
        return res
