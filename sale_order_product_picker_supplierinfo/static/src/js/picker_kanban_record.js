/* Copyright 2023 Tecnativa - Carlos Roca
 * License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
 */
odoo.define("sale_order_product_picker_supplierinfo.PickerKanbanRecord", function(
  require
) {
  "use strict";

  var KanbanRecord = require("sale_order_product_picker.PickerKanbanRecord");

  KanbanRecord.include({
    getDefaultFields: function() {
      var res = this._super.apply(this, arguments);
      res.push("supplierinfo_id", "vendor_id", "vendor_comment");
      return res;
    },
  });

  return KanbanRecord;
});
