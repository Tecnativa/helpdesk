odoo.define('ks_dashboard_ninja.KsGlobalFunction', function(require) {
    "use strict";

    const session = require('web.session');
    const field_utils = require('web.field_utils');

    return {
        ksNumIndianFormatter: function(num, digits) {
            let negative;
            const si = [{
                value: 1,
                symbol: ""
            },
            {
                value: 1E3,
                symbol: "Th"
            },
            {
                value: 1E5,
                symbol: "Lakh"
            },
            {
                value: 1E7,
                symbol: "Cr"
            },
            {
                value: 1E9,
                symbol: "Arab"
            }
            ];
            if (num < 0) {
                num = Math.abs(num)
                negative = true
            }
            const rx = /\.0+$|(\.[0-9]*[1-9])0+$/;
            let i;
            for (i = si.length - 1; i > 0; i--) {
                if (num >= si[i].value) {
                    break;
                }
            }
            if (negative) {
                return "-" + (num / si[i].value).toFixed(digits).replace(rx, "$1") + si[i].symbol;
            } else {
                return (num / si[i].value).toFixed(digits).replace(rx, "$1") + si[i].symbol;
            }

        },
        ksNumFormatter: function(num, digits) {
            let negative;
            const si = [{
                    value: 1,
                    symbol: ""
                },
                {
                    value: 1E3,
                    symbol: "k"
                },
                {
                    value: 1E6,
                    symbol: "M"
                },
                {
                    value: 1E9,
                    symbol: "G"
                },
                {
                    value: 1E12,
                    symbol: "T"
                },
                {
                    value: 1E15,
                    symbol: "P"
                },
                {
                    value: 1E18,
                    symbol: "E"
                }
            ];
            if (num < 0) {
                num = Math.abs(num)
                negative = true
            }
            const rx = /\.0+$|(\.[0-9]*[1-9])0+$/;
            let i;
            for (i = si.length - 1; i > 0; i--) {
                if (num >= si[i].value) {
                    break;
                }
            }
            if (negative) {
                return "-" + (num / si[i].value).toFixed(digits).replace(rx, "$1") + si[i].symbol;
            } else {
                return (num / si[i].value).toFixed(digits).replace(rx, "$1") + si[i].symbol;
            }
        },

        ks_monetary: function(value, currency_id) {
            const currency = session.get_currency(currency_id);
            if (!currency) {
                return value;
            }
            if (currency.position === "after") {
                return value += ' ' + currency.symbol;
            } else {
                return currency.symbol + ' ' + value;
            }
        },

        _onKsGlobalFormatter: function(ks_record_count, ks_data_format, ks_precision_digits){
            if (ks_data_format == 'exact'){
                return field_utils.format.float(ks_record_count, Float64Array,{digits:[0,ks_precision_digits]});
            }else{
                if (ks_data_format == 'indian'){
                    return this.ksNumIndianFormatter( ks_record_count, 1);
                }else if (ks_data_format == 'colombian'){
                    return this.ksNumColombianFormatter( ks_record_count, 1, ks_precision_digits);
                }else{
                    return this.ksNumFormatter(ks_record_count, 1);
                }
            }
        },

        ksNumColombianFormatter: function(num, digits, ks_precision_digits) {
            let negative;
            const si = [{
                    value: 1,
                    symbol: ""
                },
                {
                    value: 1E3,
                    symbol: ""
                },
                {
                    value: 1E6,
                    symbol: "M"
                },
                {
                    value: 1E9,
                    symbol: "M"
                },
                {
                    value: 1E12,
                    symbol: "M"
                },
                {
                    value: 1E15,
                    symbol: "M"
                },
                {
                    value: 1E18,
                    symbol: "M"
                }
            ];
            if (num < 0) {
                num = Math.abs(num)
                negative = true
            }
            let i;
            for (i = si.length-1; i > 0; i--) {
                if (num >= si[i].value) {
                    break;
                }
            }

            if (si[i].symbol === 'M') {
                num = parseInt(num) / 1000000;
                num = field_utils.format.integer(num, Float64Array);
                if (negative) {
                    return "-" + num + si[i].symbol;
                } else {
                    return num + si[i].symbol;
                }
            } else{
                if (num % 1===0) {
                    num = field_utils.format.integer(num, Float64Array);
                } else {
                    num = field_utils.format.float(num, Float64Array, {digits:[0,ks_precision_digits]});
                }
                if (negative) {
                    return "-" + num;
                } else {
                    return num;
                }
            }
        },
    }

});
