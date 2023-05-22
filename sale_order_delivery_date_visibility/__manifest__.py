# Copyright 2020 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale order delivery date visibility",
    "summary": "Better visibility of delivery date field on sale orders",
    "version": "15.0.1.0.0",
    "development_status": "Beta",
    "category": "Account",
    "website": "https://github.com/OCA/sale-workflow",
    "author": "Tecnativa",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "sale_stock",
    ],
    "data": [
        "views/sale_order_view.xml",
    ],
}
