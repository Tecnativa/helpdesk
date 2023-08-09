# Copyright 2023 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import time

from odoo import api, models
from odoo.tools import float_is_zero


class LabelFishingReportMixin(models.AbstractModel):
    _name = "label.fishing.report.mixin"
    based_model = ""

    def _compute_langs_print_partner(self, model_name, line):
        report_langs = ["ca_ES", "es_ES", "en_US", "fr_FR"]
        print_partner = False
        if model_name != "stock.quant":
            move_line = (
                line if model_name == "stock.move.line" else line["move_line_id"]
            )
            moves = self.env["stock.move"].browse(
                list(move_line["move_id"]._rollup_move_dests({move_line["move_id"].id}))
            )
            move_sale = moves.filtered("sale_line_id")[:1]
            if move_sale:
                print_partner = True
                report_langs = ["es_ES"]
                lang = move_sale.partner_id.lang
                if lang != "es_ES":
                    report_langs.append(lang)
        return report_langs, print_partner

    def _get_summarized_lines(self, lines):
        summarized_lines = []
        while lines:
            reference_line = lines[0]
            filtered_lines = lines.filtered(
                lambda line: line.product_id == reference_line.product_id
                and line.result_package_id.master_box_id
                == reference_line.result_package_id.master_box_id
                and line.lot_id == reference_line.lot_id
            )
            lines -= filtered_lines
            summarized_lines.append(
                {
                    "id": str(reference_line.lot_id.id)
                    + str(reference_line.product_id.id)
                    + str(reference_line.move_line_id.picking_id.id),
                    "lot_id": reference_line.lot_id,
                    "product_id": reference_line.product_id,
                    "label_qty": reference_line.wizard_id.label_qty,
                    "picking_partner_id": reference_line.move_line_id.picking_partner_id,
                    "move_id": reference_line.move_line_id.move_id,
                    "product_uom_id": reference_line.move_line_id.product_uom_id,
                    "qty_done": sum(filtered_lines.mapped("quantity")),
                    "result_package_id": reference_line.result_package_id,
                    "move_line_id": reference_line.move_line_id,
                }
            )
        return summarized_lines

    @api.model
    def _get_report_values(self, docids, data=None):
        model_name = self.based_model
        summarized = False
        lines_to_print = self.env[model_name].browse(docids)
        report_langs = {}
        client_elaborations = {}
        if self.based_model == "stock.picking.line.print":
            wiz = lines_to_print[:1].wizard_id
            if wiz.is_summary_label:
                summarized = True
                lines_to_print = self._get_summarized_lines(lines_to_print)
        for line in lines_to_print:
            langs, client_el = self._compute_langs_print_partner(model_name, line)
            report_langs[line["id"]] = langs
            client_elaborations[line["id"]] = client_el
        docargs = {
            "summarized": summarized,
            "env": self.env,
            "doc_ids": docids,
            "doc_model": model_name,
            "docs": lines_to_print,
            "time": time,
            "report_langs": report_langs,
            "float_is_zero": float_is_zero,
            "show_nutritional_table": self.env.context.get(
                "show_nutritional_table", False
            ),
            "use_second_page": self.env.context.get("use_second_page", False),
            "client_elaborations": client_elaborations,
            "company_id": self.env.company,
        }
        return docargs


# pylint: disable=R7980
class LabelFishingReport(models.AbstractModel):
    _inherit = "label.fishing.report.mixin"
    _name = "report.stock_production_lot_fishing_label.label_fishing"
    _description = "Report Fishing Label"
    based_model = "stock.picking.line.print"


# pylint: disable=R7980
class LabelFishingReportNutri(models.AbstractModel):
    _inherit = "label.fishing.report.mixin"
    _name = "report.stock_production_lot_fishing_label.label_fishing_nutri"
    _description = "Report Fishing Label"
    based_model = "stock.picking.line.print"

    @api.model
    def _get_report_values(self, docids, data=None):
        self = self.with_context(use_second_page=True, show_nutritional_table=True)
        return super()._get_report_values(docids, data=data)


# pylint: disable=R7980
class LabelFishingReportMove(models.AbstractModel):
    _inherit = "label.fishing.report.mixin"
    _name = "report.stock_production_lot_fishing_label.label_fishing_move"
    _description = "Report Fishing Label Move"
    based_model = "stock.move.line"


# pylint: disable=R7980
class LabelFishingReportQuant(models.AbstractModel):
    _inherit = "label.fishing.report.mixin"
    _name = "report.stock_production_lot_fishing_label.label_fishing_quant"
    _description = "Report Fishing Label Quant"
    based_model = "stock.quant"
