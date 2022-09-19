// Copyright 2021 Tecnativa - Alexandre Díaz
// License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
odoo.define(
  "web_widget_one2many_product_picker_sale_product_security_price.ProductPickerQuickModifPriceFormView",
  function(require) {
    "use strict";

    var ProductPickerQuickModifPriceFormView = require("web_widget_one2many_product_picker.ProductPickerQuickModifPriceFormView");
    var tools = require("web_widget_one2many_product_picker.tools");
    var core = require("web.core");

    var qweb = core.qweb;
    var _t = core._t;

    ProductPickerQuickModifPriceFormView.ProductPickerQuickModifPriceFormController.include(
      {
        events: _.extend(
          {},
          ProductPickerQuickModifPriceFormView
            .ProductPickerQuickModifPriceFormController.prototype.events,
          {
            "click #rise_up_to_security_price": "_onRiseUpToSecurityPrice",
          }
        ),

        custom_events: _.extend(
          {},
          ProductPickerQuickModifPriceFormView
            .ProductPickerQuickModifPriceFormController.prototype.custom_events,
          {
            update_security_price_button: "_onUpdateSecurityPriceButton",
          }
        ),

        init: function() {
          this._super.apply(this, arguments);
          this._alert_displayed = false;
        },

        /**
         * @private
         */
        _onRiseUpToSecurityPrice: function(ev) {
          if (!ev.data) {
            ev.data = {};
          }
          var state = this.model.get(this.handle).data;
          this._applyChanges(
            this.handle,
            {
              price_unit: state.security_price,
              discount: 0.0,
            },
            ev
          );
        },

        /**
         * @override
         */
        _applyChanges: function() {
          return this._super.apply(this, arguments).then(() => {
            this._updateSecurityPriceButton();
          });
        },

        /**
         * @override
         */
        _onClickChange: function() {
          if (
            this.model.isDirty(this.handle) &&
            !this._alert_displayed &&
            this._checkSecurityPrice()
          ) {
            this._alert_displayed = true;
            var state = this.model.get(this.handle);
            var security_price = tools.monetary(
              state.data.security_price,
              state.fields.security_price,
              this.currencyField,
              state.data
            );
            var msg = _.str.sprintf(
              _t(
                "The price is lower than the security price (%s). Press the button <i class='fa fa-fw o_button_icon fa-long-arrow-up btn-success rounded'></i> to use the security price or confirm the changes again."
              ),
              security_price
            );
            this.renderer.showAlert(msg);
            return Promise.resolve();
          }
          return this._super.apply(this, arguments);
        },

        /**
         * @private
         * @returns {Boolean}
         */
        _checkSecurityPrice: function() {
          var state = this.model.get(this.handle);
          var values = state.data;
          if (
            values.order_partner_security_price_control &&
            values.product_security_price_control
          ) {
            var digits = state.fields.price_unit.digits;
            return (
              parseFloat(values.price_reduce).toPrecision(digits[1]) <
              values.security_price
            );
          }
          return false;
        },

        /**
         * @private
         */
        _updateSecurityPriceButton: function() {
          if (this._checkSecurityPrice()) {
            this.renderer.showSaleProductSecurityPrice();
          } else {
            this.renderer.hideSaleProductSecurityPrice();
          }
        },

        /**
         * @private
         * @param {CustomEvent} ev
         */
        _onUpdateSecurityPriceButton: function(ev) {
          ev.stopPropagation();
          this._updateSecurityPriceButton();
        },
      }
    );

    ProductPickerQuickModifPriceFormView.ProductPickerQuickModifPriceFormRenderer.include(
      {
        /**
         * @override
         */
        _render: function() {
          return this._super.apply(this, arguments).then(() => {
            if (this.state.model === "sale.order.line") {
              this.trigger_up("update_security_price_button");
            }
          });
        },

        showAlert: function(message) {
          this.$el.find(".oe_alert_security_price").remove();
          this.$el.append(
            "<span class='oe_alert_security_price mt-4 p-2 d-block bg-warning font-weight-bold rounded'>" +
              message +
              "</span>"
          );
        },

        showSaleProductSecurityPrice: function() {
          if (this.$el.find("#rise_up_to_security_price").length) {
            return;
          }
          var $price_unit = this.$el.find("field[name='price_unit']");
          $price_unit.closest("td").css("display", "flex");
          var $button = $(
            qweb.render("One2ManyProductPicker.SaleProductSecurityPrice.Button")
          );
          $button.insertAfter($price_unit);
        },

        hideSaleProductSecurityPrice: function() {
          if (!this.$el.find("#rise_up_to_security_price").length) {
            return;
          }
          this.$el.find("#rise_up_to_security_price").remove();
          var $price_unit = this.$el.find("field[name='price_unit']");
          $price_unit.closest("td").css("display", "");
        },
      }
    );
  }
);
