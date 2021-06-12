/**
 * Created by idrees on 12/20/2017.
 */
var llMap = null;
var ArzDamsMapModel = function () {
    var me = this;
    me.geoJson = null;
    me.getMapAndTable = function () {
        var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
        var url = '../damsdata';
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
                    var jsonData = data.damsData;//JSON.parse(data.damsData);
                    var geoJsonData = JSON.parse(data.damsGeoJson);
                    var arzMapModel = new ArzLeafletDamsMapModel();
                    arzMapModel.getDamsDataPanel(jsonData);
                    arzMapModel.getLeafletMapPanel();
                    me.geoJson = geoJsonData[0].geojson;
                    arzMapModel.createLeafletMap(JSON.stringify(me.geoJson));
                }
            },
            failure: function (res) {
                box.hide();
            }
        });
    }
}

var ArzLeafletDamsMapModel = function () {
    var me = this;
    me.marker = null;
    me.pointSelectionsLayer = null;
    me.pointSelectionSource = null;
    me.irrigationDams = null;
    me.damsGeoJson = null;
    me.globalFunctions = null;
    me.whereClause = null;
    me.dataType = null;
    me.headWork = [];
    me.win = null;
    me.dischargeYearWin = null;
    me.hydroGraph = null;
    me.hwDischargeData = null;
    me.comparisonHydrograph = null;
    me.comparisonHydrographData = new Array();
    me.selectionSet = null;
    me.selectionLayer = null;
    me.gridSelectionModel = null;

    me.getLeafletMapPanel = function () {
        me.globalFunctions = new ArzGlobalFunctionsModel();
        var mapPanel = Ext.create('Ext.panel.Panel', {
            xtype: 'panel',
            headerCls: 'extPanel',
            id: 'damsLLMap',
            layout: 'fit',
            flex: 1,
            margin: '0 0 0 0',
            tbar: [
                {
                    icon: '/static/ferrp/img/irrigation/arrow_refresh.png',
                    handler: function () {
                        llMap.invalidateSize();
                    }
                }, {
                    icon: '/static/ferrp/img/irrigation/Clear.png',
                    tooltip: 'Clear Selection',
                    handler: function () {
                        me.clearAllSelection();
                    }
                }, {
                    icon: '/static/ferrp/img/irrigation/03.png',
                    tooltip: 'Select discharge for symbology.',
                    handler: function () {
                        me.getDischargeYearForm();
                    }
                },
                // Ext.create('Ext.form.ComboBox', {
                //     store: me.getYearStore(),
                //     id: 'cmbDischargeYear',
                //     queryMode: 'local',
                //     emptyText:'<--Discharge Year-->',
                //     // width:100,
                //     displayField: 'name',
                //     valueField: 'id',
                //     listeners: {
                //         select: function (cmb, value) {
                //             var id = value.data.name;
                //             var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
                //             var url = "../updatedischarge?year=" + id;
                //                 Ext.Ajax.timeout = 900000;
                //                 Ext.Ajax.request({
                //                     url: url,
                //                     method: "GET",
                //                     success: function (response) {
                //                         box.hide();
                //                         var respnseText = response.responseText;
                //                         if (respnseText != "false") {
                //                             var data = JSON.parse(respnseText);
                //                             var jsonData = JSON.parse(data.damsData);
                //                             var geoJsonData = JSON.parse(data.damsGeoJson);
                //                             me.damsGeoJson = JSON.stringify(geoJsonData[0].geojson);
                //                             me.irrigationDams.clearLayers();
                //                             me.irrigationDams.addData(geoJsonData[0].geojson);
                //                         }
                //                     },
                //                     failure: function (res) {
                //                         box.hide();
                //                     }
                //                 });
                //         }
                //     }
                // })
            ]
        });
        var dataPanel = Ext.getCmp("pnlDamsLLMap");
        dataPanel.removeAll();
        dataPanel.add(mapPanel);
    }

    me.createLeafletMap = function (geoJson) {
        me.globalFunctions = new ArzGlobalFunctionsModel();
        me.damsGeoJson = geoJson;
        var damsDiv = Ext.getCmp('damsLLMap').body.dom;
        llMap = L.map(damsDiv, {zoomControl: false}).setView([29.5, 71.6], 6);
        var zoom_bar = new L.Control.ZoomBar({position: 'topleft'}).addTo(llMap);
        me.irrigationDams = L.geoJSON(JSON.parse(me.damsGeoJson),
            {
                onEachFeature: me.onEachFeature,
                pointToLayer: function (feature, latlng) {
                    return L.circleMarker(latlng, me.getDamStyle(feature));
                }
            }).addTo(llMap);
        // var pointsArray = me.getHeatMapData(JSON.parse(me.damsGeoJson));
        // var heat = L.heatLayer(pointsArray,{
        //     radius: 20,
        //     blur: 15,
        //     maxZoom: 17,
        // }).addTo(llMap);
        me.googleRoadMap = L.gridLayer.googleMutant({
            maxZoom: 24,
            type: 'roadmap'
        }).addTo(llMap);
        me.googleSatelliteMap = L.gridLayer.googleMutant({
            maxZoom: 24,
            type: 'satellite'
        });
        me.googleTerrainMap = L.gridLayer.googleMutant({
            type: 'terrain'
        });
        L.control.layers(
            {
                Roadmap: me.googleRoadMap,
                Aerial: me.googleSatelliteMap,
                Terrain: me.googleTerrainMap
            }, {
                "Head Works": me.irrigationDams,
                // "Heat Map": heat
            },
            {
                collapsed: true
            }).addTo(llMap);

        me.selectionLayer = new L.geoJSON(me.geojsonObject, {
            pointToLayer: function (feature, latlng) {
                return L.circleMarker(latlng, me.selectionStyleFunction(feature));
            }
        });
        llMap.addLayer(me.selectionLayer);

    }

    me.onEachFeature = function (feature, layer) {
        layer.on({
            click: me.getAttributeForm
        });
    }
    me.getAttributeForm = function (e) {
        var props = e.target.feature.properties;
        var popupContent = '';
        if (props) {
            var popupContent = '<b>Headwork      :</b>' + props.dam_name + '</br>';
            popupContent = popupContent + '<b>River         :</b>' + props.river + '</br>'
            popupContent = popupContent + '<b>Catchment Area:</b>' + props.catch_skm + '</br>'
            popupContent = popupContent + '<b>Discharge     :</b>' + props.discharge + '</br>'
            this.bindPopup(popupContent);
            me.selectHighlightGridRow('damsDataPanel', 'dam_name', props.dam_name);
        }
    }

    me.selectHighlightGridRow = function (gridId, fieldName, fieldValue) {
        var grid = Ext.getCmp(gridId);
        var targetRowIndex = grid.store.find(fieldName, fieldValue);
        var row = grid.getView().getRow(targetRowIndex);
        Ext.get(row).highlight();
        grid.getView().focusRow(row);
        grid.getSelectionModel().select(targetRowIndex);
    }

    me.geojsonObject = {
        'type': 'FeatureCollection',
        'features': [{
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [0, 0]
            }
        }]
    };

    me.selectionStyleFunction = function (feature) {
        var type = feature.geometry.type;
        switch (type) {
            case 'Point':
                return {
                    radius: 12,
                    fillColor: '#ffff00',
                    color: "#ffff00",
                    weight: 2,
                    opacity: 0.8,
                    fillOpacity: 1,
                };
            case 'LineString':
                return {
                    color: '#ffff00',
                    weight: 10,
                    opacity: 0.7,
                    lineJoin: 'round',
                };
            case 'MultiLineString':
                return {
                    color: '#ffff00',
                    weight: 10,
                    opacity: 0.7,
                    lineJoin: 'round',
                };
        }
    };

    me.getDamStyle = function (feature) {
        return {
            radius: 12, //me.getDamSize(feature.properties.discharge),
            fillColor: me.getDamColor(feature.properties.discharge),
            color: "white",
            weight: 2,
            opacity: 1,
            fillOpacity: 0.8,
        };
    }

    me.getDamSize = function (discharge) {
        var geojson = JSON.parse(me.damsGeoJson);
        if (discharge != null) {
            var max = me.globalFunctions.geoJsonAttributeMax(geojson.features, 'discharge');
            var damSize = parseInt((discharge / max) * 255);
            // if(damSize <= 5){
            //     return 5
            // }else {
            return damSize;
            // }
        } else {
            return 255;
        }
    }
    me.getCyanToBlue = function (percent) {
        b = percent < 50 ? 255 : Math.floor(255 - (percent * 2 - 100) * 255 / 100);
        g = percent > 50 ? 255 : Math.floor((percent * 2) * 255 / 100);
        return 'rgb(0,' + g + ',' + b + ')';
    }
    me.getColor = function (value) {
        var hue = ((1 - value) * 120).toString(10);
        return ["hsl(", hue, ",100%,100%)"].join("");
    }

    me.getBlueColor = function (value) {
        return 'rgb(0,' + (value) + ',' + value + ')';
    }
    me.getDamColor = function (discharge) {
        var size = me.getDamSize(discharge);
        return me.getBlueColor(size);
    }

    me.getHeatMapData = function (geoJson) {
        return geoJson.features.map(function (feature) {
            return [
                feature.geometry.coordinates[1],
                feature.geometry.coordinates[0],
                feature.properties['discharge'] == null ? 0 : feature.properties['discharge']
            ];
        });
    }

    me.drawLineOnMap = function (record) {
        var geojsonText = record.data.geojson;
        var geojson = JSON.parse(geojsonText);
        var coordList = geojson.coordinates;
        var damIcon = L.icon({
            iconUrl: '/static/ferrp/img/irrigation/flashmarker.gif',
            iconSize: [10, 10], // size of the icon
        });
        me.marker = L.marker([coordList[1], coordList[0]], {icon: damIcon}).addTo(llMap);
    }

    me.setMapExtents = function (minx, miny, maxx, maxy) {
        var southWest = L.latLng(miny, minx),
            northEast = L.latLng(maxy, maxx),
            bounds = L.latLngBounds(southWest, northEast);
        llMap.fitBounds(bounds, {padding: [10, 10]});
    }

    me.reMoveLayer = function (layer) {
        if (layer) {
            llMap.removeLayer(layer);
        }
    }

    me.clearAllSelection = function () {
        if (me.selectionLayer) {
            me.selectionLayer.clearLayers();
        }
        if (me.marker) {
            llMap.removeLayer(me.marker);
        }
        var grid = Ext.getCmp('damsDataPanel');
        grid.getSelectionModel().deselectAll();
        grid.filters.clearFilters();
    }

    // Data panel functions
    me.getDamsDataPanel = function (data) {
        var gridColumns = new ArzGridColumns();
        var store = Ext.create('Ext.data.Store', {
            id: 'damsDataStore',
            fields: me.getFieldsList(data[0]),
            data: data
        });
        var gridPanel = Ext.create('Ext.grid.Panel', {
            layout: 'fit',
            id: 'damsDataPanel',
            title: 'Headworks and Barrages',
            titleAlign: 'center',
            store: store,
            stripeRows: true,
            multiSelect: true,
            columnLines: true,
            plugins: 'gridfilters',
            autoScroll: true,
            loadMask: true,
            listeners: {
                select: function (selModel, record, index, options) {
                    me.selectionLayer.clearLayers();
                    me.selectionSet = [];
                    me.headWork = [];
                    if (selModel.selected.items.length > 1) {
                        for (key in selModel.selected.items) {
                            var row = selModel.selected.items[key];
                            me.headWork.push(row.data.dam_name);
                            var geojson = JSON.parse(row.data.geojson);
                            me.selectionSet.push({
                                "type": "Feature",
                                "properties": row.data,
                                "geometry": geojson
                            });
                        }
                        me.selectionLayer.addData({type: 'FeatureCollection', features: me.selectionSet});
                    } else {
                        me.headWork.push(record.data.dam_name);
                        var geojson = JSON.parse(record.data.geojson);
                        me.selectionSet.push({
                            "type": "Feature",
                            "properties": record.data,
                            "geometry": geojson
                        });
                        me.selectionLayer.addData({type: 'FeatureCollection', features: me.selectionSet});
                    }
                },
                beforeitemcontextmenu: function (view, record, item, index, e) {
                    e.stopEvent();
                    me.contextMenu(record).showAt(e.getXY());
                },
                filterchange: function (store, filters, eOpts) {
                    if (filters.length > 0) {
                        gridPanel.getSelectionModel().selectAll();
                    } else {
                        me.selectionLayer.clearLayers();
                        gridPanel.getSelectionModel().deselectAll();
                    }
                },
            },
            autoDestroy: true,
            tbar: [
                {
                    tooltip: 'Show pivot table',
                    text: 'PT',
                    cls: 'btnPT',
                    handler: function () {
                        var ptData = gridPanel.getStore().data;
                        var gridData = me.globalFunctions.getDataFromGridItems(ptData);
                        me.globalFunctions.createPivotTableWindow(gridData);
                    }
                }, '-',
                {
                    tooltip: 'Export to Excel',
                    icon: imgPath + 'EXCLE.png',
                    handler: function () {
                        // var gridData = gridPanel.getStore().config.data;
                        var data = gridPanel.getStore().data;
                        var exportData = me.globalFunctions.getDataFromGridItems(data);
                        alasql("SELECT * INTO XLSX('headworks_barrages_table.xlsx',{headers:true}) FROM ? ", [exportData]);
                    }
                }, '-',
                {
                    icon: imgPath + '15.png',
                    tooltip: 'email data link',
                    handler: function () {
                        me.dataType = 'dams';
                        me.whereClause = 'null';
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
                        me.dataType = 'dams';
                        me.whereClause = 'null';
                        var filtersArray = me.globalFunctions.getGridFiltersList(gridPanel);
                        // me.globalFunctions.getSMSForm(me.dataType, me.whereClause, filtersArray);
                        $("#dataType").val(me.dataType);
                        $("#whereClause").val(me.whereClause);
                        $("#filtersArray").val(filtersArray);
                        $('#smsModal').modal('show');
                    }
                },
                {
                    icon: imgPath + 'discharge.png',
                    tooltip: 'Get discharge data',
                    handler: function () {
                        if (me.headWork) {
                            me.getHeadWorkData(me.headWork);
                        } else {
                            Ext.MessageBox.alert("Warning", "Please select a record first.");
                        }
                    }
                },
                '-', {
                    tooltip: 'Select All',
                    icon: imgPath + 'select_all_16.png',
                    iconMask: true,
                    handler: function () {
                        gridPanel.getSelectionModel().selectAll();
                    }
                }, {
                    tooltip: 'De-Select All',
                    icon: imgPath + 'deselect_all_16.png',
                    iconMask: true,
                    handler: function () {
                        me.clearAllSelection();
                        // gridPanel.getSelectionModel().deselectAll();
                    }
                }, '-',
            ],
            columns: gridColumns.getHeadWorkColumnsList(),
            features: [{
                id: 'group',
                ftype: 'groupingsummary',
                groupHeaderTpl: '{name}',
                hideGroupedHeader: false,
                enableGroupingMenu: true
            }, {
                ftype: 'summary',
                dock: 'bottom'
            }],
        });
        var dataPanel = Ext.getCmp("pnlDamsData");
        dataPanel.removeAll();
        dataPanel.add(gridPanel);
    }

    me.getDischargeDataPanel = function (data, title) {
        var gridColumns = new ArzGridColumns();
        var store = Ext.create('Ext.data.Store', {
            id: 'dischargeDataStore',
            fields: me.getFieldsList(data[0]),
            data: data
        });
        var dischargePanel = Ext.create('Ext.grid.Panel', {
            layout: 'fit',
            id: 'dischargeDataPanel',
            titleAlign: 'center',
            // title: title + ' Discharge data',
            store: store,
            stripeRows: true,
            columnLines: true,
            plugins: 'gridfilters',
            autoScroll: true,
            loadMask: true,
            tbar: [
                {
                    tooltip: 'Show pivot table',
                    text: 'PT',
                    cls: 'btnPT',
                    handler: function () {
                        var ptData = dischargePanel.getStore().data;
                        var gridData = me.globalFunctions.getDataFromGridItems(ptData);
                        me.globalFunctions.createPivotTableWindow(gridData);
                    }
                }, '-',
                {
                    tooltip: 'Export to Excel',
                    icon: imgPath + 'EXCLE.png',
                    handler: function () {
                        // var gridData = dischargePanel.getStore().config.data;
                        var data = dischargePanel.getStore().data;
                        var exportData = me.globalFunctions.getDataFromGridItems(data);
                        alasql("SELECT * INTO XLSX('data_table.xlsx',{headers:true}) FROM ? ", [exportData]);
                    }
                }, '-',
                {
                    icon: imgPath + '15.png',
                    tooltip: 'EMail data link',
                    handler: function () {
                        me.dataType = 'discharge';
                        me.whereClause = "head_works='" + me.headWork + "'";
                        var filtersArray = me.globalFunctions.getGridFiltersList(dischargePanel);
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
                        me.dataType = 'discharge';
                        me.whereClause = "head_works='" + me.headWork + "'";
                        var filtersArray = me.globalFunctions.getGridFiltersList(dischargePanel);
                        // me.globalFunctions.getSMSForm(me.dataType, me.whereClause, filtersArray);
                        $("#dataType").val(me.dataType);
                        $("#whereClause").val(me.whereClause);
                        $("#filtersArray").val(filtersArray);
                        $('#smsModal').modal('show');
                    }
                },
                {
                    icon: imgPath + '03.png',
                    tooltip: 'Show hydro graph',
                    handler: function () {
                        var tableData = dischargePanel.getStore().config.data;
                        var hydrographData = me.getHydroGraphDataArray(tableData);
                        me.getDamHydroGraph(hydrographData, me.headWork);
                    }
                }],
            listeners: {
                select: function (selModel, record, index, options) {
                }
            },
            autoDestroy: true,
            columns: gridColumns.getHeadWorkDischargeColumnsList(),
            features: [{
                id: 'group',
                ftype: 'groupingsummary',
                groupHeaderTpl: '{name}',
                hideGroupedHeader: false,
                enableGroupingMenu: true
            }, {
                ftype: 'summary',
                dock: 'bottom'
            }],
        });
        var dataPanel = Ext.getCmp("pnlDischargeData");
        dataPanel.removeAll();
        dataPanel.add(dischargePanel);
        var southPanel = Ext.getCmp('southDischargePanel');
        southPanel.expand();
        southPanel.setTitle(me.headWork + ' Discharge Data');
    }

    me.getDamHydroGraph = function (data, title) {
        me.comparisonHydrographData = new Array();

        if (me.win != null) {
            me.win.destroy();
        }
        me.win = Ext.create('Ext.window.Window', {
            id: 'hydroGraphWin',
            title: title + ' Hydrograph',
            layout: 'fit',
            x: 100,
            y: 90,
            width: '60%',
            height: 400,
            frame: true,
            closeAction: 'destroy',
            preventBodyReset: true,
            resizable: false,
            constrainHeader: true,
            collapsible: false,
            plain: true,
            items: [
                Ext.create('Ext.panel.Panel', {
                    layout: 'fit',
                    items: [
                        Ext.create('Ext.tab.Panel', {
                            tabPosition: 'bottom',
                            activeTab: 0,
                            layout: 'fit',
                            id: 'tabHydrograph',
                            name: 'tabHydrograph',
                            items: [
                                {
                                    title: 'Hydrograph Query',
                                    layout: 'fit',
                                    border: false,
                                    items: [
                                        {
                                            xtype: 'panel',
                                            id: 'pnlDamHydroGraph',
                                            border: false,
                                        }]
                                },
                                {
                                    title: 'Hydrograph Comparison',
                                    layout: 'fit',
                                    border: false,
                                    items: [
                                        {
                                            xtype: 'panel',
                                            id: 'pnlDamHydroGraphComparison',
                                            border: false,
                                            tbar: [
                                                {
                                                    xtype: 'combo',
                                                    emptyText: '<--Select Dam/Headwork-->',
                                                    id: 'cmbDamHeadwork',
                                                    name: 'cmbDamHeadwork',
                                                    valueField: 'dam_name',
                                                    displayField: 'dam_name',
                                                    margin: '0 0 0 10'
                                                },
                                                {
                                                    xtype: 'datefield',
                                                    fieldLabel: 'From(mm/dd/yyyy)',
                                                    labelWidth: 105,
                                                    id: 'dtFromComparisonDischarge',
                                                    name: 'dtFromComparisonDischarge',
                                                    margin: '0 0 0 10'
                                                },
                                                {
                                                    xtype: 'datefield',
                                                    fieldLabel: 'To(mm/dd/yyyy)',
                                                    labelWidth: 90,
                                                    id: 'dtToComparisonDischarge',
                                                    name: 'dtToComparisonDischarge',
                                                    margin: '0 0 0 10'
                                                },
                                                {
                                                    xtype: 'button',
                                                    text: 'Add to Graph',
                                                    margin: '0 0 0 10',
                                                    handler: function () {
                                                        var fromDate = Ext.getCmp('dtFromComparisonDischarge').getValue();
                                                        var toDate = Ext.getCmp('dtToComparisonDischarge').getValue();
                                                        if (fromDate && toDate) {
                                                            if (fromDate.getFullYear() == toDate.getFullYear()) {
                                                                var fDate = fromDate.getFullYear() + fromDate.getMonth() + fromDate.getDay();
                                                                var tDate = toDate.getFullYear() + toDate.getMonth() + toDate.getDay();
                                                                var damName = Ext.getCmp('cmbDamHeadwork').getRawValue();
                                                                if (fromDate > toDate || fDate == tDate) {
                                                                    Ext.MessageBox.alert("Error", "'From' date must be earlier than 'To' date. And Dates should not be same.");
                                                                } else {
                                                                    me.redrawComparisonHydrograph(damName, fromDate, toDate);
                                                                }
                                                            } else {
                                                                Ext.MessageBox.alert("Error", "To from Years must be same.");
                                                            }
                                                        }
                                                    }
                                                },
                                                {
                                                    xtype: 'button',
                                                    text: 'New Graph',
                                                    margin: '0 0 0 10',
                                                    handler: function () {
                                                        var seriesLength = me.comparisonHydrograph.series.length;
                                                        for (var i = seriesLength - 1; i > -1; i--) {
                                                            me.comparisonHydrograph.series[i].remove();
                                                        }
                                                    }
                                                }
                                            ]
                                        }]
                                }]
                        }),
                    ]
                }),
            ]
        });

        me.win.show();
        var chartsTab = Ext.getCmp("tabHydrograph");
        chartsTab.setActiveTab(1);
        chartsTab.setActiveTab(0);

        function createHydroGraph() {
            me.hydroGraph = null;
            var hydroGraphDiv = Ext.getCmp('pnlDamHydroGraph').body.dom;
            me.hydroGraph = Highcharts.chart(hydroGraphDiv, {
                chart: {
                    zoomType: 'x'
                },
                title: {
                    text: 'Water Discharge over time'
                },
                subtitle: {
                    text: document.ontouchstart === undefined ?
                        'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
                },
                xAxis: {
                    type: 'datetime'
                },
                yAxis: {
                    title: {
                        text: 'Discharge(cusecs)'
                    }
                },
                legend: {
                    enabled: true
                },
                plotOptions: {
                    area: {
                        fillColor: {
                            linearGradient: {
                                x1: 0,
                                y1: 0,
                                x2: 0,
                                y2: 1
                            },
                            stops: [
                                [0, Highcharts.getOptions().colors[0]],
                                [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                            ]
                        },
                        marker: {
                            radius: 2
                        },
                        lineWidth: 1,
                        states: {
                            hover: {
                                lineWidth: 1
                            }
                        },
                        threshold: null
                    }
                },
                series: data,
                // series: [{
                //     type: 'area',
                //     name: 'Discharge',
                //     data: data
                // }]
            });
        }

        function createComparisonHydrograph() {
            var comparisonGraphDiv = Ext.getCmp('pnlDamHydroGraphComparison').body.dom;
            me.comparisonHydrograph = Highcharts.chart(comparisonGraphDiv, {
                chart: {
                    zoomType: 'x',
                    type: 'spline'
                },
                title: {
                    text: 'Water discharge comparison over time'
                },
                xAxis: {
                    type: 'datetime'
                },
                yAxis: {
                    title: {
                        text: 'Discharge(cusecs)'
                    }
                },
                plotOptions: {
                    area: {
                        fillColor: {
                            linearGradient: {
                                x1: 0,
                                y1: 0,
                                x2: 0,
                                y2: 1
                            },
                            stops: [
                                [0, Highcharts.getOptions().colors[0]],
                                [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                            ]
                        },
                        marker: {
                            radius: 2
                        },
                        lineWidth: 1,
                        states: {
                            hover: {
                                lineWidth: 1
                            }
                        },
                        threshold: null
                    }
                },
                series: me.comparisonHydrographData
            });
        }

        createHydroGraph();
        createComparisonHydrograph();
        me.populateHeadworksCombo();
    }

    me.populateHeadworksCombo = function () {
        var selectedHeadworks = Ext.getCmp('damsDataPanel').getSelectionModel().selected.items;
        function getComboStore() {
            var storeItems = [];
            for (var i = 0; i < selectedHeadworks.length; i++) {
                var record = selectedHeadworks[i].data;
                storeItems.push(record);
            }
            var fieldsList = [];
            for(var key in selectedHeadworks[0].data){
                fieldsList.push(key);
            }
            var damStore = Ext.create('Ext.data.Store', {
                fields: fieldsList,
                data: storeItems
            });
            return damStore;
        }
        var damStore = getComboStore();
        var cmbDamHeadwork = Ext.getCmp('cmbDamHeadwork');
        cmbDamHeadwork.bindStore(damStore);
        cmbDamHeadwork.setRawValue(selectedHeadworks[0].data.dam_name);
    }


    me.getHydroGraphDataArray = function (data) {
        var groupByData = _.groupBy(data, 'head_works')
        var graphData = [];
        for (var key in groupByData) {
            // alert(key);
            var damData = groupByData[key];
            var profileArray = new Array();
            for (var i = 0; i < damData.length; i++) {
                var record = new Array();
                var unix_date = Date.parse(damData[i].discharge_date);
                record.push(unix_date);
                record.push(damData[i].us);
                profileArray.push(record);
            }
            graphData.push({type: 'area', name: key + ' Discharge', data: profileArray})
        }
        return graphData;
    }

    me.getComparisonHydrographDataArray = function (data) {
        var profileArray = new Array();
        for (var i = 0; i < data.length; i++) {
            var record = new Array();
            var discharge_date = data[i].discharge_date;
            discharge_date = discharge_date.replace(discharge_date.split('-')[0], '2016');
            var unix_date = Date.parse(discharge_date);
            record.push(unix_date);
            record.push(data[i].us);
            profileArray.push(record);
        }
        return profileArray;
    }

    me.getColumnsList = function (data) {
        var columns = [];
        var stringType = "string";
        var numberType = 'number';
        for (var key in data) {
            if (key === "extent" || key === "geojson" || key === "id") {
            }
            else {
                if (isNaN(parseFloat(data[key]))) {
                    columns.push({
                        dataIndex: key,
                        text: key,
                        flex: 1,
                        exportStyle: {
                            alignment: {
                                horizontal: 'Right'
                            },
                            font: {
                                bold: true
                            },
                            format: 'Text'
                        },
                        filter: {
                            type: stringType,
                            itemDefaults: {
                                emptyText: 'Search for...'
                            }
                        }
                    })
                } else {
                    columns.push({
                        dataIndex: key,
                        text: key,
                        flex: 1,
                        filter: numberType,
                        exportStyle: {
                            alignment: {
                                horizontal: 'Right'
                            },
                            font: {
                                bold: true
                            }
                        }
                    })
                }

            }
        }
        return columns;
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

    me.getFieldsList = function (data) {
        var arrField = new Array();
        for (var key in data) {
            var obj = {};
            if (key === "extent" || key === "geojson") {
            } else {
                obj.id = key;
                obj.name = key;
                arrField.push(obj);
            }
        }
        return arrField;
    }

    me.contextMenu = function (record) {
        var contextMenu = Ext.create('Ext.menu.Menu', {
            items: [
                {
                    text: 'Zoom to feature',
                    handler: function () {
                        var extent = record.data.extent;
                        var arrExtent = extent.split(',');
                        var minx = parseFloat(arrExtent[0]);
                        var miny = parseFloat(arrExtent[1]);
                        var maxx = parseFloat(arrExtent[2]);
                        var maxy = parseFloat(arrExtent[3]);
                        me.setMapExtents(minx, miny, maxx, maxy);
                    }
                },
                {
                    text: 'Get Discharge Data',
                    handler: function () {
                        var head = record.data.dam_name;
                        me.getHeadWorkData(head);
                    }
                }
            ]
        });
        return contextMenu;
    }

    me.redrawDischargeHydrograph = function (fromDate, toDate) {
        // var data = me.getHeadWorkToFromDischargeData(headwork, fromDate, toDate);
        var data = me.getDischargeDateDataFromRange(damName, fromDate, toDate);
        var hydroGraphData = me.getHydroGraphDataArray(data);
        me.hydroGraph.series[0].setData(null, true);
        me.hydroGraph.series[0].setData(hydroGraphData, true);
        me.hydroGraph.redraw();
    }

    me.redrawComparisonHydrograph = function (damName, fromDate, toDate) {
        var datasetName = damName + '-' + fromDate.toDateString() + " - " + toDate.toDateString();
        var data = me.getDischargeDateDataFromRange(damName, fromDate, toDate);
        var hydroGraphData = me.getComparisonHydrographDataArray(data);
        var record = {name: datasetName, data: hydroGraphData};
        me.comparisonHydrograph.addSeries(record, true);
    }

    me.dateBetween = function (date, start, end) {
        return date >= start.getTime() && date <= end.getTime();
    };

    me.getDischargeDateDataFromRange = function (damName, fromDate, toDate) {
        var dateRangeArray = new Array();
        var dischargeData = Ext.getCmp('dischargeDataPanel').getStore().config.data;
        var damDischargeData = _.where(dischargeData, {head_works:damName});
        var count = damDischargeData.length;
        for (var i = 0; i < count; i++) {
            var record = damDischargeData[i];
            var discharge_date = Date.parse(record.discharge_date);
            var recordDate = new Date(discharge_date);
            if (me.dateBetween(recordDate, fromDate, toDate) == true) {
                dateRangeArray.push(record);
            }
        }
        return dateRangeArray;
    }

    me.getHeadWorkData = function (headwork) {
        var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
        var url = '../hwdischarge?head=' + headwork.toString();
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
                        me.getDischargeDataPanel(data, me.headWork);
                        me.hwDischargeData = data;
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

    me.getDischargeYearForm = function () {
        if (me.win != null) {
            me.win.destroy();
        }
        me.win = Ext.create('Ext.window.Window', {
            id: 'dischargeYearWin',
            title: 'Discharge Years List',
            layout: 'fit',
            x: 250,
            y: 100,
            width: 250,
            height: 200,
            frame: true,
            closeAction: 'destroy',
            preventBodyReset: true,
            resizable: false,
            constrainHeader: true,
            collapsible: false,
            plain: true,
            bbar: [
                {
                    text: 'Update Map',
                    icon: '/static/ferrp/img/irrigation/03.png',
                    handler: function () {
                        var year = Ext.getCmp('numDischargeYear').getValue();
                        var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
                        var url = "../updatedischarge?year=" + year;
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
                                    var jsonData = JSON.parse(data.damsData);
                                    var geoJsonData = JSON.parse(data.damsGeoJson);
                                    me.damsGeoJson = JSON.stringify(geoJsonData[0].geojson);
                                    me.irrigationDams.clearLayers();
                                    me.irrigationDams.addData(geoJsonData[0].geojson);
                                }
                            },
                            failure: function (res) {
                                box.hide();
                                // alert(res.responseText);
                            }
                        });
                    }
                }
            ],
            items: [
                Ext.create('Ext.form.Panel', {
                    defaults: {
                        anchor: '100%'
                    },
                    autoScroll: true,
                    fieldLabel: 'Discharge Years',
                    id: 'frmDischargeYearsList',
                    name: 'frmDischargeYearsList',
                    items: [
                        {
                            xtype: 'fieldset',
                            title: 'Discharge Year',
                            margin: 15,
                            layout: 'fit',
                            items: [
                                {
                                    xtype: 'numberfield',
                                    id: 'numDischargeYear',
                                    name: 'numDischargeYear',
                                    value: 2013,
                                    minValue: 1978,
                                    maxValue: 2013,
                                    margin: '0 0 15 0'
                                }]
                        },
                        // {
                        //     xtype: 'fieldset',
                        //     title: 'Discharge Year',
                        //     layout: 'anchor',
                        //     defaults: {
                        //         anchor: '100%',
                        //     },
                        //     margin:10,
                        //     items:[{
                        //         xtype: 'radiogroup',
                        //         columns: 1,
                        //         items: [
                        //             {boxLabel: '2013', inputValue: 1, checked: true},
                        //             {boxLabel: '2012', inputValue: 2},
                        //             {boxLabel: '2011', inputValue: 3},
                        //             {boxLabel: '2010', inputValue: 3},
                        //             {boxLabel: '2009', inputValue: 3},
                        //             {boxLabel: '2008', inputValue: 3},
                        //             {boxLabel: '2007', inputValue: 3},
                        //             {boxLabel: '2006', inputValue: 3},
                        //             {boxLabel: '2005', inputValue: 3},
                        //             {boxLabel: '2004', inputValue: 3},
                        //             {boxLabel: '2003', inputValue: 3},
                        //             {boxLabel: '2002', inputValue: 3},
                        //             {boxLabel: '2001', inputValue: 3},
                        //             {boxLabel: '2000', inputValue: 3},
                        //             {boxLabel: '1999', inputValue: 3},
                        //             {boxLabel: '1998', inputValue: 3},
                        //             {boxLabel: '1997', inputValue: 3},
                        //             {boxLabel: '1995', inputValue: 3},
                        //         ]
                        //     },
                        //     ]
                        // }
                    ]
                })
            ]
        });

        me.win.show();
    }

    me.getYearStore = function () {
        var data = [];
        for (var i = 2013; i >= 1978; i--) {
            data.push({id: i, name: i});
        }
        var featureStore = Ext.create('Ext.data.Store', {
            fields: [
                {name: 'id', type: 'string'},
                {name: 'name', type: 'string'}
            ],
            data: data
        });
        return featureStore;
    }
}
