# Copyright 2024 Tecnativa - Carolina Fernandez
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from datetime import datetime, timedelta

from odoo.exceptions import ValidationError

from odoo.addons.hr_attendance_report_theoretical_time.tests.test_hr_attendance_report_theoretical_time import (  # noqa
    TestHrAttendanceReportTheoreticalTimeBase,
)


class TestHrAttendanceReportTimeRecord(TestHrAttendanceReportTheoreticalTimeBase):
    def setUp(self):
        super().setUp()
        self.hr_attendance = self.env["hr.attendance"]
        self.AttendanceWizard = self.env["hr.attendance.time.record.report.wizard"]
        self.department1 = self.env.ref("hr.dep_management")
        self.department2 = self.env.ref("hr.dep_rd")
        self.employee_1.department_id = self.department1.id
        self.employee_2.department_id = self.department2.id

    def test_check_date_range(self):
        with self.assertRaises(ValidationError):
            wizard_data = {
                "date_from": datetime.now(),
                "date_to": datetime.now() - timedelta(days=7),
            }
            self.AttendanceWizard.create(wizard_data)

    def test_generate_report_xlsx(self):
        with self.assertRaises(ValidationError):
            wizard_data = {
                "date_from": datetime.now(),
                "date_to": datetime.now() - timedelta(days=7),
            }
            self.AttendanceWizard.create(wizard_data)
        wizard = self.AttendanceWizard.create(
            {
                "date_from": datetime(1946, 12, 24),
                "date_to": datetime(1946, 12, 26),
            }
        )

        self.assertTrue(wizard.button_export_xlsx())
        report_name = wizard._get_report_name_xlsx()
        self.assertEqual(report_name, "Time record 1946-12-24-1946-12-26.xlsx")

        wizard.department_ids = [(4, self.department1.id)]
        self.assertTrue(wizard.button_export_xlsx())

        wizard.employee_ids = [(4, self.employee_1.id)]
        self.assertTrue(wizard.button_export_xlsx())
