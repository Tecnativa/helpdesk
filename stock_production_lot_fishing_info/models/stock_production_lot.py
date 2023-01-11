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

    def _get_harvesting_method_domain(self):
        return [
            (
                "attribute_id",
                "=",
                self.env.ref("product_fishing.harvesting_method_attribute").id,
            )
        ]

    def _get_product_presentation_domain(self):
        return [
            (
                "attribute_id",
                "=",
                self.env.ref("product_fishing.presentation_attribute").id,
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
    fishing_ship_id = fields.Many2one(
        comodel_name="fishing.ship", string="Fishing Ship"
    )
    quality = fields.Char()
    packaging_date = fields.Datetime()
    presentation_id = fields.Many2one(
        comodel_name="product.attribute.value",
        domain=lambda self: self._get_product_presentation_domain(),
        compute="_compute_fao_fishing",
        readonly=False,
        store=True,
        string="Presentation",
    )
    harvesting_id = fields.Many2one(
        comodel_name="product.attribute.value",
        domain=lambda self: self._get_harvesting_method_domain(),
        compute="_compute_fao_fishing",
        readonly=False,
        store=True,
        string="Harvesting Method",
    )
    country_id = fields.Many2one(comodel_name="res.country")
    caliber_id = fields.Many2many(
        related="product_id.product_template_variant_value_ids", string="Caliber"
    )

    @api.depends("product_id")
    def _compute_fao_fishing(self):
        for lot in self:
            if len(lot.product_id.fao_fishing_area_ids) == 1:
                lot.fao_fishing_area_id = lot.product_id.fao_fishing_area_ids[0].id
            if len(lot.product_id.fao_fishing_technique_ids) == 1:
                lot.fao_fishing_technique_id = lot.product_id.fao_fishing_technique_ids[
                    0
                ].id
            if len(lot.product_id.presentation_ids) == 1:
                lot.presentation_id = lot.product_id.presentation_ids[0].id
            if len(lot.product_id.harvesting_method_ids) == 1:
                lot.harvesting_id = lot.product_id.harvesting_method_ids[0].id
