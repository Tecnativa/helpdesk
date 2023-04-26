# Copyright 2023 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import api, models


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.model
    def _prepare_merge_moves_distinct_fields(self):
        distinct_fields = super()._prepare_merge_moves_distinct_fields()
        distinct_fields.append("vendor_comment")
        return distinct_fields

    def _prepare_procurement_values(self):
        res = super()._prepare_procurement_values()
        res["vendor_comment"] = self.vendor_comment
        return res
