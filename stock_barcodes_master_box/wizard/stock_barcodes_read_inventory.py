# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class WizStockBarcodesReadInventory(models.TransientModel):
    _inherit = "wiz.stock.barcodes.read.inventory"

    master_box_id = fields.Many2one(comodel_name="stock.quant.master.box")

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
            return False
        # Retrieve master box quants to generate inventory if needed
        for quant in quants:
            # The location already read by user
            self.set_info_from_quants(quant)
            self.action_confirm()
        return True
