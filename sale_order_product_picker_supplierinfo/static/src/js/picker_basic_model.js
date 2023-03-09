/* Copyright 2023 Tecnativa - Carlos Roca
 * License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
 */
odoo.define("sale_order_product_picker_supplierinfo.basic_model", function(require) {
  "use strict";

  var BasicModel = require("sale_order_product_picker.basic_model");

  BasicModel.include({
    getBreakFields: function() {
      var res = this._super.apply(this, arguments);
      res.push("supplierinfo_id");
      return res;
    },
  });

  return BasicModel;
});
