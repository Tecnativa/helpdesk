# Copyright 2023 Tecnativa - Carlos Dauden
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


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
            ("product_tmpl_id", "in", products.product_tmpl_id.ids),
            "&",
            "|",
            ("date_start", "=", False),
            ("date_start", "<=", today),
            "|",
            ("date_end", "=", False),
            ("date_end", ">=", today),
        ]

    def _get_product_picker_data_supplierinfo(self):
        supplierinfos = self.env["product.supplierinfo"].search(
            self._product_picker_data_supplierinfo_domain()
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
            and sol.supplierinfo_id.id == picker_data["supplierinfo_id"]
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
    vendor_id = fields.Many2one(comodel_name="res.partner")
    vendor_comment = fields.Char()
