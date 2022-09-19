# Copyright 2020 Tecnativa - Alexandre D. Díaz
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Web Widget One2Many Product Picker Partner Priority",
    "summary": "Adds support for partner priority in the"
    " sale orders product picker widget",
    "version": "13.0.1.0.0",
    "category": "Sale",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/web",
    "license": "AGPL-3",
    "depends": ["web_pwa_oca", "partner_priority_custom"],
    "data": ["views/sale_pwa_views.xml"],
    "installable": True,
    "auto_install": False,
}
