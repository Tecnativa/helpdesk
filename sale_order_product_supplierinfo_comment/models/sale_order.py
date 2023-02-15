# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    supplierinfo_comment = fields.Text(
        compute="_compute_supplierinfo_comment", store=True,
    )

    @api.depends("supplierinfo_id")
    def _compute_supplierinfo_comment(self):
        for line in self:
            line.supplierinfo_comment = line.supplierinfo_id.comment
