# Copyright 2019 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _prepare_barcode_wiz_vals(self, option_group=False):
        vals = super(StockPicking, self)._prepare_barcode_wiz_vals(
            option_group=option_group
        )
        vals["auto_put_in_pack_on_read"] = option_group.auto_put_in_pack_on_read
        return vals
