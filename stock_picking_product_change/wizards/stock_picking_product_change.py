# Copyright 2019 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tests import Form
from odoo.tools import float_compare


class StockPickingProductChange(models.TransientModel):
    _name = "stock.picking.product.change.wiz"

    picking_ids = fields.Many2many(
        comodel_name="stock.picking", string="Pickings to process",
    )
    old_product_id = fields.Many2one(
        comodel_name="product.product", string="Original Product",
    )
    new_product_id = fields.Many2one(
        comodel_name="product.product", string="New product",
    )
    keep_secondary_unit = fields.Boolean(string="Keep secondary unit", default=True,)
    keep_description = fields.Boolean(string="Keep description",)
    keep_price = fields.Boolean(string="Keep price",)
    only_qty_needed = fields.Boolean(string="Only quantity needed",)
    line_ids = fields.One2many(
        comodel_name="stock.picking.product.change.line.wiz",
        inverse_name="wizard_id",
        compute="_compute_line_ids",
        string="Lines",
        readonly=False,
        store=True,
    )

    @api.depends("old_product_id", "only_qty_needed")
    def _compute_line_ids(self):
        self.line_ids = False
        model_name = self.env.context.get("active_model")
        if not model_name:
            return
        records = self.env[model_name].browse(self.env.context.get("active_ids"))
        precision = self.env["decimal.precision"].precision_get(
            "Product Unit of Measure"
        )
        if model_name == "stock.picking":
            picking_ids = records
        else:
            picking_ids = records.picking_ids
        moves = picking_ids.mapped("move_lines").filtered(
            lambda m: m.product_id == self.old_product_id
            and m.state not in ["done", "cancel"]
        )
        for move in moves:
            if self.only_qty_needed:
                qty_needed = move.product_uom_qty - move.reserved_availability
                if float_compare(qty_needed, 0.0, precision_digits=precision) == 1:
                    self.line_ids |= self.line_ids.new(
                        self._prepare_wizard_line(move, qty_needed)
                    )
            else:
                self.line_ids |= self.line_ids.new(
                    self._prepare_wizard_line(move, move.product_uom_qty)
                )

    def _prepare_wizard_line(self, move, qty):
        return {
            "move_id": move.id,
            "product_uom_qty": qty,
        }

    def action_change_product(self):
        if not self.line_ids:
            raise UserError(_("There is no picking lines to change"))
        for line in self.line_ids:
            if line.product_uom_qty > 0.0:
                line.sudo()._create_new_so_line()


class StockPickingProductChangeLine(models.TransientModel):
    _name = "stock.picking.product.change.line.wiz"

    wizard_id = fields.Many2one(
        comodel_name="stock.picking.product.change.wiz",
        ondelete="cascade",
        readonly=True,
    )
    move_id = fields.Many2one(comodel_name="stock.move", string="Move", readonly=True,)
    warehouse_id = fields.Many2one(
        comodel_name="stock.warehouse",
        string="Warehouse",
        related="move_id.warehouse_id",
    )
    picking_id = fields.Many2one(
        comodel_name="stock.picking", related="move_id.picking_id", string="Picking",
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner", related="picking_id.partner_id", string="Partner",
    )
    old_product_id = fields.Many2one(
        comodel_name="product.product",
        related="move_id.product_id",
        string="Original Product",
    )
    new_product_id = fields.Many2one(
        comodel_name="product.product",
        compute="_compute_new_product_id",
        string="New product",
        readonly=False,
        store=True,
        required=True,
    )
    old_product_uom_qty = fields.Float(
        related="move_id.product_uom_qty",
        string="Initial Demand",
        digits="Product Unit of Measure",
    )
    old_reserved_availability = fields.Float(
        related="move_id.reserved_availability",
        string="Quantity Reserved",
        digits="Product Unit of Measure",
    )
    new_product_free_qty = fields.Float(
        compute="_compute_new_product_free_qty", digits="Product Unit of Measure",
    )
    product_uom_qty = fields.Float(
        string="Qty. to change", digits="Product Unit of Measure",
    )

    # TODO: Move to other module
    old_secondary_qty = fields.Float(
        related="move_id.sale_line_id.secondary_uom_qty",
        digits="Product Unit of Measure",
    )
    old_secondary_uom_id = fields.Many2one(
        comodel_name="product.secondary.unit",
        related="move_id.sale_line_id.secondary_uom_id",
    )

    @api.depends("wizard_id.new_product_id")
    def _compute_new_product_id(self):
        self.new_product_id = self.wizard_id.new_product_id

    @api.depends("new_product_id")
    def _compute_new_product_free_qty(self):
        for line in self:
            line.new_product_free_qty = line.new_product_id.with_context(
                warehouse=line.picking_id.picking_type_id.warehouse_id.id,
                so_product_stock_inline=True,
            ).free_qty

    def _get_new_secondary_unit(self):
        old_factor = self.move_id.sale_line_id.secondary_uom_id.factor
        return self.new_product_id.secondary_uom_ids.filtered(
            lambda s: s.factor == old_factor
        )[:1]

    def _prepare_new_so_line_values(self):
        origin_so_line = self.move_id.sale_line_id
        order_form = Form(origin_so_line.order_id)
        with order_form.order_line.new() as line_form:
            line_form.product_id = self.new_product_id
            if self.wizard_id.keep_secondary_unit and origin_so_line.secondary_uom_id:
                secondary_uom = self._get_new_secondary_unit()
                if secondary_uom:
                    line_form.secondary_uom_id = self._get_new_secondary_unit()
            line_form.product_uom_qty = self.product_uom_qty
            if self.wizard_id.keep_description:
                line_form.name = origin_so_line.name
            if self.wizard_id.keep_price:
                line_form.price_unit = origin_so_line.price_unit
                line_form.discount = origin_so_line.discount
            if "elaboration_ids" in origin_so_line._fields:
                # To avoid sale_elaboration dependency.
                # Copy elaboration data
                for elaboration in origin_so_line.elaboration_ids:
                    line_form.elaboration_ids.add = elaboration
                line_form.elaboration_note = origin_so_line.elaboration_note
            new_line_vals = line_form._values_to_save()
        return new_line_vals

    def _create_new_so_line(self):
        origin_so_line = self.move_id.sale_line_id
        if origin_so_line:
            vals = self._prepare_new_so_line_values()
            origin_so_line.order_id.order_line = [(0, 0, vals)]
            self._update_old_so_line()

    def _update_old_so_line(self):
        origin_so_line = self.move_id.sale_line_id
        origin_order = origin_so_line.order_id
        index = origin_order.order_line.ids.index(origin_so_line.id)
        order_form = Form(origin_order)
        with order_form.order_line.edit(index) as line_form:
            line_form.product_uom_qty = (
                self.move_id.product_uom_qty - self.product_uom_qty
            )
        order_form.save()
        # Store replaced qty as normal method because the field is not in the
        # view definition
        origin_so_line.replaced_qty = self.product_uom_qty
