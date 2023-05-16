# Copyright 2019 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from odoo import models

_logger = logging.getLogger(__name__)


class WizStockBarcodesReadPicking(models.TransientModel):
    _inherit = "wiz.stock.barcodes.read.picking"

    def action_confirm(self):
        res = super(WizStockBarcodesReadPicking, self).action_confirm()
        if (
            res
            and self.picking_id.picking_type_id.print_label
            and self.picking_id.picking_type_id.default_label_report
        ):
            return self.action_print_label_report()
        return res

    def action_print_label_report(self):
        report = self.picking_id.picking_type_id.default_label_report
        last_sml = self.picking_id.move_line_ids.sorted(key="write_date", reverse=True)[
            :1
        ]
        wiz = (
            self.env["stock.picking.print"]
            .with_context(
                stock_move_line_to_print=last_sml.id,
                active_model="stock.picking",
                active_ids=self.picking_id.ids,
            )
            .create(
                {
                    "barcode_report": report.id,
                }
            )
        )
        wiz._onchange_picking_ids()
        return wiz.print_labels()
