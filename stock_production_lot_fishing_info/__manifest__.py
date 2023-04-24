# Copyright 2022 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Stock Production Lot Fishing Info",
    "version": "15.0.1.0.2",
    "development_status": "Beta",
    "category": "Inventory",
    "website": "https://www.tecnativa.com",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "product_fao_fishing",
        "stock",
        "product_attribute_value_range",
        "product_expiry",
        "product_fishing",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/stock_production_lot_view.xml",
        "views/res_company_view.xml",
    ],
}
