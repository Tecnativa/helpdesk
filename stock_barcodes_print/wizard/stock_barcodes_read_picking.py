# Copyright 2019 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging
import threading
from functools import partial

from odoo import fields, models, registry

_logger = logging.getLogger(__name__)


class WizStockBarcodesReadPicking(models.TransientModel):
    _inherit = "wiz.stock.barcodes.read.picking"

    auto_print_on_confirm = fields.Boolean(string="Auto print")

    def action_confirm(self):
        res = super().action_confirm()
        if (
            res
            and self.auto_print_on_confirm
            and self.picking_id.picking_type_id.print_label
            and self.picking_id.picking_type_id.default_label_report
        ):
            ICP = self.env["ir.config_parameter"].sudo()
            if ICP.get_param("stock_barcodes_print.print_in_new_thread"):
                # Get last sml from operations linked to this picking read wizard
                # Pass the id instead of recordset to load in a new thread to avoid
                # access to record with a closed record
                last_sml = self.move_line_ids.sorted(key="write_date", reverse=True)[:1]
                self._cr.postcommit.add(partial(self._launch_print_thread, last_sml.id))
            else:
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

    def _launch_print_thread(self, last_sml_id):
        threaded_calculation = threading.Thread(
            target=self.action_print_label_report_threaded,
            args=(self.picking_id.ids, last_sml_id),
        )
        threaded_calculation.start()

    def action_print_label_report_threaded(self, picking_id, last_sml_id):
        with registry(self._cr.dbname).cursor() as cr:
            self = self.with_env(self.env(cr=cr))
            picking = self.env["stock.picking"].browse(picking_id)
            report = picking.picking_type_id.default_label_report
            last_sml = self.env["stock.move.line"].browse(last_sml_id)
            wiz = (
                self.env["stock.picking.print"]
                .sudo()
                .with_context(
                    stock_move_line_to_print=last_sml.id,
                    active_model="stock.picking",
                    active_ids=picking.ids,
                )
                .create(
                    {
                        "barcode_report": report.id,
                    }
                )
            )
            wiz._onchange_picking_ids()
            report.print_document(wiz.product_print_moves.ids)
