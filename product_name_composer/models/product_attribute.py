# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    product_name_composer_include = fields.Boolean()
