# Copyright 2022 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Sale Order Product Supplier Info Comment",
    "summary": """
        Add the Supplierinfo comment field to the sale order line
        """,
    "version": "15.0.1.0.0",
    "license": "LGPL-3",
    "website": "https://github.com/OCA/product-attribute",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "depends": [
        "product_supplierinfo_comment",
        "sale_order_product_recommendation_supplierinfo",
    ],
    "data": ["views/sale_order_views.xml"],
    "installable": True,
}
