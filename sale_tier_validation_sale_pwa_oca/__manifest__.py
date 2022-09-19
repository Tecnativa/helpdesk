# Copyright 2020 Tecnativa - Alexandre D. Díaz
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Sale Tier Validation Sale PWA OCA",
    "summary": "Adds support for tier validation in standalone mode"
    " one2many product picker widget",
    "version": "13.0.1.0.0",
    "category": "Sale",
    "author": "Tecnativa, " "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/web",
    "license": "AGPL-3",
    "depends": ["sale_tier_validation", "sale_pwa_oca"],
    "data": ["views/sale_pwa_views.xml"],
    "installable": True,
    "auto_install": False,
}
