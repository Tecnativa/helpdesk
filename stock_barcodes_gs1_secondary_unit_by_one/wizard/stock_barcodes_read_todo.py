# Copyright 2023 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class WizStockBarcodesReadTodo(models.TransientModel):
    _inherit = "wiz.stock.barcodes.read.todo"

    def fill_from_pending_line(self):
        res = super().fill_from_pending_line()
        if self.wiz_barcode_id.set_secondary_unit_one_by_one:
            self.wiz_barcode_id.secondary_uom_qty = 1.0
        return res
