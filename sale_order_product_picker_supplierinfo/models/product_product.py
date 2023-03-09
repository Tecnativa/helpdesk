# Copyright 2023 Tecnativa - Carlos Dauden
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    # Add force_filter_supplier_id to context
    @api.depends_context("force_filter_supplier_id")
    def _compute_product_price(self):
        return super()._compute_product_price()
