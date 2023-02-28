# Copyright 2020 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Stock Picking Product Change",
    "summary": "Change products from pickings",
    "version": "15.0.1.0.0",
    "category": "Warehouse",
    "website": "https://github.com/OCA/stock-logistics-workflow",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "sale_order_secondary_unit",
        "sale_stock",
        "stock_picking_batch_extended",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizards/stock_picking_product_change.xml",
    ],
}
