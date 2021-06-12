/**
 * Created by idrees on 12/20/2017.
 */

var llMap = null;
var heatLayer = null;

var ArzWLMapModel = function () {
    var me = this;
    me.getMapAndTable = function () {
        var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
        var url = '../groundwaterdata';
        Ext.Ajax.timeout = 900000;
        Ext.Ajax.request({
            url: url,
            method: "GET",
            success: function (response) {
                var southPanel = Ext.getCmp("southWLPanel");
                southPanel.collapse();
                box.hide();
                var respText = response.responseText;
                var respnseText = eval('(' + JXG.decompress(respText) + ')');
                if (respnseText != "false") {
                    var data = respnseText;
                    var jsonData = JSON.parse(data.json);
                    var geoJsonData = JSON.parse(data.geojson);
                    var arzMapModel = new ArzLeafletWLMapModel();
                    arzMapModel.getWLDataPanel(jsonData);
                    arzMapModel.getLeafletMapPanel();
                    arzMapModel.createLeafletMap(JSON.stringify(geoJsonData[0].geojson));
                    legend.style.visibility = 'visible';
                }
            },
            failure: function (res) {
                box.hide();
            }
        });
    }
}

var ArzLeafletWLMapModel = function () {
    var me = this;
    me.irrigationWL = null;
    me.marker = null;
    me.wlGeoJson = null;
    me.dataType = null;
    me.whereClause = null;
    me.globalFunctions = null;
    me.ql_id = null;
    me.ql_type = null;
    me.currentLevel = 0;
    me.levelGraphData = null;
    me.qualityGraphData = null;
    me.levelGraph = null;
    me.qualityGraph = null;
    me.win = null;
    me.selectionSet = null;
    me.selectionLayer = null;
    me.gridSelectionModel = null;
    var adminHierarchy = new ArzAdminHierarchyToolbar();

    me.getLeafletMapPanel = function () {
        me.globalFunctions = new ArzGlobalFunctionsModel();
        var mapPanel = Ext.create('Ext.panel.Panel', {
            xtype: 'panel',
            headerCls: 'extPanel',
            id: 'wlLLMap',
            layout: 'fit',
            flex: 1,
            margin: '0 0 0 0',
            tbar: [
                adminHierarchy.getAdminToolbar(),
                {
                    icon: imgPath + 'arrow_refresh.png',
                    handler: function () {
                        llMap.invalidateSize();
                    }
                }, {
                    icon: imgPath + 'Clear.png',
                    tooltip: 'Clear Selection',
                    handler: function () {
                        me.clearAllSelection();
                    }
                }, {
                    icon: imgPath + '12.png',
                    tooltip: 'Create water level surface',
                    handler: function () {
                        $('#levelSurfaceModal').modal('show');
                    }
                }
            ]
        });
        var dataPanel = Ext.getCmp("pnlWLllMap");
        dataPanel.removeAll();
        dataPanel.add(mapPanel);
    }

    me.createLeafletMap = function (geoJson) {
        me.wlGeoJson = geoJson;
        me.globalFunctions = new ArzGlobalFunctionsModel();

        var mapDiv = Ext.getCmp('wlLLMap').body.dom;
        llMap = L.map(mapDiv, {zoomControl: false}).setView([30.5, 72.5], 7);
        var Legend = new L.Control.Legend({
            position: 'topleft',
            collapsed: true,
            controlButton: {
                title: "Legend"
            }
        });
        llMap.addControl(Legend);
        $(".legend-container").append($("#legend"));
        $(".legend-toggle").append("<i class='legend-toggle-icon fa fa-info fa-2x' style='color: #000'></i>");
        var zoom_bar = new L.Control.ZoomBar({position: 'topleft'}).addTo(llMap);
        var pointsArray = me.getHeatMapData(JSON.parse(me.wlGeoJson));
        heatLayer = L.heatLayer(pointsArray, {
            radius: 10,
            blur: 15,
            maxZoom: 17,
        }).addTo(llMap);
        me.irrigationWL = L.geoJSON(JSON.parse(me.wlGeoJson), {
            onEachFeature: me.onEachFeature,
            pointToLayer: function (feature, latlng) {
                return L.circleMarker(latlng, me.getGWStyle(feature));
            }
        }).addTo(llMap);
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
                "Ground Water": me.irrigationWL,
                "Heat Map": heatLayer
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
        // me.selectionLayer.clearLayers();

    }

    me.clearAllSelection = function () {
        if (me.selectionLayer) {
            me.selectionLayer.clearLayers();
        }
        if (me.marker) {
            llMap.removeLayer(me.marker);
        }
        var grid = Ext.getCmp('wlDataPanel');
        grid.getSelectionModel().deselectAll();
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
                    radius: 8,
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

    me.onEachFeature = function (feature, layer) {
        layer.on({
            click: me.getAttributeForm
        });
    }

    me.getAttributeForm = function (e) {
        var props = e.target.feature.properties;
        var popupContent = '';
        if (props) {
            var popupContent = '<b>Zone      :</b>' + props.zone + '</br>';
            popupContent = popupContent + '<b>Circle         :</b>' + props.circle + '</br>'
            popupContent = popupContent + '<b>Division:</b>' + props.division + '</br>'
            popupContent = popupContent + '<b>Major Canal     :</b>' + props.major_canal + '</br>'
            popupContent = popupContent + '<b>Minor Canal     :</b>' + props.disty_minor + '</br>'
            popupContent = popupContent + '<b>Reclamation     :</b>' + props.reclamation + '</br>'
            popupContent = popupContent + '<b>Type     :</b>' + props.type_wl_wq + '</br>'
            popupContent = popupContent + '<b>Elevation     :</b>' + props.elevation + '</br>';
            this.bindPopup(popupContent);
        }
    }

    me.drawLineOnMap = function (record) {
        me.reMoveLayer(me.marker);
        var geojsonText = record.data.geojson;
        var geojson = JSON.parse(geojsonText);
        var coordList = geojson.coordinates;
        var damIcon = L.icon({
            iconUrl: imgPath + 'flashmarker.gif',
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

    me.getWLDataPanel = function (data) {
        var gridColumns = new ArzGridColumns();
        var store = Ext.create('Ext.data.Store', {
            id: 'wlDataStore',
            fields: me.getFieldsList(data[0]),
            data: data,
            groupField: 'type_wl_wq'
        });
        var gridPanel = Ext.create('Ext.grid.Panel', {
            layout: 'fit',
            id: 'wlDataPanel',
            title: 'Ground Water Data',
            titleAlign: 'center',
            store: store,
            multiSelect: true,
            stripeRows: true,
            columnLines: true,
            plugins: 'gridfilters',
            autoScroll: true,
            loadMask: true,
            listeners: {
                select: function (selModel, record, index, options) {
                    me.gridSelectionModel = selModel;
                    me.ql_id = [];
                    me.ql_type = record.data.type_wl_wq;
                    me.selectionLayer.clearLayers();
                    me.selectionSet = [];
                    if (selModel.selected.items.length > 1) {
                        for (key in selModel.selected.items) {
                            var row = selModel.selected.items[key];
                            me.ql_id.push(row.data.id);
                            var geojson = JSON.parse(row.data.geojson);
                            me.selectionSet.push({
                                "type": "Feature",
                                "properties": row.data,
                                "geometry": geojson
                            });
                        }
                        me.selectionLayer.addData({type: 'FeatureCollection', features: me.selectionSet});
                    } else {
                        me.ql_id.push(record.data.id);
                        var geojson = JSON.parse(record.data.geojson);
                        me.selectionSet.push({
                            "type": "Feature",
                            "properties": record.data,
                            "geometry": geojson
                        });
                        me.selectionLayer.addData({type: 'FeatureCollection', features: me.selectionSet});
                        // me.drawLineOnMap(record);
                    }

                    // me.highlightPointOnMap(record);

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
                    // console.log('datachanged/count: ' + store.count())
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
                        alasql("SELECT * INTO XLSX('data_table.xlsx',{headers:true}) FROM ? ", [exportData]);
                    }
                }, '-',
                {
                    icon: imgPath + '15.png',
                    tooltip: 'email data link',
                    handler: function () {
                        me.dataType = 'ground_water';
                        me.whereClause = 'null';
                        var filtersArray = me.globalFunctions.getGridFiltersList(gridPanel);
                        // me.globalFunctions.getEmailForm(me.dataType, me.whereClause);
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
                        me.dataType = 'ground_water';
                        me.whereClause = 'null';
                        var filtersArray = me.globalFunctions.getGridFiltersList(gridPanel);
                        // me.globalFunctions.getSMSForm(me.dataType, me.whereClause);
                        $("#dataType").val(me.dataType);
                        $("#whereClause").val(me.whereClause);
                        $("#filtersArray").val(filtersArray);
                        $('#smsModal').modal('show');
                    }
                },
                {
                    icon: imgPath + '12.png',
                    tooltip: 'Show water level histroy.',
                    handler: function () {
                        if (me.ql_id) {
                            me.getWaterLevelQualityData(me.ql_id);
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
                },
                {
                    tooltip: 'DeSelect All',
                    icon: imgPath + 'deselect_all_16.png',
                    iconMask: true,
                    handler: function () {
                        me.clearAllSelection();
                    }
                }, '-',
            ],
            columns: gridColumns.getGroundWaterColumnsList(),
            features: [{
                id: 'group',
                ftype: 'groupingsummary',
                groupHeaderTpl: '{name}',
                hideGroupedHeader: false,
                enableGroupingMenu: true,
                startCollapsed: true
            }, {
                ftype: 'summary',
                dock: 'bottom'
            }],
        });
        var dataPanel = Ext.getCmp("pnlWLData");
        dataPanel.removeAll();
        dataPanel.add(gridPanel);
    }

    me.clearAllSelection = function () {
        if (me.selectionLayer) {
            me.selectionLayer.clearLayers();
        }
        if (me.marker) {
            llMap.removeLayer(me.marker);
        }
        var grid = Ext.getCmp('wlDataPanel');
        grid.getSelectionModel().deselectAll();
        grid.filters.clearFilters();
    }

    me.getWLHistoryDataPanel = function (data) {

        var gridColumns = new ArzGridColumns();

        var store = Ext.create('Ext.data.Store', {
            id: 'wlHistoryDataStore',
            fields: me.getFieldsList(data[0]),
            data: data
        });
        var dischargePanel = Ext.create('Ext.grid.Panel', {
            layout: 'fit',
            id: 'wlHistoryDataPanel',
            titleAlign: 'center',
            store: store,
            stripeRows: true,
            columnLines: true,
            plugins: 'gridfilters',
            autoScroll: true,
            loadMask: true,
            bbar: [
                {
                    tooltip: 'Export to Excel',
                    icon: imgPath + 'EXCLE.png',
                    handler: function () {
                        // var gridData = dischargePanel.getStore().config.data;
                        var data = dischargePanel.getStore().data;
                        var exportData = me.globalFunctions.getDataFromGridItems(data);
                        alasql("SELECT * INTO XLSX('discharge_data_table.xlsx',{headers:true}) FROM ? ", [exportData]);
                    }
                }, '-', {
                    icon: imgPath + '15.png',
                    tooltip: 'email data link',
                    handler: function () {
                        me.dataType = 'ground_water';
                        me.whereClause = 'null';
                        me.globalFunctions.getEmailForm(me.dataType, me.whereClause);
                    }
                },
                {
                    icon: imgPath + '05.png',
                    tooltip: 'SMS data link',
                    handler: function () {
                        me.dataType = 'ground_water';
                        me.whereClause = 'null';
                        me.globalFunctions.getSMSForm(me.dataType, me.whereClause);
                    }
                }],
            listeners: {
                select: function (selModel, record, index, options) {
                }
            },
            autoDestroy: true,
            columns: gridColumns.getGroundWaterColumnsList(),
        });
        var dataPanel = Ext.getCmp("pnlWLHistoryData");
        dataPanel.removeAll();
        dataPanel.add(dischargePanel);
        Ext.getCmp('southWLPanel').expand();
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
                }
            ]
        });
        return contextMenu;
    }

    me.getWLHistoryData = function (name) {
        var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
        var url = '../hwdischarge?head=' + name;
        Ext.Ajax.timeout = 900000;
        Ext.Ajax.request({
            url: url,
            method: "GET",
            success: function (response) {
                box.hide();
                var respnseText = response.responseText;
                if (respnseText != "false") {
                    var data = JSON.parse(respnseText);
                    if (data.length > 0) {
                        me.getWLHistoryDataPanel(data);
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

    me.getHeatMapData = function (geoJson) {
        return geoJson.features.map(function (feature) {
            return [
                feature.geometry.coordinates[1],
                feature.geometry.coordinates[0],
                feature.properties['elevation'] == 'NA' ? 0 : feature.properties['elevation']
            ];
        });
    }

    me.getGWStyle = function (feature) {
        return {
            radius: 4,
            fillColor: me.getGWColor(feature.properties.type_wl_wq),
            // color: "#ff03e7",
            weight: 1,
            opacity: 1,
            fillOpacity: 0.8,
        };
    }

    me.getGWColor = function (type) {
        if (type == 'Level') {
            return 'rgb(0,0,255)';
        }
        if (type == 'Quality') {
            return 'rgb(0,255,0)';
        } else {
            return 'rgb(255,0,0)';
        }
    }

    me.highlightPointOnMap = function (record) {
        me.reMoveLayer(me.marker);
        var geojsonText = record.data.geojson;
        var geojson = JSON.parse(geojsonText);
        var coordList = geojson.coordinates;
        var gwIcon = L.icon({
            iconUrl: '/static/ferrp/img/irrigation/flashmarker.gif',
            iconSize: [10, 10], // size of the icon
        });
        me.marker = L.marker([coordList[1], coordList[0]], {icon: gwIcon}).addTo(llMap);
    }


    me.getWaterLevelQualityData = function (ql_id) {
        var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
        var url = '../wl_wq_detail_data?ql_id=' + ql_id.toString();
        Ext.Ajax.timeout = 900000;
        Ext.Ajax.request({
            url: url,
            method: "GET",
            success: function (response) {
                box.hide();
                var respText = response.responseText;
                var respnseText = eval('(' + JXG.decompress(respText) + ')');
                if (respnseText != "false") {
                    var southPanel = Ext.getCmp("southWLPanel");
                    southPanel.expand();
                    var data = respnseText;
                    var level = data['level'];
                    var quality = data['quality'];
                    me.levelGraphData = JSON.parse(level);
                    me.qualityGraphData = JSON.parse(quality);
                    me.currentLevel = 0;
                    me.drawLevelQualityGraphs();
                }
            },
            failure: function (res) {
                box.hide();
            }
        });
    }

    //
    //
    // me.getNextRecordGraph = function () {
    //     me.currentLevel += 1;
    //     me.drawLevelQualityGraphs();
    // }
    //
    // me.getNextPreviousButtons = function () {
    //     var buttons = [
    //         {
    //         xtype: 'button',
    //         id: 'btnPrevious',
    //         icon: imgPath + 'arrow_left.png',
    //         tooltip: 'Get previous record graph',
    //         handler: function () {
    //             me.getPreviousRecordGraph();
    //
    //         }
    //     },
    //         {
    //             xtype: 'button',
    //             id: 'btnNext',
    //             icon: imgPath + 'arrow_right.png',
    //             tooltip: 'Get next record graph',
    //             handler: function () {
    //                 me.getNextRecordGraph();
    //             }
    //         }];
    //     return buttons;
    // }
    //
    // me.getPreviousRecordGraph = function () {
    //     me.currentLevel -= 1;
    //     me.drawLevelQualityGraphs();
    // }

    me.drawLevelQualityGraphs = function () {
        var groundWaterTab = Ext.getCmp("tabGroundWater");
        if (me.ql_type == 'Both') {
            groundWaterTab.setActiveTab(0);
            me.getGroundWaterDetailGrid(me.levelGraphData, 'Level')
            me.getGroundWaterDetailGrid(me.qualityGraphData, 'Quality')
            // var levelYearsList = me.getLevelGraphDataYears(me.levelGraphData);
            // var qualityYearsList = me.getLevelGraphDataYears(me.qualityGraphData);
            //
            // var selectedData = Ext.getCmp('wlDataPanel').getSelectionModel().selected.items;
            // var firstRecordId = selectedData[me.currentLevel].data.id;
            // var fLevelData = _.where(me.levelGraphData, {ql_id: firstRecordId});
            // var fQualityData = _.where(me.qualityGraphData, {ql_id: firstRecordId});
            // var levelData = me.getLevelGraphData(fLevelData);
            //
            // var ecData = me.getQualityPreGraphData(fQualityData, 'EC');
            // var rscData = me.getQualityPreGraphData(fQualityData, 'RSC');
            // var sarData = me.getQualityPreGraphData(fQualityData, 'SAR');
            //
            // me.getLevelGraph(levelData, levelYearsList, 'Pre and Post Monson Water Depth(Feet)', 'pnlLevelGraph', 'Water Depth(Feet)');
            // me.getQualityGraph(ecData, qualityYearsList, 'Pre and Post Monson Water EC', 'pnlQualityEC', 'Water EC Values');
            // me.getQualityGraph(rscData, qualityYearsList, 'Pre and Post Monson Water RSC', 'pnlQualityRSC', 'Water RSC Values');
            // me.getQualityGraph(sarData, qualityYearsList, 'Pre and Post Monson Water SAR', 'pnlQualitySAR', 'Water SAR Values');
        }
        if (me.ql_type == 'Level') {
            groundWaterTab.setActiveTab(0);
            // var selectedData = Ext.getCmp('wlDataPanel').getSelectionModel().selected.items;
            // var firstRecordId = selectedData[me.currentLevel].data.id;
            // var fLevelData = _.where(me.levelGraphData, {ql_id: firstRecordId});
            // var levelYearsList = me.getLevelGraphDataYears(fLevelData);
            // var levelData = me.getLevelGraphData(fLevelData);

            me.getGroundWaterDetailGrid(me.levelGraphData, 'Level')
            // me.getLevelGraph(levelData, levelYearsList, 'Pre and Post Monson Water Depth(Feet)', 'pnlLevelGraph', 'Water Depth(Feet)');
        }
        if (me.ql_type == 'Quality') {
            groundWaterTab.setActiveTab(1);

            // var selectedData = Ext.getCmp('wlDataPanel').getSelectionModel().selected.items;
            // var firstRecordId = selectedData[me.currentLevel].data.id;
            // var fQualityData = _.where(me.qualityGraphData, {ql_id: firstRecordId});
            // var yearsList = me.getLevelGraphDataYears(fQualityData);
            //
            // var ecData = me.getQualityPreGraphData(fQualityData, 'EC');
            // var rscData = me.getQualityPreGraphData(fQualityData, 'RSC');
            // var sarData = me.getQualityPreGraphData(fQualityData, 'SAR');

            me.getGroundWaterDetailGrid(me.qualityGraphData, 'Quality')
            // me.getQualityGraph(ecData, yearsList, 'Pre and Post Monson Water EC', 'pnlQualityEC', 'Water EC Values');
            // me.getQualityGraph(rscData, yearsList, 'Pre and Post Monson Water RSC', 'pnlQualityRSC', 'Water RSC Values');
            // me.getQualityGraph(sarData, yearsList, 'Pre and Post Monson Water SAR', 'pnlQualitySAR', 'Water SAR Values');
        }
    }

    me.getLevelGraph = function (data, years, xLabel, divId, yTitle) {
        var chartPanel = Ext.getCmp(divId);
        chartPanel.removeAll();
        var chartDiv = chartPanel.body.dom;
        me.levelGraph = Highcharts.chart(chartDiv, {
            chart: {
                type: 'column'
            },
            title: {
                text: xLabel
            },
            xAxis: {
                categories: years
            },
            yAxis: {
                title: {
                    text: yTitle
                }
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle'
            },
            plotOptions: {
                line: {
                    dataLabels: {
                        enabled: true
                    },
                    enableMouseTracking: true
                }
            },
            series: data
        });
    }

    me.getQualityGraph = function (data, years, xLabel, divId, yTitle) {
        var chartPanel = Ext.getCmp(divId);
        chartPanel.removeAll();
        var chartDiv = chartPanel.body.dom;
        me.levelGraph = Highcharts.chart(chartDiv, {
            title: {
                text: xLabel
            },
            xAxis: {
                categories: years
            },
            yAxis: {
                title: {
                    text: yTitle
                }
            },
            legend: {
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle'
            },
            plotOptions: {
                line: {
                    dataLabels: {
                        enabled: true
                    },
                    enableMouseTracking: true
                }
            },
            series: data
        });
    }

    me.getLevelGraphData = function (data) {
        var preMonsonData = [];
        var postMonsonData = [];
        for (var i = 0; i < data.length; i++) {
            var season = data[i]['season'];
            var sField = data[i]['water_depth'];
            sField = parseFloat(sField);
            if ((isNaN(sField)) == true) {
                sField = 0;
            }
            if (season == 'Pre Monson') {
                preMonsonData.push(sField - (sField * 2));
            }
            if (season == 'Post Monson') {
                postMonsonData.push(sField - (sField * 2));
            }
        }
        return [{name: 'Pre Monsoon', data: preMonsonData}, {name: 'Post Monsoon', data: postMonsonData}];
    }

    me.getLevelGraphDataYears = function (data) {
        var yearsList = [];
        for (var i = 0; i < data.length; i++) {
            var year = data[i]['year'];
            if (yearsList.includes(year) == false) {
                yearsList.push(year);
            }
        }
        return yearsList;
    }

    me.createQualityBarChart = function (data, yearsList, xLabel, divId) {
        var chartPanel = Ext.getCmp(divId);
        chartPanel.removeAll();
        var chartDiv = chartPanel.body.dom;
        Highcharts.chart(chartDiv, {
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
                categories: yearsList
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
            series: data
        });
    }

    me.getQualityPreGraphData = function (data, qualityType) {
        var preMonsonData = [];
        var postMonsonData = [];
        for (var i = 0; i < data.length; i++) {
            var season = data[i]['season'];
            var quality_val = data[i]['water_quality'];
            var quality_type = data[i]['quality_type'];
            quality_val = parseFloat(quality_val);
            if ((isNaN(quality_val)) == true) {
                quality_val = 0;
            }
            if (quality_type == qualityType) {
                if (season == 'Pre Monson') {
                    preMonsonData.push(quality_val);
                }
                if (season == 'Post Monson') {
                    postMonsonData.push(quality_val);
                }
            }
        }
        return [{name: 'Pre Monsoon', data: preMonsonData}, {name: 'Post Monsoon', data: postMonsonData}];
    }

    me.removeLevelGraphSeries = function () {
        var seriesLength = me.levelGraph.series.length;
        for (var i = seriesLength - 1; i > -1; i--) {
            me.levelGraph.series[i].remove();
        }
    }

    me.getGroundWaterDetailGrid = function (data, level_quality) {
        var columns = null;
        var gridColumns = new ArzGridColumns();
        if (level_quality == 'Level') {
            columns = gridColumns.getGroundWaterLevelColumnsList();
        } else {
            columns = gridColumns.getGroundWaterQualityColumnsList();
        }
        var store = Ext.create('Ext.data.Store', {
            id: level_quality + 'DataStore',
            fields: me.getFieldsList(data[0]),
            data: data,
        });
        var gridPanel = Ext.create('Ext.grid.Panel', {
            layout: 'fit',
            id: level_quality + 'DataPanel',
            titleAlign: 'center',
            store: store,
            stripeRows: true,
            columnLines: true,
            plugins: 'gridfilters',
            autoScroll: true,
            loadMask: true,
            listeners: {
                select: function (selModel, record, index, options) {

                },
                beforeitemcontextmenu: function (view, record, item, index, e) {
                    e.stopEvent();
                }
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
                        if(level_quality == 'Level'){
                            me.globalFunctions.createPivotTableWindow(gridData, [{"uniqueName": "ql_id",}, {"uniqueName": "year"}], [{"uniqueName": "season"}], [{"uniqueName": "water_depth_double", "aggregation": "average"}]);
                        }else{
                            me.globalFunctions.createPivotTableWindow(gridData, [{"uniqueName": "ql_id",}, {"uniqueName": "year"}], [{"uniqueName": "season"}], [{"uniqueName": "water_quality", "aggregation": "average"}]);
                        }

                    }
                }
            ],
            columns: columns,
            features: [{
                id: 'group',
                ftype: 'groupingsummary',
                groupHeaderTpl: '{name}',
                hideGroupedHeader: false,
                enableGroupingMenu: true,
                startCollapsed: true
            }, {
                ftype: 'summary',
                dock: 'bottom'
            }],
        });
        if (level_quality == 'Level') {
            var dataPanel = Ext.getCmp("pnlLevelData");
            dataPanel.removeAll();
            dataPanel.add(gridPanel);
        } else {
            var dataPanel = Ext.getCmp("pnlQualityData");
            dataPanel.removeAll();
            dataPanel.add(gridPanel);
        }

    }

}

