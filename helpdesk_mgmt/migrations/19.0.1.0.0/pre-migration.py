# Copyright 2026 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openupgradelib import openupgrade

RENAMED_XMLIDS = [
    ("helpdesk_mgmt.stage_new", "helpdesk_mgmt.helpdesk_ticket_stage_new"),
    (
        "helpdesk_mgmt.stage_in_progress",
        "helpdesk_mgmt.helpdesk_ticket_stage_in_progress",
    ),
    ("helpdesk_mgmt.stage_on_hold", "helpdesk_mgmt.helpdesk_ticket_stage_awaiting"),
    ("helpdesk_mgmt.stage_solved", "helpdesk_mgmt.helpdesk_ticket_stage_done"),
    (
        "helpdesk_mgmt.stage_cancelled",
        "helpdesk_mgmt.helpdesk_ticket_stage_cancelled",
    ),
]


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_xmlids(env.cr, RENAMED_XMLIDS)
    env["ir.model.data"].search(
        [
            ("module", "=", "helpdesk_mgmt"),
            ("name", "=", "new_ticket_request_email_template"),
        ]
    ).unlink()
    env["ir.model.data"].search(
        [
            ("module", "=", "helpdesk_mgmt"),
            ("name", "=", "solved_ticket_request_email_template"),
        ]
    ).unlink()
    openupgrade.rename_models(
        env.cr,
        [
            ("helpdesk.tag", "helpdesk.ticket.tag"),
            ("helpdesk.stage", "helpdesk.ticket.stage"),
            ("helpdesk.team", "helpdesk.ticket.team"),
        ],
    )
    openupgrade.rename_tables(
        env.cr,
        [
            ("helpdesk_stage", "helpdesk_ticket_stage"),
            ("helpdesk_tag", "helpdesk_ticket_tag"),
            ("helpdesk_team", "helpdesk_ticket_team"),
            (
                "helpdesk_tag_helpdesk_ticket_rel",
                "helpdesk_ticket_helpdesk_ticket_tag_rel",
            ),
            ("helpdesk_team_res_users_rel", "helpdesk_ticket_team_res_users_rel"),
        ],
    )
    openupgrade.rename_columns(
        env.cr,
        {
            "helpdesk_ticket_team_res_users_rel": [
                ("helpdesk_team_id", "helpdesk_ticket_team_id")
            ],
            "helpdesk_ticket_helpdesk_ticket_tag_rel": [
                ("helpdesk_tag_id", "helpdesk_ticket_tag_id")
            ],
        },
    )
    openupgrade.rename_fields(
        env,
        [
            ("helpdesk.ticket.stage", "helpdesk_ticket_stage", "is_close", "closed"),
            ("helpdesk.ticket.team", "helpdesk_ticket_team", "member_ids", "user_ids"),
            (
                "helpdesk.ticket",
                "helpdesk_ticket",
                "date_last_stage_update",
                "last_stage_update",
            ),
            ("helpdesk.ticket", "helpdesk_ticket", "assign_date", "assigned_date"),
            ("helpdesk.ticket", "helpdesk_ticket", "close_date", "closed_date"),
            ("helpdesk.ticket", "helpdesk_ticket", "duplicated_id", "duplicate_id"),
            (
                "helpdesk.ticket",
                "helpdesk_ticket",
                "ticket_count",
                "helpdesk_ticket_count",
            ),
        ],
    )
    openupgrade.logged_query(
        env.cr, "UPDATE helpdesk_ticket SET description = '/' WHERE description is null"
    )
