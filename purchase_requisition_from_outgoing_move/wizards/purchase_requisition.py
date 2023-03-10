# Copyright 2019 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, fields, models
from odoo.exceptions import ValidationError


class PurchaseRequisitionWiz(models.TransientModel):
    _name = "purchase.requisition.wiz"
    _description = "Purchase requisition wiz"

    date_from = fields.Datetime()
    date_to = fields.Datetime()
    product_attribute_ids = fields.Many2many(
        comodel_name="product.attribute.value",
        string="Product Attribute",
    )

    def print_report(self):
        domain = [
            ("state", "not in", ("cancel", "done")),
            ("location_dest_id.usage", "=", "customer"),
        ]
        if self.product_attribute_ids:
            domain.append(
                (
                    "product_id.attribute_line_ids.value_ids",
                    "in",
                    self.product_attribute_ids.ids,
                )
            )
        if self.date_from:
            domain.append(("date", ">=", self.date_from))
        if self.date_to:
            domain.append(("date", "<=", self.date_to))

        moves = self.env["stock.move"].search(domain)
        if not moves:
            raise ValidationError(_("There is no moves to print"))

        return self.env.ref(
            "purchase_requisition_from_outgoing_move.report_purchase_requisition_outgoing"
        ).report_action(moves)
