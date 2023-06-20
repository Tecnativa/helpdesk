# Copyright 2023 Tecnativa - Carlos Dauden
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import models


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    def _is_applicable_for(self, product, qty_in_product_uom):
        """Allow combine supplierinfo pricelists with other pricelists having two items
        for the one affected product in the same pricelist"""
        vendor_id = self.env.context.get("force_filter_supplier_id", False)
        if bool(vendor_id) != (self.base == "supplierinfo"):
            return False
        return super()._is_applicable_for(product, qty_in_product_uom)
