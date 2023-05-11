# Copyright 2022 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Stock Barcodes GS1 Secondary unit One By One",
    "summary": "Set always one unit of secondary unit for each scan process",
    "version": "15.0.1.0.0",
    "development_status": "Beta",
    "category": "Warehouse",
    "website": "https://github.com/OCA/stock-logistics-barcode",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "stock_barcodes_gs1_secondary_unit",
    ],
    "data": [
        "views/stock_barcodes_option_view.xml",
        "wizard/stock_barcodes_read_picking_views.xml",
    ],
}
