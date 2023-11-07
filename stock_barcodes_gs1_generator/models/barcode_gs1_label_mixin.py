# Copyright 2023 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from babel.dates import format_date

from odoo import api, fields, models


class BarcodeGs1LabelMixin(models.AbstractModel):
    _name = "barcode.gs1.label.mixin"
    _description = "Barcode Gs1 Label Mixin"
    _qty_field = False

    barcode = fields.Char(compute="_compute_barcode")
    barcode_human_readable = fields.Char(compute="_compute_barcode_human_readable")

    @api.model
    def _get_field_gs1_depends(self):
        field_list = [
            "product_id",
        ]
        if self._name != "stock.production.lot":
            field_list.append("lot_id")
        if self._qty_field:
            field_list.append(self._qty_field)
        return field_list

    def _get_lot_record(self):
        # Is the record a lot?
        if self._name == "stock.production.lot":
            lot = self
        else:
            lot = self.lot_id
        return lot

    @api.depends(lambda s: s._get_field_gs1_depends())
    def _compute_barcode(self):
        product_identifier = self.env.context.get("product_gs1_identifier", "02")
        for record in self:
            pattern = ""
            if not record.product_id.barcode:
                record.barcode = ""
                continue
            pattern += f"{product_identifier}{record.product_id.barcode}"
            if self._qty_field:
                pattern += f"3103{str(int(record[self._qty_field] * 1000)).zfill(6)}"
            lot = self._get_lot_record()
            if lot:
                if lot.expiration_date:
                    pattern += "15{}".format(
                        format_date(lot.expiration_date, format="YYMdd")
                    )
                pattern += f"10{lot.name}"
            record.barcode = pattern

    @api.depends(lambda s: s._get_field_gs1_depends())
    def _compute_barcode_human_readable(self):
        product_identifier = self.env.context.get("product_gs1_identifier", "02")
        for record in self:
            pattern = ""
            if not record.product_id.barcode:
                record.barcode_human_readable = ""
                continue
            pattern += f"({product_identifier}){record.product_id.barcode}"
            if self._qty_field:
                pattern += f"(3103){str(int(record[self._qty_field] * 1000)).zfill(6)}"
            lot = self._get_lot_record()
            if lot:
                if lot.expiration_date:
                    pattern += "(15){}".format(
                        format_date(lot.expiration_date, format="YYMdd")
                    )
                pattern += f"(10){lot.name}"
            record.barcode_human_readable = pattern
