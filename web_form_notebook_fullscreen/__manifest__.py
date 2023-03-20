# Copyright 2023 Tecnativa - Carlos Roca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Web Form Notebook Fullscreen",
    "version": "15.0.1.0.0",
    "development_status": "Beta",
    "category": "Web",
    "website": "https://github.com/OCA/sale-workflow",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["web"],
    "assets": {
        "web.assets_backend": [
            "web_form_notebook_fullscreen/static/src/js/form_renderer.js",
            "web_form_notebook_fullscreen/static/src/scss/web_form_notebook_fullscreen.scss",
        ],
        "web.assets_qweb": [
            "web_form_notebook_fullscreen/static/src/xml/fullscreen.xml"
        ],
    },
}
