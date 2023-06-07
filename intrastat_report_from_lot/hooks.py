# Copyright 2023 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import SUPERUSER_ID, api


def post_init_hook(cr, registry, vals=None):
    """Set is_country_attr True in 'Origin country' product attribute,
    to show the column 'Country' in its 'attribute values' list view."""
    env = api.Environment(cr, SUPERUSER_ID, {})
    env.ref("product_fishing.product_origin_country_attribute").is_country_attr = True
