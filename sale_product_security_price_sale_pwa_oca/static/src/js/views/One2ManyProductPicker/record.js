// Copyright 2021 Tecnativa - Alexandre Díaz
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
odoo.define(
  "web_widget_one2many_product_picker_sale_product_security_price.One2ManyProductPickerRecord",
  function(require) {
    "use strict";

    var One2ManyProductPickerRecord = require("web_widget_one2many_product_picker.One2ManyProductPickerRecord");

    One2ManyProductPickerRecord.include({
      /**
       * @override
       */
      _render: function() {
        return this._super.apply(this, arguments).then(() => {
          if (this.state && this.state.data.security_price_warning) {
            this.$(".price_unit").addClass("bg-danger");
          }
        });
      },
    });
  }
);
