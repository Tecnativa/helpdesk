# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase


class TestProductTemplateComposer(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.product"].create(
            {
                "name": "product name",
                "base_name": "product name",
                "type": "service",
            }
        )
        cls.attribute_1 = cls.env["product.attribute"].create(
            {
                "name": "attr test 01",
                "create_variant": "no_variant",
                "display_type": "radio",
                "product_name_composer_include": True,
            }
        )
        cls.att1_value1 = cls.env["product.attribute.value"].create(
            {
                "attribute_id": cls.attribute_1.id,
                "name": "att1_value1",
            }
        )
        cls.att1_value2 = cls.env["product.attribute.value"].create(
            {
                "attribute_id": cls.attribute_1.id,
                "name": "att1_value2",
            }
        )
        cls.attribute_2 = cls.env["product.attribute"].create(
            {
                "name": "attr test 02",
                "create_variant": "no_variant",
                "display_type": "radio",
                "product_name_composer_include": True,
            }
        )
        cls.att2_value1 = cls.env["product.attribute.value"].create(
            {
                "attribute_id": cls.attribute_2.id,
                "name": "att2_value1",
            }
        )
        cls.att2_value2 = cls.env["product.attribute.value"].create(
            {
                "attribute_id": cls.attribute_2.id,
                "name": "att2_value2",
            }
        )

        # Set attributes on product template
        cls.product.write(
            {
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.attribute_1.id,
                            "value_ids": [(6, 0, cls.att1_value1.ids)],
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.attribute_2.id,
                            "value_ids": [(6, 0, cls.att2_value2.ids)],
                        },
                    ),
                ],
            }
        )
        # Set pattern on default lang
        cls.lang = (
            cls.env["res.lang"]
            .search([("code", "=", cls.env.user.lang)])
            .product_name_composer
        ) = "{base_name} {attr test 01} {attr test 02}"

    def test_name_composer(self):
        self.product.product_tmpl_id.action_compose_name()
        self.assertEqual(self.product.name, "product name att1_value1 att2_value2")
