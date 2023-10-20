# Copyright 2023 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Stock Production Lot Fishing Label",
    "version": "15.0.1.0.0",
    "development_status": "Beta",
    "category": "Inventory",
    "website": "https://www.tecnativa.com",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "company_sanitary_registry",
        "product_drained_weight",
        "product_expiry",
        "sale_elaboration",
        "stock_barcodes_master_box",
        "stock_production_lot_fishing_info",
        "stock_picking_product_barcode_report",
        "nutritional_info_stock_lot",
        "stock_barcodes_master_box",
    ],
    "data": [
        "data/paperformat_label.xml",
        "report/report_templates.xml",
        "report/report_fishing_label_master_box_template.xml",
        "report/report_fishing_label_template.xml",
        "report/report_label_barcode.xml",
        "wizards/stock_barcode_selection_printing.xml",
    ],
    "assets": {
        "web.report_assets_common": [
            "stock_production_lot_fishing_label/static/src/scss/*.scss",
        ]
    },
}
