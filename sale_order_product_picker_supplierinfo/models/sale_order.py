# Copyright 2023 Tecnativa - Carlos Dauden
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    picker_origin_data = fields.Selection(
        selection_add=[("supplierinfo", "Vendor pricelists")],
    )

    def _get_supplierinfo_comment(self):
        if "comment" in self.env["product.supplierinfo"]._fields:
            return "comment"
        return "product_name"

    def _product_picker_data_supplierinfo_domain(self):
        """Domain to find recent SO lines."""
        today = fields.Date.context_today(self)
        products = self.env["product.product"].browse(self._get_picker_product_ids())
        return [
            "&",
            "|",
            ("product_id", "in", products.ids),
            (
                "product_tmpl_id",
                "in",
                products.product_tmpl_id.filtered(
                    lambda pt: pt.product_variant_count == 1
                ).ids,
            ),
            "&",
            "|",
            ("date_start", "=", False),
            ("date_start", "<=", today),
            "|",
            ("date_end", "=", False),
            ("date_end", ">=", today),
        ]

    def _get_product_picker_data_supplierinfo(self):
        limit = self._get_product_picker_limit()
        supplierinfos = self.env["product.supplierinfo"].search(
            self._product_picker_data_supplierinfo_domain(),
            limit=limit,
        )
        return [
            {
                "product_id": (
                    ln.product_id.id or ln.product_tmpl_id.product_variant_id.id,
                    ln.product_id.name or ln.product_tmpl_id.product_variant_id.name,
                ),
                "supplierinfo_id": ln.id,
                "vendor_id": (ln.name.id, ln.name.name),
                "comment": ln[self._get_supplierinfo_comment()],
            }
            for ln in supplierinfos
        ]

    # TODO: Use field list instead overwrite method
    def filter_picker_so_lines(self, picker_data):
        return self.order_line.filtered(
            lambda sol: sol.product_id.id == picker_data["product_id"][0]
            and sol.supplierinfo_id.id == picker_data.get("supplierinfo_id", False)
        )

    def _prepare_product_picker_vals(self, group_line, so_lines):
        vals = super()._prepare_product_picker_vals(group_line, so_lines)
        vals["supplierinfo_id"] = group_line.get("supplierinfo_id", False)
        if group_line.get("vendor_id", False):
            vals["vendor_id"] = group_line["vendor_id"][0]
        if group_line.get("comment", False):
            vals["vendor_comment"] = group_line["comment"]
        return vals


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    supplierinfo_id = fields.Many2one(comodel_name="product.supplierinfo")

    @api.onchange("product_uom", "product_uom_qty")
    def product_uom_change(self):
        if self.vendor_id:
            self = self.with_context(force_filter_supplier_id=self.vendor_id)
        return super().product_uom_change()

    @api.depends("vendor_id", "supplierinfo_id")
    def _compute_purchase_price(self):
        """get purchase_price from supplierinfo_id or vendor."""
        processed_lines = self.browse()
        for line in self:
            if not line.supplierinfo_id and not line.vendor_id:
                continue
            if line.state in ("sale", "done"):
                purchase_line_id = (
                    line.move_ids._get_moves_orig()
                    .filtered(lambda sm: sm.state != "cancel")
                    .move_orig_ids.purchase_line_id
                )
                if purchase_line_id:
                    if line.purchase_price != purchase_line_id.price_unit:
                        line.purchase_price = purchase_line_id.price_unit
                    processed_lines += line
                    continue
            supplier_info = line.supplierinfo_id or line._get_vendor_supplier_info()
            if supplier_info:
                line.purchase_price = supplier_info.price
                processed_lines += line
        return super(SaleOrderLine, self - processed_lines)._compute_purchase_price()

    # TODO: Move this to sale_purchase_force_vendor
    def _get_vendor_supplier_info(self):
        self.ensure_one()
        return self.product_id.with_company(self.company_id.id)._select_seller(
            partner_id=self.vendor_id,
            quantity=self.product_uom_qty,
            uom_id=self.product_uom,
        )

    # TODO: Replace after create glue module sale_purchase_force_vendor and sale_margin
    # @api.depends('supplierinfo_id')
    # def _compute_purchase_price(self):
    #     """ Get purchase_price from supplierinfo """
    #     supplierinfo_lines = self.filtered("supplierinfo_id")
    #     for line in supplierinfo_lines:
    #         line.purchase_price = line.supplierinfo_id.price
    #     return super(SaleOrderLine, self - supplierinfo_lines)._compute_purchase_price()

    # TODO: Move this to sale_purchase_force_vendor_sale_margin
    # @api.depends("vendor_id")
    # def _compute_purchase_price(self):
    #     """Get purchase_price from vendor supplierinfo."""
    #     processed_lines = self.browse()
    #     for line in self.filtered("vendor_id"):
    #         supplier_info = line._get_vendor_supplier_info()
    #         if supplier_info:
    #             line.purchase_price = supplier_info.price
    #             processed_lines += line
    #     return super(SaleOrderLine, self - processed_lines)._compute_purchase_price()
    #
