# Copyright 2024 Tecnativa - Carolina Fernandez
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from datetime import datetime, timedelta

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestHrAttendanceReportTimeRecord(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.hr_attendance = cls.env["hr.attendance"]
        cls.AttendanceWizard = cls.env["hr.attendance.time.record.report.wizard"]
        cls.department1 = cls.env.ref("hr.dep_management")
        cls.department2 = cls.env.ref("hr.dep_rd")
        cls.calendar = cls.env["resource.calendar"].create(
            {"name": "Test Calendar", "attendance_ids": False, "tz": "UTC"}
        )
        for day in range(5):  # From monday to friday
            cls.calendar.attendance_ids = [
                (
                    0,
                    0,
                    {
                        "name": "Attendance",
                        "dayofweek": str(day),
                        "hour_from": "08",
                        "hour_to": "12",
                    },
                ),
                (
                    0,
                    0,
                    {
                        "name": "Attendance",
                        "dayofweek": str(day),
                        "hour_from": "14",
                        "hour_to": "18",
                    },
                ),
            ]
        cls.employee_1 = cls.env["hr.employee"].create(
            {
                "name": "Employee 1",
                "resource_calendar_id": cls.calendar.id,
            }
        )
        cls.employee_2 = cls.env["hr.employee"].create(
            {
                "name": "Employee 2",
                "resource_calendar_id": cls.calendar.id,
            }
        )
        cls.employee_1.department_id = cls.department1.id
        cls.employee_2.department_id = cls.department2.id
        for employee in (cls.employee_1, cls.employee_2):
            for day in range(23, 27):
                cls.env["hr.attendance"].create(
                    {
                        "employee_id": employee.id,
                        "check_in": "1946-12-%s 08:00:00" % day,
                        "check_out": "1946-12-%s 12:00:00" % day,
                    }
                )
                cls.env["hr.attendance"].create(
                    {
                        "employee_id": employee.id,
                        "check_in": "1946-12-%s 14:00:00" % day,
                        "check_out": "1946-12-%s 18:00:00" % day,
                    }
                )

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
