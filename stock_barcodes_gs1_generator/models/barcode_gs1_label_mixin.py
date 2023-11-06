# Copyright 2023 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from babel.dates import format_date

from odoo import api, fields, models


class BarcodeGs1LabelMixin(models.AbstractModel):
    _name = "barcode.gs1.label.mixin"
    _description = "Barcode Gs1 Label Mixin"
    _qty_field = []

    barcode = fields.Char(compute="_compute_barcode")
    barcode_human_readable = fields.Char(compute="_compute_barcode_human_readable")

    @api.depends(lambda s: ["product_id", "lot_id"] + s._qty_field)
    def _compute_barcode(self):
        for record in self:
            pattern = ""
            if not record.product_id.barcode:
                record.barcode = ""
                continue
            pattern += f"01{record.product_id.barcode}"
            pattern += f"3103{str(int(record[self._qty_field[0]] * 1000)).zfill(6)}"
            if record.lot_id:
                if record.lot_id.expiration_date:
                    pattern += "15{}".format(
                        format_date(record.lot_id.expiration_date, format="YYMdd")
                    )
                pattern += f"10{record.lot_id.name}"
            record.barcode = pattern

    @api.depends(lambda s: ["product_id", "lot_id"] + s._qty_field)
    def _compute_barcode_human_readable(self):
        for record in self:
            pattern = ""
            if not record.product_id.barcode:
                record.barcode_human_readable = ""
                continue
            pattern += f"(01){record.product_id.barcode}"
            pattern += f"(3103){str(int(record[self._qty_field[0]] * 1000)).zfill(6)}"
            if record.lot_id:
                if record.lot_id.expiration_date:
                    pattern += "(15){}".format(
                        format_date(record.lot_id.expiration_date, format="YYMdd")
                    )
                pattern += f"(10){record.lot_id.name}"
            record.barcode_human_readable = pattern
