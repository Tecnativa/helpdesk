# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockQuantPackage(models.Model):
    _inherit = "stock.quant.package"

    master_box_id = fields.Many2one(
        comodel_name="stock.quant.master.box", ondelete="restrict"
    )
