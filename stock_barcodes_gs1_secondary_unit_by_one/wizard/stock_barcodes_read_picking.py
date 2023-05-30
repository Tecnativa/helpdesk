# Copyright 2019 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from odoo import models

_logger = logging.getLogger(__name__)


class WizStockBarcodesReadPicking(models.TransientModel):
    _inherit = "wiz.stock.barcodes.read.picking"

    def action_done(self):
        res = super().action_done()
        if res and self.set_secondary_unit_one_by_one and self.secondary_uom_id:
            self.secondary_uom_qty = 1.0
        return res
