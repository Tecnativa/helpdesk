# Copyright 2023 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import models


class StockProductionLot(models.Model):
    _inherit = ["stock.production.lot", "barcode.gs1.label.mixin"]
    _name = "stock.production.lot"
