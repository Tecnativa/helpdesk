# Copyright 2023 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductPrintingQty(models.TransientModel):
    _inherit = "stock.picking.line.print"

    result_package_id = fields.Many2one(
        comodel_name="stock.quant.package", related="move_line_id.result_package_id"
    )


class WizStockBarcodeSelectionPrinting(models.TransientModel):
    _inherit = "stock.picking.print"

    @api.model
    def _get_move_lines(self, picking):
        if self.barcode_report == self.env.ref(
            "stock_production_lot_fishing_label.action_label_fishing_report"
        ):
            return picking.move_line_ids.filtered(
                lambda ml: ml.product_id.default_code and ml.lot_id
            )
        elif self.barcode_report == self.env.ref(
            "stock_production_lot_fishing_label.action_label_fishing_report_mini"
        ):
            return picking.move_line_ids.filtered("result_package_id")
        return super()._get_move_lines(picking)
