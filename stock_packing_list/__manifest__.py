# Copyright 2023 Tecnativa - Sergio Teruel
# Copyright 2023 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Stock Packing List",
    "version": "15.0.1.0.0",
    "depends": ["sale_stock", "delivery"],
    "category": "Warehouse Management",
    "author": "Tecnativa",
    "license": "AGPL-3",
    "website": "https://www.tecnativa.com",
    "data": [
        "data/report_paperformat.xml",
        "security/ir.model.access.csv",
        "views/stock_move_line_view.xml",
        "views/stock_packing_list_item_view.xml",
        "views/stock_packing_list_item_detail_view.xml",
        "views/stock_picking_view.xml",
        "report/report_picking_carrier_label.xml",
        "report/report_picking_packing_list.xml",
        "report/report_picking_pallet_label.xml",
        "report/report_views.xml",
    ],
    "installable": True,
    "assets": {
        "web.report_assets_common": [
            "stock_packing_list/static/src/scss/report.scss",
        ]
    },
}
