# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    # qty_available = fields.Float(related="product_id.qty_available")

    def do_purchase_order(self):
        pass
