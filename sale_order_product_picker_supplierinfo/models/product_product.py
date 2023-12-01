# Copyright 2023 Tecnativa - Carlos Dauden
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    # Add force_filter_supplier_id to context
    @api.depends_context("force_filter_supplier_id", "force_supplierinfo_item_id")
    def _compute_product_price(self):
        return super()._compute_product_price()

    def _select_seller(
        self, partner_id=False, quantity=0.0, date=None, uom_id=False, params=False
    ):
        force_supplierinfo_item_id = self.env.context.get(
            "force_supplierinfo_item_id", False
        )
        if force_supplierinfo_item_id:
            return self.env["product.supplierinfo"].browse(force_supplierinfo_item_id)
        return super()._select_seller(partner_id, quantity, date, uom_id, params)
