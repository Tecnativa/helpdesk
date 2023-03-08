# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product name composer",
    "version": "15.0.1.0.0",
    "development_status": "Beta",
    "category": "Product",
    "website": "https://www.tecnativa.com",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["product"],
    "data": [
        "data/action_server.xml",
        "views/product_attribute_views.xml",
        "views/product_views.xml",
        "views/res_lang_views.xml",
    ],
}
