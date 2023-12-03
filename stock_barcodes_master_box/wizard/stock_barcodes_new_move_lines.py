# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import threading
from functools import partial

from odoo import api, fields, models, registry


class WizStockBarcodesNewMoveLines(models.TransientModel):
    _name = "wiz.stock.barcodes.new.move.lines"
    _description = "Generate new stock move lines according a wizard values"

    """

    Procesame 200kg en paquetes de 2Kg y Masterboxes de 10 paquetes

    """
    stock_barcode_wiz_id = fields.Many2one(
        comodel_name="wiz.stock.barcodes.read.picking", readonly=True
    )
    product_id = fields.Many2one(related="stock_barcode_wiz_id.product_id")
    product_uom = fields.Many2one(related="stock_barcode_wiz_id.product_uom_id")

    product_uom_qty = fields.Float("Product Qty", digits="Product Unit of Measure")
    package_qty = fields.Float(
        string="Quantity per package", digits="Product Unit of Measure"
    )
    master_box_qty = fields.Float(
        string="Packages by master box", digits="Product Unit of Measure"
    )

    total_packages = fields.Integer(compute="_compute_total")
    total_master_box = fields.Integer(compute="_compute_total")

    # Qty pending of read for a product
    product_uom_qty_pending = fields.Float(
        "Pending Qty",
        digits="Product Unit of Measure",
        compute="_compute_product_uom_qty_pending",
    )
    print_master_box_label = fields.Boolean(default=True)

    @api.depends("product_uom_qty", "package_qty", "master_box_qty")
    def _compute_total(self):
        total_packages = self.product_uom_qty / (self.package_qty or 1.0)
        total_master_box = (
            self.master_box_qty and total_packages / (self.master_box_qty or 1.0) or 0.0
        )
        self.total_packages = total_packages
        self.total_master_box = total_master_box

    @api.depends("product_id")
    def _compute_product_uom_qty_pending(
        self,
    ):
        product_uom_qty = 0.0
        qty_done = 0.0
        for pending_move in self.stock_barcode_wiz_id.pending_move_ids.filtered(
            lambda ln: ln.product_id == self.product_id
        ):
            product_uom_qty += pending_move.product_uom_qty
            qty_done += pending_move.qty_done
        self.product_uom_qty_pending = product_uom_qty - qty_done

    def action_confirm(self):
        if self.product_uom_qty > self.product_uom_qty_pending:
            # TODO: Any restriction??
            pass
        self.stock_barcode_wiz_id.master_box_id = False
        wiz_autoprint = self.stock_barcode_wiz_id.auto_print_on_confirm
        self.stock_barcode_wiz_id.auto_print_on_confirm = False
        max_packages = self.total_master_box * int(self.master_box_qty)
        elements_count = self.total_master_box and max_packages or self.total_packages
        sml_ids = []
        new_master_box_ids = []
        for package_index in range(elements_count):
            if self.master_box_qty and package_index % self.master_box_qty == 0:
                # new master box
                new_master_box = self.env["stock.quant.master.box"].create({})
                self.stock_barcode_wiz_id.master_box_id = new_master_box
                new_master_box_ids.append(new_master_box.id)
            # New package
            new_package = self.env["stock.quant.package"].create({})
            self.stock_barcode_wiz_id.result_package_id = new_package
            self.stock_barcode_wiz_id.product_qty = self.package_qty
            # Confirming each package
            if package_index < elements_count - 1:
                sml_dict = self.stock_barcode_wiz_id.with_context(
                    skip_clean_values=True
                ).action_confirm()
            else:
                sml_dict = self.stock_barcode_wiz_id.action_confirm()
            sml_ids.extend(sml_dict.keys())
        if wiz_autoprint:
            # Print each sml if the barcode wizard has checked the autoprint
            self._action_print_move_lines(sml_ids)
            self.stock_barcode_wiz_id.auto_print_on_confirm = wiz_autoprint
        if new_master_box_ids and self.print_master_box_label:
            # Print all masterbox in new thread
            self.stock_barcode_wiz_id.action_print_master_box(new_master_box_ids)
        self.stock_barcode_wiz_id.master_box_id = False
        # Recompute moves todo
        self.stock_barcode_wiz_id.fill_todo_records()
        return {"type": "ir.actions.act_window_close"}

    def _action_print_move_lines(self, move_line_ids):
        ICP = self.env["ir.config_parameter"].sudo()
        if ICP.get_param("stock_barcodes_print.print_in_new_thread"):
            self._cr.postcommit.add(
                partial(
                    self._launch_print_thread,
                    self.stock_barcode_wiz_id.picking_id.id,
                    move_line_ids,
                )
            )
        else:
            pass
            # return self.action_print_label_report()

    def _launch_print_thread(self, picking_id, last_sml_ids):
        threaded_calculation = threading.Thread(
            target=self._action_print_move_lines_threaded,
            args=(picking_id, last_sml_ids),
        )
        threaded_calculation.start()

    def _action_print_move_lines_threaded(self, picking_id, move_line_ids):
        with registry(self._cr.dbname).cursor() as cr:
            self = self.with_env(self.env(cr=cr))
            picking = self.env["stock.picking"].browse(picking_id)
            report = picking.picking_type_id.default_label_report
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
