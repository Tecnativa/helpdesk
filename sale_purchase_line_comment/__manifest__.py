# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Sale Purchase Line Comment",
    "summary": """
        Add the vendor comment field from the sale order line to purchase order line
        """,
    "version": "15.0.1.0.0",
    "license": "LGPL-3",
    "website": "https://github.com/OCA/sale-workflow",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "depends": [
        "purchase",
        "sale",
    ],
    "data": ["views/purchse_order_views.xml", "views/sale_order_views.xml"],
    "installable": True,
}
