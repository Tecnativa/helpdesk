# Copyright 2019 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class WizStockBarcodesReadPicking(models.TransientModel):
    _inherit = "wiz.stock.barcodes.read.picking"

    auto_put_in_pack_on_read = fields.Boolean(string="Auto package")

    def action_confirm(self):
        # Auto put in pack for each barcode read
        if not self.result_package_id and self.auto_put_in_pack_on_read:
            self.action_create_package()
        res = super().action_confirm()
        if (
            self.result_package_id
            and self.auto_put_in_pack_on_read
            and not self.keep_result_package
        ):
            self.result_package_id = False
        return res
