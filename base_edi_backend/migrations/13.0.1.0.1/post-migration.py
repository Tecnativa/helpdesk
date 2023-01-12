# Copyright 2023 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE ir_cron ic
        SET edi_backend_id = eb.id
        FROM edi_backend eb
        WHERE ic.cron_name = 'EDI Backend ' || eb.name OR
            ic.cron_name = '[' || UPPER(eb.provider) || '] EDI Backend ' || eb.name
        """,
    )
    # Deactivate the crons that not match
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE ir_cron ic
        SET active = false
        FROM edi_backend eb
        WHERE edi_backend_id IS NULL AND
            ic.cron_name LIKE '%EDI Backend%'
        """,
    )
