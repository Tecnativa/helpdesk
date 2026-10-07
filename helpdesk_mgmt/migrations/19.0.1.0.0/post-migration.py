# Copyright 2026 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # helpdesk teams for stages
    openupgrade.logged_query(
        env.cr,
        "INSERT INTO helpdesk_ticket_stage_helpdesk_ticket_team_rel "
        "(helpdesk_ticket_team_id, helpdesk_ticket_stage_id) "
        "SELECT helpdesk_team_id, helpdesk_stage_id FROM team_stage_rel",
    )
