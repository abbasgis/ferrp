/**
 * Created by ather on 5/7/2017.
 */
var TabularModel = function (aaVM) {
    var me = this;
    me.aaVM = aaVM;
    me.initialize = function () {
        try {
            var yearlyData = me.aaVM.schemesStats; // loaded from sampledata.js
            var dataObj = yearlyData[0];
            var fields = me.createFieldsList(dataObj);
            $('#' + me.aaVM.containerDivId).dxPivotGrid({
                allowSortingBySummary: true,
                allowSorting: true,
                allowFiltering: true,
                allowExpandAll: true,
                height: '100%',
                showBorders: true,
                fieldChooser: {
                    enabled: true
                },
                fieldPanel: {
                    visible: true, // shows the Field Panel
                    allowFieldDragging: false,

                },
                export: {
                    enabled: true,
                    fileName: "ADP Analysis"
                },
                onContextMenuPreparing: function(e){me.onContextProcessing(e)},
                dataSource: {
                    fields: fields,
                    store: yearlyData
                }
            });

        } catch (err) {
            console.error(err.stack);
        }
    }
    me.onContextProcessing = function (e) {
        if (e.field && e.field.area == 'data') {
            // Obtaining the PivotGrid's data source
            var dataSource = e.component.getDataSource();

            // Implementing a click event handler for the context menu items
            var changeSummaryType = function (clickedItem) {
                dataSource.field(e.field.index, {
                    summaryType: clickedItem.itemData.value,
                    summaryDisplayMode: null,
                });
                dataSource.load();
            };
            var changeSummaryDisplayMode = function (clickedItem) {
                dataSource.field(e.field.index, {
                    summaryType:"sum",
                    summaryDisplayMode: clickedItem.itemData.value
                });
                dataSource.load();
            };

            // Declaring an array of summary types to be present in the context menu
            var items = [
                {text: 'Sum', value: 'sum', onItemClick: changeSummaryType},
                {text: 'Avg', value: 'avg', onItemClick: changeSummaryType},
                {text: 'Min', value: 'min', onItemClick: changeSummaryType},
                {text: 'Max', value: 'max', onItemClick: changeSummaryType},
                {text: 'Count', value: 'count', onItemClick: changeSummaryType},
                // { text: 'Custom', value: 'custom', onItemClick: changeSummaryType },
                // { text: 'Absolute Variation', value: 'absoluteVariation', onItemClick: changeSummaryDisplayMode },
                // { text: 'Percent Variation', value: 'percentVariation', onItemClick: changeSummaryDisplayMode },
                {text: 'Percent of Column Total', value: 'percentOfColumnTotal', onItemClick: changeSummaryDisplayMode },
                {text: "Percent of Row Total", value: "percentOfRowTotal", onItemClick: changeSummaryDisplayMode},
                // { text: "Percent of Column Grand Total", value: "percentOfColumnGrandTotal" },
                // { text: "Percent of Row Grand Total", value: "percentOfRowGrandTotal" },
                {text: "Percent of Grand Total", value: "percentOfGrandTotal", onItemClick: changeSummaryDisplayMode}
            ];

            // Applying the "selected" style to the item that represents the current summary type
            $.each(items, function (_, item) {
                if (item.value == dataSource.field(e.field.index).summaryType)
                    item.selected = true;
            });

            // Pushing the array of summary types to the array of context menu items
            Array.prototype.push.apply(e.items, items)
        }
    }
    me.initialFields = function (fieldVal) {
        var choossenField = [{name: "Sector", area: "row"}, {name: "ADPYear", area: "column"}, {
            name: "Allocation",
            area: "data"
        }];

        for (var i = 0; i < choossenField.length; i++) {
            if (choossenField[i].name == fieldVal) {
                return choossenField[i];
            }
        }
        return null;
    }

    me.createFieldsList = function (dataObj) {
        var fields = [];
        var summaryDisplayModes = [
            {text: "Sum", value: "sum"},
            // { text: "Absolute Variation", value: "absoluteVariation" },
            // { text: "Percent Variation", value: "percentVariation" },
            {text: "Percent of Column Total", value: "percentOfColumnTotal"},
            {text: "Percent of Row Total", value: "percentOfRowTotal"},
            // { text: "Percent of Column Grand Total", value: "percentOfColumnGrandTotal" },
            // { text: "Percent of Row Grand Total", value: "percentOfRowGrandTotal" },
            {text: "Percent of Grand Total", value: "percentOfGrandTotal"}
        ];
        for (var key in dataObj) {
            var initialFields = me.initialFields(key);
            var area = null;
            if (initialFields) area = initialFields.area;
            var numberField = !isNaN(parseFloat(dataObj[key]));
            if (numberField) {
                var displayFolder = key
                // for (var i = 0; i < summaryDisplayModes.length; i++) {
                    var fieldObj = {
                        caption: key,  //+ " " + summaryDisplayModes[i].text,
                        // width: 120,
                        dataField: key,
                        summaryType: 'sum' | 'min' | 'max' | 'avg' | 'count', //summaryDisplayModes[i].value,
                        // displayFolder: displayFolder,
                        isMeasure: true,
                        area: area
                    };
                    fields.push(fieldObj);
                    area = null;
                // }
            } else {
                var fieldObj = {
                    caption: key,
                    // width: 120,
                    dataField: key,
                    area: area
                };
                fields.push(fieldObj);
            }

        }
        return fields;
    }
}