# Copyright 2023 Tecnativa - Sergio Teruel
# Copyright 2023 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class StockPackingListItem(models.Model):
    _name = "stock.packing.list.item"
    _description = "Stock packing list items"
    _order = "pallet_number asc, item_number asc"

    name = fields.Char(readonly=True, compute="_compute_name")
    package_type_id = fields.Many2one(comodel_name="stock.package.type")
    package_quantity = fields.Integer(default=1)
    pallet_number = fields.Integer(default=0)
    item_number = fields.Integer(compute="_compute_item_number", store=True)
    item_length = fields.Float(
        required=True,
        compute="_compute_item_measures",
        store=True,
        readonly=False,
    )
    width = fields.Float(
        required=True,
        compute="_compute_item_measures",
        store=True,
        readonly=False,
    )
    height = fields.Float(
        required=True,
        compute="_compute_item_measures",
        store=True,
        readonly=False,
    )
    weight = fields.Float(default=0, digits="Stock Weight")
    volume = fields.Float(compute="_compute_volume", digits="Volume")
    item_size = fields.Char(compute="_compute_item_size")
    picking_id = fields.Many2one(
        comodel_name="stock.picking",
        string="Picking",
        required=True,
        index=True,
        ondelete="cascade",
    )
    list_item_detail_ids = fields.One2many(
        comodel_name="stock.packing.list.detail",
        inverse_name="packing_list_item_id",
        string="Details",
    )
    is_pallet = fields.Boolean(string="Is a pallet?", default=False)
    total_boxes_weight = fields.Float(
        readonly=True,
        compute="_compute_total_boxes_weight",
    )
    total_pallet_weight = fields.Float(
        compute="_compute_total_pallet_weight",
    )
    total_boxes_volume = fields.Float(
        readonly=True,
        compute="_compute_total_boxes_volume",
    )
    total_pallet_volume = fields.Float(
        compute="_compute_total_pallet_volume",
    )
    picking_move_line_ids = fields.One2many(
        comodel_name="stock.move.line", related="picking_id.move_line_ids"
    )

    @api.depends("item_number", "list_item_detail_ids")
    def _compute_name(self):
        for item in self:
            name = "{}".format(item.item_number)
            for detail in item.list_item_detail_ids:
                name += " | {} ({})".format(
                    detail.product_id.default_code, int(detail.qty)
                )
            item.name = name

    @api.depends("item_length", "width", "height")
    def _compute_volume(self):
        for item in self:
            item.volume = item.package_quantity * (
                item.item_length * item.width * item.height / 1000000
            )

    @api.depends("item_length", "width", "height")
    def _compute_item_size(self):
        for item in self:
            item.item_size = "{}x{}x{}".format(
                int(item.item_length), int(item.width), int(item.height)
            )

    @api.depends("picking_id", "pallet_number")
    def _compute_total_boxes_weight(self):
        for item in self:
            items = item.picking_id.packing_list_item_ids.filtered(
                lambda x: x.pallet_number == item.pallet_number and not x.is_pallet
            )
            item.total_boxes_weight = sum(items.mapped("weight"))

    @api.depends("weight", "total_boxes_weight")
    def _compute_total_pallet_weight(self):
        for item in self:
            item.total_pallet_weight = item.weight + item.total_boxes_weight

    @api.depends("picking_id", "pallet_number")
    def _compute_total_boxes_volume(self):
        for item in self:
            items = item.picking_id.packing_list_item_ids.filtered(
                lambda x: x.pallet_number == item.pallet_number and not x.is_pallet
            )
            item.total_boxes_volume = sum(items.mapped("volume"))

    @api.depends("volume", "total_boxes_volume")
    def _compute_total_pallet_volume(self):
        for item in self:
            item.total_pallet_volume = item.volume + item.total_boxes_volume

    @api.depends("package_type_id")
    def _compute_item_measures(self):
        for item in self:
            item.item_length = item.package_type_id.packaging_length
            item.width = item.package_type_id.width
            item.height = item.package_type_id.height

    @api.depends(
        "picking_id.packing_list_item_ids",
        "picking_id.packing_list_item_ids.package_quantity",
    )
    def _compute_item_number(self):
        for picking in self.picking_id:
            item_count = 1
            for item in picking.packing_list_item_ids:
                if item.is_pallet:
                    item.item_number = 0
                    continue
                item.item_number = item_count
                item_count += item.package_quantity

    @api.onchange("total_pallet_weight")
    def _cal_weight_pallet_depends(self):
        for item in self:
            item.weight = item.total_pallet_weight - item.total_boxes_weight

    def action_fill_package(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "stock.stock_move_line_action"
        )
        tree_view_ref = self.env.ref("stock.view_move_line_tree_detailed")
        form_view_ref = self.env.ref("stock.view_move_line_form")
        action["context"] = {"create": 0, "packing_list_item_id": self.id}
        action["target"] = "new"
        action["views"] = [(tree_view_ref.id, "tree"), (form_view_ref.id, "form")]
        packing_list_items = self.picking_id.packing_list_item_ids
        move_lines_used = packing_list_items.list_item_detail_ids.stock_move_line_id
        action["domain"] = [
            ("id", "in", (self.picking_id.move_line_ids - move_lines_used).ids),
        ]
        return action
