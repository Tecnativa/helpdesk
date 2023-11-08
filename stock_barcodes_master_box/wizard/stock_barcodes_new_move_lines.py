# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


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

        max_packages = self.total_master_box * int(self.master_box_qty)
        elements_count = self.total_master_box and max_packages or self.total_packages
        for package_index in range(elements_count):
            if self.master_box_qty and package_index % self.master_box_qty == 0:
                # If there is a previous masterbox print the label
                if (
                    self.print_master_box_label
                    and self.stock_barcode_wiz_id.master_box_id
                ):
                    self.stock_barcode_wiz_id.action_print_master_box()
                # new master box
                new_master_box = self.env["stock.quant.master.box"].create({})
                self.stock_barcode_wiz_id.master_box_id = new_master_box
            # New package
            new_package = self.env["stock.quant.package"].create({})
            self.stock_barcode_wiz_id.result_package_id = new_package
            self.stock_barcode_wiz_id.product_qty = self.package_qty
            # Confirming each package
            if package_index < elements_count - 1:
                self.stock_barcode_wiz_id.with_context(
                    skip_clean_values=True
                ).action_confirm()
            else:
                self.stock_barcode_wiz_id.action_confirm()
        self.stock_barcode_wiz_id.master_box_id = False

        # Recompute moves todo
        self.stock_barcode_wiz_id.fill_todo_records()
        return {"type": "ir.actions.act_window_close"}
