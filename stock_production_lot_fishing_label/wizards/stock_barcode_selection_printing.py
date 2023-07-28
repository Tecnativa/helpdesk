# Copyright 2023 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class WizStockBarcodeSelectionPrinting(models.TransientModel):
    _inherit = "stock.picking.print"

    is_summary_label = fields.Boolean()
    can_be_summarized = fields.Boolean(related="barcode_report.can_be_summarized")

    @api.model
    def _get_move_lines(self, picking):
        stock_move_lines = super()._get_move_lines(picking)
        if self.is_summary_label:
            return picking.move_line_ids.filtered("qty_done")
        if self.barcode_report in [
            self.env.ref(
                "stock_production_lot_fishing_label.action_label_fishing_report"
            ),
            self.env.ref(
                "stock_production_lot_fishing_label.action_label_fishing_nutritional_report"
            ),
        ]:
            return stock_move_lines.filtered(
                lambda ml: ml.product_id.default_code and ml.lot_id
            )
        elif self.barcode_report == self.env.ref(
            "stock_production_lot_fishing_label.action_label_fishing_report_mini"
        ):
            return stock_move_lines.filtered("result_package_id")
        return stock_move_lines

    @api.onchange("picking_ids", "barcode_report", "is_summary_label")
    def _onchange_picking_ids(self):
        # We don't make a direct assignation to avoid set summary label when it can be
        # summarized.
        if not self.can_be_summarized:
            self.is_summary_label = False
        return super()._onchange_picking_ids()
