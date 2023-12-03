# Copyright 2023 Pilar Vargas - Tecnativa
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    so_require_client_order_ref = fields.Boolean(
        related="partner_id.commercial_partner_id.require_client_order_ref"
    )
