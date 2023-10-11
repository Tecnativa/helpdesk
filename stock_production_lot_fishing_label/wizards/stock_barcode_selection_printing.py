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
