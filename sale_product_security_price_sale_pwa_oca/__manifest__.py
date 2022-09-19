# Copyright 2020 Tecnativa - Alexandre D. Díaz
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Sale Product Security Price Sale PWA OCA",
    "summary": "Adds support for sale product security price in the standalone mode",
    "version": "13.0.1.0.0",
    "category": "Sale",
    "author": "Tecnativa, " "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/web",
    "license": "AGPL-3",
    "depends": ["sale_product_security_price", "sale_pwa_oca"],
    "data": ["templates/assets.xml", "views/sale_pwa_views.xml"],
    "qweb": ["static/src/xml/one2many_product_picker.xml"],
    "installable": True,
    "auto_install": False,
}
