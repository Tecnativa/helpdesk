# Copyright 2022 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl
from odoo import fields, models


class FishingShip(models.Model):
    _inherit = "res.company"
    _description = "Fishing Ship"

    sanitary_registry = fields.Char()
