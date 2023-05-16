# Copyright 2019 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def action_print_label_report(self):
        action = self.env["ir.actions.act_window"]._for_xml_id(
            "stock_picking_product_barcode_report.act_stock_barcode_selection_printing"
        )
        action["context"] = {
            "active_model": "stock.picking",
            "active_ids": self.picking_id.ids,
        }
        return action
