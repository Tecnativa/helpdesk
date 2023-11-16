# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    master_box_id = fields.Many2one(related="package_id.master_box_id")
    result_master_box_id = fields.Many2one(related="result_package_id.master_box_id")
