# Copyright 2019 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from odoo import models

_logger = logging.getLogger(__name__)


class WizStockBarcodesReadPicking(models.TransientModel):
    _inherit = "wiz.stock.barcodes.read.picking"

    def action_confirm(self):
        # Auto put in pack for each barcode read
        if (
            not self.result_package_id
            and self.option_group_id.auto_put_in_pack_on_read
            and self.product_id.auto_put_in_pack_on_read
        ):
            self.action_create_package()
        return super().action_confirm()
