# Copyright 2019 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.tools import groupby


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    has_lot_mixed = fields.Boolean(compute="_compute_has_lot_mixed")

    @api.depends("move_line_ids")
    def _compute_has_lot_mixed(self):
        self.has_lot_mixed = False
        for batch in self:
            for product, lots in groupby(  # noqa: B007
                batch.move_line_ids.lot_id, key=lambda ln: ln.product_id
            ):
                if len(lots) > 1:
                    batch.has_lot_mixed = True
                    break

    def action_print_label_mixed_lot(self):
        """Print label lots for lots"""
        self.ensure_one()
        lots_to_print_label = self.env["stock.production.lot"].browse()
        for product, lots in groupby(  # noqa: B007
            self.move_line_ids.lot_id, key=lambda ln: ln.product_id
        ):
            if len(lots) > 1:
                for lot in lots:
                    lots_to_print_label += lot
        return self.env.ref("stock.action_report_lot_label").report_action(
            lots_to_print_label
        )
