# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Order Product Picker",
    "version": "15.0.1.0.0",
    "development_status": "Beta",
    "category": "Sale",
    "website": "https://github.com/OCA/sale-workflow",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["sale_stock"],
    "data": ["security/ir.model.access.csv", "views/sale_order_views.xml"],
    "assets": {
        "web.assets_backend": [
            "sale_order_product_picker/static/src/js/relational_fields.js",
            "sale_order_product_picker/static/src/js/picker_kanban_record.js",
            "sale_order_product_picker/static/src/js/picker_basic_model.js",
            "sale_order_product_picker/static/src/js/form_renderer.js",
            "sale_order_product_picker/static/src/scss/picker.scss",
        ],
        "web.assets_qweb": ["sale_order_product_picker/static/src/xml/fullscreen.xml"],
    },
}
