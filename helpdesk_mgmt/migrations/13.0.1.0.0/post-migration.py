# Copyright 2021 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

delete_xmlids_spec = [
    "helpdesk_mgmt.new_ticket_request_email_template",
    "helpdesk_mgmt.helpdesk_manager_rule",
    "helpdesk_mgmt.helpdesk_user_rule",
]

del_rec_trans_spec = [
    "closed_ticket_template",
]


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.delete_records_safely_by_xml_id(env, delete_xmlids_spec)
    openupgrade.load_data(
        env.cr, "helpdesk_mgmt", "migrations/13.0.1.0.0/noupdate_changes.xml"
    )
    openupgrade.delete_record_translations(env.cr, "helpdesk_mgmt", del_rec_trans_spec)
    # Set helpdesk ticket numbers according on the sequence pattern
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE helpdesk_ticket
        SET number = 'HT' || LPAD(id::text, 5, '0')
        """,
    )
    last_ht = env["helpdesk.ticket"].search([], order="id desc", limit=1)
    if last_ht:
        ht_seq = env["ir.sequence"].search([("code", "=", "helpdesk.ticket.sequence")])
        ht_seq.write({"number_next": last_ht.id + 1})
