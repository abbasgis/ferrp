/**
 * Created by idrees on 11/6/2017.
 */

var ArzDataModel = function () {
    var me = this;
    me.nameValue = null;
    me.adminName = null;
    me.adminLevel = null;
    me.dataType = null;
    me.whereClause = null;
    me.globalFunctions = null;
    me.ptData = null;

    me.getDataPanel = function (gridData, level, value) {
        me.ptData = gridData;
        me.adminName = value;
        me.adminLevel = level;
        me.globalFunctions = new ArzGlobalFunctionsModel();
        var store = Ext.create('Ext.data.Store', {
            id: 'dataStore',
            fields: me.globalFunctions.getFieldsList(gridData[0]),
            data: gridData,
            // groupField: 'name'
        });
        var gridPanel = Ext.create('Ext.grid.Panel', {
            layout: 'fit',
            id: 'dataPanel',
            store: store,
            plugins: 'gridfilters',
            selModel: 'cellmodel',
            stripeRows: true,
            columnLines: true,
            titleAlign: 'center',
            title: 'Data Description',
            autoScroll: true,
            loadMask: true,
            listeners: {
                select: function (selModel, record, index, options) {
                    me.nameValue = record.data.name;
                },
                beforeshowtip: function (grid, tip, data) {
                    var cellNode = tip.pointerEvent.getTarget(tip.view.getCellSelector());
                    if (cellNode) {
                        data.colName = tip.view.headerCt.columnManager.getHeaderAtIndex(cellNode.cellIndex).text;
                    }
                }
            },
            tbar: [
                {
                    tooltip: 'Show pivot table',
                    text: 'PT',
                    cls:'btnPT',
                    handler: function () {
                        var ptData = gridPanel.getStore().data;
                        var gridData = me.globalFunctions.getDataFromGridItems(ptData);
                        me.globalFunctions.createPivotTableWindow(gridData);
                    }
                },'-',
                {
                    icon: imgPath + 'EXCLE.png',
                    tooltip: 'Export to Excel',
                    handler: function () {
                        // var gridData = gridPanel.getStore().config.data;
                        var data = gridPanel.getStore().data;
                        var exportData = me.globalFunctions.getDataFromGridItems(data);
                        alasql("SELECT * INTO XLSX('commanded_area_table.xlsx',{headers:true}) FROM ? ", [exportData]);
                    }
                }, '-', {
                    icon: imgPath + '15.png',
                    tooltip: 'Email data link',
                    handler: function () {
                        me.dataType = 'commanded_area';
                        me.whereClause = me.adminLevel + '=\'' + me.adminName + '\'';
                        var filtersArray = me.globalFunctions.getGridFiltersList(gridPanel);
                        // me.globalFunctions.getEmailForm(me.dataType, me.whereClause, filtersArray);
                        $("#dataType").val(me.dataType);
                        $("#whereClause").val(me.whereClause);
                        $("#filtersArray").val(filtersArray);
                        $('#eMailModal').modal('show');
                    }
                },
                {
                    icon: imgPath + '05.png',
                    tooltip: 'SMS data link',
                    handler: function () {
                        me.dataType = 'commanded_area';
                        me.whereClause = me.adminLevel + '=\'' + me.adminName + '\'';
                        var filtersArray = me.globalFunctions.getGridFiltersList(gridPanel);
                        // me.globalFunctions.getSMSForm(me.dataType, me.whereClause, filtersArray);
                        $("#dataType").val(me.dataType);
                        $("#whereClause").val(me.whereClause);
                        $("#filtersArray").val(filtersArray);
                        $('#smsModal').modal('show');
                    }
                }, '-',
                {
                    icon: imgPath + '04.png',
                    tooltip: 'Show districts information',
                    handler: function () {
                        if (me.nameValue) {
                            if (level != 'cca') {
                                var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
                                var url = 'admindistricts?level=' + level + '&value=' + me.nameValue;
                                Ext.Ajax.timeout = 900000;
                                Ext.Ajax.request({
                                    url: url,
                                    method: "GET",
                                    success: function (response) {
                                        box.hide();
                                        var respText = response.responseText;
                                        var respnseText = eval('(' + JXG.decompress(respText) + ')');
                                        if (respnseText != "false") {
                                            var data = respnseText;
                                            if (data.length > 0) {
                                                me.createDistrictsWindow(data);
                                            } else {
                                                Ext.MessageBox.alert("Warning", "No record found.");
                                            }
                                        }
                                    },
                                    failure: function (res) {
                                        box.hide();
                                    }
                                });
                            }

                        } else {
                            alert('Please select a row first.');
                        }
                    }
                }, '-'
            ],
            autoDestroy: true,
            columns: me.getCAColumnsList(me.adminLevel),
            features: [{
                id: 'group',
                ftype: 'groupingsummary',
                groupHeaderTpl: '{name}',
                hideGroupedHeader: true,
                enableGroupingMenu: true
            }, {
                ftype: 'summary',
                dock: 'bottom'
            }],
        });
        var dataPanel = Ext.getCmp("dataTableCA");
        dataPanel.removeAll();
        dataPanel.add(gridPanel);
    }

    me.getCAColumnsList = function (level) {
        var gridColumns = new ArzGridColumns();
        if (level == 'CCA') {
            return gridColumns.getCCAColumnsList(level);
        } else {
            return gridColumns.getCommandedAreaColumnsList(level);
        }
    }

    me.createDistrictsWindow = function (data) {
        var gridColumns = new ArzGridColumns();
        var store = Ext.create('Ext.data.Store', {
            id: 'distDataStore',
            fields: me.globalFunctions.getFieldsList(data[0]),
            data: data
        });

        var districtPanel = Ext.create('Ext.grid.Panel', {
            id: 'distDataPanel',
            store: store,
            stripeRows: true,
            columnLines: true,
            plugins: 'gridfilters',
            autoScroll: true,
            tbar: [
                {
                    // icon: imgPath + 'EXCLE.png',
                    tooltip: 'Show pivot table',
                    text: 'PT',
                    cls:'btnPT',
                    handler: function () {
                        var ptData = districtPanel.getStore().data;
                        var gridData = me.globalFunctions.getDataFromGridItems(ptData);
                        me.globalFunctions.createPivotTableWindow(gridData);
                    }
                }, '-',
                {
                    tooltip: 'Export to Excel',
                    icon: imgPath + 'EXCLE.png',
                    handler: function () {
                        var data = districtPanel.getStore().data;
                        var exportData = me.globalFunctions.getDataFromGridItems(data);
                        alasql("SELECT * INTO XLSX('district_table.xlsx',{headers:true}) FROM ? ", [exportData]);
                    }
                }, '-', {
                    icon: imgPath + '15.png',
                    tooltip: 'Email data link',
                    handler: function () {
                        me.dataType = 'district';
                        me.whereClause = me.adminLevel + "='" + me.nameValue + "'";
                        var filtersArray = me.globalFunctions.getGridFiltersList(districtPanel);
                        // me.globalFunctions.getEmailForm(me.dataType, me.whereClause, filtersArray);
                        $("#dataType").val(me.dataType);
                        $("#whereClause").val(me.whereClause);
                        $("#filtersArray").val(filtersArray);
                        $('#eMailModal').modal('show');
                    }
                },
                {
                    icon: imgPath + '05.png',
                    tooltip: 'SMS data link',
                    handler: function () {
                        me.dataType = 'district';
                        me.whereClause = me.adminLevel + "='" + me.nameValue + "'";
                        var filtersArray = me.globalFunctions.getGridFiltersList(districtPanel);
                        // me.globalFunctions.getSMSForm(me.dataType, me.whereClause, filtersArray);
                        $("#dataType").val(me.dataType);
                        $("#whereClause").val(me.whereClause);
                        $("#filtersArray").val(filtersArray);
                        $('#smsModal').modal('show');
                    }
                }],
            columns: gridColumns.getCommandedAreaDistrictsColumnsList(me.adminLevel),
            features: [{
                id: 'group',
                ftype: 'groupingsummary',
                groupHeaderTpl: '{name}',
                hideGroupedHeader: true,
                enableGroupingMenu: true
            }, {
                ftype: 'summary',
                dock: 'bottom'
            }],
        });
        var dataPanel = Ext.getCmp("pnlDistrictsInformation");
        dataPanel.removeAll();
        dataPanel.add(districtPanel);
        var chartsTab = Ext.getCmp("tabChartsPanel");
        chartsTab.setActiveTab(3);
    }

    me.getComboStore = function (storeId) {
        var fieldStore = Ext.create('Ext.data.Store', {
            fields: [
                {name: 'id', type: 'string'},
                {name: 'name', type: 'string'}
            ],
            id: storeId,
            data: []
        });
        return fieldStore;
    }

}

var ArzChartModel = function () {
    var me = this;
    me.canalsBarChart = null;
    me.commandedAreaBarChart = null;
    me.outletsChart = null;

    me.createBarChart = function (data, xLabel) {
        var chartPanel = Ext.getCmp("dataChartPanel");
        chartPanel.removeAll();
        var chartDiv = chartPanel.body.dom;
        var commandedAreaName = me.commandedAreaNamesList(data);
        var chartData = me.createChartData(data);
        me.commandedAreaBarChart = Highcharts.chart(chartDiv, {
            chart: {
                type: 'column'
            },
            title: {
                text: xLabel
            },
            credits: {
                enabled: false
            },
            xAxis: {
                categories: commandedAreaName
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle',
                floating: false
            },
            yAxis: {
                min: 0,
                title: {
                    text: ''
                }
            },
            tooltip: {
                headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                pointFormat: '<tr><td style="color:{series.color};padding:0; font-size:10px;">{series.name}: </td>' +
                '<td style="padding:0; font-size:10px;"><b>{point.y:.1f}</b></td></tr>',
                footerFormat: '</table>',
                shared: true,
                useHTML: true
            },
            plotOptions: {
                column: {
                    pointPadding: 0.2,
                    borderWidth: 5
                }
            },
            series: chartData
        });

        me.createCanalsChart(data, xLabel);
        me.getOutletsChart(data, xLabel);

    }

    me.commandedAreaNamesList = function (data) {
        var namesList = new Array();
        for (var i = 0; i < data.length; i++) {
            var name = data[i].name;
            var recordData = [name];
            namesList.push(recordData);
        }
        return namesList;
    }
    me.createChartData = function (data) {
        var dataList = new Array();
        var gcaList = [];
        var ccaList = [];
        var gcaGeomList = [];
        var ccaGeomList = [];
        var gca = "GCA";
        var cca = "CCA";
        var gca_geom = "GCA Shape";
        var cca_geom = "CCA Shape";
        for (var i = 0; i < data.length; i++) {
            var gcaData = data[i].gca_ma;
            var ccaData = data[i].cca_ma;
            var gcaGeomData = data[i].gca_geom_ma;
            var ccaGeomData = data[i].cca_geom_ma;
            gcaList.push(gcaData);
            ccaList.push(ccaData);
            gcaGeomList.push(gcaGeomData);
            ccaGeomList.push(ccaGeomData);
        }
        var recordGCA = {name: gca, data: gcaList};
        var recordCCA = {name: cca, data: ccaList};
        var recordGCAGeom = {name: gca_geom, data: gcaGeomList};
        var recordCCAGeom = {name: cca_geom, data: ccaGeomList};
        dataList.push(recordGCA);
        dataList.push(recordCCA);
        dataList.push(recordGCAGeom);
        dataList.push(recordCCAGeom);
        return dataList;
    }

    me.createCanalsChart = function (data, xLabel) {
        var canalsChartPanel = Ext.getCmp("canalsChartPanel");
        canalsChartPanel.removeAll();
        var canalsChartDiv = canalsChartPanel.body.dom;
        var canalNames = me.canalsNameList(data);
        var chartData = me.createCanalsChartData(data);
        me.canalsBarChart = Highcharts.chart(canalsChartDiv, {
            chart: {
                type: 'column'
            },
            title: {
                text: xLabel
            },
            credits: {
                enabled: false
            },
            xAxis: {
                categories: canalNames
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle',
                floating: false
            },
            yAxis: {
                min: 0,
                title: {
                    text: ''
                }
            },
            tooltip: {
                headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                pointFormat: '<tr><td style="color:{series.color};padding:0; font-size:10px;">{series.name}: </td>' +
                '<td style="padding:0; font-size:10px;"><b>{point.y:.1f}</b></td></tr>',
                footerFormat: '</table>',
                shared: true,
                useHTML: true
            },
            plotOptions: {
                column: {
                    pointPadding: 0.2,
                    borderWidth: 5
                }
            },
            series: chartData
        });
    }
    me.canalsNameList = function (data) {
        var namesList = new Array();
        for (var i = 0; i < data.length; i++) {
            var name = data[i].name;
            var recordData = [name];
            namesList.push(recordData);
        }
        return namesList;
    }
    me.createCanalsChartData = function (data) {
        var dataList = new Array();
        var countList = [];
        var shapeCountList = [];
        var name = "Length";
        var shapeName = 'Shape Length';

        for (var i = 0; i < data.length; i++) {
            var length = data[i].length;
            var shapeLength = data[i].shape_length;
            countList.push(length);
            shapeCountList.push(shapeLength);
        }
        var recordLength = {name: name, data: countList};
        var recordShapeLengthLength = {name: shapeName, data: shapeCountList};
        dataList.push(recordLength);
        dataList.push(recordShapeLengthLength);
        return dataList;
    }

    me.getOutletsChart = function (data, xLabel) {
        var chartPanel = Ext.getCmp("outletsChartPanel");
        chartPanel.removeAll();
        var chartDiv = chartPanel.body.dom;
        var canalNames = me.canalsNameList(data);
        var outletsData = me.createOutletsChartData(data);
        me.outletsChart = Highcharts.chart(chartDiv, {
            chart: {
                type: 'column'
            },
            title: {
                text: xLabel
            },
            credits: {
                enabled: false
            },
            xAxis: {
                categories: canalNames
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle',
                floating: false
            },
            yAxis: {
                min: 0,
                title: {
                    text: ''
                }
            },
            tooltip: {
                headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                pointFormat: '<tr><td style="color:{series.color};padding:0; font-size:10px;">{series.name}: </td>' +
                '<td style="padding:0; font-size:10px;"><b>{point.y:.1f}</b></td></tr>',
                footerFormat: '</table>',
                shared: true,
                useHTML: true
            },
            plotOptions: {
                column: {
                    pointPadding: 0.2,
                    borderWidth: 5
                }
            },
            series: outletsData
        });

    }
    me.createOutletsChartData = function (data) {
        var dataList = new Array();
        var outletsList = [];
        var name = "Outlets";

        for (var i = 0; i < data.length; i++) {
            var outlets = data[i].outlets;
            outletsList.push(outlets);
        }
        var recordOutlets = {name: name, data: outletsList};
        dataList.push(recordOutlets);
        return dataList;
    }


}
