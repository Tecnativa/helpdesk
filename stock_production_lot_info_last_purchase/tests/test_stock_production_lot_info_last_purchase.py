# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import Form, TransactionCase


class TestPurchaseOrder(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super(TestPurchaseOrder, cls).setUpClass()
        cls.supplier = cls.env["res.partner"].create({"name": "Supplier for testing"})
        cls.supplier_2 = cls.env["res.partner"].create(
            {"name": "Supplier2 for testing"}
        )
        # Product with tracking
        cls.product = cls.env["product.product"].create(
            {"name": "product for tests", "type": "product", "tracking": "lot"}
        )
        cls.fao_fishing_area_attribute = cls.env.ref(
            "product_fao_fishing.fao_fishing_area"
        )

    def _create_purchse_order(self, supplier=False):
        po_form = Form(self.env["purchase.order"])
        po_form.partner_id = supplier or self.supplier
        with po_form.order_line.new() as line_a:
            line_a.product_id = self.product
            line_a.product_qty = 10.0
            line_a.price_unit = 25.00
        return po_form.save()

    def test_copy_lot_info_from_last_purchase(self):
        po = self._create_purchse_order()
        po.button_confirm()
        picking = po.picking_ids
        picking.move_line_ids.lot_name = "LOT-00001"
        picking.move_line_ids.qty_done = 10.0
        picking.button_validate()
        # Fill some data in lot created in reception
        fao_fishing_area_01 = self.env["product.attribute.value"].search(
            [("attribute_id", "=", self.fao_fishing_area_attribute.id)]
        )[:1]
        picking.move_line_ids.lot_id.fao_fishing_area_id = fao_fishing_area_01
        picking.move_line_ids.lot_id.quality = "HG-10"

        # Do a second po for the same supplier, the new lot created must have the same
        # lot info.
        po2 = self._create_purchse_order()
        po2.button_confirm()
        picking2 = po2.picking_ids
        picking2.move_line_ids.lot_name = "LOT-00002"
        picking2.move_line_ids.qty_done = 10.0
        picking2.button_validate()

        self.assertEqual(
            picking2.move_line_ids.lot_id.fao_fishing_area_id, fao_fishing_area_01
        )
        self.assertEqual(picking2.move_line_ids.lot_id.quality, "HG-10")

        # Do a third po for the same product but with distinct product, the new lot
        # created must have the False lot info.
        po3 = self._create_purchse_order(supplier=self.supplier_2)
        po3.button_confirm()
        picking3 = po3.picking_ids
        picking3.move_line_ids.lot_name = "LOT-00003"
        picking3.move_line_ids.qty_done = 10.0
        picking3.button_validate()

        self.assertFalse(picking3.move_line_ids.lot_id.fao_fishing_area_id)
        self.assertFalse(picking3.move_line_ids.lot_id.quality)
