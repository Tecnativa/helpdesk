# Copyright 2022 Tecnativa - Carlos Dauden
# Copyright 2022 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ReportPrintBatchPickingAllMoves(models.AbstractModel):
    _name = "report.stock_picking_batch_report.report_bp_all_moves"
    _description = "Report Batch Picking All Moves"

    def key_level_0(self, operation):
        elevated_location = 1 if operation.location_id.posz else 0
        return (
            operation.picking_id.batch_id.id,
            elevated_location,
            operation.move_line_ids[:1].location_id.type_goods
            or operation.location_id.type_goods,
        )

    def key_level_1(self, operation):
        partner_break = operation.product_uom.id == self.env.ref("uom.product_uom_kgm")
        return (
            operation.product_id.id,
            partner_break and operation.picking_id.partner_id.id or 0,
            operation.id or 0,
            operation.secondary_uom_id.id or 0,
            operation.location_id.id or 0,
        )

    def new_level_0(self, operation):
        level_0_name = False
        location = operation.move_line_ids[:1].location_id or operation.location_id
        if location.type_goods:
            field_values = location.fields_get(["type_goods"])["type_goods"][
                "selection"
            ]
            if operation.posz:
                level_0_name = (
                    f"{dict(field_values)[operation.location_id.type_goods]} (Altura)"
                )
            else:
                level_0_name = dict(field_values)[operation.location_id.type_goods]
        return {
            "name": level_0_name,
            "location": location,
            "location_dest": operation.move_line_ids[:1].location_dest_id,
            "l1_items": {},
        }

    @api.model
    def new_level_1(self, operation):
        locations = (
            operation.move_line_ids.mapped("location_id")
            or operation.location_id._get_putaway_strategy(operation.product_id)
            or operation.location_id
        )
        vals = {
            "product": operation.product_id,
            "product_qty": (operation.quantity_done or operation.reserved_availability),
            "initial_demand": operation.product_uom_qty,
            "operations": operation,
            "secondary_uom": operation.secondary_uom_id,
            "locations": locations,
        }
        if operation.secondary_uom_id:
            vals["secondary_uom_qty"] = vals["secondary_uom"]._get_secondary_qty(
                vals["product_qty"], operation.product_uom
            )
        else:
            vals["secondary_uom_qty"] = 0.0
        return vals

    def update_level_1(self, group_dict, operation):
        group_dict["product_qty"] += (
            operation.quantity_done or operation.reserved_availability
        )
        group_dict["initial_demand"] += operation.product_uom_qty
        group_dict["operations"] += operation
        if operation.secondary_uom_id:
            group_dict["secondary_uom_qty"] = group_dict[
                "secondary_uom"
            ]._get_secondary_qty(group_dict["product_qty"], operation.product_uom)
        return group_dict

    def sort_level_0(self, rec_list):
        return sorted(rec_list, key=lambda rec: (rec["location"].type_goods or ""))

    def sort_level_1(self, rec_list):
        return sorted(
            rec_list,
            key=lambda rec: (
                rec["locations"][:1].posx,
                rec["locations"][:1].posy,
                rec["locations"][:1].posz,
                rec["locations"][:1].name,
                rec["product"].default_code or "",
                rec["product"].name,
            ),
        )

    def _get_grouped_data(self, batch):
        grouped_data = {}
        for op in batch.move_ids:
            l0_key = self.key_level_0(op)
            if l0_key not in grouped_data:
                grouped_data[l0_key] = self.new_level_0(op)
            l1_key = self.key_level_1(op)
            if l1_key in grouped_data[l0_key]["l1_items"]:
                self.update_level_1(grouped_data[l0_key]["l1_items"][l1_key], op)
            else:
                grouped_data[l0_key]["l1_items"][l1_key] = self.new_level_1(op)
        for l0_key in list(grouped_data.keys()):
            grouped_data[l0_key]["l1_items"] = self.sort_level_1(
                list(grouped_data[l0_key]["l1_items"].values())
            )
        return self.sort_level_0(list(grouped_data.values()))

    def _get_report_values(self, docids, data=None):
        report_name = "stock_picking_batch_report.report_bp_all_moves"
        report_obj = self.env["ir.actions.report"]
        report = report_obj._get_report_from_name(report_name)
        docargs = {
            "doc_ids": docids,
            "doc_model": report.model,
            "docs": self.env[report.model].browse(docids),
            "get_grouped_data": self._get_grouped_data,
            "now": fields.Datetime.now,
            "uom_kg": self.env.ref("uom.product_uom_kgm"),
        }
        return docargs


# In this report operations are stock.move instead of stock.move.line
class ReportPrintBatchPickingAllMovesByProduct(models.AbstractModel):
    _name = "report.stock_picking_batch_report.report_batch_all_mov_prod"
    _inherit = "report.stock_picking_batch_report.report_bp_all_moves"
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
