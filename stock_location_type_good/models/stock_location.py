# Copyright 2022 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    type_goods = fields.Selection(
        [
            ("fresh_goods", "Fresh Goods"),
            ("frozen_goods", "Frozen Goods"),
            ("dray_goods", "Dray Goods"),
            ("cool_goods", "Cool Goods"),
            ("icecream_goods", "Ice Cream Goods"),
        ],
    )
