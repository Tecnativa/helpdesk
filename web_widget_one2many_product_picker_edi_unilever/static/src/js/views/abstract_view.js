// Copyright 2022 Tecnativa - Sergio Teruel
// License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
odoo.define("web_widget_one2many_product_picker_edi_unilever.AbstractView", function(
  require
) {
  "use strict";

  const core = require("web.core");
  const AbstractView = require("web.AbstractView");

  const _t = core._t;

  /**
   * Helper function to create field view definitions
   *
   * @private
   * @param {Object} params
   * @returns {Object}
   */
  function _constructFakeFieldDef(params) {
    return _.extend(
      {
        change_default: false,
        company_dependent: false,
        manual: false,
        views: {},
        searchable: true,
        store: false,
        readonly: true,
        required: false,
        sortable: false,
      },
      params
    );
  }

  /**
   * This is pure hard-coded magic. Adds new fields to the widget form view.
   */
  AbstractView.include({
    /**
     * @override
     */
    init: function(viewInfo, params) {
      if (viewInfo.model === "sale.order") {
        const widget_name = $(viewInfo.arch)
          .find("field[name='order_line']")
          .attr("widget");
        if (widget_name === "one2many_product_picker") {
          this._injectEdiUnileverFields(viewInfo);
        }
        return this._super(viewInfo, params);
      }
      this._super.apply(this, arguments);
    },

    /**
     * @private
     * @param {Object} viewInfo
     */
    _injectEdiUnileverFields: function(viewInfo) {
      const to_inject = {
        unilever_agreement_id: _constructFakeFieldDef({
          depends: [],
          relation: "agreement",
          string: _t("Agreement"),
          store: true,
          sortable: false,
          readonly: true,
          invisible: true,
          type: "many2one",
        }),
      };
      viewInfo.viewFields.order_line.views.form.fields = _.extend(
        {},
        to_inject,
        viewInfo.viewFields.order_line.views.form.fields
      );

      // Add fields to arch
      const $arch = $(viewInfo.viewFields.order_line.views.form.arch);

      // Add unilever_agreement_id
      const $field = $arch.find("field[name='unilever_agreement_id']");
      if (!$field.length) {
        $("<FIELD/>", {
          name: "unilever_agreement_id",
          on_change: 0,
          can_create: "true",
          can_write: "true",
          class: "mb-1",
          invisible: 1,
          force_save: "true",
          attrs: '{"invisible": true, "readonly": true}',
          modifiers: '{"invisible": true, "readonly": true}',
        }).appendTo($arch);
      }
      viewInfo.viewFields.order_line.views.form.arch = $arch[0].outerHTML;
    },
  });
});
