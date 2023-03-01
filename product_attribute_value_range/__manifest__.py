# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Product Attribute Value Range",
    "summary": "Add range value for attribute values",
    "version": "15.0.1.0.0",
    "development_status": "Beta",
    "category": "Fishing",
    "website": "https://github.com/OCA/community-data-files",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["product"],
    "data": [
        "data/product_attribute_value_range_data.xml",
        "views/product_attribute_views.xml",
    ],
}
