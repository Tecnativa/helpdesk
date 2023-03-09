/* Copyright 2023 Tecnativa - Carlos Roca
 * License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
 */
odoo.define("sale_order_product_picker.relational_fields", function(require) {
  "use strict";

  var relational_fields = require("web.relational_fields");

  relational_fields.FieldOne2Many.include({
    /**
     * If the add is done on picker view bypass editRecord
     *
     * @override
     * @private
     */
    reset: function(record, ev) {
      if (ev && ev.target && ev.target.picker) {
        // Trick to avoid paint editable mode
        this.picker = undefined;
        ev.target = Object.assign({}, ev.target);
      }
      return this._super.apply(this, arguments);
    },
    /**
     * If it is clicked inside the #picker-multiline-modal it will
     * close the modal and work as expected.
     *
     * @override
     * @private
     */
    _onOpenRecord: function() {
      $("#picker-multiline-modal").modal("hide");
      return this._super.apply(this, arguments);
    },
  });
});
