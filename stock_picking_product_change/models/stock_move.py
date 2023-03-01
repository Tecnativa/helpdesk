# Copyright 2019 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_so_line_from_move(self):
        """ Get so line for chained moves """
        self.ensure_one()
        sale_line = self.sale_line_id
        while not sale_line and self.move_dest_ids:
            sale_line = self.move_dest_ids[:1]._get_so_line_from_move()
        return sale_line
