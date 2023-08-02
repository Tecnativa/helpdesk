# Copyright 2023 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import io

from odoo import fields, models


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    can_be_summarized = fields.Boolean()
    single_rendering = fields.Boolean()

    def _render_qweb_pdf(self, res_ids=None, data=None):
        """Overwritten method to allow separate computation of report headers"""
        if self.single_rendering and len(res_ids) > 1:
            pdfs = []
            for res_id in res_ids:
                pdf = io.BytesIO(
                    super()._render_qweb_pdf(res_ids=[res_id], data=data)[0]
                )
                pdfs.append(pdf)
            return self._merge_pdfs(pdfs), "pdf"
        return super()._render_qweb_pdf(res_ids=res_ids, data=data)
