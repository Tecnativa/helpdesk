# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Purchase Requisition From Outgoing Moves Supplierinfo",
    "summary": "Purchase requisition based on outgoing stock moves with supplierinfo data",
    "version": "15.0.1.0.0",
    "development_status": "Beta",
    "category": "Purchase",
    "website": "https://github.com/OCA/purchase-workflow",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "purchase_requisition_from_outgoing_move",
        "sale_order_product_picker_supplierinfo",
    ],
    "data": [
        "report/purchase_requisition_template.xml",
    ],
}
