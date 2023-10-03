# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Purchase Stock Move Vendor Update",
    "summary": """Update vendor on stock move when change vendor on purchase orders""",
    "version": "15.0.1.0.0",
    "license": "LGPL-3",
    "website": "https://github.com/OCA/purchase-workflow",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "depends": [
        "purchase_line_reassign",
        "procurement_purchase_no_grouping_comment",
    ],
    "installable": True,
}
