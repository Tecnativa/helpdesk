# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


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
