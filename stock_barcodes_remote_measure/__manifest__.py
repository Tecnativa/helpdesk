# Copyright 2022 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Stock Barcodes Remote Measure",
    "summary": "Get remote measure from devices",
    "version": "15.0.1.0.0",
    "development_status": "Beta",
    "category": "Warehouse",
    "website": "https://github.com/OCA/stock-logistics-barcode",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "stock_barcodes",
        "stock_remote_measure",
    ],
    "data": [
        "wizard/stock_barcodes_read_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "stock_barcodes_remote_measure/static/src/**/*.js",
        ],
    },
}
