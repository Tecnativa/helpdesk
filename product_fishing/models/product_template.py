# Copyright 2023 Tecnativa - Stefan Ungureanu
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    harvesting_method_ids = fields.Many2many(
        comodel_name="product.attribute.value",
        compute="_compute_harvesting_method_ids",
    )
    presentation_ids = fields.Many2many(
        comodel_name="product.attribute.value",
        compute="_compute_product_presentation_ids",
    )

    def _compute_harvesting_method_ids(self):
        """
        Helper method to retrieve the harvesting method from product attributes
        """
        harvesting_method_attribute = self.env.ref(
            "product_fishing.harvesting_method_attribute"
        )
        ptal_obj = self.env["product.template.attribute.line"]
        for template in self:
            attribute_line = ptal_obj.search(
                [
                    ("product_tmpl_id", "=", template.id),
                    ("attribute_id", "=", harvesting_method_attribute.id),
                ]
            )
            template.harvesting_method_ids = attribute_line.value_ids

    def _compute_product_presentation_ids(self):
        """
        Helper method to retrieve the product presentation from product attributes
        """
        presentation_attribute = self.env.ref("product_fishing.presentation_attribute")
        ptal_obj = self.env["product.template.attribute.line"]
        for template in self:
            attribute_line = ptal_obj.search(
                [
                    ("product_tmpl_id", "=", template.id),
                    ("attribute_id", "=", presentation_attribute.id),
                ]
            )
            template.presentation_ids = attribute_line.value_ids
