/**
 * Created by Dr. Ather Ashraf on 7/8/2018.
 */
var JqxChartModel = function (viewModel,divID) {
    var me = this;
    me.viewModel = viewModel

    me.outputSize = me.viewModel.getOutputPanelSize();
    me.chartTarget = $('#' + divID);
    me.dataAdapter = null;

    me.toolTipCustomFormatFn = function (value, itemIndex, serie, group, categoryValue, categoryAxis) {
        var record = me.dataAdapter.records[itemIndex];
        me.viewModel.olMapModel.showSelectedFeatureGeometry(record['point'],true);
        return "Value: " + value;
    };

    me.createDataAdapter = function (dataFields, data) {
        var source = {
            datatype: 'json',
            datafields: dataFields,
            localdata: data
        }
        me.dataAdapter = new $.jqx.dataAdapter(source, {autoBind: true});
    }

    me.createLineChart = function (title, xDataField, yDataField, maxX) {
        // alert(me.outputWidth)
        if (me.dataAdapter) {
            var settings = {
                title: null, //title,
                description: null,//"In this example the range selector works with (non-date) axis",
                enableAnimations: true,
                showLegend: false,
                animationDuration: 1500,
                enableCrosshairs: true,
                padding: {left: 5, top: 10, right: 30, bottom: 5},
                colorScheme: 'scheme02',
                source: me.dataAdapter,
                xAxis: {
                    minValue: 0,
                    maxValue: maxX,
                    dataField: xDataField,
                    flip: false,
                    valuesOnTicks: true,
                    rangeSelector: {
                        serieType: 'area',
                        padding: {/*left: 0, right: 0,*/ top: 10, bottom: 0},
                        // Uncomment the line below to render the selector in a separate container
                        //renderTo: $('#selectorContainer'),
                        backgroundColor: 'white',
                        size: 70,
                        gridLines: {visible: true},
                    }
                },
                seriesGroups: [
                    {
                        type: 'line',
                        toolTipFormatFunction: me.toolTipCustomFormatFn,
                        valueAxis: {
                            flip: false,
                            title: {text: 'Distance<br><br>'}
                        },
                        series: [
                            {dataField: yDataField, lineWidth: 1, lineWidthSelected: 1}
                        ]
                    }

                ]
            };
            me.chartTarget.jqxChart(settings);

            me.chartTarget.jqxChart('refresh');
        }
    }
}