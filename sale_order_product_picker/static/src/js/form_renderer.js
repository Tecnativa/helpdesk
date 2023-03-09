/* Copyright 2023 Tecnativa - Carlos Roca
 * License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
 */
odoo.define("sale_order_product_picker.FormRenderer", function(require) {
  "use strict";

  var core = require("web.core");
  var FormRenderer = require("web.FormRenderer");

  var QWeb = core.qweb;

  FormRenderer.include({
    events: _.extend({}, FormRenderer.prototype.events, {
      "click #product_picker_maximize": "_onClickPickerMaximize",
    }),
    _renderTagNotebook: function() {
      var $notebook = this._super.apply(this, arguments);
      $notebook.find(".o_notebook_headers").addClass("d-flex");
      $notebook.find(".o_notebook_headers ul").css("width", "100%");
      $notebook
        .find(".o_notebook_headers")
        .append($(QWeb.render("sale_order_product_picker.fullscreen", this)));
      return $notebook;
    },
    _onClickPickerMaximize: function() {
      var $notebook = $(".o_notebook");
      $notebook.toggleClass(
        "position-relative h-100 bg-white oe_field_one2many_product_picker_maximized"
      );
    },
  });
});
