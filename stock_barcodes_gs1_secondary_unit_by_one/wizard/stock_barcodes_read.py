# Copyright 2019 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class WizStockBarcodesRead(models.AbstractModel):
    _inherit = "wiz.stock.barcodes.read"

    set_secondary_unit_one_by_one = fields.Boolean(
        string="Set secondary unit one by one",
    )

    def reset_qty(self):
        res = super().reset_qty()
        if self.set_secondary_unit_one_by_one and self.secondary_uom_id:
            self.secondary_uom_qty = 1.0
        else:
            self.secondary_uom_qty = 0.0
        return res

    def action_clean_values(self):
        res = super().action_clean_values()
        if self.set_secondary_unit_one_by_one and self.secondary_uom_id:
            self.secondary_uom_qty = 1.0
        else:
            self.secondary_uom_qty = 0.0
        return res

    @api.onchange("secondary_uom_id", "set_secondary_unit_one_by_one")
    def onchange_secondary_uom_id(self):
        if self.set_secondary_unit_one_by_one and self.secondary_uom_id:
            self.secondary_uom_qty = 1.0
        else:
            self.secondary_uom_qty = 0.0
