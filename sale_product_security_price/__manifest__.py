# Copyright 2020 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Product Security Prices",
    "summary": "Set an security price for sale products",
    "version": "15.0.1.0.1",
    "development_status": "Production/Stable",
    "category": "Product",
    "website": "https://github.com/OCA/sale-workflow",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["sale", "product_cost_security"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_amount_extra_template_views.xml",
        "views/product_views.xml",
        "views/res_config_settings_views.xml",
        "views/res_partner.xml",
        "views/sale_order_views.xml",
    ],
}
