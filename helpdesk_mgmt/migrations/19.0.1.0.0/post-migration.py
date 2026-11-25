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
    # set the number to the ticket id
    openupgrade.logged_query(
        env.cr,
        "UPDATE helpdesk_ticket SET number = id",
    )
    # Set the sequence number_next_actual to the nest ticket id
    env.cr.execute(
        "SELECT CASE WHEN is_called THEN last_value + 1 "
        "ELSE last_value END FROM helpdesk_ticket_id_seq"
    )
    next_ticket_id = env.cr.fetchall()
    env.ref("helpdesk_mgmt.helpdesk_ticket_sequence").write(
        {
            "padding": 4,
            "prefix": "",
            "number_next_actual": next_ticket_id[0][0],
        }
    )
