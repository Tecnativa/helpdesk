# Copyright 2023 Tecnativa - Sergio Teruel
# Copyright 2023 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockPackingListDetail(models.Model):
    _name = "stock.packing.list.detail"
    _description = "Stock packing list detail"

    name = fields.Char(readonly=True, compute="_compute_name")
    stock_move_line_id = fields.Many2one(
        comodel_name="stock.move.line",
        domain="[('id', 'in', parent.picking_move_line_ids)]",
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        compute="_compute_product_id",
        store=True,
        readonly=False,
    )
    lot_id = fields.Many2one(related="stock_move_line_id.lot_id")
    result_package_id = fields.Many2one(related="stock_move_line_id.result_package_id")
    qty = fields.Float(required=True, default=1.0)
    packing_list_item_id = fields.Many2one(
        comodel_name="stock.packing.list.item",
        string="Packing List Box",
        required=True,
        index=True,
        ondelete="cascade",
    )
    picking_id = fields.Many2one(
        comodel_name="stock.picking",
        string="Picking",
        related="packing_list_item_id.picking_id",
    )

    @api.depends("product_id", "qty")
    def _compute_name(self):
        for item in self:
            item.name = "{} - {}".format(item.product_id.display_name, item.qty)

    @api.depends("stock_move_line_id")
    def _compute_product_id(self):
        for item in self:
            item.product_id = item.stock_move_line_id.product_id
