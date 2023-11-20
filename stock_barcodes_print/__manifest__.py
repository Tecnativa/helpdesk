# Copyright 2022 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Stock Barcodes Print",
    "summary": "Print labels from barcode wizard interface",
    "version": "15.0.1.0.0",
    "development_status": "Beta",
    "category": "Warehouse",
    "website": "https://github.com/OCA/stock-logistics-barcode",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "base_report_to_printer",
        "stock_barcodes",
        "stock_picking_product_barcode_report",
    ],
    "data": [
        "views/stock_barcodes_option_view.xml",
        "views/stock_picking_views.xml",
        "wizard/stock_barcodes_read_picking_views.xml",
    ],
}
