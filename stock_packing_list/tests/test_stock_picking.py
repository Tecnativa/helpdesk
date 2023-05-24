# Copyright 2021 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo.tests import Form, common


class TestStockPicking(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product_a = cls.env["product.product"].create(
            {"name": "Product Test A", "type": "product", "hs_code": "CODE-A"}
        )
        cls.product_b = cls.env["product.product"].create(
            {"name": "Product Test B", "type": "product", "hs_code": "CODE-B"}
        )
        cls.picking = cls._create_stock_picking(cls)

    def _create_stock_picking(self):
        picking_form = Form(
            self.env["stock.picking"].with_context(
                default_picking_type_id=self.env.ref("stock.picking_type_out").id
            )
        )
        with picking_form.move_ids_without_package.new() as line_form:
            line_form.product_id = self.product_a
            line_form.product_uom_qty = 1
        with picking_form.move_ids_without_package.new() as line_form:
            line_form.product_id = self.product_b
            line_form.product_uom_qty = 1
        picking = picking_form.save()
        picking.action_confirm()
        return picking

    def _create_add_item_to_packing_list(self, item, product):
        wizard = Form(
            self.env["add.item.to.packing.list"].with_context(
                active_id=item.id,
            )
        )
        wizard.product_id = product
        wizard.qty = wizard.pending_qty
        record = wizard.save()
        return record.add_item_to_packing_list()

    def test_stock_picking_out(self):
        picking_form = Form(self.picking)
        with picking_form.packing_list_item_ids.new() as box_line:
            box_line.pallet_number = 1
            box_line.box_length = 100
            box_line.width = 100
            box_line.height = 100
            box_line.weight = 10
        with picking_form.packing_list_item_ids.new() as box_line:
            box_line.is_pallet = True
            box_line.pallet_number = 1
        picking_form.save()
        with picking_form.packing_list_item_ids.new() as box_line:
            box_line.pallet_number = 1
            box_line.box_length = 100
            box_line.width = 100
            box_line.height = 200
            box_line.weight = 10
        picking_form.save()
        # Box A
        box_a = self.picking.packing_list_item_ids.filtered(
            lambda x: not x.is_pallet and x.height == 100
        )
        self.assertEqual(box_a.item_number, 1)
        self.assertEqual(box_a.volume, 1)
        self._create_add_item_to_packing_list(box_a, self.product_a)
        self.assertEqual(len(box_a.list_item_ids), 1)
        self.assertEqual(box_a.list_item_ids.product_id, self.product_a)
        # Box B
        box_b = self.picking.packing_list_item_ids.filtered(
            lambda x: not x.is_pallet and x.height == 200
        )
        self.assertEqual(box_b.item_number, 2)
        self._create_add_item_to_packing_list(box_b, self.product_b)
        self.assertEqual(len(box_b.list_item_ids), 1)
        self.assertEqual(box_b.list_item_ids.product_id, self.product_b)
        self.assertEqual(box_b.volume, 2)
        # Pallet
        pallet = self.picking.packing_list_item_ids.filtered(lambda x: x.is_pallet)
        self.assertEqual(pallet.total_pallet_weight, 20)
        self.assertEqual(pallet.total_pallet_volume, 3)
        # Confirm packing list
        self.picking.confirm_packing_list()
        # Report
        report = self.env.ref("stock_packing_list.action_report_picking_packing_list")
        res = str(report.render_qweb_html(self.picking.ids)[0])
        self.assertRegexpMatches(res, "CODE-A")
        self.assertRegexpMatches(res, "CODE-B")
        self.assertRegexpMatches(res, "3.0")
