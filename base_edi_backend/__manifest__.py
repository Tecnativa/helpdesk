# Copyright 2022 Tecnativa - Sergio Teruel
# Copyright 2022 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "EDI Backend Base Module",
    "version": "13.0.1.0.0",
    "development_status": "Beta",
    "category": "Product",
    "website": "https://www.tecnativa.com",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": ["xlrd", "openupgradelib"]},
    "depends": ["base_edi", "queue_job", "l10n_es_aeat"],  # TODO: Break dependency
    "data": [
        "security/ir.model.access.csv",
        "views/edi_backend_configuration_view.xml",
        "views/edi_backend_view.xml",
        "views/edi_backend_communication_history_view.xml",
        "views/edi_backend_menu.xml",
    ],
}
