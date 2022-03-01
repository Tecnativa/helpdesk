odoo.define('ks_dashboard_ninja_list.ks_widget_toggle', function (require) {
    "use strict";

    const registry = require('web.field_registry');
    const AbstractField = require('web.AbstractField');
    const core = require('web.core');

    const QWeb = core.qweb;


    const KsWidgetToggle = AbstractField.extend({
        supportedFieldTypes: ['char'],
        events: _.extend({}, AbstractField.prototype.events, {
            'change .ks_toggle_icon_input': 'ks_toggle_icon_input_click',
        }),

        _render: function () {
            this.$el.empty();
            const $view = $(QWeb.render('ks_widget_toggle'));
            if (this.value) {
                $view.find("input[value='" + this.value + "']").prop("checked", true);
            }
            this.$el.append($view)

            if (this.mode === 'readonly') {
                this.$el.find('.ks_select_dashboard_item_toggle').addClass('ks_not_click');
            }
        },

        ks_toggle_icon_input_click: function (e) {
            this._setValue(e.currentTarget.value);
        }
    });

    const KsWidgetToggleKPI = AbstractField.extend({
        supportedFieldTypes: ['char'],
        events: _.extend({}, AbstractField.prototype.events, {
            'change .ks_toggle_icon_input': 'ks_toggle_icon_input_click',
        }),

        _render: function () {
            this.$el.empty();
            const $view = $(QWeb.render('ks_widget_toggle_kpi'));
            if (this.value) {
                $view.find("input[value='" + this.value + "']").prop("checked", true);
            }
            this.$el.append($view)
            if (this.mode === 'readonly') {
                this.$el.find('.ks_select_dashboard_item_toggle').addClass('ks_not_click');
            }
        },

        ks_toggle_icon_input_click: function (e) {
            this._setValue(e.currentTarget.value);
        }
    });

    const KsWidgetToggleKpiTarget = AbstractField.extend({
        supportedFieldTypes: ['char'],
        events: _.extend({}, AbstractField.prototype.events, {
            'change .ks_toggle_icon_input': 'ks_toggle_icon_input_click',
        }),

        _render: function () {
            this.$el.empty();
            const $view = $(QWeb.render('ks_widget_toggle_kpi_target_view'));
            if (this.value) {
                $view.find("input[value='" + this.value + "']").prop("checked", true);
            }
            this.$el.append($view)

            if (this.mode === 'readonly') {
                this.$el.find('.ks_select_dashboard_item_toggle').addClass('ks_not_click');
            }
        },

        ks_toggle_icon_input_click: function (e) {
            this._setValue(e.currentTarget.value);
        }
    });

    registry.add('ks_widget_toggle', KsWidgetToggle);
    registry.add('ks_widget_toggle_kpi', KsWidgetToggleKPI);
    registry.add('ks_widget_toggle_kpi_target', KsWidgetToggleKpiTarget);

    return {
        KsWidgetToggle: KsWidgetToggle,
        KsWidgetToggleKPI: KsWidgetToggleKPI,
        KsWidgetToggleKpiTarget :KsWidgetToggleKpiTarget
    };

});
