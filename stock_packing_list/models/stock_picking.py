# Copyright 2023 Tecnativa - Sergio Teruel
# Copyright 2023 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    packing_list_item_ids = fields.One2many(
        comodel_name="stock.packing.list.item",
        inverse_name="picking_id",
        string="Packing List Items",
    )
