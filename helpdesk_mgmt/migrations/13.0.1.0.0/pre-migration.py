# Copyright 2021 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

rename_models_spec = [
    ("helpdesk.tag", "helpdesk.ticket.tag"),
    ("helpdesk.stage", "helpdesk.ticket.stage"),
    ("helpdesk.team", "helpdesk.ticket.team"),
    ("helpdesk.ticket.type", "helpdesk.ticket.category"),
]

rename_tables_spec = [
    ("helpdesk_tag", "helpdesk_ticket_tag"),
    ("helpdesk_stage", "helpdesk_ticket_stage"),
    ("helpdesk_team", "helpdesk_ticket_team"),
    ("helpdesk_ticket_type", "helpdesk_ticket_category"),
]

rename_fields_spec = [
    ("helpdesk.ticket.stage", "helpdesk_ticket_stage", "is_close", "closed"),
    (
        "helpdesk.ticket.stage",
        "helpdesk_ticket_stage",
        "template_id",
        "mail_template_id",
    ),
    ("helpdesk.ticket.team", "helpdesk_ticket_team", "member_ids", "user_ids"),
    ("helpdesk.ticket", "helpdesk_ticket", "assign_date", "assigned_date"),
    ("helpdesk.ticket", "helpdesk_ticket", "close_date", "closed_date"),
    ("helpdesk.ticket", "helpdesk_ticket", "ticket_type_id", "category_id"),
]

rename_xmlids_spec = [
    # Adapt stages
    ("helpdesk_mgmt.stage_new", "helpdesk_mgmt.helpdesk_ticket_stage_new",),
    (
        "helpdesk_mgmt.stage_in_progress",
        "helpdesk_mgmt.helpdesk_ticket_stage_in_progress",
    ),
    ("helpdesk_mgmt.stage_solved", "helpdesk_mgmt.helpdesk_ticket_stage_done",),
    ("helpdesk_mgmt.stage_cancelled", "helpdesk_mgmt.helpdesk_ticket_stage_cancelled",),
    # mail templates
    (
        "helpdesk_mgmt.solved_ticket_request_email_template",
        "helpdesk_mgmt.closed_ticket_template",
    ),
    # ir.rule
    (
        "helpdesk_mgmt.helpdesk_ticket_company_rule",
        "helpdesk_mgmt.helpdesk_ticket_comp_rule",
    ),
    (
        "helpdesk_mgmt.helpdesk_portal_ticket_rule",
        "helpdesk_mgmt.helpdesk_ticket_rule_portal",
    ),
]


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE ir_module_module
        SET state='to install'
        WHERE name='helpdesk_mgmt_rating'
        """,
    )
    openupgrade.rename_models(env.cr, rename_models_spec)
    openupgrade.rename_tables(env.cr, rename_tables_spec)
    openupgrade.rename_fields(env, rename_fields_spec)
    openupgrade.rename_xmlids(env.cr, rename_xmlids_spec)
    # Description is required in helpdesk_mgmt
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE helpdesk_ticket
        SET description = name
        WHERE description IS NULL
        """,
    )
    # Remove team multi-company rule in this way because the record was
    # declared without id and therefore there is no linked record in
    # ir_model_data table
    openupgrade.logged_query(
        env.cr,
        """
        DELETE FROM ir_rule ir
        USING ir_model im
        WHERE
            im.id = ir.model_id
            AND im.model = 'helpdesk.team'
            AND ir.global = true
        """,
    )
