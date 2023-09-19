# Copyright 2023 Tecnativa - Carlos Dauden
# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductSecondaryUnit(models.Model):
    _inherit = "product.secondary.unit"

    is_master_box = fields.Boolean()
