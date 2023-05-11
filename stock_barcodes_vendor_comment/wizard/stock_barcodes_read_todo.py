# Copyright 2023 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class WizStockBarcodesReadTodo(models.TransientModel):
    _inherit = "wiz.stock.barcodes.read.todo"

    vendor_id = fields.Many2one(
        comodel_name="res.partner",
        compute="_compute_vendor_fields",
    )
    vendor_comment = fields.Char(compute="_compute_vendor_fields")

    def _compute_vendor_fields(self):
        for line in self:
            moves = line.stock_move_ids or line.line_ids.mapped("move_id")
            line.vendor_id = moves[:1].vendor_id
            line.vendor_comment = moves[:1].vendor_comment

    @api.model
    def fields_to_fill_from_pending_line(self):
        res = super().fields_to_fill_from_pending_line()
        res.extend(["vendor_id", "vendor_comment"])
        return res
