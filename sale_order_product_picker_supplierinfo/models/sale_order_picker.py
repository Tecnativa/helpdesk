# Copyright 2023 Tecnativa - Carlos Dauden
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class SaleOrderPicker(models.Model):
    _inherit = "sale.order.picker"

    supplierinfo_id = fields.Many2one(comodel_name="product.supplierinfo")
    vendor_id = fields.Many2one(comodel_name="res.partner")
    vendor_comment = fields.Char()

    def _get_picker_price_unit_context(self):
        ctx = super()._get_picker_price_unit_context()
        if self.vendor_id:
            ctx["force_filter_supplier_id"] = self.vendor_id
        return ctx
