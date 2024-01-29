/** @odoo-module **/
/* Copyright 2024 Tecnativa - Carlos Roca
 * License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
 */
const {Component} = owl;
import {formatMonetary} from "@web/fields/formatters";
import rpc from "web.rpc";
import utils from "web.utils";
import widgetRegistryOwl from "web.widgetRegistry";

export class WidgetSecurityPrice extends Component {
    setup() {
        this.security_price_monetary = formatMonetary(
            this.props.record.data.security_price,
            {currency_id: this.props.record.data.currency_id.res_id}
        );
    }

    async _onClick() {
        const record = this.props.record;
        if (record.data.security_price > record.data.price_reduce) {
            if (record.data.discount == 100) {
                this.__owl__.parent.parentWidget.trigger_up("field_changed", {
                    dataPointID: record.id,
                    changes: {
                        price_unit: record.data.security_price,
                        discount: 0,
                    },
                });
            } else {
                const discount = record.data.discount;
                const precision = await rpc.query({
                    model: "decimal.precision",
                    method: "precision_get",
                    args: ["Product Price"],
                });
                await this.__owl__.parent.parentWidget.trigger_up("field_changed", {
                    dataPointID: record.id,
                    changes: {
                        price_unit: utils.round_decimals(
                            (record.data.security_price * 100) /
                                (100 - record.data.discount),
                            precision
                        ),
                    },
                });
                // The sol discount is reset when price unit changes.
                // We apply the discount after update the price unit
                this.__owl__.parent.parentWidget.trigger_up("field_changed", {
                    dataPointID: record.id,
                    changes: {
                        discount: discount,
                    },
                });
            }
        }
    }
}
WidgetSecurityPrice.template = "sale_product_security_price.WidgetSecurityPrice";

widgetRegistryOwl.add("security_price_button", WidgetSecurityPrice);
