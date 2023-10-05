/* Copyright 2023 Tecnativa - Carlos Roca
 * License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
 */
odoo.define("sale_order_product_picker.FormController", function (require) {
    "use strict";

    const FormController = require("web.FormController");
    const FormRenderer = require("web.FormRenderer");

    FormController.include({
        /**
         * Select by default the picker tab
         *
         * @override
         */
        update: async function () {
            await this._super.apply(this, arguments);
            const $picker_tab = $(".nav-item.picker-tab a");
            if ($picker_tab.length) {
                if (this.mode === "edit") {
                    $picker_tab.trigger("click");
                }
                if (this.mode === "readonly" && $picker_tab.hasClass("active")) {
                    $($picker_tab.closest(".nav-tabs").find(".nav-link")[0]).trigger(
                        "click"
                    );
                }
            }
        },
    });
    FormRenderer.include({
        /**
         * Select by default the picker tab
         *
         * @override
         */
        _updateView: function () {
            this._super.apply(this, arguments);
            const $picker_tab = this.$el.find(".nav-item.picker-tab a");
            if ($picker_tab.length) {
                if (this.mode === "edit") {
                    $picker_tab
                        .closest(".nav")
                        .find(".nav-link.active")
                        .removeClass("active");
                    this.$el.find(".tab-pane.active").removeClass("active");
                    $picker_tab.addClass("active");
                    this.$el.find($picker_tab.getAttributes().href).addClass("active");
                }
            }
        },
    });
});
