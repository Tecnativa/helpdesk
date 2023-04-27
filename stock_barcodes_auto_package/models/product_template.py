# Copyright 2018 Sergio Teruel - Tecnativa <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    auto_put_in_pack_on_read = fields.Boolean(
        string="Auto put in pack in read barcode",
        help="Auto put in pack when a barcode is readed",
    )
