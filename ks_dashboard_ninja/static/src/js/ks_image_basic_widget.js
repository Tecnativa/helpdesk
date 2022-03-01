odoo.define('ks_dashboard_ninja_list.ks_image_basic_widget', function(require) {
    "use strict";

    const core = require('web.core');
    const basic_fields = require('web.basic_fields');
    const registry = require('web.field_registry');

    const QWeb = core.qweb;

    const KsImageWidget = basic_fields.FieldBinaryImage.extend({

        init: function(parent, state, params) {
            this._super.apply(this, arguments);
            this.ksSelectedIcon = false;
            this.ks_icon_set = ['home', 'puzzle-piece', 'clock-o', 'comments-o', 'car', 'calendar', 'calendar-times-o', 'bar-chart', 'commenting-o', 'star-half-o', 'address-book-o', 'tachometer', 'search', 'money', 'line-chart', 'area-chart', 'pie-chart', 'check-square-o', 'users', 'shopping-cart', 'truck', 'user-circle-o', 'user-plus', 'sun-o', 'paper-plane', 'rss', 'gears', 'check', 'book'];
        },

        template: 'KsFieldBinaryImage',

        events: _.extend({}, basic_fields.FieldBinaryImage.prototype.events, {
            'click .ks_icon_container_list': 'ks_icon_container_list',
            'click .ks_image_widget_icon_container': 'ks_image_widget_icon_container',
            'click .ks_icon_container_open_button': 'ks_icon_container_open_button',
            'click .ks_fa_icon_search': 'ks_fa_icon_search',
            'keyup .ks_modal_icon_input': 'ks_modal_icon_input_enter',
        }),

        _render: function() {
            const url = this.placeholder;
            if (this.value) {
                this.$('> img').remove();
                this.$('> span').remove();
                $('<span>').addClass('fa fa-' + this.recordData.ks_default_icon + ' fa-5x').appendTo(this.$el).css('color', 'black');
            } else {
                const $img = $(QWeb.render("FieldBinaryImage-img", {
                    widget: this,
                    url: url
                }));
                this.$('> img').remove();
                this.$('> span').remove();
                this.$el.prepend($img);
            }

            const $ks_icon_container_modal = $(QWeb.render('ks_icon_container_modal_template', {
                ks_fa_icons_set: this.ks_icon_set
            }));

            $ks_icon_container_modal.prependTo(this.$el);
        },

        //This will show modal box on clicking on open icon button.
        ks_image_widget_icon_container: function(e) {
            $('#ks_icon_container_modal_id').modal({
                show: true,
            });
        },

        ks_icon_container_list: function(e) {
            this.ksSelectedIcon = $(e.currentTarget).find('span').attr('id').split('.')[1]
            _.each($('.ks_icon_container_list'), function(selected_icon) {
                $(selected_icon).removeClass('ks_icon_selected');
            });

            $(e.currentTarget).addClass('ks_icon_selected')
            $('.ks_icon_container_open_button').show()
        },

        //Imp :  Hardcoded for svg file only. If different file, change this code to dynamic.
        ks_icon_container_open_button: function(e) {
            this._setValue(this.ksSelectedIcon);
        },

        ks_fa_icon_search: function(e) {
            this.$el.find('.ks_fa_search_icon').remove();
            let ks_fa_icon_name = this.$el.find('.ks_modal_icon_input')[0].value;
            if (ks_fa_icon_name.slice(0, 3) === "fa-") {
                ks_fa_icon_name = ks_fa_icon_name.slice(3)
            }
            const ks_fa_icon_render = $('<div>').addClass('ks_icon_container_list ks_fa_search_icon')
            $('<span>').attr('id', 'ks.' + ks_fa_icon_name.toLocaleLowerCase()).addClass("fa fa-" + ks_fa_icon_name.toLocaleLowerCase() + " fa-4x").appendTo($(ks_fa_icon_render))
            $(ks_fa_icon_render).appendTo(this.$el.find('.ks_icon_container_grid_view'))
        },

        ks_modal_icon_input_enter: function(e) {
            if (e.keyCode == 13) {
                this.$el.find('.ks_fa_icon_search').click()
            }
        },
    });

    registry.add('ks_image_widget', KsImageWidget);

    return {
        KsImageWidget: KsImageWidget,
    };
});
