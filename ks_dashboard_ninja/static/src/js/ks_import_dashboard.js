odoo.define('ks_dashboard_ninja.import_button', function(require) {
    "use strict";

    const core = require('web.core');
    const ListController = require('web.ListController');
    const framework = require('web.framework');
    const Dialog = require('web.Dialog');

    const _t = core._t;


    ListController.include({
        // TO add custom dashboard export option under action button
        _getActionMenuItems: function(state) {
            //Only for our custom model
            const props = this._super(...arguments);
            if (props && this.modelName == "ks_dashboard_ninja.board") {
                if (this.hasActionMenus) {
                    const otherActionItems = [{
                        description: _t("Export Dashboard"),
                        callback: this.ks_dashboard_export.bind(this)
                    }];
                    if (this.archiveEnabled) {
                        otherActionItems.push({
                            description: _t("Archive"),
                            callback: () => {
                                Dialog.confirm(this, _t("Are you sure that you want to archive all the selected records?"), {
                                    confirm_callback: this._toggleArchiveState.bind(this, true),
                                });
                            }
                        });
                        otherActionItems.push({
                            description: _t("Unarchive"),
                            callback: this._toggleArchiveState.bind(this, false)
                        });
                    }
                    if (this.is_action_enabled('delete')) {
                        otherActionItems.push({
                            description: _t('Delete'),
                            callback: this._onDeleteSelectedRecords.bind(this)
                        });
                    }
                    return Object.assign(props, {
                        items: Object.assign({}, this.toolbarActions, { other: otherActionItems }),
                        context: state.getContext(),
                        domain: state.getDomain(),
                        isDomainSelected: this.isDomainSelected,
                    });
                }
            }
            return props
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
