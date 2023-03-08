# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Lang(models.Model):
    _inherit = "res.lang"

    product_name_composer = fields.Char()
