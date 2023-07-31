/** @odoo-module **/
import BarcodesModelsMixin from "stock_barcodes.BarcodesModelsMixin";
import BasicController from "web.BasicController";
import {RemoteMeasure} from "@web_widget_remote_measure/js/remote_measure_widget.esm";

RemoteMeasure.include(BarcodesModelsMixin);
RemoteMeasure.include({
    /**
     * @override
     */
    init() {
        this._super(...arguments);
        this._is_valid_barcode_model = this._isAllowedBarcodeModel(this.model);
        if (this._is_valid_barcode_model) {
            // Controller base is used when the renderer its initialized by a field
            this._controller_base = this.findAncestor((parent) => {
                return parent instanceof BasicController;
            });
        }
    },
    /**
     * Avoid intercept events in valid barcodes models.
     * This is necessary to get the event in the controller.
     *
     * @override
     */
    _onKeydown(ev) {
        if (this._is_valid_barcode_model && ev.keyCode === $.ui.keyCode.ENTER) {
            if (this._controller_base) {
                ev.stopPropagation();
                this._controller_base._onDocumentKeyDown(ev);
            }
        } else {
            this._super(...arguments);
        }
    },
});
