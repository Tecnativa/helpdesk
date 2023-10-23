# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models
from odoo.exceptions import UserError


class WizStockBarcodesReadPicking(models.TransientModel):
    _inherit = "wiz.stock.barcodes.read.picking"

    master_box_id = fields.Many2one(comodel_name="stock.quant.master.box")

    def action_clean_master_box(self):
        self.master_box_id = False

    def action_create_master_box(self):
        self.master_box_id = self.env["stock.quant.master.box"].create({})

    def _assig_master_box_to_package(self, sml):
        if sml.result_package_id.master_box_id != self.master_box_id:
            sml.result_package_id.master_box_id = self.master_box_id

    def _update_stock_move_line(self, line, sml_vals):
        res = super()._update_stock_move_line(line, sml_vals)
        self._assig_master_box_to_package(line)
        return res

    def create_new_stock_move_line(self, moves_todo, available_qty):
        sml = super().create_new_stock_move_line(moves_todo, available_qty)
        self._assig_master_box_to_package(sml)
        return sml

    def action_print_master_box(self):
        # TODO: Mover desde donde se imprime ahora la etiqueta de master box
        pass

    def process_barcode_master_box_id(self):
        if self.env.context.get("force_master_box", False):
            master_box = self.master_box_id.name
        else:
            master_box = self.barcode
        quant_domain = [
            ("package_id.master_box_id.name", "=", master_box),
        ]
        quants = self.env["stock.quant"].search(quant_domain)
        if not quants:
            self._set_messagge_info("more_match", _("Master box not fount"))
            return False
        # Retrieve master box quants to generate sml if needed
        sml_vals_list = []
        for quant in quants:
            sml = self.picking_id.move_line_ids.filtered(
                lambda ln: ln.package_id
                and ln.product_id == quant.product_id
                and ln.package_id == quant.package_id
                and ln.lot_id == quant.lot_id
            )
            if sml:
                sml.qty_done = quant.quantity
            else:
                if self.product_id != quant.product_id:
                    self._set_messagge_info(
                        "not_found", _("Master box contains other product")
                    )
                    return False
                sml_vals_list.append(
                    {
                        "company_id": self.picking_id.company_id.id,
                        "picking_id": self.picking_id.id,
                        "product_id": quant.product_id.id,
                        "product_uom_id": self.product_uom_id.id,
                        "location_id": quant.location_id.id,
                        "location_dest_id": self.location_dest_id.id,
                        "lot_id": quant.lot_id.id,
                        "package_id": quant.package_id.id,
                        "result_package_id": quant.package_id.id,
                        "owner_id": quant.owner_id.id,
                        "secondary_uom_id": self.secondary_uom_id.id,
                        "qty_done": quant.quantity,
                    }
                )
        if sml_vals_list:
            self.env["stock.move.line"].create(sml_vals_list)
        # Recalcular moves todo
        # self.fill_todo_records()
        # self._compute_todo_line_display_ids()
        return True

    def action_mass_move_lines(self):
        if not self.product_id:
            raise UserError(_("There is no product readed"))
        ctx = dict(self.env.context, default_stock_barcode_wiz_id=self.id)
        return {
            "type": "ir.actions.act_window",
            "res_model": "wiz.stock.barcodes.new.move.lines",
            "view_mode": "form",
            "target": "new",
            "context": ctx,
        }
