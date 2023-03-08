# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    base_name = fields.Char()

    @api.onchange("name")
    def _onchange_name(self):
        if not self.base_name:
            self.base_name = self.name

    def get_product_name_composer_dic(self):
        self.ensure_one()
        res = {}
        # Attribute fields
        for product_attr in self.env["product.attribute"].search(
            [("product_name_composer_include", "=", True)]
        ):
            key = product_attr.with_context(lang="en_US").name
            value = (
                self.attribute_line_ids.filtered(
                    lambda attr: attr.attribute_id == product_attr
                )
                .value_ids[:1]
                .name
            )
            res[key] = value
        # Other fields
        field_list = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("product_name_composer.product_field_list", "base_name")
            .split(",")
        )
        for item in field_list:
            field_name = item.strip()
            res[field_name] = (
                self._fields[field_name].convert_to_display_name(self[field_name], self)
                if field_name in self
                else ""
            )
        return res

    def action_compose_name(self):
        langs = self.env["res.lang"].search([])
        for template in self:
            for lang in langs:
                product_template = template.with_context(lang=lang.code)
                value = (lang.product_name_composer or "{base_name}").format(
                    **product_template.get_product_name_composer_dic()
                )
                product_template.name = value
