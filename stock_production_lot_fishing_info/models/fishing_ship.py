# Copyright 2022 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl
from odoo import fields, models


class FishingShip(models.Model):
    _name = "fishing.ship"
    _description = "Fishing Ship"

    code = fields.Char()
    name = fields.Char(required=True)
    license_plate = fields.Char()
