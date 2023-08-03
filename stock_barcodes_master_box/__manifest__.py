# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Barcodes Master Box",
    "summary": "Group packages in master box",
    "version": "15.0.1.0.0",
    "author": "Tecnativa, " "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/stock-logistics-barcode",
    "license": "AGPL-3",
    "category": "Inventory",
    "depends": [
        "stock_barcodes",
    ],
    "data": ["wizard/stock_barcodes_read_picking_views.xml"],
    "installable": True,
}
