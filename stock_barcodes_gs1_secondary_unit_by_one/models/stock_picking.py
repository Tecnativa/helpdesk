# Copyright 2019 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _prepare_barcode_wiz_vals(self, option_group=False):
        vals = super(StockPicking, self)._prepare_barcode_wiz_vals(
            option_group=option_group
        )
        vals[
            "set_secondary_unit_one_by_one"
        ] = option_group.set_secondary_unit_one_by_one
        if option_group.set_secondary_unit_one_by_one:
            vals["secondary_uom_qty"] = 1.0
        return vals
