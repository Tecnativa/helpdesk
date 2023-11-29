from odoo.tests.common import Form, TransactionCase


class TestSaleOrderRequireClientOrderRef(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_company = cls.env["res.partner"].create(
            {
                "name": "Test Partner Company",
                "is_company": True,
            }
        )
        cls.partner_contact = cls.env["res.partner"].create(
            {
                "name": "Test Partner Contact",
                "parent_id": cls.partner_company.id,
            }
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test product",
                "type": "service",
                "lst_price": 10,
                "invoice_policy": "order",
            }
        )

    def _create_sale_order(self, partner):
        sale_form = Form(self.env["sale.order"])
        sale_form.partner_id = partner
        with sale_form.order_line.new() as line_form:
            line_form.product_id = self.product
        return sale_form

    def test_01_partner_child_no_require_client_order_ref(self):
        """The partner's failure to require a customer order reference should not affect
        the sales order."""
        sale_order = self._create_sale_order(self.partner_contact)
        sale_order.save()
        self.assertFalse(self.partner_contact.require_client_order_ref)
        self.assertFalse(sale_order.so_require_client_order_ref)
        self.assertFalse(sale_order.client_order_ref)

    def test_02_partner_parent_no_require_client_order_ref(self):
        """The partner's failure to require a customer order reference should not affect
        the sales order."""
        sale_order = self._create_sale_order(self.partner_company)
        sale_order.save()
        self.assertFalse(self.partner_company.require_client_order_ref)
        self.assertFalse(sale_order.so_require_client_order_ref)
        self.assertFalse(sale_order.client_order_ref)

    def test_03_partner_child_require_client_order_ref(self):
        """The company's requirement for a client order reference affects the sale order."""
        self.partner_company.require_client_order_ref = True
        # The requirement is on the company, not the children.
        self.assertFalse(self.partner_contact.require_client_order_ref)
        sale_order = self._create_sale_order(self.partner_contact)
        # The sales order cannot be saved/confirmed until the field is not completed.
        with self.assertRaises(AssertionError):
            sale_order.save()
        self.assertTrue(sale_order.so_require_client_order_ref)
        sale_order.client_order_ref = "ABC000"
        sale_order.save()

    def test_04_partner_parent_require_client_order_ref(self):
        """The company's requirement for a client order reference affects the sale order."""
        self.partner_company.require_client_order_ref = True
        sale_order = self._create_sale_order(self.partner_company)
        # The sales order cannot be saved/confirmed until the field is not completed.
        with self.assertRaises(AssertionError):
            sale_order.save()
        self.assertTrue(sale_order.so_require_client_order_ref)
        sale_order.client_order_ref = "ABC000"
        sale_order.save()
