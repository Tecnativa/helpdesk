# Copyright 2022 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    qty_per_packaging = fields.Integer(
        string="Qty per packaging",
        related="product_variant_ids.qty_per_packaging",
        help="Qty per packaging of the product.",
        readonly=False,
    )
