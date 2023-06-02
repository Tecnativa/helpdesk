# Copyright 2023 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute"

    is_country_attr = fields.Boolean()


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    country_id = fields.Many2one(comodel_name="res.country")
