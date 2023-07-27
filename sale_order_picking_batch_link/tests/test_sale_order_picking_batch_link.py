# Copyright 2023 Tecnativa - Stefan Ungureanu
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests.common import TransactionCase


class TestSaleOrderPickingBatchLink(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.stock_location = cls.env.ref("stock.stock_location_stock")
        cls.customer_location = cls.env.ref("stock.stock_location_customers")
        cls.picking_type_out = cls.env["ir.model.data"]._xmlid_to_res_id(
            "stock.picking_type_out"
        )
        cls.env["stock.picking.type"].browse(
            cls.picking_type_out
        ).reservation_method = "manual"
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "partner for test",
            }
        )
        cls.productA = cls.env["product.product"].create(
            {
                "name": "Product A",
                "type": "product",
            }
        )
        cls.picking_client = cls.env["stock.picking"].create(
            {
                "location_id": cls.stock_location.id,
                "location_dest_id": cls.customer_location.id,
                "picking_type_id": cls.picking_type_out,
                "company_id": cls.env.company.id,
            }
        )
        cls.order = cls.env["sale.order"].create(
            {
                "partner_id": cls.partner.id,
                "picking_ids": cls.picking_client,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": cls.productA.id,
                            "product_uom_qty": 5,
                            "price_unit": 20,
                        },
                    )
                ],
            }
        )
        cls.batch = cls.env["stock.picking.batch"].create(
            {
                "name": "Batch 1",
                "company_id": cls.env.company.id,
            }
        )

    def test_sale_order_picking_batch_link(self):
        self.assertEqual(len(self.order.picking_batch_ids), 0)
        self.batch.write({"picking_ids": [(4, self.picking_client.id)]})
        self.order._compute_picking_batch_ids()
        self.assertEqual(len(self.order.picking_batch_ids), 1)
