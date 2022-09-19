# Copyright 2019 Alexandre D. Díaz - Tecnativa
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    order_partner_security_price_control = fields.Boolean(
        related="order_id.partner_id.security_price_control",
        # compute_sudo=True,
        # compute="_compute_security_price_control",
        groups="base.group_user",
    )
    product_security_price_control = fields.Boolean(
        related="product_id.security_price_control",
        # compute_sudo=True,
        # compute="_compute_security_price_control",
        groups="base.group_user",
    )

    def _compute_security_price_control(self):
        for rec in self:
            rec.order_partner_security_price_control = (
                rec.order_id.partner_id.security_price_control
            )
            rec.product_security_price_control = rec.product_id.security_price_control
