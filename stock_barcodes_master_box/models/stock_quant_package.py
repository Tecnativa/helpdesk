# Copyright 2023 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockQuantPackage(models.Model):
    _inherit = "stock.quant.package"

    master_box_id = fields.Many2one(comodel_name="stock.quant.master.box")

    def name_get(self):
        if self.env.context.get("hide_master_box_in_package_name", False):
            return super().name_get()
        self.browse(self.ids).read(["name", "master_box_id"])
        return [
            (
                package.id,
                "%s%s"
                % (
                    package.name,
                    package.master_box_id
                    and " (%s)" % package.master_box_id.name
                    or "",
                ),
            )
            for package in self
        ]
