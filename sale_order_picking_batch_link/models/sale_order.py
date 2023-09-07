# Copyright 2023 Tecnativa - Stefan Ungureanu
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    picking_batch_ids = fields.Many2many(
        comodel_name="stock.picking.batch",
        string="Batch Pickings",
        compute="_compute_picking_batch_ids",
        compute_sudo=True,
    )

    @api.depends("picking_ids", "picking_ids.batch_id")
    def _compute_picking_batch_ids(self):
        for order in self:
            order.picking_batch_ids = order.picking_ids.batch_id
