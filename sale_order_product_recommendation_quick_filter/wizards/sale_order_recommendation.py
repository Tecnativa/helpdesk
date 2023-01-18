# Copyright 2019 David Vidal <david.vidal@tecnativa.com>
# Copyright 2020 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrderRecommendation(models.TransientModel):
    _inherit = "sale.order.recommendation"

    quick_filter_recommendation = fields.Selection(
        [
            ("previous_sale_order", "Previous Orders"),
            ("product_fresh", "Company Fresh"),
            ("product_frozen", "Company Frozen"),
            ("supplier_info_fresh", "External Fresh"),
            ("supplier_info_frozen", "External Frozen"),
            ("all", "All"),
        ],
        string="Recommendations",
    )

    @api.onchange("quick_filter_recommendation")
    def _onchange_gamma_attribute_value(self):
        if self.quick_filter_recommendation == "previous_sale_order":
            self.origin_recommendation = "sale_order"
            self.product_attribute_value_id = False
        elif self.quick_filter_recommendation == "product_fresh":
            self.origin_recommendation = "products"
            self.product_attribute_value_id = self.env.ref(
                "product_fishing.product_gamma_f"
            )
        elif self.quick_filter_recommendation == "product_frozen":
            self.origin_recommendation = "products"
            self.product_attribute_value_id = self.env.ref(
                "product_fishing.product_gamma_c"
            )
        elif self.quick_filter_recommendation == "supplier_info_fresh":
            self.origin_recommendation = "supplierinfo"
            self.product_attribute_value_id = self.env.ref(
                "product_fishing.product_gamma_f"
            )
        elif self.quick_filter_recommendation == "supplier_info_frozen":
            self.origin_recommendation = "supplierinfo"
            self.product_attribute_value_id = self.env.ref(
                "product_fishing.product_gamma_c"
            )
        elif self.quick_filter_recommendation == "all":
            self.origin_recommendation = "products"
            self.product_attribute_value_id = False
            self.product_name_search = False
