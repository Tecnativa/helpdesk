# Copyright 2020 Tecnativa - Alexandre D. Díaz
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Sale PWA OCA",
    "summary": "Optimize sale order form for standalone mode"
    " sale orders product picker widget",
    "version": "13.0.1.0.0",
    "category": "Sale",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/web",
    "license": "AGPL-3",
    "depends": [
        "sale_management",
        "web_pwa_oca",
        "web_widget_one2many_product_picker",
        "sale_order_type",
    ],
    "data": ["views/sale_pwa_views.xml"],
    "installable": False,
    "auto_install": False,
}
