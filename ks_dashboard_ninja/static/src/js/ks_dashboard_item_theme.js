odoo.define('ks_dashboard_ninja_list.ks_dashboard_item_theme', function(require) {
    "use strict";

    const registry = require('web.field_registry');
    const AbstractField = require('web.AbstractField');
    const core = require('web.core');

    const QWeb = core.qweb;

    //Widget for dashboard item theme using while creating dashboard item.
    const KsDashboardTheme = AbstractField.extend({
        supportedFieldTypes: ['char'],
        events: _.extend({}, AbstractField.prototype.events, {
            'click .ks_dashboard_theme_input_container': 'ks_dashboard_theme_input_container_click',
        }),

        /**
         * @override
         */
        _render: function() {
            this.$el.empty();
            const $view = $(QWeb.render('ks_dashboard_theme_view'));
            if (this.value) {
                $view.find(`input[value='${this.value}']`).prop("checked", true);
            }
            this.$el.append($view)
            if (this.mode === 'readonly') {
                this.$el.find('.ks_dashboard_theme_view_render').addClass('ks_not_click');
            }
        },

        /**
         * @param {ClickEvent} e
         */
        ks_dashboard_theme_input_container_click: function(e) {
            const $box = $(e.currentTarget).find(':input');
            if ($box.is(":checked")) {
                this.$el.find('.ks_dashboard_theme_input').prop('checked', false)
                $box.prop("checked", true);
            } else {
                $box.prop("checked", false);
            }
            this._setValue($box[0].value);
        },
    });

    registry.add('ks_dashboard_item_theme', KsDashboardTheme);

    return {
        KsDashboardTheme: KsDashboardTheme
    };

});
