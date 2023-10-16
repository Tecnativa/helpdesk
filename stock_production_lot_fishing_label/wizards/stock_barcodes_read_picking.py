# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, models
from odoo.exceptions import UserError


class WizStockBarcodesReadPicking(models.TransientModel):
    _inherit = "wiz.stock.barcodes.read.picking"

    def action_print_master_box(self):
        # TODO: Move to stock_barcodes_master_box changing dependencies
        #  of stock_production_lot_fishing_label
        report = self.env.ref(
            "stock_production_lot_fishing_label.action_label_master_box_report"
        )
        last_sml = self.picking_id.move_line_ids.filtered(
            lambda ln: ln.master_box_id == self.master_box_id
        ).sorted(key="write_date", reverse=True)[:1]
        if not last_sml:
            raise UserError(_("Master box is empty"))
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
