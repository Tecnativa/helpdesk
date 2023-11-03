# Copyright 2019 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def write(self, vals):
        # Cuando se cambia de producto se confirma con el contexto force_create_move
        # para evitar error de stock negativo. Al pasar este contexto se graba el
        # stock move line con barcode_scan_state = 'force_done' con lo que ya no está
        # pending. Con esto hacemos que el sml siga estando pendiente
        if (
            self.env.context.get("skip_done_force_state", False)
            and "barcode_scan_state" in vals
        ):
            vals.pop("barcode_scan_state", None)
        return super().write(vals)
