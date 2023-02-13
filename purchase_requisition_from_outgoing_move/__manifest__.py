# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Purchase Requisition From Outgoing Moves",
    "summary": "Purchase requisition based on outgoing stock moves",
    "version": "15.0.1.0.0",
    "development_status": "Beta",
    "category": "Purchase",
    "website": "https://github.com/OCA/sale-workflow",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "purchase_stock",
        "sale_stock_secondary_unit",
        "sale_elaboration",
        "sale_order_product_recommendation_supplierinfo",
    ],
    "data": [
        "security/ir.model.access.csv",
        "report/purchase_requisition_report.xml",
        "report/purchase_requisition_template.xml",
        "wizards/purchase_requisition_view.xml",
    ],
}
