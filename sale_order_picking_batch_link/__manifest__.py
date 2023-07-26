# Copyright 2023 Tecnativa - Stefan Ungureanu
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Order Picking Batch Link",
    "summary": "Show the sale order's associated batch pickings",
    "version": "15.0.1.0.0",
    "category": "stock",
    "website": "https://github.com/OCA/sale-workflow",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["sale_stock", "stock_picking_batch"],
    "data": [
        "views/sale_order_views.xml",
    ],
}
