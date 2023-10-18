# Copyright 2022 Tecnativa - Sergio Teruel
# Copyright 2022 Tecnativa - Carlos Dauden
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models
from odoo.tools import float_compare


class SaleOrderPicker(models.Model):
    _name = "sale.order.picker"
    _description = "sale.order.picker"

    order_id = fields.Many2one(comodel_name="sale.order")
    product_id = fields.Many2one(comodel_name="product.product")
    product_image = fields.Image(related="product_id.image_256")
    sale_line_id = fields.Many2one(comodel_name="sale.order.line")
    is_in_order = fields.Boolean()
    product_uom_qty = fields.Float(string="Quantity", digits="Product Unit of Measure")
    uom_id = fields.Many2one(comodel_name="uom.uom", related="product_id.uom_id")
    qty_available = fields.Float(
        string="On Hand",
        digits="Product Unit of Measure",
        related="product_id.qty_available",
    )
    qty_delivered = fields.Float(string="Delivered", digits="Product Unit of Measure")
    times_delivered = fields.Integer()
    price_unit = fields.Float(
        string="Unit Price", compute="_compute_price_unit", digits="Product Price"
    )
    category_id = fields.Many2one("product.category", related="product_id.categ_id")
    currency_id = fields.Many2one(related="order_id.currency_id", depends=["order_id"])
    list_price = fields.Float(related="product_id.list_price")
    is_different_price = fields.Boolean(compute="_compute_is_different_price")

    # TODO: Dummy fields to remove
    state = fields.Selection(
        [
            ("draft", "Quotation"),
            ("sent", "Quotation Sent"),
            ("sale", "Sales Order"),
            ("done", "Locked"),
            ("cancel", "Cancelled"),
        ],
        compute="_compute_dummy_fields",
    )
    move_ids = fields.Many2many("stock.move", compute="_compute_dummy_fields")
    virtual_available_at_date = fields.Float(
        compute="_compute_dummy_fields", digits="Product Unit of Measure"
    )
    scheduled_date = fields.Datetime(compute="_compute_dummy_fields")
    forecast_expected_date = fields.Datetime(compute="_compute_dummy_fields")
    free_qty_today = fields.Float(
        compute="_compute_dummy_fields", digits="Product Unit of Measure"
    )
    qty_available_today = fields.Float(compute="_compute_dummy_fields")
    warehouse_id = fields.Many2one("stock.warehouse", compute="_compute_dummy_fields")
    qty_to_deliver = fields.Float(
        compute="_compute_dummy_fields", digits="Product Unit of Measure"
    )
    is_mto = fields.Boolean(compute="_compute_dummy_fields")
    display_qty_widget = fields.Boolean(compute="_compute_dummy_fields")

    def _get_picker_price_unit_context(self):
        return {
            "partner": self.order_id.partner_id,
            "pricelist": self.order_id.pricelist_id.id,
            "quantity": self.product_uom_qty,
        }

    @api.depends("product_id", "order_id.partner_id", "order_id.picker_price_origin")
    def _compute_price_unit(self):
        """
        Get product price unit from product list price or from last sale price
        """
        price_origin = fields.first(self).order_id.picker_price_origin or "pricelist"
        for line in self:
            if price_origin == "last_sale_price":
                line.price_unit = line._get_last_sale_price_product()
            else:
                line.price_unit = line.product_id.with_context(
                    **line._get_picker_price_unit_context()
                ).price

    @api.depends("product_id")
    def _compute_dummy_fields(self):
        for line in self:
            line.move_ids = self.env["stock.move"]
            line.virtual_available_at_date = 1.0
            line.scheduled_date = line.order_id.date_order
            line.forecast_expected_date = line.order_id.date_order
            line.free_qty_today = 1.0
            line.qty_available_today = 1.0
            line.warehouse_id = line.order_id.warehouse_id
            line.qty_to_deliver = 1.0
            line.is_mto = False
            line.display_qty_widget = True
            line.state = "draft"

    def _get_last_sale_price_product(self):
        """
        Get last price from last order.
        Use sudo to read sale order from other users like as other commercials.
        """
        self.ensure_one()
        so_line = (
            self.env["sale.order.line"]
            .sudo()
            .search(
                [
                    ("company_id", "=", self.order_id.company_id.id),
                    ("order_partner_id", "=", self.order_id.partner_id.id),
                    ("state", "not in", ("draft", "sent", "cancel")),
                    ("product_id", "=", self.product_id.id),
                ],
                limit=1,
                order="id DESC",
            )
            .with_context(prefetch_fields=False)
        )
        return so_line.price_unit or 0.0

    def add_to_cart(self):
        self.ensure_one()
        so_line = self.order_id.order_line.new({"product_id": self.product_id.id})
        so_line.product_id_change()
        self.order_id.order_line += so_line

    @api.depends("list_price", "price_unit")
    def _compute_is_different_price(self):
        digits = self.env["decimal.precision"].precision_get("Product Price")
        for line in self:
            line.is_different_price = bool(
                float_compare(line.price_unit, line.list_price, precision_digits=digits)
            )
