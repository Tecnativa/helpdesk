odoo.define('ks_dashboard_ninja.ks_to_do_dashboard_filter', function (require) {
    "use strict";

    const KsDashboard = require('ks_dashboard_ninja.ks_dashboard');
    const core = require('web.core');
    const QWeb = core.qweb;
    const Dialog = require('web.Dialog');

    const _t = core._t;


    return KsDashboard.include({
         events: _.extend({}, KsDashboard.prototype.events, {
            'click .ks_edit_content': '_onKsEditTask',
            'click .ks_delete_content': '_onKsDeleteContent',
            'click .header_add_btn': '_onKsAddTask',
            'click .ks_li_tab': '_onKsUpdateAddButtonAttribute',
            'click .ks_do_item_active_handler': '_onKsActiveHandler',
        }),

        ksRenderDashboardItems: function(items) {
            this.$el.find('.print-dashboard-btn').addClass("ks_pro_print_hide");

            if (this.ks_dashboard_data.ks_gridstack_config) {
                this.gridstackConfig = JSON.parse(this.ks_dashboard_data.ks_gridstack_config);
            }
            let item_view;
            for (let i = 0; i < items.length; i++) {
                if (this.grid) {
                    if (items[i].ks_dashboard_item_type === 'ks_tile') {
                        const item_view = this._ksRenderDashboardTile(items[i])
                        if (items[i].id in this.gridstackConfig) {
                            this.grid.addWidget($(item_view)[0], {x:this.gridstackConfig[items[i].id].x, y:this.gridstackConfig[items[i].id].y, w:this.gridstackConfig[items[i].id].w, h:this.gridstackConfig[items[i].id].h,autoPosition:false,minW:2,maxW:null,minH:2,maxH:2,id:items[i].id,});
                        } else {
                            this.grid.addWidget($(item_view)[0], {x:0, y:0, w:3, h:2,autoPosition:true,minW:2,maxW:null,minH:2,maxH:2,id:items[i].id});
                        }
                    } else if (items[i].ks_dashboard_item_type === 'ks_list_view') {
                        this._renderListView(items[i], this.grid)
                    } else if (items[i].ks_dashboard_item_type === 'ks_kpi') {
                        const $kpi_preview = this.renderKpi(items[i], this.grid)
                        if (items[i].id in this.gridstackConfig) {
                            this.grid.addWidget($kpi_preview[0], {x:this.gridstackConfig[items[i].id].x, y:this.gridstackConfig[items[i].id].y, w:this.gridstackConfig[items[i].id].w, h:this.gridstackConfig[items[i].id].h,autoPosition:false,minW:2,maxW:null,minH:2,maxH:3,id:items[i].id});
                        } else {
                            this.grid.addWidget($kpi_preview[0], {x:0, y:0, w:3, h:2,autoPosition:true,minW:2,maxW:null,minH:2,maxH:3,id:items[i].id});
                        }

                    }  else if (items[i].ks_dashboard_item_type === 'ks_to_do'){
                        const $to_do_preview = this.ksRenderToDoDashboardView(items[i]);
                        if (items[i].id in this.gridstackConfig) {
                            this.grid.addWidget($to_do_preview[0], {x:this.gridstackConfig[items[i].id].x, y:this.gridstackConfig[items[i].id].y, w:this.gridstackConfig[items[i].id].w, h:this.gridstackConfig[items[i].id].h, autoPosition:false, minW:5, maxW:null, minH:2, maxH:null, id:items[i].id});
                        } else {
                            this.grid.addWidget($to_do_preview[0], {x:0, y:0, w:6, h:4, autoPosition:true, minW:5, maxW:null, minH:2, maxH:null, id:items[i].id})
                        }
                    } else {
                        this._renderGraph(items[i], this.grid)
                    }
                }
            }
        },

        ksRenderToDoDashboardView: function(item){
            const item_title = item.name;
            const item_id = item.id;
            const list_to_do_data = JSON.parse(item.ks_to_do_data)
            const ks_header_color = this._ks_get_rgba_format(item.ks_header_bg_color);
            const ks_font_color = this._ks_get_rgba_format(item.ks_font_color);
            const ks_rgba_button_color = this._ks_get_rgba_format(item.ks_button_color);
            const $ksItemContainer = this.ksRenderToDoView(item);
            const $ks_gridstack_container = $(QWeb.render('ks_to_do_dashboard_container', {
                ks_chart_title: item_title,
                ksIsDashboardManager: this.ks_dashboard_data.ks_dashboard_manager,
                ks_dashboard_list: this.ks_dashboard_data.ks_dashboard_list,
                item_id: item_id,
                to_do_view_data: list_to_do_data,
                 ks_rgba_button_color:ks_rgba_button_color,
            })).addClass('ks_dashboarditem_id')
            $ks_gridstack_container.find('.ks_card_header').addClass('ks_bg_to_color').css({"background-color": ks_header_color });
            $ks_gridstack_container.find('.ks_card_header').addClass('ks_bg_to_color').css({"color": ks_font_color + ' !important' });
            $ks_gridstack_container.find('.ks_li_tab').addClass('ks_bg_to_color').css({"color": ks_font_color + ' !important' });
            $ks_gridstack_container.find('.ks_list_view_heading').addClass('ks_bg_to_color').css({"color": ks_font_color + ' !important' });
            $ks_gridstack_container.find('.ks_to_do_card_body').append($ksItemContainer)
            return $ks_gridstack_container;
        },

        ksRenderToDoView: function(item, ks_tv_play=false) {
            const item_id = item.id;
            const list_to_do_data = JSON.parse(item.ks_to_do_data);
            const $todoViewContainer = $(QWeb.render('ks_to_do_dashboard_inner_container', {
                ks_to_do_view_name: "Test",
                to_do_view_data: list_to_do_data,
                item_id: item_id,
                ks_tv_play: ks_tv_play
            }));

            return $todoViewContainer
        },

        _onKsEditTask: function(e){
            const ks_description_id = e.currentTarget.dataset.contentId;
            const ks_item_id = e.currentTarget.dataset.itemId;
            const ks_section_id = e.currentTarget.dataset.sectionId;
            const ks_description = $(e.currentTarget.parentElement.parentElement).find('.ks_description').attr('value');

            const $content = "<div><input type='text' class='ks_description' value='"+ ks_description +"' placeholder='Task'></input></div>"
            const dialog = new Dialog(this, {
                title: _t('Edit Task'),
                size: 'medium',
                $content: $content,
                buttons: [
                    {
                        text: 'Save',
                        classes: 'btn-primary',
                        click: (e) => {
                            let content = $(e.currentTarget.parentElement.parentElement).find('.ks_description').val();
                            if (content.length === 0){
                                content = ks_description;
                            }
                            this.onSaveTask(content, parseInt(ks_description_id), parseInt(ks_item_id), parseInt(ks_section_id));
                        },
                        close: true,
                    },
                    {
                        text: _t('Close'),
                        classes: 'btn-secondary o_form_button_cancel',
                        close: true,
                    }
                ],
            });
            dialog.open();
        },

        onSaveTask: function(content, ks_description_id, ks_item_id, ks_section_id){
            this._rpc({
                model: 'ks_to.do.description',
                method: 'write',
                args: [ks_description_id, {
                    "ks_description": content
                }],
            }).then(() => {
                return this.ksFetchUpdateItem(ks_item_id);
            }).then(() => {
                $(".ks_li_tab[data-item-id=" + ks_item_id + "]").removeClass('active');
                $(".ks_li_tab[data-section-id=" + ks_section_id + "]").addClass('active');
                $(".ks_tab_section[data-item-id=" + ks_item_id + "]").removeClass('active');
                $(".ks_tab_section[data-item-id=" + ks_item_id + "]").removeClass('show');
                $(".ks_tab_section[data-section-id=" + ks_section_id + "]").addClass('active');
                $(".ks_tab_section[data-section-id=" + ks_section_id + "]").addClass('show');
                $(".header_add_btn[data-item-id=" + ks_item_id + "]").attr('data-section-id', ks_section_id);
            });
        },

        _onKsDeleteContent: function(e){
            const ks_description_id = e.currentTarget.dataset.contentId;
            const ks_item_id = e.currentTarget.dataset.itemId;
            const ks_section_id = e.currentTarget.dataset.sectionId;

            Dialog.confirm(this, (_t("Are you sure you want to remove this task?")), {
                confirm_callback: () => {
                    this._rpc({
                        model: 'ks_to.do.description',
                        method: 'unlink',
                        args: [parseInt(ks_description_id)],
                    }).then(() => {
                        this.ksFetchUpdateItem(ks_item_id).then(() => {
                            $(".ks_li_tab[data-item-id=" + ks_item_id + "]").removeClass('active');
                            $(".ks_li_tab[data-section-id=" + ks_section_id + "]").addClass('active');
                            $(".ks_tab_section[data-item-id=" + ks_item_id + "]").removeClass('active');
                            $(".ks_tab_section[data-item-id=" + ks_item_id + "]").removeClass('show');
                            $(".ks_tab_section[data-section-id=" + ks_section_id + "]").addClass('active');
                            $(".ks_tab_section[data-section-id=" + ks_section_id + "]").addClass('show');
                            $(".header_add_btn[data-item-id=" + ks_item_id + "]").attr('data-section-id', ks_section_id);
                        });
                    });
                },
            });
        },

        _onKsAddTask: function(e){
            const ks_section_id = e.currentTarget.dataset.sectionId;
            const ks_item_id = e.currentTarget.dataset.itemId;
            const $content = "<div><input type='text' class='ks_section' placeholder='Task' required></input></div>"
            const dialog = new Dialog(this, {
                title: _t('New Task'),
                $content: $content,
                size: 'medium',
                buttons: [
                    {
                        text: 'Save',
                        classes: 'btn-primary',
                        click: (e) => {
                            const content = $(e.currentTarget.parentElement.parentElement).find('.ks_section').val();
                            if (content.length !== 0){
                                this._onCreateTask(content, parseInt(ks_section_id), parseInt(ks_item_id));
                            }
                        },
                        close: true,
                    },
                    {
                        text: _t('Close'),
                        classes: 'btn-secondary o_form_button_cancel',
                        close: true,
                    }
                ],
            });
            dialog.open();
        },

        _onCreateTask: function(content, ks_section_id, ks_item_id){
            this._rpc({
                model: 'ks_to.do.description',
                method: 'create',
                args: [{
                    ks_to_do_header_id: ks_section_id,
                    ks_description: content,
                }],
            }).then(() => {
                return this.ksFetchUpdateItem(ks_item_id);
            }).then(() => {
                $(".ks_li_tab[data-item-id=" + ks_item_id + "]").removeClass('active');
                $(".ks_li_tab[data-section-id=" + ks_section_id + "]").addClass('active');
                $(".ks_tab_section[data-item-id=" + ks_item_id + "]").removeClass('active');
                $(".ks_tab_section[data-item-id=" + ks_item_id + "]").removeClass('show');
                $(".ks_tab_section[data-section-id=" + ks_section_id + "]").addClass('active');
                $(".ks_tab_section[data-section-id=" + ks_section_id + "]").addClass('show');
                $(".header_add_btn[data-item-id=" + ks_item_id + "]").attr('data-section-id', ks_section_id);
            });
        },

        _onKsUpdateAddButtonAttribute: function(e){
            const item_id = e.currentTarget.dataset.itemId;
            const sectionId = e.currentTarget.dataset.sectionId;
            $(".header_add_btn[data-item-id=" + item_id + "]").attr('data-section-id', sectionId);
        },

        _onKsActiveHandler: function(e){
            const ks_item_id = e.currentTarget.dataset.itemId;
            const content_id = e.currentTarget.dataset.contentId;
            const ks_section_id = e.currentTarget.dataset.sectionId;
            let ks_value = e.currentTarget.dataset.valueId;
            if (ks_value == 'True'){
                ks_value = false
            }else{
                ks_value = true
            }
            this.content_id = content_id;
            this._rpc({
                model: 'ks_to.do.description',
                method: 'write',
                args: [content_id, {
                    "ks_active": ks_value
                }],
            }).then(() => {
                return this.ksFetchUpdateItem(ks_item_id);
            }).then(() => {
                $(".ks_li_tab[data-item-id=" + ks_item_id + "]").removeClass('active');
                $(".ks_li_tab[data-section-id=" + ks_section_id + "]").addClass('active');
                $(".ks_tab_section[data-item-id=" + ks_item_id + "]").removeClass('active');
                $(".ks_tab_section[data-item-id=" + ks_item_id + "]").removeClass('show');
                $(".ks_tab_section[data-section-id=" + ks_section_id + "]").addClass('active');
                $(".ks_tab_section[data-section-id=" + ks_section_id + "]").addClass('show');
                $(".header_add_btn[data-item-id=" + ks_item_id + "]").attr('data-section-id', ks_section_id);
            });
        }
})

});
