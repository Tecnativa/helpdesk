# Copyright 2023 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import date, datetime

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
            # pattern += f"{product_identifier}{record.product_id.barcode}" + '&#29'
            # fnc = "\x1d"
            # pp = r"(Alt029|#|\x1D)"
            if len(record.product_id.barcode) == 14:
                product_barcode = record.product_id.barcode
            else:
                # zero left padding
                product_barcode = record.product_id.barcode.zfill(14)
                # Send GS (Group separator non ASCII char)
                # product_barcode = record.product_id.barcode + '^029'

            pattern += f"{product_identifier}{product_barcode}"
            if self._qty_field:
                pattern += f"3103{str(int(record[self._qty_field] * 1000)).zfill(6)}"
            lot = record._get_lot_record()
            if lot:
                if lot.expiration_date:
                    pattern += "15{}".format(
                        format_date(lot.expiration_date, format="YYMMdd")
                    )
                pattern += f"10{lot.name}"
            record.barcode = pattern

    @api.depends(lambda s: s._get_field_gs1_depends())
    def _compute_barcode_human_readable(self):
        gs1_nomenclature = self.env.ref(
            "barcodes_gs1_nomenclature.default_gs1_nomenclature"
        )
        for record in self:
            # Try parse the barcode generated to print set a human readable string
            gs1_list = gs1_nomenclature.parse_barcode(record.barcode)
            readable_string = ""
            for element in gs1_list:
                # Use string_value key to keep the original values without format
                readable_string += f"({element['ai']}){element['string_value']}"
            record.barcode_human_readable = readable_string

    @api.model
    def get_gs1_barcode(self, record, gs1_structure_list):
        gs1_barcode = ""
        gs1_barcode_human_readable = ""
        for ai, field_path in gs1_structure_list:
            value = record
            for fname in field_path.split("."):
                if fname in value:
                    value = value[fname]
                elif hasattr(value, fname):
                    fname = getattr(value, fname)
                    value = value[fname]
            if ai in ("01", "02"):
                value = value.zfill(14)
            if ai in ("3103",):
                value = str(int(value * 1000)).zfill(6)
            if isinstance(value, (date, datetime)):
                value = format_date(value, format="YYMMdd")
            gs1_barcode += f"{ai}{value}"
            gs1_barcode_human_readable += f"({ai}){value}"
        return gs1_barcode, gs1_barcode_human_readable
