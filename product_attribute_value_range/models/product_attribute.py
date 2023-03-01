# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    from_range = fields.Float(digits="Product Unit of Measure")
    to_range = fields.Float(digits="Product Unit of Measure")
    tolerance_range = fields.Float()
