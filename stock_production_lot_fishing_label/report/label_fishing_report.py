# Copyright 2023 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import time

from odoo import api, models
from odoo.tools import float_is_zero


class LabelFishingReport(models.AbstractModel):
    _name = "report.stock_production_lot_fishing_label.label_fishing_report"
    _description = "Report Fishing Label"

    @api.model
    def _get_report_values(self, docids, data=None):
        model = self.env.context.get("active_model", "stock.move.line")
        sotck_move_lines = self.env[model].browse(docids)
        report_langs = {}
        for sml in sotck_move_lines:
            moves = self.env["stock.move"].browse(
                list(sml.move_id._rollup_move_dests({sml.move_id.id}))
            )
            move_sale = moves.filtered("sale_line_id")[:1]
            if move_sale:
                report_langs[sml] = ["es_ES"]
                lang = move_sale.partner_id.lang
                if lang != "es_ES":
                    report_langs[sml].append(lang)
            else:
                report_langs[sml] = ["ca_ES", "es_ES", "en_US", "fr_FR"]
        docargs = {
            "doc_ids": docids,
            "doc_model": model,
            "docs": sotck_move_lines,
            "time": time,
            "report_langs": report_langs,
            "float_is_zero": float_is_zero,
            # TODO: Compute values
            "show_nutritional_table": False,
            "use_second_page": False,
            "show_client_elaborations": True,
        }
        return docargs
