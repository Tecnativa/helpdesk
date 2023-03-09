/* Copyright 2023 Tecnativa - Carlos Roca
 * License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
 */
odoo.define("sale_order_product_picker.basic_model", function(require) {
  "use strict";

  var BasicModel = require("web.BasicModel");

  BasicModel.include({
    getBreakFields: function() {
      return ["product_id"];
    },
    checkLineToProcess: function(solRecordData, pickerRecord, context) {
      var res = true;
      for (var field of this.getBreakFields()) {
        var default_field = "default_" + field;
        if (context && context[default_field]) {
          res =
            res &&
            context[default_field] ===
              this.localData[pickerRecord._changes[field]].res_id;
        } else if (solRecordData[field] && pickerRecord._changes[field]) {
          res =
            res &&
            this.localData[solRecordData[field]].res_id ===
              this.localData[pickerRecord._changes[field]].res_id;
        } else {
          res = res && !solRecordData[field] && !pickerRecord._changes[field];
        }
      }
      return res;
    },
    _applyChange: async function(recordID, changes) {
      if (
        recordID &&
        this.get(recordID).model === "sale.order" &&
        Object.keys(changes).includes("order_line")
      ) {
        if (
          changes.order_line.operation === "UPDATE" &&
          !(changes.order_line.data && changes.order_line.data.product_id)
        ) {
          var solRecord = this.localData[changes.order_line.id];
          var solRecordChanges = Object.assign(
            {},
            solRecord._changes,
            changes.order_line.data
          );
          changes.order_line.diff_qty = 0;
          if (!solRecord.last_qty && solRecord.data.product_uom_qty) {
            solRecord.last_qty = 0;
          } else if (!solRecord.last_qty && !solRecord.data.product_uom_qty) {
            solRecord.last_qty = 1;
          }
          changes.order_line.diff_qty =
            solRecordChanges.product_uom_qty -
            ((solRecord.data && solRecord.data.product_uom_qty) || 0) -
            solRecord.last_qty;
          solRecord.last_qty += changes.order_line.diff_qty;
        }
        var soRecord = this.localData[recordID];
        var picker_ids = {};
        if (soRecord._changes && soRecord._changes.picker_ids) {
          picker_ids = this.localData[soRecord._changes.picker_ids];
        }
        var pickerRecords = [];
        for (var change of picker_ids._changes || []) {
          if (change.operation === "ADD") {
            pickerRecords.push(change.id);
          }
        }
        if (pickerRecords.length) {
          var picker_changes = this._applyChangesPicker(
            recordID,
            changes.order_line,
            pickerRecords
          );
          if (picker_changes) {
            changes.picker_ids = picker_changes;
          }
        }
        if (changes.order_line.operation === "DELETE") {
          for (var line_id of changes.order_line.ids) {
            var line = this.localData[line_id];
            line.deleted = true;
          }
        }
      }
      var res = this._super(...arguments);
      return res;
    },
    _applyChangesPicker: function(recordID, command, pickerRecords) {
      var picker_id = command.picker_record_id;
      var picker_changes = undefined;
      switch (command.operation) {
        case "ADD":
          picker_changes = this._computeAddedRecord(command, picker_id, pickerRecords);
          break;
        case "CREATE":
          picker_changes = this._computeCreatedRecord(
            command,
            picker_id,
            pickerRecords
          );
          break;
        case "UPDATE":
          picker_changes = this._computeUpdatedRecord(
            command,
            picker_id,
            pickerRecords
          );
          break;
        case "DELETE":
          picker_changes = this._computeDeletedRecord(
            command,
            picker_id,
            pickerRecords
          );
          break;
        case "DELETE_ALL":
          var lines_id = Object.keys(this.localData).filter(key => {
            return (
              this.localData[key].parentID === recordID &&
              this.localData[key].model === "sale.order.line"
            );
          })[0];
          var keys = Object.keys(this.localData).filter(key => {
            return (
              this.localData[key].parentID === lines_id &&
              this.localData[key].model === "sale.order.line" &&
              !this.localData[key].deleted
            );
          });
          picker_changes = this._computeDeletedRecord({ids: keys}, null, pickerRecords);
          break;
        case "MULTI":
          picker_changes = {
            operation: "MULTI",
            commands: [],
          };
          _.each(command.commands, function(innerCommand) {
            picker_changes.commands.push(
              this._applyChangesPicker(recordID, innerCommand, pickerRecords)
            );
          });
          break;
      }
      return picker_changes;
    },
    _computeAddedRecord: function(command, picker_id, pickerRecords) {
      var solRecord = this.localData[command.id];
      solRecord.last_qty = solRecord._changes.product_uom_qty;
      var pickerRecord = undefined;
      if (picker_id) {
        pickerRecord = this.localData[picker_id];
      } else {
        for (var record_id of pickerRecords) {
          var possiblePickerRecord = this.localData[record_id];
          if (this.checkLineToProcess(solRecord._changes, possiblePickerRecord)) {
            pickerRecord = possiblePickerRecord;
            break;
          }
        }
      }
      return {
        operation: "UPDATE",
        id: pickerRecord.id,
        data: {
          is_in_order: true,
          product_uom_qty:
            pickerRecord._changes.product_uom_qty + solRecord._changes.product_uom_qty,
        },
      };
    },
    _computeCreatedRecord: function(command, picker_id, pickerRecords) {
      if (picker_id) {
        var pickerRecord = this.localData[picker_id];
        return {
          operation: "UPDATE",
          id: picker_id,
          data: {
            is_in_order: true,
            product_uom_qty: pickerRecord._changes.product_uom_qty + 1,
          },
        };
      }
      if (command.context) {
        var product_id = command.context[0].default_product_id;
        var qty = command.context[0].default_product_uom_qty;
        if (!product_id) {
          return;
        }
        for (var record_id of pickerRecords) {
          var pickerRecord = this.localData[record_id];
          if (this.checkLineToProcess({}, pickerRecord, command.context[0])) {
            return {
              operation: "UPDATE",
              id: record_id,
              data: {
                is_in_order: true,
                product_uom_qty: pickerRecord._changes.product_uom_qty + qty || 1,
              },
            };
          }
        }
      }
    },
    _computeDeletedRecord: function(command, picker_id, pickerRecords) {
      if (picker_id) {
        var pickerRecord = this.localData[picker_id];
        var deleted_qty =
          this.localData[command.ids[0]]._changes.product_uom_qty ||
          this.localData[command.ids[0]].data.product_uom_qty;
        var qty = pickerRecord._changes.product_uom_qty - deleted_qty;
        return {
          operation: "UPDATE",
          id: picker_id,
          data: {
            is_in_order: Boolean(qty),
            product_uom_qty: qty,
          },
        };
      }
      var operation = {
        operation: "MULTI",
        commands: [],
      };
      var qty_by_picker = {};
      for (var line_id of command.ids) {
        var line = this.localData[line_id];
        var line_data = Object.assign({}, line.data, line._changes);
        if (!line_data.product_id) {
          break;
        }
        for (var record_id of pickerRecords) {
          var pickerRecord = this.localData[record_id];
          if (this.checkLineToProcess(line_data, pickerRecord)) {
            qty_by_picker[record_id] =
              (qty_by_picker[record_id] || pickerRecord._changes.product_uom_qty) -
              line_data.product_uom_qty;
            break;
          }
        }
      }
      for (var [key, value] of Object.entries(qty_by_picker)) {
        operation.commands.push({
          operation: "UPDATE",
          id: key,
          data: {
            is_in_order: Boolean(value),
            product_uom_qty: value,
          },
        });
      }
      return operation;
    },
    _computeUpdatedRecord: function(command, picker_id, pickerRecords) {
      var diff_qty = 0;
      var solRecord = this.localData[command.id];
      var changes = Object.assign({}, solRecord._changes, command.data);
      if (command.data && command.data.product_id) {
        solRecord.last_qty = changes.product_uom_qty;
        for (var record_id of pickerRecords) {
          var pickerRecord = this.localData[record_id];
          if (
            this.checkLineToProcess({}, pickerRecord, {
              default_product_id: command.data.product_id.id,
            })
          ) {
            return {
              operation: "UPDATE",
              id: record_id,
              data: {
                is_in_order: Boolean(
                  pickerRecord._changes.product_uom_qty + changes.product_uom_qty
                ),
                product_uom_qty:
                  pickerRecord._changes.product_uom_qty + changes.product_uom_qty,
              },
            };
          }
        }
      }
      diff_qty = command.diff_qty;
      if (picker_id) {
        var pickerRecord = this.localData[picker_id];
        return {
          operation: "UPDATE",
          id: picker_id,
          data: {
            is_in_order: Boolean(pickerRecord._changes.product_uom_qty + diff_qty),
            product_uom_qty: pickerRecord._changes.product_uom_qty + diff_qty,
          },
        };
      }
      var solRecordData = Object.assign({}, solRecord.data, solRecord._changes);
      for (var record_id of pickerRecords) {
        var pickerRecord = this.localData[record_id];
        if (this.checkLineToProcess(solRecordData, pickerRecord)) {
          return {
            operation: "UPDATE",
            id: record_id,
            data: {
              is_in_order: Boolean(pickerRecord._changes.product_uom_qty + diff_qty),
              product_uom_qty: pickerRecord._changes.product_uom_qty + diff_qty,
            },
          };
        }
      }
    },
  });

  return BasicModel;
});
