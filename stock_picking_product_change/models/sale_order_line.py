# Copyright 2019 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    replaced_qty = fields.Float(
        string="Replaced qty",
        digits="Product Unit of Measure",
        readonly=True,
    )
