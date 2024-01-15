# Copyright 2024 Tecnativa - Carolina Fernandez
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Hr Attendance - Time Record Report",
    "summary": "Time Record Report XLSX",
    "version": "15.0.1.0.0",
    "development_status": "Beta",
    "category": "Purchase",
    "website": "https://github.com/OCA/hr-attendance",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "hr_attendance",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/hr_attendance_time_record_wizard_views.xml",
    ],
}
