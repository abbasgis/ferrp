/**
 * Created by Dr. Ather Ashraf on 11/9/2018.
 */

var StaticViewModel = function (olMapModel, mapInfo) {
    var me = this;
    me.statsModel = new StatsModel();
    me.statsModel.initializeStatsModel(olMapModel);
    me.init = function () {
        // me.statsModel.createStatsTreeGrid([]);
    }
};
var StatsModel = function () {
    var me = this;
    me.treeGridEl = null;
    me.olMapModel = null;
    me.btnSendSMS = $("#btnSendSMS");
    me.initializeStatsModel = function (olMapModel) {
        me.treeGridEl = $("#treegrid");
        me.olMapModel = olMapModel;
        if (me.treeGridEl[0].children.length === 0) {
            me.createStatsTreeGrid([]);
        }
    };
    me.getStatsSummaryFromDB = function (project_id, buffer) {
        var formData = new FormData();
        formData.append("project_id", project_id);
        formData.append("buffer", buffer);
        var params = {
            url: "/web_services/wps/get_project_geo_stats/",
            type: "POST",
            data: formData,
            dataType: "json",
            processData: false,
            contentType: false,
            async: true,
            headers: {'X-CSRFToken': me.olMapModel.csrfToken},
        }
        callAJAX(params, function (data) {
            var title = "Stats Within " + buffer + " meter";
            data = data.data;
            $("#id_buffer_val").text(title);
            // alert(JSON.stringify(data));
            me.updateGridDataWithLocalData(data);
        })
    };
    me.getGeoStatistics = function (feature, buffer) {
        var wkt = me.olMapModel.getGeometryWKT(feature.getGeometry());
        var formData = new FormData();
        formData.append("buffer", buffer);
        formData.append("WKT", wkt);
        var params = {
            url: "/web_services/wps/get_geostatics/",
            type: "POST",
            data: formData,
            dataType: "json",
            processData: false,
            contentType: false,
            async: true,
            headers: {'X-CSRFToken': me.olMapModel.csrfToken},

        }
        callAJAX(params, function (data) {
            var title = "Stats Within " + data.buffer + " meter";
            data = data.data;
            $("#id_buffer_val").text(title);
            // alert(JSON.stringify(data));
            me.updateGridDataWithLocalData(data);
        })
    };
    me.getStatsDetail = function (ids, infoRequired) {
        var formData = new FormData();
        formData.append("ids", ids);
        formData.append("infoRequired", infoRequired);
        var url = "/web_services/wps/get_stats_detail/";
        var params = {
            url: url,
            type: "POST",
            data: formData,
            dataType: "json",
            processData: false,
            contentType: false,
            async: true,
            headers: {'X-CSRFToken': me.olMapModel.csrfToken},
        };
        callAJAX(params, function (data) {
            if (infoRequired === 'climate' || infoRequired === 'headwork_detail' || infoRequired === 'water_quality' || infoRequired === 'water_level') {
                me.createAnalysisGridDialog(data, infoRequired)
            }
            else if (infoRequired === 'school_ids') {
                me.createSchoolsDetailGrid(data)
            }
        });

    };
    me.createStatsTreeGrid = function (data) {

        var source =
            {
                dataType: "json",
                dataFields: [
                    {name: 's_id', type: 'number'},
                    {name: 'property', type: 'string'},
                    {name: 'value', type: 'string'},
                    {name: 'parent', type: 'number'},

                ],
                hierarchy: {
                    keyDataField: {name: 's_id'},
                    parentDataField: {name: 'parent'}
                },
                id: 's_id',
                localData: data
            };
        var dataAdapter = new $.jqx.dataAdapter(source);
        // create Tree Grid
        me.treeGridEl.jqxTreeGrid(
            {
                width: '100%',
                height: '500px',
                source: dataAdapter,
                altRows: true,
                sortable: true,
                ready: function () {
                    me.treeGridEl.jqxTreeGrid('expandRow', '2');
                },
                columns: [
                    {text: 'Property', dataField: 'property', width: 200},
                    {
                        text: 'Value', dataField: 'value', width: 200,
                        // cellsrenderer: function (row, column, value) {
                        //     var v = value.toString();
                        //     if (v.indexOf('button') > -1) {
                        //         // var rowData = me.treeGridEl.jqxTreeGrid('getrowdata', row);
                        //         return '<a href="#">' + value + '</a>';
                        //     } else {
                        //         return value;
                        //     }
                        //
                        // }
                    }
                ],
                showToolbar: true,
                toolbarHeight: 25,
                renderToolbar: function (toolBar) {
                    var toTheme = function (className) {
                        if (theme == "") return className;
                        return className + " " + className + "-" + theme;
                    }
                    // appends buttons to the status bar.
                    var container = $("<div style='overflow: hidden; position: relative; height: 100%; width: 100%;'></div>");
                    var title = $("<div id='id_buffer_val' style='text-align: center;font-size: large'></div>")
                    // var buttonTemplate = "<div style='float: left; padding: 3px; margin: 2px;'><div style='margin: 4px; width: 16px; height: 16px;'></div></div>";
                    // var cancelButton = $(buttonTemplate);
                    container.append(title);
                    toolBar.append(container);
                    // cancelButton.jqxButton({
                    //     cursor: "pointer",
                    //     height: 25,
                    //     width: 25
                    // });
                    // cancelButton.find('div:first').addClass(toTheme('jqx-icon-cancel'));
                    // cancelButton.jqxTooltip({position: 'bottom', content: "Cancel"});
                    // cancelButton.click(function (event) {
                    //     if (!cancelButton.jqxButton('disabled')) {
                    //         // cancel changes.
                    //         $("#treegrid").jqxTreeGrid('endRowEdit', rowKey, true);
                    //     }
                    // });

                },

            });
        me.treeGridEl.on('rowClick', function (event) {
            // event args.
            var args = event.args;
            // row data.
            var row = args.row;
            // row key.
            var key = args.key;
            // data field
            var dataField = args.dataField;
            // original click event.
            var clickEvent = args.originalEvent;
            var cellValue = me.treeGridEl.jqxTreeGrid('getCellValue', key, 'value');
            if (cellValue.indexOf('button') > -1) {
                var button = $(cellValue);
                me.getStatsDetail(button.val(), button[0].title);
            }
        });

    };


    me.updateGridDataWithLocalData = function (data) {
        var adapter = me.treeGridEl.jqxTreeGrid('source');
        var gridSource = adapter._source;
        var newSource = {
            dataType: "json",
            dataFields: gridSource.dataFields,
            hierarchy: {
                keyDataField: {name: 's_id'},
                parentDataField: {name: 'parent'},
                //root: 'children'
            },
            id: 's_id',
            // url: '/projects/proj_dir_data?project_id=' + project_id,
            localData: data
        };
        var newDataAdapter = new $.jqx.dataAdapter(newSource);
        me.treeGridEl.jqxTreeGrid({
            source: newDataAdapter
        });
        me.treeGridEl.jqxTreeGrid('updateBoundData');


    }
    me.createAnalysisGridDialog = function (data, infoRequired) {
        me.dimensionModelingGridTarget = $('<div id="dimension_modeling_grid_target"></div>')
        var div = $('<div style="margin-top: 20px;"></div>');
        div.append(me.dimensionModelingGridTarget);
        me.analysisGridDialog = new BootstrapDialog({
            size: BootstrapDialog.SIZE_WIDE,
            message: div,
            draggable: true,
            buttons: [
                {
                    label: 'Close',
                    cssClass: 'btn-primary',
                    action: function (dialogRef) {
                        dialogRef.close();
                    }
                }
            ]
        });
        me.analysisGridDialog.realize();
        me.analysisGridDialog.setTitle('Data Analysis (Dimension Modeling)');
        me.analysisGridDialog.setType(BootstrapDialog.TYPE_SUCCESS);
        me.analysisGridDialog.getModalHeader().css('height', '45');
        me.analysisGridDialog.open();
        var rows = [];
        var measures = [];
        var columns = [{
            "uniqueName": "quality_type",
        }];
        if (infoRequired === 'climate') {
            rows = [
                {
                    "uniqueName": "date_acquired.Year",
                },
                {
                    "uniqueName": "date_acquired.Month",
                },

            ];
            measures = [
                {
                    "uniqueName": "temp_fahrenheit",
                    "aggregation": "max"
                },
                {
                    "uniqueName": "precipitation_inches",
                    "aggregation": "sum"
                }
            ];
            me.createFlexMonsterPivotTable(data, rows, measures, columns);
        }
        else if (infoRequired === 'headwork_detail') {
            rows = [
                {
                    "uniqueName": "head_works"
                },
                {
                    "uniqueName": "discharge_date.Year",
                },
                {
                    "uniqueName": "discharge_date.Month",
                }

            ];
            measures = [
                {
                    "uniqueName": "upstream",
                    "aggregation": "max"
                },
                {
                    "uniqueName": "downstream",
                    "aggregation": "max"
                }
            ];
            me.createFlexMonsterPivotTable(data, rows, measures, columns);
        }
        else if (infoRequired === 'water_quality') {
            rows = [
                {
                    "uniqueName": "year"
                },
                {
                    "uniqueName": "season",
                }

            ];
            columns = [{
                "uniqueName": "quality_type",
            }];
            measures = [
                {
                    "uniqueName": "water_quality",
                    "aggregation": "max"
                },

            ];
            me.createFlexMonsterPivotTable(data, rows, measures, columns);
        }
        else if (infoRequired === 'water_level') {
            rows = [
                {
                    "uniqueName": "year"
                }

            ];
            columns = [{
                "uniqueName": "season",
            }];
            measures = [
                {
                    "uniqueName": "water_depth",
                    "aggregation": "max"
                },
            ];
            me.createFlexMonsterPivotTable(data, rows, measures, columns);
        }
    }
    me.createDimensionModelingGrid = function (data) {
        me.dimensionModelingGridTarget.append(JSON.stringify(data))
    };
    me.createFlexMonsterPivotTable = function (data, rows, measures, columns) {
        me.dimensionModelingGridTarget.flexmonster({
            // container: container_id,
            componentFolder: "https://cdn.flexmonster.com/",
            toolbar: true,
            height: '100%',
            report: {
                dataSource: {
                    data: data
                },
                "slice": {
                    "rows": rows,
                    "columns": columns,
                    "measures": measures
                },
            },
            licenseKey: 'Z7HI-XG503S-5O4M4H-6F456Z-0A3E3Z-1X663C-5O4R35-4R'// for dch server
            // licenseKey: 'Z7CJ-XF9J50-5J4J6X-2H136N-2L036W-1A0O01-6S5S6R-0W0T20-3C' // for localhost
        });

    }
    me.createSchoolsDetailGrid = function (data) {
        var fields = me.createFields(data[0]);
        var columns = me.schoolGridColumns();
        var source = {
            datatype: 'json',
            datafields: fields,
            localdata: data
        };
        var dataSource = new $.jqx.dataAdapter(source, {autoBind: true});
        var modalbody = $('<div ></div>');
        me.gridEl = $('<div id="jqxgrid"></div>');
        me.showBootStrapDialog(modalbody);
        me.createJqxGrid(me.gridEl, columns, dataSource);
        modalbody.jqxPanel({width: "100%", height: 350});
        modalbody.jqxPanel('append', me.gridEl[0]);

    };
    me.showBootStrapDialog = function (bodyContent) {
        var dialog = new BootstrapDialog({
            title: "Search New Site",
            type: BootstrapDialog.TYPE_SUCCESS,
            // size: BootstrapDialog.SIZE_SMALL,
            draggable: true,
            message: bodyContent,
            buttons: [
                {
                    label: 'Close',
                    action: function (dialogItself) {
                        dialogItself.close()
                    }
                },

            ]
        });
        dialog.realize();
        dialog.open();
    };
    me.createJqxGrid = function (gridEl, columns, source) {
        me.gridEl.jqxGrid({
            theme: 'light',
            source: source,
            sortable: true,
            enabletooltips: true,
            selectionmode: 'singlerow',
            columns: columns,
            columnsresize: true,
        });

    };
    me.schoolGridColumns = function () {
        var cols = [];
        cols.push({
            text: 'Emiscode',
            // width: 300,
            dataField: 'emiscode',
            cellsrenderer: function (row, column, value) {
                var url = 'http://schoolportal.punjab.gov.pk/census/SchCriteriaEmisCode.asp?myemiscode=' + value;
                return '<a target="_blank" href="' + url + '">' + value + '</a>';
            }
        });
        cols.push({
            text: 'School Name',
            // width: 300,
            dataField: 'school_nam'
        });
        cols.push({
            text: 'Gender',
            // width: 300,
            dataField: 'gender',
        });
        cols.push({
            text: 'Level',
            // width: 300,
            dataField: 'level',
        });

        return cols;
    }
    me.createFields = function (obj) {
        var arrFields = [];
        for (var key in obj) {
            arrFields.push({name: key, type: 'string'});
        }
        return arrFields;
    };
};