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

    def button_validate(self):
        if (
            self.picking_type_id.barcode_option_group_id.auto_put_in_pack
            and not self.move_line_ids.mapped("result_package_id")
        ):
            self.action_put_in_pack()
        return super().button_validate()
