# Copyright 2019 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockBarcodesOptionGroup(models.Model):
    _inherit = "stock.barcodes.option.group"

    auto_put_in_pack_on_read = fields.Boolean(
        string="Auto put in pack in read barcode",
        help="Auto put in pack when a barcode is read and product is checked to do it",
    )
