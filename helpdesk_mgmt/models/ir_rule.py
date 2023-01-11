# Copyright 2023 Tecnativa - Víctor Martínez
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, models, tools
from odoo.osv import expression
from odoo.tools import config


class IrRule(models.Model):
    _inherit = "ir.rule"

    @api.model
    @tools.conditional(
        "xml" not in config["dev_mode"],
        tools.ormcache(
            "self.env.uid",
            "self.env.su",
            "model_name",
            "mode",
            "tuple(self._compute_domain_context_values())",
        ),
    )
    def _compute_domain(self, model_name, mode="read"):
        """Inject extra domain for restricting tickets when the user
        has the group 'User: Team tickets'.
        Re-create domain to remove helpdesk_ticket_personal_rule and avoid the use case
        of accessing an unassigned ticket from another team.
        """
        res = super()._compute_domain(model_name, mode=mode)
        user = self.env.user
        group1 = "helpdesk_mgmt.group_helpdesk_user_team"
        group2 = "helpdesk_mgmt.group_helpdesk_user"
        if model_name == "helpdesk.ticket" and not self.env.su:
            if user.has_group(group1) and not user.has_group(group2):
                res = [
                    "|",
                    ("company_id", "=", False),
                    ("company_id", "in", self.env.companies.ids),
                ]
                extra_domain = [
                    "|",
                    ("team_id", "in", user.helpdesk_team_ids.ids),
                    ("team_id", "=", False),
                ]
                res = expression.AND([extra_domain, res])
        return res
