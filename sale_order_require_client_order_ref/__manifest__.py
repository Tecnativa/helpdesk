# Copyright 2023 Tecnativa - Pilar Vargas
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Sale Order Require Client Order Ref",
    "version": "15.0.1.0.0",
    "category": "Sales",
    "summary": "Make client_order_ref field required based on partner configuration",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/web",
    "license": "AGPL-3",
    "depends": ["sale"],
    "data": [
        "views/res_partner_views.xml",
        "views/sale_order_views.xml",
    ],
    "installable": True,
}
