/* Copyright 2023 Tecnativa - Carlos Roca
 * License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
 */
odoo.define("sale_order_product_picker.PickerKanbanRecord", function (require) {
    "use strict";

    var KanbanRecord = require("web.KanbanRecord");
    var core = require("web.core");
    var _t = core._t;

    KanbanRecord.include({
        events: _.defaults(
            {
                "click .o_picker_quick_add": "_onQuickAddClicked",
                "click .o_picker_form_add": "_onFormAddClicked",
            },
            KanbanRecord.prototype.events
        ),
        getDefaultFields: function () {
            return ["product_id", "price_unit"];
        },
        _getContextPicker: function () {
            var ctx = this.getSession().user_context;
            for (var field of this.getDefaultFields()) {
                if (this.recordData[field]) {
                    var key = "default_" + field;
                    ctx[key] = this.recordData[field].res_id || this.recordData[field];
                }
            }
            return ctx;
        },
        /**
         * Return the kanban object and the ordered lines from a Kanban Card.
         *
         * @private
         */
        _getListObject: function () {
            const kanban_object = this.getParent();
            const order_form = kanban_object.getParent().getParent().__parentedChildren;
            const list = order_form.filter((obj) => {
                return obj.name === "order_line";
            })[0];
            return list;
        },
        /**
         * @private
         */
        _getLinesOfRecord: async function (list) {
            var model = list.getParent().getParent().model;
            var list_changes = model.localData[list.value.id]._changes;
            var lines = Object.fromEntries(
                Object.entries(model.localData).filter(([, value]) => {
                    return (
                        value.parentID === list.value.id &&
                        value.model === "sale.order.line" &&
                        !value.deleted
                    );
                })
            );
            var lines_of_record = [];
            for (var key in lines) {
                var line = lines[key];
                if (
                    !line.data.product_uom_qty &&
                    (!list_changes ||
                        !list_changes.filter((ob) => ob.id === key).length)
                ) {
                    line.deleted = true;
                }
                var data = Object.assign({}, line.data, line._changes);
                if (!data.name && !line.deleted) {
                    await model._fetchRecord(line);
                    data = line.data;
                }
                if (
                    model.checkLineToProcess(data, model.localData[this.db_id]) &&
                    !line.deleted
                ) {
                    lines_of_record.push({line: line, data: data});
                }
            }
            return lines_of_record;
        },
        /**
         * When a KanbanRecord is clicked anywhere inside the card with the class
         * `o_picker_kanban`, the method open record has to open the created record on
         * lines, or create a new one if it does not exist.
         *
         * Furthermore, if it is clicked inside the #picker-multiline-modal it will
         * close the modal and work as expected.
         *
         * @override
         * @private
         */
        _openRecord: function () {
            var $kanban = this.$el.closest(".o_picker_kanban");
            if ($kanban.length) {
                this._openRecordPickerForm();
            } else {
                this._super.apply(this, arguments);
            }
        },
        /**
         * Open or add record with form.
         *
         * @private
         */
        _openRecordPickerForm: async function () {
            var ctx = this._getContextPicker();
            const list = this._getListObject();
            const lines = await this._getLinesOfRecord(list);
            if (!lines.length) {
                list._openFormDialog({
                    context: ctx,
                    disable_multiple_selection: true,
                    on_saved: (record) => {
                        list._setValue({
                            operation: "ADD",
                            id: record.id,
                            picker_record_id: this.db_id,
                        });
                    },
                });
            } else if (lines.length === 1) {
                const id = lines[0].line.id;
                list._openFormDialog({
                    id: id,
                    disable_multiple_selection: true,
                    on_saved: (record) => {
                        list._setValue({
                            operation: "UPDATE",
                            id: record.id,
                            picker_record_id: this.db_id,
                        });
                    },
                    on_remove: () => {
                        list._setValue({
                            operation: "DELETE",
                            ids: [id],
                            picker_record_id: this.db_id,
                        });
                    },
                    deletable: true,
                });
            } else {
                this._openMultiLineModalPicker(list, lines, ctx);
            }
        },
        /**
         * Add a record quickly to lines.
         *
         * @private
         */
        _onQuickAddClicked: async function (ev) {
            const $target = $(ev.currentTarget);
            $target.attr("disabled", "disabled");
            var $kanban = this.$el.parent(".o_picker_kanban");
            if (!$kanban.length) {
                return;
            }
            var ctx = this._getContextPicker();
            const list = this._getListObject();
            const lines = await this._getLinesOfRecord(list);
            if (!lines.length) {
                Object.assign(ctx, {
                    created_from_picker: true,
                });
                list.trigger_up("edited_list", {id: list.value.id});
                list.picker = true;
                var changes = await list._setValue({
                    operation: "CREATE",
                    editable: "bottom",
                });
                var id = changes.filter((change) => change.name === "order_line")[0]
                    .value.data[0].id;
                var dataLine = {};
                for (var key of this.getDefaultFields()) {
                    dataLine[key] = this.recordData[key].res_id
                        ? {id: this.recordData[key].res_id}
                        : this.recordData[key];
                }
                list._setValue({
                    operation: "UPDATE",
                    id: id,
                    data: dataLine,
                    picker_record_id: this.db_id,
                });
            } else if (lines.length === 1) {
                const id = lines[0].line.id;
                const changes = {};
                if (lines[0].data.secondary_uom_id) {
                    Object.assign(changes, {
                        secondary_uom_qty: lines[0].data.secondary_uom_qty + 1,
                    });
                } else {
                    Object.assign(changes, {
                        product_uom_qty: lines[0].data.product_uom_qty + 1,
                    });
                }
                list.picker = true;
                list._setValue({
                    operation: "UPDATE",
                    id: id,
                    data: changes,
                    picker_record_id: this.db_id,
                });
            } else {
                $target.removeAttr("disabled");
                this._openMultiLineModalPicker(list, lines, ctx);
            }
        },
        /**
         * Add new record using form to lines.
         *
         * @private
         */
        _onFormAddClicked: async function () {
            var $kanban = this.$el.parent(".o_picker_kanban");
            if (!$kanban.length) {
                return;
            }
            var ctx = this._getContextPicker();
            const list = this._getListObject();
            list._openFormDialog({
                context: ctx,
                disable_multiple_selection: true,
                on_saved: (record) => {
                    list._setValue({
                        operation: "ADD",
                        id: record.id,
                        picker_record_id: this.db_id,
                    });
                },
            });
        },
        /**
         * Open lines selector modal to select the line that want to modify.
         *
         * @private
         */
        _openMultiLineModalPicker: async function (list, lines) {
            $("#picker-multiline-modal").remove();
            var new_list = Object.assign({}, list);
            var $new_list = list.$el.clone(true);
            new_list.$el = $new_list;
            var $cards = undefined;
            if ($new_list.find(".o_list_view").length !== 0) {
                // Check if tree mode
                $new_list
                    .find("tr:has(.o_field_x2many_list_row_add)")
                    .addClass("d-none");
                $cards = $new_list.find(".o_data_row");
            } else {
                $new_list.find(".o_x2m_control_panel").addClass("d-none");
                $cards = $new_list.find(".oe_kanban_card.o_kanban_record");
            }
            for (var line of lines) {
                var line_showed = list.value.data.filter(
                    (el) => el.id === line.line.id
                )[0];
                var index = list.value.data.indexOf(line_showed);
                $($cards[index]).addClass("product-selected");
            }
            $("body").append(
                _t(`
                <div class="modal o_legacy_dialog o_technical_modal" id="picker-multiline-modal" role="dialog">
                    <div class="modal-dialog modal-lg ui-draggable">
                        <!-- Modal content-->
                        <div class="modal-content">
                            <div class="modal-header ui-draggable-handle">
                                <h4 class="modal-title">Select witch line you want to modify</h4>
                                <button type="button" class="close" data-dismiss="modal">&times;</button>
                            </div>
                            <div class="modal-body" />
                            <div class="modal-footer">
                                <button type="button" class="btn btn-primary" data-dismiss="modal">Close</button>
                            </div>
                        </div>
                    </div>
                </div>`)
            );
            $("#picker-multiline-modal .modal-body").append($new_list);
            $("#picker-multiline-modal").modal({show: true});
        },
    });

    return KanbanRecord;
});
