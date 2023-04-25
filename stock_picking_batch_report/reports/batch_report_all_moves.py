# Copyright 2022 Tecnativa - Carlos Dauden
# Copyright 2022 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


# In this report operations are stock.move instead of stock.move.line
class ReportPrintBatchPickingAllMovesByProduct(models.AbstractModel):
    _name = "report.stock_picking_batch_report.report_batch_all_mov_prod"
    _inherit = "report.congeladosromero_custom.report_batch_picking_all_moves"
    _description = "Report batch picking all moves product elaboration"

    def key_level_0(self, operation):
        return (
            operation.picking_id.batch_id.id,
            operation.product_id.weight_type,
        )

    def new_level_0(self, operation):
        level_0_name = ""
        product = operation.product_id
        if product.weight_type:
            # Extract translated string from selection fields
            field_values = product.fields_get(["weight_type"])["weight_type"][
                "selection"
            ]
            level_0_name = dict(field_values)[product.weight_type]
        return {
            "name": level_0_name,
            "location": operation.move_line_ids[:1].location_id
            or operation.location_id,
            "location_dest": operation.move_line_ids[:1].location_dest_id
            or operation.location_dest_id,
            "l1_items": {},
        }

    def sort_level_1(self, rec_list):
        return sorted(rec_list, key=lambda rec: (rec["product"].name))

    def key_level_1(self, operation):
        res = super().key_level_1(operation)
        res_list = list(res)
        res_list.insert(1, 1 if operation.sudo().sale_line_id.elaboration_ids else 0)
        return tuple(res_list)

    def new_level_1(self, operation):
        res = super().new_level_1(operation)
        res["elaboration"] = operation.sudo().sale_line_id.elaboration_ids
        return res
