# Copyright 2023 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import SUPERUSER_ID, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def write(self, vals):
        if vals.get("tracking", False) == "lot":
            self_sudo = self.with_user(SUPERUSER_ID)
            lot_name = "000000"
            for product in self_sudo.product_variant_ids:
                quants = self_sudo.env["stock.quant"].search(
                    [("product_id", "=", product.id), ("lot_id", "=", False)]
                )
                if not quants:
                    continue
                for company in quants.mapped("company_id"):
                    lot = (
                        self_sudo.env["stock.production.lot"]
                        .with_company(company)
                        .create(
                            {
                                "name": lot_name,
                                "product_id": product.id,
                                "company_id": company.id,
                            }
                        )
                    )
                    quants.filtered(lambda q: q.company_id == company).lot_id = lot
                    # Actualizar sml en estado por hacer
                    smls = self_sudo.env["stock.move.line"].search(
                        [
                            ("company_id", "=", company.id),
                            ("product_id", "=", product.id),
                            ("state", "not in", ["done", "cancel"]),
                        ]
                    )
                    smls.with_context(bypass_reservation_update=True).lot_id = lot.id
        return super(ProductTemplate, self).write(vals)
