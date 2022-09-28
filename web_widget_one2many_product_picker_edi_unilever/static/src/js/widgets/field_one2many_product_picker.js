// Copyright 2022 Tecnativa - Sergio Teruel
// License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
odoo.define(
  "web_widget_one2many_product_picker_edi_unilever.FieldOne2ManyProductPicker",
  function(require) {
    "use strict";

    const FieldOne2ManyProductPicker = require("web_widget_one2many_product_picker.FieldOne2ManyProductPicker");

    FieldOne2ManyProductPicker.include({
      /**
       * @private
       * @returns {Object}
       */
      _getDefaultOptions: function() {
        const res = this._super.apply(this, arguments);
        res.field_map.unilever_agreement = "unilever_agreement_id";
        return res;
      },
    });
  }
);
