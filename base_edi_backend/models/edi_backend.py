# Copyright 2022 Tecnativa - Sergio Teruel
# Copyright 2022 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl
import base64
import json
import logging
from io import BytesIO

from dateutil.relativedelta import relativedelta

from odoo import _, api, exceptions, fields, models
from odoo.tools.safe_eval import safe_eval

_logger = logging.getLogger(__name__)
try:
    import ftplib
except ImportError:
    _logger.debug("Cannot import ftplib")
try:
    from odoo.addons.queue_job.job import job
except ImportError:
    _logger.debug("Can not `import queue_job`.")
    import functools

    def empty_decorator_factory(*argv, **kwargs):
        return functools.partial

    job = empty_decorator_factory


class EdiBackend(models.Model):
    _name = "edi.backend"
    _description = "EDI Backend"

    active = fields.Boolean(default=True)
    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    company_id = fields.Many2one(
        comodel_name="res.company", default=lambda self: self.env.company,
    )
    sequence_id = fields.Many2one(comodel_name="ir.sequence", string="Sequence file",)
    # The module will work as it is. However, some providers might override some things
    provider = fields.Selection(selection=[("base", "Generic")], required=True)
    communication_type = fields.Selection(
        selection=[("ftp", "FTP"), ("email", "E-Mail")], default="ftp", required=True,
    )
    register_record_state = fields.Boolean(
        help="If set the record state will be set on every backend communication",
    )
    sequence_number_next = fields.Integer(
        related="sequence_id.number_next_actual",
        string="Next sequence",
        readonly=False,
    )
    last_sync_date = fields.Datetime(
        string="Last Export", default="2000-01-01 00:00:00"
    )
    export_config_id = fields.Many2one(
        comodel_name="edi.backend.config",
        string="Export config",
        ondelete="cascade",
        required=True,
    )
    model_id = fields.Many2one(comodel_name="ir.model", string="Odoo model",)
    filter_domain = fields.Char(string="Apply on")
    model_name = fields.Char()
    special_domain = fields.Char(
        compute="_compute_special_domain", string="Special domain",
    )
    date_field = fields.Many2one(
        comodel_name="ir.model.fields",
        string="Date field to filter",
        ondelete="restrict",
    )
    date_range = fields.Selection(
        selection=[("current_month", "Current Month"), ("last_month", "Last Month")],
        string="Date Field Range",
    )
    security_days = fields.Integer(string="Security days")
    data = fields.Binary(string="Last File", readonly=True)
    extension = fields.Char(default=".txt",)
    file_name = fields.Char(string="File name")
    # FTP data
    ftp_host = fields.Char()
    ftp_user = fields.Char()
    ftp_password = fields.Char()
    ftp_file_special_name = fields.Char(
        string="File Special Name", help="File will allways be synced with this name",
    )
    remote_path = fields.Char(string="Remote path")
    # Mail data
    destination_partner_ids = fields.Many2many(
        comodel_name="res.partner",
        help="When mailing is enabled these will be the partners we'll communicate to",
    )
    email_author = fields.Many2one(comodel_name="res.partner",)
    # Communication history
    history_count = fields.Integer(compute="_compute_history_count")
    group_key = fields.Char(string="Group key",)
    anonymize_entries = fields.Boolean()
    anonymized_domain = fields.Char()
    char_for_anonymize = fields.Char(default="x", size=1)

    @api.depends("date_field", "date_range", "last_sync_date", "security_days")
    def _compute_special_domain(self):
        """Relative dates to every sync"""
        self.special_domain = False
        for edi in self:
            if not edi.date_field:
                edi.special_domain = False
                continue
            domain = []
            if edi.security_days:
                domain.extend([(edi.date_field.name, "<", edi.get_relative_date())])
            elif edi.date_range:
                dates = edi.get_relative_date()
                domain.extend(
                    [
                        (edi.date_field.name, ">", dates[0]),
                        (edi.date_field.name, "<", dates[1]),
                    ]
                )
            edi.special_domain = str(domain)

    def get_relative_date(self, date=False):
        if self.security_days:
            security_date = date or fields.Date.today()
            return fields.Date.to_string(
                fields.Date.from_string(security_date)
                - relativedelta(days=self.security_days)
            )
        today = fields.Date.today()
        if not self.date_range:
            return (today, today)
        date_from = date_to = fields.Date.from_string(today)
        if self.date_range == "last_month":
            date_from = fields.Date.from_string(today) - relativedelta(months=1)
        elif self.date_range == "current_month":
            date_to = fields.Date.from_string(today) + relativedelta(months=1)
        if self.date_field.ttype == "datetime":
            date_from = date_from.strftime("%Y-%m-01 00:00:00")
            date_to = date_to.strftime("%Y-%m-01 00:00:00")
        else:
            date_from = date_from.strftime("%Y-%m-01")
            date_to = date_to.strftime("%Y-%m-01")
        return (date_from, date_to)

    def _compute_history_count(self):
        for edi in self:
            edi.history_count = self.env[
                "edi.backend.communication.history"
            ].search_count([("edi_backend_id", "=", edi.id)])

    def get_records(self):
        domain = (
            self.env.context.get("applied_domain", False) or self.get_complete_domain()
        )
        records = self.env[self.model_id.model].search(domain)
        return records

    def get_mapped_records(self, mapped_field):
        records = self.get_records()
        records = records.mapped(mapped_field)
        return records

    @api.onchange("model_id")
    def onchange_model_id(self):
        self.model_name = self.model_id.model

    def action_export(self):
        self.data = False
        self.action_export_run()

    def create_cron(self):
        IrCron = self.env["ir.cron"]
        name = "EDI Backend {}"
        if self.provider != "base":
            name = "[{}] EDI Backend {}".format(self.provider.upper(), self.name)
        else:
            name = "EDI Backend {}".format(self.name)
        ir_cron = IrCron.with_context(active_test=False).search([("name", "=", name)])
        if not ir_cron:
            ir_cron = self.env["ir.cron"].create(
                {
                    "name": name,
                    "model_id": self.env.ref("base_edi_backend.model_edi_backend").id,
                    "state": "code",
                    "interval_number": 1,
                    "interval_type": "weeks",
                    "numbercall": -1,
                }
            )
        ir_cron.write({"code": "model.browse({}).action_export_job()".format(self.id)})
        action = self.env.ref("base.ir_cron_act").read()[0]
        if len(ir_cron) == 1:
            form = self.env.ref("base.ir_cron_view_form")
            action["views"] = [(form.id, "form")]
            action["res_id"] = ir_cron.id
        else:
            action["domain"] = [("id", "in", ir_cron.ids)]
        return action

    def action_communication_history(self):
        action = self.env.ref(
            "base_edi_backend." "action_edi_backend_communication_history"
        ).read()[0]
        action["domain"] = [("edi_backend_id", "=", self.id)]
        return action

    def action_export_job(self):
        self.with_delay().action_export_run()

    def get_complete_domain(self):
        domain = safe_eval(self.filter_domain)
        if self.special_domain:
            domain.extend(safe_eval(self.special_domain))
        return domain

    def get_anonymize_domain(self):
        return safe_eval(self.anonymized_domain)

    def _get_anonymized_records(self):
        anonymized_records = []
        if self.anonymize_entries:
            domain = self.get_anonymize_domain()
            anonymized_records = self.env[self.model_name].search(domain).ids
        return anonymized_records

    @job
    def action_export_run(self, history_line=False):
        if not self.export_config_id:
            raise exceptions.UserError(_("No export configuration selected."))
        if history_line:
            domain = safe_eval(history_line.applied_domain)
        else:
            domain = self.get_complete_domain()
        records = self.with_context(applied_domain=domain).get_records()
        now = fields.Datetime.now()
        if not records:
            return
        anonymized_records = self._get_anonymized_records()
        # Get sequence and write it in context to be used in content file
        sequence_file = (
            history_line
            and history_line.applied_sequence
            or self.sequence_id.next_by_id()
        )
        WizExport = self.env["edi.backend.file.wiz"]
        wiz_export = WizExport.with_context(
            active_model=self._name,
            active_id=self.id,
            today=fields.Date.today(),
            sequence_file=sequence_file,
            anonymized_records=anonymized_records,
            anonymize_char=self.char_for_anonymize,
        ).create({"name": "File {}".format(self.name)})
        contents = b""
        contents += wiz_export.with_context(
            applied_domain=domain
        ).action_get_file_from_config(self)
        # Generate the file and save as attachment
        file = base64.b64encode(contents)
        file_name = self._get_backend_filename(contents, sequence_file, records)
        if not history_line:
            self.write(
                {
                    "data": file,
                    "file_name": file_name,
                    "last_sync_date": self.security_days or now,
                }
            )
        # When adding an extra sending option, we'll add the proper method
        getattr(self, "send_file_by_%s" % self.communication_type)(file, file_name)
        if history_line:
            history_line.write(
                {
                    "state": "sent",
                    "data": file,
                    "file_name": file_name,
                    "applied_records": records.ids,
                }
            )
        else:
            history_line = self.env["edi.backend.communication.history"].create(
                {
                    "edi_backend_id": self.id,
                    "state": "sent",
                    "applied_domain": domain,
                    "applied_records": records.ids,
                    "applied_sequence": sequence_file,
                    "data": file,
                    "file_name": file_name,
                }
            )
        # In order to be able use record state the model should have edi.backend.mixin
        # Every provider should have their proper wildcard methods declared.
        if self.register_record_state and hasattr(
            records, "%s_action_backend_sent" % self.provider
        ):
            getattr(records, "%s_action_backend_sent" % self.provider)()
        return history_line

    def _get_backend_filename(self, contents, sequence_file, records):
        lines_count = contents.count(b"\n")
        return "{}{}{}{}".format(self.code, lines_count, sequence_file, self.extension,)

    # FTP Connection methods
    def _ftp_connection_params(self):
        return {
            "host": self.ftp_host,
            "user": self.ftp_user,
            "passwd": self.ftp_password,
        }

    def action_ftp_test_connection(self):
        """Check if the ftp settings are correct."""
        try:
            with self._ftp_connection() as ftp:
                if ftp.getwelcome():
                    raise exceptions.Warning(_("Connection Test OK!"))
        except exceptions.Warning:
            raise exceptions.Warning(_("Connection Test OK!"))
        except Exception:
            raise exceptions.ValidationError(
                _("Connection Test Failed! %s" % Exception)
            )

    def _ftp_connection(self):
        """Return a new FTP connection with found parameters."""
        _logger.debug(
            "Trying to connect to ftp://%(user)s@%(host)s",
            extra=self._ftp_connection_params(),
        )
        ftp = ftplib.FTP(**self._ftp_connection_params())
        _logger.info("Connected to sftp://{}".format(self.ftp_user))
        return ftp

    def _file_to_ftp(self, file_name, data):
        if not (data and self.data):
            return
        with self._ftp_connection() as ftp:
            ftp.cwd(self.remote_path)
            file = base64.b64decode(data or self.data)
            ftp.storbinary("STOR " + file_name, BytesIO(file))

    def send_file_by_ftp(self, file, file_name):
        if not self.ftp_host or not self.ftp_user:
            return
        ftp_file_name = self.ftp_file_special_name or file_name
        self._file_to_ftp(ftp_file_name, file)

    # Email connection methods

    def _prepare_mail_values(self, file, file_name):
        return {
            "author_id": self.email_author.id,
            "recipient_ids": [(4, p.id) for p in self.destination_partner_ids],
            "subject": "Exportation of {}".format(file_name),
            "body_html": """
                <body>
                    <p>
                        This the data
                    </p>
                </body>
            """,
            "notification": False,
            "auto_delete": False,
            "attachment_ids": [(0, 0, {"name": file_name, "datas": file})],
        }

    def send_file_by_email(self, file, file_name):
        if not self.destination_partner_ids:
            return
        vals = self._prepare_mail_values(file, file_name)
        mail = self.env["mail.mail"].create(vals)
        mail.send()

    @api.model
    def _create_sequence(self, vals):
        seq_vals = {
            "name": "EDI Backend {}".format(vals["name"]),
            "code": "edi.backend",
            "padding": 4,
            "number_increment": 1,
        }
        if "company_id" in vals:
            seq_vals["company_id"] = vals["company_id"]
        return self.env["ir.sequence"].create(seq_vals)

    @api.model
    def create(self, vals):
        if not vals.get("sequence_id", False):
            vals["sequence_id"] = self._create_sequence(vals).id
        return super().create(vals)


class EdiBackendCommunicationHistory(models.Model):
    _name = "edi.backend.communication.history"
    _description = "EDI Backend communication history"
    _rec_name = "create_date"
    _order = "create_date DESC"

    edi_backend_id = fields.Many2one(
        comodel_name="edi.backend", string="EDI Backend", required=True,
    )
    company_id = fields.Many2one(
        related="edi_backend_id.company_id",
        string="Company",
        store=True,
        readonly=True,
        index=True,
    )
    state = fields.Selection(
        selection=[
            ("not_sent", "Not sent"),
            ("sent", "Sent"),
            ("sent_errors", "Errors"),
            ("cancelled", "Cancelled"),
        ],
        string="Export state",
        default="not_sent",
        copy=False,
        help="Indicates the state of the Export send state",
    )
    model_name = fields.Char(related="edi_backend_id.model_name", readonly=True,)
    applied_domain = fields.Char()
    applied_records = fields.Char()
    applied_sequence = fields.Char()
    data = fields.Binary(string="Last File", attachment=True, readonly=True)
    file_name = fields.Char(string="File name")

    def get_applied_records(self):
        """
        Do a new search with all record ids due to an user can be delete a
        record so we can do not a browse aver this ids directly.
        """
        records = self.env[self.model_name].browse()
        if self.applied_records:
            record_ids = json.loads(self.applied_records)
            records = self.env[self.model_name].search([("id", "in", record_ids)])
        return records

    def action_set_no_send(self):
        records = self.get_applied_records()
        if records:
            getattr(
                records, "%s_action_backend_not_sent" % self.edi_backend_id.provider
            )()

    def action_rebuild_file(self):
        self.data = False
        self.edi_backend_id.action_export_run(history_line=self)

    def action_open_applied_records(self):
        records = self.get_applied_records()
        if records:
            action = {
                "type": "ir.actions.act_window",
                "view_mode": "tree,form",
                "name": _(
                    "Applied records ({})".format(self.edi_backend_id.model_id.name)
                ),
                "res_model": self.model_name,
                "domain": [("id", "in", records.ids)],
            }
            return action
