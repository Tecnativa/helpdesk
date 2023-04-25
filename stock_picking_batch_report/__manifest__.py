# Copyright 2022 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Stock Picking Batch Reports",
    "summary": "Batch picking reports",
    "version": "15.0.1.0.0",
    "development_status": "Beta",
    "category": "Sale",
    "website": "https://github.com/OCA/sale-workflow",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "auto_install": True,
    "depends": [
        "stock_picking_batch_extended",
        "sale_elaboration",
        "congeladosromero_custom",
    ],
    "data": [
        "views/stock_picking_batch_report_driver.xml",
        "views/stock_picking_batch_report_elaboration.xml",
        "reports/stock_picking_batch_report.xml",
    ],
}
