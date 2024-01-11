/** @odoo-module **/
import {FormViewDialog} from "web.view_dialogs";
import {patch} from "@web/core/utils/patch";
import {_t} from "web.core";

patch(FormViewDialog.prototype, "sale_product_security_price.FormViewDialog", {
    _save: async function () {
        const res = await this._super(...arguments);
        if (
            this.form_view.model.get(this.form_view.handle).data.security_price_warning
        ) {
            this.displayNotification({
                message: _t("The price set is under security price."),
                type: "danger",
            });
        }
        return res;
    },
});
