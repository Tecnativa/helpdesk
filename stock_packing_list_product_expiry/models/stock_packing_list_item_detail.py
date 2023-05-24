# Copyright 2023 Tecnativa - Sergio Teruel
# Copyright 2023 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockPackingListDetail(models.Model):
    _inherit = "stock.packing.list.detail"

    scientific_name_ids = fields.Many2many(
        related="stock_move_line_id.product_id.scientific_name_ids"
    )
    packaging_date = fields.Datetime(related="stock_move_line_id.lot_id.packaging_date")
    expiration_date = fields.Datetime(
        related="stock_move_line_id.lot_id.expiration_date"
    )
