# Copyright 2022 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl
from odoo import api, fields, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    def _get_fao_fishing_area_domain(self):
        return [
            (
                "attribute_id",
                "=",
                self.env.ref("product_fao_fishing.fao_fishing_area").id,
            )
        ]

    def _get_fao_fishing_technique_domain(self):
        return [
            (
                "attribute_id",
                "=",
                self.env.ref("product_fao_fishing.fao_fishing_technique").id,
            )
        ]

    fao_fishing_area_id = fields.Many2one(
        comodel_name="product.attribute.value",
        domain=lambda self: self._get_fao_fishing_area_domain(),
        compute="_compute_fao_fishing",
        readonly=False,
        store=True,
        string="Fishing Area",
    )
    fao_fishing_technique_id = fields.Many2one(
        comodel_name="product.attribute.value",
        domain=lambda self: self._get_fao_fishing_technique_domain(),
        compute="_compute_fao_fishing",
        readonly=False,
        store=True,
        string="Fishing Technique",
    )

    @api.depends("product_id")
    def _compute_fao_fishing(self):
        for lot in self:
            lot.fao_fishing_area_id = fields.first(
                lot.product_id.fao_fishing_area_ids
            ).id
            lot.fao_fishing_technique_id = fields.first(
                lot.product_id.fao_fishing_technique_ids
            ).id
