# Copyright 2023 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Intrastat Product Declaration for Spain - lot origin country",
    "summary": "Take product origin country from lot",
    "version": "15.0.1.0.0",
    "category": "Sale",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/extra-addons",
    "license": "AGPL-3",
    "depends": [
        "intrastat_product",
        "stock_picking_invoice_link",
        "stock_production_lot_fishing_info",
    ],
    "data": [
        "views/product_attribute_views.xml",
    ],
    "post_init_hook": "post_init_hook",
}
