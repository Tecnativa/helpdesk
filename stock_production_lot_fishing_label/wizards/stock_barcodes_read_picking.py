# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import threading
from functools import partial

from odoo import _, models, registry
from odoo.exceptions import UserError


class WizStockBarcodesReadPicking(models.TransientModel):
    _inherit = "wiz.stock.barcodes.read.picking"

    def action_print_master_box(self, master_box_ids=None):
        # TODO: Move to stock_barcodes_master_box changing dependencies
        #  of stock_production_lot_fishing_label
        last_sml_ids = []
        if master_box_ids is None:
            last_sml_ids = (
                self.picking_id.move_line_ids.filtered(
                    lambda ln: ln.result_package_id.master_box_id == self.master_box_id
                )
                .sorted(key="write_date", reverse=True)[:1]
                .ids
            )
        else:
            # Obtener un sml de cada masterbox
            for mb_id in master_box_ids:
                smls = self.picking_id.move_line_ids.filtered(
                    lambda ln: ln.result_package_id.master_box_id.id == mb_id
                ).sorted(key="write_date", reverse=True)[:1]
                if smls.result_package_id.master_box_id.id not in last_sml_ids:
                    last_sml_ids.append(smls.id)
        if not last_sml_ids:
            raise UserError(_("Master box is empty"))
        ICP = self.env["ir.config_parameter"].sudo()
        if ICP.get_param("stock_barcodes_print.print_in_new_thread"):
            self._cr.postcommit.add(
                partial(
                    self._launch_print_thread_master_box,
                    self.picking_id.id,
                    last_sml_ids,
                )
            )

    def _launch_print_thread_master_box(self, picking_id, last_sml_ids):
        threaded_calculation = threading.Thread(
            target=self._action_print_master_box_threaded,
            args=(picking_id, last_sml_ids),
        )
        threaded_calculation.start()

    def _action_print_master_box_threaded(self, picking_id, move_line_ids):
        with registry(self._cr.dbname).cursor() as cr:
            self = self.with_env(self.env(cr=cr))
            report = self.env.ref(
                "stock_production_lot_fishing_label.action_label_master_box_report"
            )
            wiz = (
                self.env["stock.picking.print"]
                .sudo()
                .with_context(
                    stock_move_line_to_print=move_line_ids,
                    active_model="stock.picking",
                    active_ids=[picking_id],
                )
                .create(
                    {
                        "barcode_report": report.id,
                    }
                )
            )
            wiz._onchange_picking_ids()
            report.print_document(wiz.product_print_moves.ids)
