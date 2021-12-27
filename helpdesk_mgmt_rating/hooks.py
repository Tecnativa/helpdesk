# Copyright 2021 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade

rename_xmlids_spec = [
    (
        "helpdesk_mgmt.rating_ticket_request_email_template",
        "helpdesk_mgmt_rating.rating_ticket_email_template",
    ),
    ("helpdesk_mgmt.mt_ticket_rated", "helpdesk_mgmt_rating.mt_ticket_rating",),
]

delete_record_translations_spec = [
    "rating_ticket_email_template",
]


def pre_init_hook(cr):
    openupgrade.rename_xmlids(cr, rename_xmlids_spec)


def post_init_hook(cr, registry):
    openupgrade.load_data(cr, "helpdesk_mgmt_rating", "noupdate_changes.xml")
    openupgrade.delete_record_translations(
        cr, "helpdesk_mgmt_rating", delete_record_translations_spec
    )
    # Set rating email template on rating_mail_template_id field
    openupgrade.logged_query(
        cr,
        """
        UPDATE
            helpdesk_ticket_stage hts
        SET
            mail_template_id = NULL,
            rating_mail_template_id = mt.id
        FROM
            ir_model_data imd, mail_template mt
        WHERE
            imd.name = 'rating_ticket_email_template'
            AND imd.module = 'helpdesk_mgmt_rating'
            AND imd.model = 'mail.template'
            AND mt.id = imd.res_id
            AND hts.mail_template_id = mt.id
        """,
    )
