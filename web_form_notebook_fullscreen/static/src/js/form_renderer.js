/* Copyright 2023 Tecnativa - Carlos Roca
 * License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
 */
odoo.define("web_form_notebook_fullscreen.FormRenderer", function (require) {
    "use strict";

    var core = require("web.core");
    var FormRenderer = require("web.FormRenderer");

    var QWeb = core.qweb;

    FormRenderer.include({
        events: _.extend({}, FormRenderer.prototype.events, {
            "click #notebook_maximize": "_onClickNotebookMaximize",
        }),
        _renderTagNotebook: function () {
            var $notebook = this._super.apply(this, arguments);
            $notebook.find(".o_notebook_headers").addClass("d-flex");
            $notebook.find(".o_notebook_headers ul").css("width", "100%");
            $notebook
                .find(".o_notebook_headers")
                .append(
                    $(QWeb.render("web_form_notebook_fullscreen.fullscreen", this))
                );
            return $notebook;
        },
        _onClickNotebookMaximize: function () {
            var $notebook = $(".o_notebook");
            $notebook.toggleClass(
                "position-relative h-100 bg-white oe_notebook_fullscreen"
            );
        },
    });
});
