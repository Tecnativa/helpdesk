# Copyright 2023 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class StockMoveLine(models.Model):
    _inherit = ["stock.move.line", "barcode.gs1.label.mixin"]
    _name = "stock.move.line"
    _qty_field = ["qty_done"]
