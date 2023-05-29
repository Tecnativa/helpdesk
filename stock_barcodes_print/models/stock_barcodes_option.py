# Copyright 2019 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockBarcodesOptionGroup(models.Model):
    _inherit = "stock.barcodes.option.group"

    auto_print_on_confirm = fields.Boolean(
        string="Auto print label report",
        help="Print label report when the read has been confirmed",
    )
