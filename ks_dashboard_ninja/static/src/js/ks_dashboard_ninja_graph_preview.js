odoo.define('ks_dashboard_ninja_list.ks_dashboard_graph_preview', function(require) {
    "use strict";

    const registry = require('web.field_registry');
    const AbstractField = require('web.AbstractField');
    const core = require('web.core');
    const field_utils = require('web.field_utils');
    const KsGlobalFunction = require('ks_dashboard_ninja.KsGlobalFunction');

    const QWeb = core.qweb;


    const KsGraphPreview = AbstractField.extend({
        supportedFieldTypes: ['char'],
        resetOnAnyFieldChange: true,
        jsLibs: [
            '/ks_dashboard_ninja/static/lib/js/Chart.bundle.min.js',
            '/ks_dashboard_ninja/static/lib/js/chartjs-plugin-datalabels.js'
        ],
        cssLibs: [
            '/ks_dashboard_ninja/static/lib/css/Chart.min.css'
        ],

        /**
         * @override
         */
        start: function() {
            this.ks_set_default_chart_view();
            core.bus.on("DOM_updated", this, this._onCoreDOMUpdated);
            Chart.plugins.unregister(ChartDataLabels);
            return this._super.apply(this, arguments);
        },

        /**
         * @override
         */
        destroy: function() {
            core.bus.off("DOM_updated", this._onCoreDOMUpdated);
            return this._super.apply(this, arguments);
        },

        /**
         * @private
         * @param {DOMEvent} ev
         */
        _onCoreDOMUpdated: function(ev) {
            if (this.shouldRenderChart && this.$('#ksMyChart').length > 0) {
                this.renderChart();
            }
        },

        ks_set_default_chart_view: function() {
            Chart.plugins.register({
                afterDraw: (chart) => {
                    if (chart.data.labels.length === 0) {
                        // No data is present
                        const ctx = chart.chart.ctx;
                        const width = chart.chart.width;
                        const height = chart.chart.height
                        chart.clear();
                        ctx.save();
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'middle';
                        ctx.font = "3rem 'Lucida Grande'";
                        ctx.fillText('No data available', width / 2, height / 2);
                        ctx.restore();
                    }
                }
            });

            Chart.Legend.prototype.afterFit = function() {
                const chart_type = this.chart.config.type;
                if (chart_type === "pie" || chart_type === "doughnut") {
                    this.height = this.height;
                } else {
                    this.height = this.height + 20;
                };
            }
        },

        /**
         * @override
         */
        _render: function() {
            this.$el.empty()
            if (this.recordData.ks_dashboard_item_type !== 'ks_tile' && this.recordData.ks_dashboard_item_type !== 'ks_kpi' && this.recordData.ks_dashboard_item_type !== 'ks_list_view' && this.recordData.ks_dashboard_item_type !== 'ks_to_do') {
                if (this.recordData.ks_model_id) {
                    if (this.recordData.ks_chart_groupby_type == 'date_type' && !this.recordData.ks_chart_date_groupby) {
                        return this.$el.append($('<div>').text("Select Group by date to create chart based on date groupby"));
                    } else if (this.recordData.ks_chart_data_count_type === "count" && !this.recordData.ks_chart_relation_groupby) {
                        this.$el.append($('<div>').text("Select Group By to create chart view"));
                    } else if (this.recordData.ks_chart_data_count_type !== "count" && (this.recordData.ks_chart_measure_field.count === 0 || !this.recordData.ks_chart_relation_groupby)) {
                        this.$el.append($('<div>').text("Select Measure and Group By to create chart view"));
                    } else if (!this.recordData.ks_chart_data_count_type) {
                        this.$el.append($('<div>').text("Select Chart Data Count Type"));
                    } else {
                        this._getChartData();
                    }
                } else {
                    this.$el.append($('<div>').text("Select a Model first."));
                }

            }

        },

        /**
         * @private
         */
        _getChartData: function() {
            this.shouldRenderChart = true;
            let field = this.recordData;
            let ks_chart_name;
            if (field.name) {
                ks_chart_name = field.name;
            } else if (field.ks_model_name) {
                ks_chart_name = field.ks_model_id.data.display_name;
            } else {
                ks_chart_name = "Name";
            }

            this.chart_type = this.recordData.ks_dashboard_item_type.split('_')[1];
            this.chart_data = JSON.parse(this.recordData.ks_chart_data);

            if (field.ks_chart_cumulative_field){
                for (let i=0; i< this.chart_data.datasets.length; i++){
                    let ks_temp_com = 0;
                    const datasets = {};
                    const data = [];
                    if (this.chart_data.datasets[i].ks_chart_cumulative_field) {
                        for (let j=0; j < this.chart_data.datasets[i].data.length; j++) {
                            ks_temp_com = ks_temp_com + this.chart_data.datasets[i].data[j];
                            data.push(ks_temp_com);
                        }
                        datasets.label =  'Cumulative' + this.chart_data.datasets[i].label;
                        datasets.data = data;
                        if (field.ks_chart_cumulative){
                            datasets.type =  'line';
                        }
                        this.chart_data.datasets.push(datasets);
                    }
                }
            }

            const $chartContainer = $(QWeb.render('ks_chart_form_view_container', {
                ks_chart_name: ks_chart_name
            }));
            this.$el.append($chartContainer);

            switch (this.chart_type) {
                case "pie":
                case "doughnut":
                case "polarArea":
                    this.chart_family = "circle";
                    break;
                case "bar":
                case "horizontalBar":
                case "line":
                case "area":
                    this.chart_family = "square"
                    break;
                default:
                    this.chart_family = "none";
                    break;
            }

            if (this.chart_family === "circle") {
                if (this.chart_data && this.chart_data['labels'].length > 30) {
                    this.$el.find(".card-body").empty().append($("<div style='font-size:20px;'>Too many records for selected Chart Type. Consider using <strong>Domain</strong> to filter records or <strong>Record Limit</strong> to limit the no of records under <strong>30.</strong>"));
                    return;
                }
            }
            if (this.$('#ksMyChart').length > 0) {
                this.renderChart();
            }
        },

        renderChart: function() {
            const scales = {}
            if (this.recordData.ks_chart_measure_field_2.count && this.recordData.ks_dashboard_item_type === 'ks_bar_chart') {
                scales.yAxes = [{
                        type: "linear",
                        display: true,
                        position: "left",
                        id: "y-axis-0",
                        gridLines: {
                            display: true
                        },
                        labels: {
                            show: true,
                        }
                    },
                    {
                        type: "linear",
                        display: true,
                        position: "right",
                        id: "y-axis-1",
                        labels: {
                            show: true,
                        },
                        ticks: {
                            beginAtZero: true,
                            callback: (value, index, values) => {
                                const ks_selection = this.chart_data.ks_selection;
                                if (ks_selection === 'monetary') {
                                    const ks_currency_id = this.chart_data.ks_currency;
                                    let ks_data = KsGlobalFunction._onKsGlobalFormatter(value, this.recordData.ks_data_format, this.recordData.ks_precision_digits);
                                    ks_data = KsGlobalFunction.ks_monetary(ks_data, ks_currency_id);
                                    return ks_data;
                                } else if (ks_selection === 'custom') {
                                    const ks_field = this.chart_data.ks_field;
                                    return KsGlobalFunction._onKsGlobalFormatter(value, this.recordData.ks_data_format, this.recordData.ks_precision_digits) + ' ' + ks_field;
                                }else {
                                    return KsGlobalFunction._onKsGlobalFormatter(value, this.recordData.ks_data_format, this.recordData.ks_precision_digits);
                                }
                            },
                        }
                    }
                ]
            }
            let chart_plugin = [];
            if (this.recordData.ks_show_data_value) {
                chart_plugin.push(ChartDataLabels);
            }
            this.ksMyChart = new Chart(this.$('#ksMyChart')[0], {
                type: this.chart_type === "area" ? "line" : this.chart_type,
                plugins: chart_plugin,
                data: {
                    labels: this.chart_data['labels'],
                    datasets: this.chart_data.datasets,
                },
                options: {
                    maintainAspectRatio: false,
                    animation: {
                        easing: 'easeInQuad',
                    },
                    legend: {
                            display: this.recordData.ks_hide_legend
                        },
                    layout: {
                        padding: {
                            bottom: 0,
                        }
                    },
                    scales: scales,
                    plugins: {
                        datalabels: {
                            backgroundColor: (context) => {
                                return context.dataset.backgroundColor;
                            },
                            borderRadius: 4,
                            color: 'white',
                            font: {
                                weight: 'bold'
                            },
                            anchor: 'center',
                            textAlign: 'center',
                            display: 'auto',
                            clamp: true,
                            formatter: (value, ctx) => {
                                let sum = 0;
                                let dataArr = ctx.dataset.data;
                                dataArr.map(data => {
                                    sum += data;
                                });
                                let percentage = sum === 0 ? 0 + "%" : (value * 100 / sum).toFixed(2) + "%";
                                return percentage;
                            },
                        },
                    },

                }
            });
            if (this.chart_data && this.chart_data["datasets"].length > 0) {
                this.ksChartColors(this.recordData.ks_chart_item_color, this.ksMyChart, this.chart_type, this.chart_family, this.recordData.ks_show_data_value);
            }
        },

        ksHideFunction: function(options, recordData, ksChartFamily, chartType) {
            return options;
        },

        ksChartColors: function(palette, ksMyChart, ksChartType, ksChartFamily, ks_show_data_value) {
            let currentPalette = "cool";
            if (!palette) {
                palette = currentPalette;
            }
            currentPalette = palette;

            /*Gradients
              The keys are percentage and the values are the color in a rgba format.
              You can have as many "color stops" (%) as you like.
              0% and 100% is not optional.*/
            let gradient;
            let color_set = [];
            switch (palette) {
                case 'cool':
                    gradient = {
                        0: [255, 255, 255, 1],
                        20: [220, 237, 200, 1],
                        45: [66, 179, 213, 1],
                        65: [26, 39, 62, 1],
                        100: [0, 0, 0, 1]
                    };
                    break;
                case 'warm':
                    gradient = {
                        0: [255, 255, 255, 1],
                        20: [254, 235, 101, 1],
                        45: [228, 82, 27, 1],
                        65: [77, 52, 47, 1],
                        100: [0, 0, 0, 1]
                    };
                    break;
                case 'neon':
                    gradient = {
                        0: [255, 255, 255, 1],
                        20: [255, 236, 179, 1],
                        45: [232, 82, 133, 1],
                        65: [106, 27, 154, 1],
                        100: [0, 0, 0, 1]
                    };
                    break;

                case 'default':
                    color_set = ['#F04F65', '#f69032', '#fdc233', '#53cfce', '#36a2ec', '#8a79fd', '#b1b5be', '#1c425c', '#8c2620', '#71ecef', '#0b4295', '#f2e6ce', '#1379e7']
            }

            //Find datasets and length
            const chartType = ksMyChart.config.type;
            let datasets;
            let setsCount;
            switch (chartType) {
                case "pie":
                case "doughnut":
                case "polarArea":
                    datasets = ksMyChart.config.data.datasets[0];
                    setsCount = datasets.data.length;
                    break;
                case "bar":
                case "horizontalBar":
                case "line":
                    datasets = ksMyChart.config.data.datasets;
                    setsCount = datasets.length;
                    break;
            }

            //Calculate colors
            const chartColors = [];
            if (palette !== "default") {
                //Get a sorted array of the gradient keys
                let gradientKeys = Object.keys(gradient);
                gradientKeys.sort((a, b) => +a - +b);
                for (let i = 0; i < setsCount; ++i) {
                    const gradientIndex = (i + 1) * (100 / (setsCount + 1)); //Find where to get a color from the gradient
                    for (let j = 0; j < gradientKeys.length; ++j) {
                        const gradientKey = gradientKeys[j];
                        if (gradientIndex === +gradientKey) { //Exact match with a gradient key - just get that color
                            chartColors[i] = 'rgba(' + gradient[gradientKey].toString() + ')';
                            break;
                        } else if (gradientIndex < +gradientKey) { //It's somewhere between this gradient key and the previous
                            const prevKey = gradientKeys[j - 1];
                            const gradientPartIndex = (gradientIndex - prevKey) / (gradientKey - prevKey); //Calculate where
                            const color = [];
                            for (let k = 0; k < 4; k++) { //Loop through Red, Green, Blue and Alpha and calculate the correct color and opacity
                                color[k] = gradient[prevKey][k] - ((gradient[prevKey][k] - gradient[gradientKey][k]) * gradientPartIndex);
                                if (k < 3) color[k] = Math.round(color[k]);
                            }
                            chartColors[i] = 'rgba(' + color.toString() + ')';
                            break;
                        }
                    }
                }
            } else {
                for (let i = 0, counter = 0; i < setsCount; ++i, ++counter) {
                    if (counter >= color_set.length) {
                        counter = 0; // reset back to the beginning
                    }
                    chartColors.push(color_set[counter]);
                }
            }

            let options = ksMyChart.config.options;
            options.legend.labels.usePointStyle = true;
            if (ksChartFamily == "circle") {
                if (ks_show_data_value) {
                    options.legend.position = 'top';
                    options.layout.padding.top = 10;
                    options.layout.padding.bottom = 20;
                } else {
                    options.legend.position = 'bottom';
                }

                options = this.ksHideFunction(options, this.recordData, ksChartFamily, chartType);
                options.plugins.datalabels.align = 'center';
                options.plugins.datalabels.anchor = 'end';
                options.plugins.datalabels.borderColor = 'white';
                options.plugins.datalabels.borderRadius = 25;
                options.plugins.datalabels.borderWidth = 2;
                options.plugins.datalabels.clamp = true;
                options.plugins.datalabels.clip = false;
                options.tooltips.callbacks = {
                    title: (tooltipItem, data) => {
                        let k_amount = data.datasets[tooltipItem[0].datasetIndex]['data'][tooltipItem[0].index];
                        const ks_selection = this.chart_data.ks_selection;
                        if (ks_selection === 'monetary') {
                            const ks_currency_id = this.chart_data.ks_currency;
                            k_amount = KsGlobalFunction.ks_monetary(k_amount, ks_currency_id);
                            return data.datasets[tooltipItem[0].datasetIndex]['label'] + " : " + k_amount
                        } else if (ks_selection === 'custom') {
                            const ks_field = this.chart_data.ks_field;
                            //                                                        ks_type = field_utils.format.char(ks_field);
                            k_amount = field_utils.format.float(k_amount, Float64Array, {digits: [0, this.recordData.ks_precision_digits]});
                            return data.datasets[tooltipItem[0].datasetIndex]['label'] + " : " + k_amount + " " + ks_field;
                        } else {
                            k_amount = field_utils.format.float(k_amount, Float64Array, {digits: [0, this.recordData.ks_precision_digits]});
                            return data.datasets[tooltipItem[0].datasetIndex]['label'] + " : " + k_amount
                        }
                    },
                    label: (tooltipItem, data) => {
                        return data.labels[tooltipItem.index];
                    },

                }
                for (let i = 0; i < datasets.length; i++) {
                    datasets[i].backgroundColor = chartColors;
                    datasets[i].borderColor = "rgba(255,255,255,1)";
                }
                if (this.recordData.ks_semi_circle_chart && (chartType === "pie" || chartType === "doughnut")) {
                    options.rotation = 1 * Math.PI;
                    options.circumference = 1 * Math.PI;
                }
            } else if (ksChartFamily == "square") {
                options = this.ksHideFunction(options, this.recordData, ksChartFamily, chartType);
                options.scales.xAxes[0].gridLines.display = false;
                options.scales.yAxes[0].ticks.beginAtZero = true;
                options.plugins.datalabels.align = 'end';
                options.plugins.datalabels.formatter = (value, ctx) => {
                    const ks_selection = this.chart_data.ks_selection;
                    if (ks_selection === 'monetary') {
                        const ks_currency_id = this.chart_data.ks_currency;
                        let ks_data = KsGlobalFunction._onKsGlobalFormatter(value, this.recordData.ks_data_format, this.recordData.ks_precision_digits);
                            ks_data = KsGlobalFunction.ks_monetary(ks_data, ks_currency_id);
                        return ks_data;
                    } else if (ks_selection === 'custom') {
                        const ks_field = this.chart_data.ks_field;
                        return `${KsGlobalFunction._onKsGlobalFormatter(value, this.recordData.ks_data_format, this.recordData.ks_precision_digits)} ${ks_field}`;
                    }else {
                        return KsGlobalFunction._onKsGlobalFormatter(value, this.recordData.ks_data_format, this.recordData.ks_precision_digits);
                    }
                };

                if (chartType === "line") {
                    options.plugins.datalabels.backgroundColor = (context) => {
                        return context.dataset.borderColor;
                    };
                }
                if (chartType === "horizontalBar") {
                    options.scales.xAxes[0].ticks.callback = (value, index, values) => {
                        const ks_selection = this.chart_data.ks_selection;
                        if (ks_selection === 'monetary') {
                            const ks_currency_id = this.chart_data.ks_currency;
                            let ks_data = KsGlobalFunction._onKsGlobalFormatter(value, this.recordData.ks_data_format, this.recordData.ks_precision_digits);
                                ks_data = KsGlobalFunction.ks_monetary(ks_data, ks_currency_id);
                            return ks_data;
                        } else if (ks_selection === 'custom') {
                            const ks_field = this.chart_data.ks_field;
                            return `${KsGlobalFunction._onKsGlobalFormatter(value, this.recordData.ks_data_format, this.recordData.ks_precision_digits)} ${ks_field}`;
                        }else {
                            return KsGlobalFunction._onKsGlobalFormatter(value, this.recordData.ks_data_format, this.recordData.ks_precision_digits);
                        }
                    }
                    options.scales.xAxes[0].ticks.beginAtZero = true;
                } else {
                    options.scales.yAxes[0].ticks.callback = (value, index, values) => {
                        const ks_selection = this.chart_data.ks_selection;
                        if (ks_selection === 'monetary') {
                            const ks_currency_id = this.chart_data.ks_currency;
                            let ks_data = KsGlobalFunction._onKsGlobalFormatter(value, this.recordData.ks_data_format, this.recordData.ks_precision_digits);
                                ks_data = KsGlobalFunction.ks_monetary(ks_data, ks_currency_id);
                            return ks_data;
                        } else if (ks_selection === 'custom') {
                            const ks_field = this.chart_data.ks_field;
                            return `${KsGlobalFunction._onKsGlobalFormatter(value, this.recordData.ks_data_format, this.recordData.ks_precision_digits)} ${ks_field}`;
                        }else {
                            return KsGlobalFunction._onKsGlobalFormatter(value, this.recordData.ks_data_format, this.recordData.ks_precision_digits);
                        }
                    }
                }
                options.tooltips.callbacks = {
                    label: (tooltipItem, data) => {
                        let k_amount = data.datasets[tooltipItem.datasetIndex]['data'][tooltipItem.index];
                        const ks_selection = this.chart_data.ks_selection;
                        if (ks_selection === 'monetary') {
                            const ks_currency_id = this.chart_data.ks_currency;
                            k_amount = KsGlobalFunction.ks_monetary(k_amount, ks_currency_id);
                            return `${data.datasets[tooltipItem.datasetIndex]['label']} : ${k_amount}`;
                        } else if (ks_selection === 'custom') {
                            const ks_field = this.chart_data.ks_field;
                            k_amount = field_utils.format.float(k_amount, Float64Array, {digits: [0, this.recordData.ks_precision_digits]});
                            return `${data.datasets[tooltipItem.datasetIndex]['label']} : ${k_amount} ${ks_field}`;
                        } else {
                            k_amount = field_utils.format.float(k_amount, Float64Array, {digits: [0, this.recordData.ks_precision_digits]});
                            return `${data.datasets[tooltipItem.datasetIndex]['label']} : ${k_amount}`;
                        }
                    }
                }

                for (let i = 0; i < datasets.length; ++i) {
                    switch (ksChartType) {
                        case "bar":
                        case "horizontalBar":
                            if (datasets[i].type && datasets[i].type == "line") {
                                datasets[i].borderColor = chartColors[i];
                                datasets[i].backgroundColor = "rgba(255,255,255,0)";
                                datasets[i]['datalabels'] = {
                                    backgroundColor: chartColors[i],
                                }

                            } else {
                                datasets[i].backgroundColor = chartColors[i];
                                datasets[i].borderColor = "rgba(255,255,255,0)";
                                options.scales.xAxes[0].stacked = this.recordData.ks_bar_chart_stacked;
                                options.scales.yAxes[0].stacked = this.recordData.ks_bar_chart_stacked;
                            }
                            break;
                        case "line":
                            datasets[i].borderColor = chartColors[i];
                            datasets[i].backgroundColor = "rgba(255,255,255,0)";
                            break;
                        case "area":
                            datasets[i].borderColor = chartColors[i];
                            break;
                    }
                }
            }

            ksMyChart.update();
            if (this.$el.find('canvas').height() < 250) {
                this.$el.find('canvas').height(250);
            }
        },
    });

    registry.add('ks_dashboard_graph_preview', KsGraphPreview);

    return {
        KsGraphPreview: KsGraphPreview,
    };

});
