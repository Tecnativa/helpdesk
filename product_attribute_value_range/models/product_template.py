# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    caliber_ids = fields.Many2many(
        comodel_name="product.attribute.value", compute="_compute_caliber_ids"
    )

    def _compute_caliber_ids(self):
        """
        Helper method to retrieve the caliber from product attributes
        """
        caliber = self.env.ref("product_attribute_value_range.attribute_caliber")
        ptal_obj = self.env["product.template.attribute.line"]
        for template in self:
            attribute_line = ptal_obj.search(
                [
                    ("product_tmpl_id", "=", template.id),
                    ("attribute_id", "=", caliber.id),
                ]
            )
            template.caliber_ids = attribute_line.value_ids
