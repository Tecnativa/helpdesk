# Copyright 2022 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    weight_type = fields.Selection(
        [("variable", "Variable"), ("fixed", "Fixed")],
        default="fixed",
    )
