# Copyright 2020 Tecnativa - Alexandre D. Díaz
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Sale Product Set Sale PWA OCA",
    "summary": "Adds support for sale product set in the standalone mode",
    "version": "13.0.1.0.0",
    "category": "Sale",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/web",
    "license": "AGPL-3",
    "depends": ["web_pwa_oca", "sale_product_set"],
    "data": ["views/sale_pwa_views.xml"],
    "installable": False,
    "auto_install": False,
}
