# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo.tests import Form, TransactionCase


class TestSaleFreshProduct(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_elaboration = cls.env["product.product"].create(
            {
                "name": "Product Elaboration",
                "type": "service",
                "list_price": 10.0,
                "invoice_policy": "order",
                "is_elaboration": True,
            }
        )
        cls.elaboration = cls.env["product.elaboration"].create(
            {
                "code": "0000",
                "name": "Elaboration",
                "product_id": cls.product_elaboration.id,
            }
        )
        cls.customer = cls.env["res.partner"].create({"name": "Test customer"})
        cls.attribute_gama = cls.env["product.attribute"].create(
            {
                "name": "Att. Gamma",
                "create_variant": "no_variant",
            }
        )
        cls.gamma_fresh = cls.env["product.attribute.value"].create(
            {
                "attribute_id": cls.attribute_gama.id,
                "name": "Fresh",
            }
        )

        cls.product = cls.env["product.template"].create(
            {
                "name": "Test product",
                "type": "product",
                "invoice_policy": "order",
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.attribute_gama.id,
                            "value_ids": [(4, cls.gamma_fresh.id)],
                        },
                    ),
                ],
            }
        )
        cls.order = cls._create_sale_order(cls)
        cls.order.action_confirm()

    def _create_sale_order(self):
        order_form = Form(self.env["sale.order"])
        order_form.partner_id = self.customer
        with order_form.order_line.new() as line_form:
            line_form.product_id = self.product.product_variant_id
            line_form.product_uom_qty = 10.0
            line_form.elaboration_ids.add(self.elaboration)
        return order_form.save()

    def test_report_purchase_requisition_sale(self):
        wizard = self.env["purchase.requisition.wiz"].create(
            {
                "date_from": datetime.today() - relativedelta(days=1),
                "date_to": datetime.today(),
            }
        )
        action = wizard.with_context(discard_logo_check=True).print_report()
        report_html = self.env.ref(
            "purchase_requisition_from_outgoing_move.report_purchase_requisition_outgoing"
        )._render_qweb_html(action["context"]["active_ids"], False)
        report_html = str(report_html)
        self.assertRegex(report_html, "Test customer")
        self.assertRegex(report_html, "Test product")
