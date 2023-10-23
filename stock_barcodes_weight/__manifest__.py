# Copyright 2019 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Barcodes Weight",
    "summary": "It provides improvements to weight products",
    "version": "15.0.1.0.0",
    "author": "Tecnativa, " "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/stock-logistics-barcode",
    "license": "AGPL-3",
    "category": "Extra Tools",
    "depends": [
        "stock_barcodes_gs1_secondary_unit",
        "product_attribute_value_range",
        "stock_picking_product_change",
    ],
    "data": ["wizard/stock_barcodes_read_picking_views.xml"],
    "installable": True,
    "auto_install": False,
}
