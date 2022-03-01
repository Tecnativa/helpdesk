odoo.define('ks_dashboard_ninja_list.ks_to_do_preview', function(require) {
    "use strict";

    const registry = require('web.field_registry');
    const AbstractField = require('web.AbstractField');
    const core = require('web.core');

    const QWeb = core.qweb;


    const KsToDOViewPreview = AbstractField.extend({
        supportedFieldTypes: ['char'],
        resetOnAnyFieldChange: true,

        init: function(parent, state, params) {
            this._super.apply(this, arguments);
            this.state = {};
        },

        _render: function() {
            this.$el.empty()
            const rec = this.recordData;
            if (rec.ks_dashboard_item_type === 'ks_to_do') {
                this.ksRenderToDoView(rec);
            }
        },

        _ks_get_rgba_format: function(val) {
            let rgba = val.split(',')[0].match(/[A-Za-z0-9]{2}/g);
            rgba = rgba.map((v) => parseInt(v, 16)).join(",");
            return "rgba(" + rgba + "," + val.split(',')[1] + ")";
        },

        ksRenderToDoView: function(rec) {
            const ks_header_color = this._ks_get_rgba_format(rec.ks_header_bg_color);
            const ks_font_color = this._ks_get_rgba_format(rec.ks_font_color);
            let list_to_do_data = {}
            if (rec.ks_to_do_data){
                list_to_do_data = JSON.parse(rec.ks_to_do_data)
            }
            const $todoViewContainer = $(QWeb.render('ks_to_do_container', {
                ks_to_do_view_name: rec.name ? rec.name : 'Name',
                to_do_view_data: list_to_do_data,
            }));
            $todoViewContainer.find('.ks_card_header').addClass('ks_bg_to_color').css({"background-color": ks_header_color });
            $todoViewContainer.find('.ks_card_header').addClass('ks_bg_to_color').css({"color": ks_font_color + ' !important' });
            $todoViewContainer.find('.ks_li_tab').addClass('ks_bg_to_color').css({"color": ks_font_color + ' !important' });
            $todoViewContainer.find('.ks_chart_heading').addClass('ks_bg_to_color').css({"color": ks_font_color + ' !important' });
            this.$el.append($todoViewContainer);
        },
    });

    registry.add('ks_dashboard_to_do_preview', KsToDOViewPreview);

    return {
        KsToDOViewPreview: KsToDOViewPreview,
    };

});
