# Copyright 2023 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    can_be_summarized = fields.Boolean()
