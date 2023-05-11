# Copyright 2019 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class WizStockBarcodesRead(models.TransientModel):
    _inherit = "wiz.stock.barcodes.read"

    set_secondary_unit_one_by_one = fields.Boolean(
        string="Set secondary unit one by one",
    )
