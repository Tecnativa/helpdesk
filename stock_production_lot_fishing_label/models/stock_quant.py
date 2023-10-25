# Copyright 2023 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import models


class StockQuant(models.Model):
    _inherit = ["stock.quant", "barcode.gs1.label.mixin"]
    _name = "stock.quant"
    _qty_field = ["quantity"]
