# Copyright 2023 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import time

from odoo import api, models
from odoo.tools import float_is_zero


class LabelFishingReportMixin(models.AbstractModel):
    _name = "label.fishing.report.mixin"

    def _compute_langs(self, move_line=False):
        report_langs = ["ca_ES", "es_ES", "en_US", "fr_FR"]
        if move_line:
            moves = self.env["stock.move"].browse(
                list(move_line.move_id._rollup_move_dests({move_line.move_id.id}))
            )
            move_sale = moves.filtered("sale_line_id")[:1]
            if move_sale:
                report_langs = ["es_ES"]
                lang = move_sale.partner_id.lang
                if lang != "es_ES":
                    report_langs.append(lang)
        return report_langs


# pylint: disable=R7980
class LabelFishingReport(models.AbstractModel):
    _inherit = "label.fishing.report.mixin"
    _name = "report.stock_production_lot_fishing_label.label_fishing"
    _description = "Report Fishing Label"

    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env.context.get("active_model", "stock.picking.line.print")
        lines_to_print = self.env[model].browse(docids)
        report_langs = {}
        for line in lines_to_print:
            report_langs[line] = self._compute_langs(move_line=line.move_line_id)
        docargs = {
            "doc_ids": docids,
            "doc_model": model,
            "docs": lines_to_print,
            "time": time,
            "report_langs": report_langs,
            "float_is_zero": float_is_zero,
            # TODO: Compute values
            "show_nutritional_table": False,
            "use_second_page": False,
            "show_client_elaborations": False,
        }
        return docargs


# pylint: disable=R7980
class LabelFishingReportMove(models.AbstractModel):
    _inherit = "label.fishing.report.mixin"
    _name = "report.stock_production_lot_fishing_label.label_fishing_move"
    _description = "Report Fishing Label Move"

    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env.context.get("active_model", "stock.move.line")
        lines_to_print = self.env[model].browse(docids)
        report_langs = {}
        for line in lines_to_print:
            report_langs[line] = self._compute_langs(move_line=line)
        docargs = {
            "doc_ids": docids,
            "doc_model": model,
            "docs": lines_to_print,
            "time": time,
            "report_langs": report_langs,
            "float_is_zero": float_is_zero,
            # TODO: Compute values
            "show_nutritional_table": False,
            "use_second_page": False,
            "show_client_elaborations": False,
        }
        return docargs


class LabelFishingReportQuant(models.AbstractModel):
    _inherit = "label.fishing.report.mixin"
    _name = "report.stock_production_lot_fishing_label.label_fishing_quant"
    _description = "Report Fishing Label Quant"

    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env.context.get("active_model", "stock.quant")
        lines_to_print = self.env[model].browse(docids)
        report_langs = {}
        for line in lines_to_print:
            report_langs[line] = self._compute_langs()
        docargs = {
            "doc_ids": docids,
            "doc_model": model,
            "docs": lines_to_print,
            "time": time,
            "report_langs": report_langs,
            "float_is_zero": float_is_zero,
            # TODO: Compute values
            "show_nutritional_table": False,
            "use_second_page": False,
            "show_client_elaborations": False,
        }
        return docargs
