# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Stock Detailed Operation Existing Lot",
    "summary": "Set lot_id in detailed operations " "when user sets the lot_name field",
    "version": "15.0.1.0.0",
    "development_status": "Beta",
    "category": "Stock",
    "website": "https://github.com/OCA/stock-logistics-warehouse",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["stock"],
    "data": ["views/stock_picking_views.xml"],
}
