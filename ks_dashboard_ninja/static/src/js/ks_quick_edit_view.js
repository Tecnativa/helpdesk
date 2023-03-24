odoo.define('ks_dashboard_ninja.quick_edit_view', function(require) {
    "use strict";

    const Widget = require("web.Widget");
    const data = require('web.data');
    const QuickCreateFormView = require('web.QuickCreateFormView');


    const QuickEditView = Widget.extend({
        template: 'ksQuickEditViewOption',
        events: {
            'click .ks_quick_edit_action': 'ksOnQuickEditViewAction',
        },

        init: function(parent, options) {
            this._super.apply(this, arguments);
            this.ksDashboardController = parent;

            this.ksOriginalItemData = $.extend({}, options.item);
            this.item = options.item;
            this.item_name = options.item.name;

        },

        willStart: function() {
            return $.when(this._super()).then(() => {
                return this._ksCreateController();
            });
        },

        _ksCreateController: function() {
            this.context = $.extend({}, this.getSession().user_context);
            this.context['form_view_ref'] = 'ks_dashboard_ninja.item_quick_edit_form_view';
            this.context['res_id'] = this.item.id;
            this.res_model = "ks_dashboard_ninja.item";
            this.dataset = new data.DataSet(this, this.res_model, this.context);
            const def = this.loadViews(this.dataset.model, this.context, [
                [false, 'list'],
                [false, 'form']
            ], {});
            return $.when(def).then((fieldsViews) => {
                this.formView = new QuickCreateFormView(fieldsViews.form, {
                    context: this.context,
                    modelName: this.res_model,
                    userContext: this.getSession().user_context,
                    currentId: this.item.id,
                    index: 0,
                    mode: 'edit',
                    footerToButtons: true,
                    default_buttons: false,
                    withControlPanel: false,
                    ids: [this.item.id],
                });
                return this.formView.getController(this);
            }).then((controller) => {
                this.controller = controller;
                this.controller._confirmChange = this._confirmChange.bind(this);
            });
        },

        //This Function is replacing Controllers to intercept in between to fetch changed data and update our item view.
        _confirmChange: function(id, fields, e) {
            if (e.name === 'discard_changes' && e.target.reset) {
                // the target of the discard event is a field widget.  In that
                // case, we simply want to reset the specific field widget,
                // not the full view
                return e.target.reset(this.controller.model.get(e.target.dataPointID), e, true);
            }

            const state = this.controller.model.get(this.controller.handle);
            this.controller.renderer.confirmChange(state, id, fields, e);
            return this.ks_Update_item();
        },

        ks_Update_item: function() {
            const ksChanges = this.controller.renderer.state.data;

            if (ksChanges['name']) this.item['name'] = ksChanges['name'];

            this.item['ks_font_color'] = ksChanges['ks_font_color'];
            this.item['ks_icon_select'] = ksChanges['ks_icon_select'];
            this.item['ks_icon'] = ksChanges['ks_icon'];
            this.item['ks_background_color'] = ksChanges['ks_background_color'];
            this.item['ks_default_icon_color'] = ksChanges['ks_default_icon_color'];
            this.item['ks_layout'] = ksChanges['ks_layout'];
            this.item['ks_record_count'] = ksChanges['ks_record_count'];

            if (ksChanges['ks_list_view_data']) this.item['ks_list_view_data'] = ksChanges['ks_list_view_data'];

            if (ksChanges['ks_chart_data']) this.item['ks_chart_data'] = ksChanges['ks_chart_data'];

            if (ksChanges['ks_kpi_data']) this.item['ks_kpi_data'] = ksChanges['ks_kpi_data'];

            if (ksChanges['ks_list_view_type']) this.item['ks_list_view_type'] = ksChanges['ks_list_view_type'];

            if (ksChanges['ks_chart_item_color']) this.item['ks_chart_item_color'] = ksChanges['ks_chart_item_color'];

            this.ksUpdateItemView();
        },

        start: function() {
            this._super.apply(this, arguments);
        },

        renderElement: function() {
            this._super.apply(this, arguments);
            this.controller.appendTo(this.$el.find(".ks_item_field_info"));

            this.trigger('canBeRendered', {});
        },

        ksUpdateItemView: function() {
            this.ksDashboardController.ksUpdateDashboardItem([this.item.id]);
            this.item_el = $.find('#' + this.item.id + '.ks_dashboarditem_id');

        },

        ksDiscardChanges: function() {
            this.ksDashboardController.ksFetchUpdateItem(this.item.id);
            this.destroy();
        },


        ksOnQuickEditViewAction: function(e) {
            this.need_reset = false;
            if (e.currentTarget.dataset['ksItemAction'] === 'saveItemInfo') {
                this.controller.saveRecord().then(() => {
                    this.ksDiscardChanges();
                })
            } else if (e.currentTarget.dataset['ksItemAction'] === 'fullItemInfo') {
                this.trigger('openFullItemForm', {});
            } else {
                this.ksDiscardChanges();
            }
        },

        destroy: function(options) {
            this.trigger('canBeDestroyed', {});
            this.controller.destroy();
            this._super();
        },
    });

    return {
        QuickEditView: QuickEditView,
    };
});
