# Copyright 2023 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Sale Order Product Picker SupplierInfo",
    "version": "15.0.1.0.0",
    "development_status": "Beta",
    "category": "Sale",
    "website": "https://github.com/OCA/sale-workflow",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "sale_margin",
        "sale_order_product_picker",
        "sale_purchase_force_vendor",
        "sale_purchase_line_comment",
    ],
    "data": ["views/sale_order_views.xml"],
    "assets": {
        "web.assets_backend": [
            "sale_order_product_picker_supplierinfo/static/src/js/picker_basic_model.js",
            "sale_order_product_picker_supplierinfo/static/src/js/picker_kanban_record.js",
        ],
    },
}
