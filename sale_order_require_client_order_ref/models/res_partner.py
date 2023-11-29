# Copyright 2023 Pilar Vargas - Tecnativa
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    require_client_order_ref = fields.Boolean(
        string='Require Client Order Reference',
        help='If checked, the client order reference is required for this partner and its contacts.'
    )
