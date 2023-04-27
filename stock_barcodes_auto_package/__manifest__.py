# Copyright 2022 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Stock Barcodes Auto Package",
    "summary": "Create automatically a package when a barcode is read",
    "version": "15.0.1.0.0",
    "development_status": "Beta",
    "category": "Warehouse",
    "website": "https://github.com/OCA/stock-logistics-barcode",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "stock_barcodes",
    ],
    "data": [
        "views/product_template_views.xml",
        "views/stock_barcodes_option_view.xml",
    ],
}
