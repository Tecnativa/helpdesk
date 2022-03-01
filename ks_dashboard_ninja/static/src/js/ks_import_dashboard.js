odoo.define('ks_dashboard_ninja.import_button', function(require) {
    "use strict";

    const core = require('web.core');
    const Sidebar = require('web.Sidebar');
    const ListController = require('web.ListController');
    const framework = require('web.framework');
    const Dialog = require('web.Dialog');

    const _t = core._t;


    ListController.include({
        // TO add custom dashboard export option under action button
        renderSidebar: function($node) {
            //Only for our custom model
            if (this.modelName == "ks_dashboard_ninja.board") {
                if (this.hasSidebar) {
                    const other = [{
                        label: _t("Export Dashboard"),
                        callback: this.ks_dashboard_export.bind(this)
                    }];
                    if (this.archiveEnabled) {
                        other.push({
                            label: _t("Archive"),
                            callback: () => {
                                Dialog.confirm(this, _t("Are you sure that you want to archive all the selected records?"), {
                                    confirm_callback: this._toggleArchiveState.bind(this, true),
                                });
                            }
                        });
                        other.push({
                            label: _t("Unarchive"),
                            callback: this._toggleArchiveState.bind(this, false)
                        });
                    }
                    if (this.is_action_enabled('delete')) {
                        other.push({
                            label: _t('Delete'),
                            callback: this._onDeleteSelectedRecords.bind(this)
                        });
                    }
                    this.sidebar = new Sidebar(this, {
                        editable: this.is_action_enabled('edit'),
                        env: {
                            context: this.model.get(this.handle, {
                                raw: true
                            }).getContext(),
                            activeIds: this.getSelectedIds(),
                            model: this.modelName,
                        },
                        actions: _.extend(this.toolbarActions, {
                            other: other
                        }),
                    });
                    return this.sidebar.appendTo($node).then(() => {
                        this._toggleSidebar();
                    });
                }
                return Promise.resolve();
            } else {
                this._super.apply(this, arguments);
            }
        },

        ks_dashboard_export: function() {
            this.ks_on_dashboard_export(this.getSelectedIds());
        },

        ks_on_dashboard_export: function(ids) {
            this._rpc({
                model: 'ks_dashboard_ninja.board',
                method: 'ks_dashboard_export',
                args: [JSON.stringify(ids)],
            }).then((result) => {
                const name = "dashboard_ninja";
                const data = {
                    "header": name,
                    "dashboard_data": result,
                }
                framework.blockUI();
                this.getSession().get_file({
                    url: '/ks_dashboard_ninja/export/dashboard_json',
                    data: {
                        data: JSON.stringify(data)
                    },
                    complete: framework.unblockUI,
                    error: (error) => this.call('crash_manager', 'rpc_error', error),
                });
            })
        },
    });

    core.action_registry.add('ks_dashboard_ninja.import_button', ListController);

    return ListController;
});
