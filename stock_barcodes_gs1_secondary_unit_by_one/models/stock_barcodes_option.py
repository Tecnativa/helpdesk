# Copyright 2023 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockBarcodesOptionGroup(models.Model):
    _inherit = "stock.barcodes.option.group"

    set_secondary_unit_one_by_one = fields.Boolean(
        string="Set secondary unit one by one",
    )
