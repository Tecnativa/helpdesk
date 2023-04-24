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
        "product_drained_weight",
        "sale_elaboration",
        "stock_production_lot_fishing_info",
        "stock_picking_product_barcode_report",
        "nutritional_info_stock_lot",
    ],
    "data": [
        "data/paperformat_label.xml",
        "report/report_templates.xml",
        "report/report_fishing_label_template.xml",
        "report/report_label_barcode.xml",
    ],
    "assets": {
        "web.report_assets_common": [
            "stock_production_lot_fishing_label/static/src/scss/nutrition_table_style.scss",
        ]
    },
}
