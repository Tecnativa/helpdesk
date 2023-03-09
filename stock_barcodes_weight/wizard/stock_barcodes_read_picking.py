# Copyright 2019 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models


class WizStockBarcodesReadPicking(models.TransientModel):
    _inherit = "wiz.stock.barcodes.read.picking"

    visible_change_product = fields.Boolean()
    recommended_product_id = fields.Many2one(comodel_name="product.product")

    def _get_product_by_caliber(self, product, qty):
        calibers = self.product_id.product_tmpl_id.caliber_ids
        caliber_att = calibers[:1].attribute_id
        if calibers:
            actual_caliber = (
                self.product_id.product_template_variant_value_ids.filtered(
                    lambda v: v.attribute_id == caliber_att
                )
            )
            att_value = actual_caliber.product_attribute_value_id
            from_range = att_value.from_range * (1 - att_value.tolerance_range / 100)
            to_range = att_value.to_range * (1 + att_value.tolerance_range / 100)
            if qty < from_range or qty > to_range:
                recommended_caliber = calibers.filtered(
                    lambda c: c.from_range <= qty and c.to_range >= qty
                )
                product = (
                    self.product_id.product_tmpl_id.product_variant_ids.filtered(
                        lambda p: (
                            p.product_template_variant_value_ids.product_attribute_value_id
                            == recommended_caliber
                        )
                    )
                    or product
                )
        return product

    def check_done_conditions(self):
        res = super().check_done_conditions()
        if res:
            recommended_product = self._get_product_by_caliber(
                self.product_id, self.product_qty
            )
            if recommended_product != self.product_id and not self.env.context.get(
                "force_create_move", False
            ):
                self._set_messagge_info(
                    "more_match", _("The weight is outside the limits of the caliber")
                )
                # El peso está fuera de los limites del calibre
                self.visible_change_product = True
                self.recommended_product_id = recommended_product

                self.visible_force_done = True
                return False
        return res

    def action_change_product(self):
        moves = self.picking_id.move_lines.filtered(
            lambda ln: ln.product_id == self.recommended_product_id
        )
        if not moves:
            move = self.selected_pending_move_id.stock_move_ids[:1]
            wiz = self.env["stock.picking.product.change.wiz"].create(
                {
                    "picking_ids": [(6, 0, self.picking_id.ids)],
                    "old_product_id": self.product_id.id,
                    "new_product_id": self.recommended_product_id.id,
                    "line_ids": [
                        (
                            0,
                            0,
                            {
                                "move_id": move.id,
                                "new_product_id": self.recommended_product_id.id,
                                "product_uom_qty": self.product_qty,
                            },
                        )
                    ],
                }
            )
            wiz.action_change_product()
        if self.lot_id:
            lot = self.env["stock.production.lot"].search(
                [
                    ("product_id", "=", self.recommended_product_id.id),
                    ("name", "=", self.lot_id.name),
                ]
            )
            if not lot:
                lot = self.lot_id.copy(
                    {
                        "name": self.lot_id.name,
                        "product_id": self.recommended_product_id.id,
                    }
                )
            self.lot_id = lot
        self.product_id = self.recommended_product_id
        self.fill_todo_records()
        self.todo_line_id = self.todo_line_ids.filtered(
            lambda t: t._origin.state == "pending"
            and t.product_id == self.recommended_product_id
        )[:1]
        res = self.with_context(force_create_move=True).action_confirm()
        self.visible_change_product = False
        return res
