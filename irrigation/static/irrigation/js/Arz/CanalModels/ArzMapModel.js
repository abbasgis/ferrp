/**
 * Created by idrees on 12/18/2017.
 */

var canalsData = null;
var llMap = null;
var layerControl = null;
var canalsLayer = null;
var canalsGeoJson = null;

var ArzCanalsMapModel = function () {
    var me = this;
    me.canalsGeoJson = null;
    me.getMapAndTable = function () {
        var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
        var url = '../canalsdata';
        Ext.Ajax.request({
            url: url,
            timedout: false,
            // timeout:90000000,
            method: "GET",
            success: function (response) {
                box.hide();
                var respText = response.responseText;
                var respnseText = eval('(' + JXG.decompress(respText) + ')');
                if (respnseText != "false") {
                    var data = respnseText;
                    canalsData = JSON.parse(data.data);
                    var geoJsonData = JSON.parse(data.geojson);
                    var arzMapModel = new ArzLeafletCanalMapModel();
                    arzMapModel.getCanalsDataPanel(canalsData);
                    arzMapModel.getLeafletMapPanel();
                    canalsGeoJson = geoJsonData[0].geojson;
                    arzMapModel.createLeafletMap(canalsGeoJson);
                    legend.style.visibility = 'visible';
                }
            },
            failure: function (res) {
                box.hide();
            }
        });
    }

}

var ArzLeafletCanalMapModel = function () {
    var me = this;
    me.imisCode = null;
    me.canalRecord = null;
    me.lineGeom = null;
    me.canalsGeoJson = null;
    me.info = L.control();
    me.xsLineGeom = null;
    me.drawLineEvent = false;
    me.xsPointsArray = [];
    me.xsLine = null;
    me.marker = null;
    me.detailMarker = null;
    me.dataType = null;
    me.whereClause = null;
    me.attributeWin = null;
    me.rightClick = false;
    me.xsProfileData = null;
    me.googleRoadMap = null;
    me.googleSatelliteMap = null;
    me.googleTerrainMap = null;
    me.globalFunctions = null;
    me.profileHighGraph = null;
    me.gatesGeojson = null;
    me.canalDetailsLayer = null;
    me.selectionSet = null;
    me.selectionLayer = null;
    me.gridSelectionModel = null;
    me.canalsDetailMapLayer = new ArzCanalsDetailMapLayer();

    me.getLeafletMapPanel = function () {
        var mapPanel = Ext.create('Ext.panel.Panel', {
            xtype: 'panel',
            headerCls: 'extPanel',
            id: 'canalsLLMap',
            layout: 'fit',
            flex: 1,
            margin: '0 0 0 0',
            tbar: [
                {
                    icon: '/static/ferrp/img/irrigation/arrow_refresh.png',
                    handler: function () {
                        llMap.invalidateSize();
                    }
                },
                {
                    icon: '/static/ferrp/img/irrigation/Clear.png',
                    tooltop: 'Clear selection',
                    handler: function () {
                        me.removeAllLayers();
                        if (me.lineGeom) {
                            llMap.removeLayer(me.lineGeom);
                        }
                        var grid = Ext.getCmp('canalsDataPanel');
                        grid.filters.clearFilters();
                        grid.getSelectionModel().deselectAll();
                        canalsLayer.addData(canalsGeoJson);
                    }
                }, '-',
                {
                    icon: '/static/ferrp/img/irrigation/drawline.png',
                    tooltip: 'Draw line on map to see terrain of earth.',
                    handler: function () {
                        Ext.MessageBox.alert('Draw Line', 'Single click to draw line on map and right click to end draw.');
                        me.xsPointsArray = [];
                        me.rightClick = false;
                        if (me.rightClick == false) {
                            L.DomUtil.addClass(llMap._container, 'crosshair-cursor-enabled');
                            llMap.on('click', me.drawXSLineOnMap);
                            llMap.on('contextmenu', function (e) {
                                me.drawXSLineOnMap(e);
                                me.xsLine.completeShape;
                                llMap.off('click', me.drawXSLineOnMap);
                                llMap.off('contextmenu', me.drawXSLineOnMap);
                                me.rightClick = true;
                                L.DomUtil.removeClass(llMap._container, 'crosshair-cursor-enabled');
                                var wkt = me.getWKT();
                                me.getHeightProfile(wkt);
                            });
                        }
                    }
                }
            ]
        });
        var dataPanel = Ext.getCmp("canalsLLMapPanel");
        dataPanel.removeAll();
        dataPanel.add(mapPanel);
    }

    me.createLeafletMap = function (geoJson) {
        me.canalsGeoJson = geoJson
        var mapDiv = Ext.getCmp('canalsLLMap').body.dom;
        llMap = L.map(mapDiv, {zoomControl: false}).setView([30.7, 72.5], 7);
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
        //
        var zoom_bar = new L.Control.ZoomBar({position: 'topleft'}).addTo(llMap);
        me.info.onAdd = function () {
            this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
            this.update();
            return this._div;
        };
        me.info.addTo(llMap);

        canalsLayer = L.geoJson(me.canalsGeoJson, {
            style: me.getCanalStyle,
            onEachFeature: me.onEachFeature
        }).addTo(llMap);

        layerControl = L.control.layers(
            {
                Roadmap: me.googleRoadMap,
                Aerial: me.googleSatelliteMap,
                Terrain: me.googleTerrainMap
            },
            {
                Canals: canalsLayer
            },
            {
                collapsed: true
            }
        ).addTo(llMap);


        // Initialise the FeatureGroup to store editable layers
        var editableLayers = new L.FeatureGroup();
        llMap.addLayer(editableLayers);
        // me.selectionLayer.

        // define custom marker
        // var MyCustomMarker = L.Icon.extend({
        //     options: {
        //         shadowUrl: null,
        //         iconAnchor: new L.Point(12, 12),
        //         iconSize: new L.Point(24, 24),
        //         iconUrl: 'http://www.pdclipart.org/albums/Buildings/igloo.png'
        //     }
        // });
        // var drawPluginOptions = {
        //   position: 'topright',
        //   draw: {
        //     polyline: {
        //       shapeOptions: {
        //         color: '#f357a1',
        //         weight: 10
        //       }
        //     },
        //     polygon: {
        //       allowIntersection: false, // Restricts shapes to simple polygons
        //       drawError: {
        //         color: '#e1e100', // Color the shape will turn when intersects
        //         message: '<strong>Oh snap!<strong> you can\'t draw that!' // Message that will show when intersect
        //       },
        //       shapeOptions: {
        //         color: '#bada55'
        //       }
        //     },
        //     circle: false, // Turns off this drawing tool
        //     rectangle: {
        //       shapeOptions: {
        //         clickable: false
        //       }
        //     },
        //     marker: {
        //       icon: new MyCustomMarker()
        //     }
        //   },
        //   edit: {
        //     featureGroup: editableLayers, //REQUIRED!!
        //     remove: false
        //   }
        // };
        // Initialise the draw control and pass it the FeatureGroup of editable layers
        // var drawControl = new L.Control.Draw(drawPluginOptions);
        // llMap.addControl(drawControl);
        //
        //
        // var editableLayers = new L.FeatureGroup();
        // llMap.addLayer(editableLayers);

        me.selectionLayer = new L.geoJSON(me.geojsonObject, {
            style: me.selectionStyleFunction,
        });
        llMap.addLayer(me.selectionLayer);
        me.selectionLayer.clearLayers();

        llMap.on('draw:created', function (e) {
            var type = e.layerType,
                layer = e.layer;

            if (type === 'marker') {
                layer.bindPopup('A popup!');
            }

            editableLayers.addLayer(layer);
        });


    }

    me.info.update = function (props) {
        // this._div.innerHTML = (props ?
        //     '<b>' + props.channel_name + '</b><br />'
        //     + '<h5>Length: <b>' + props.length_km.toFixed(2) + '</b> KM</h5>': 'click on canal');
        // '<b style="color:' + me.getCanalColor("MC") + ';">Main Canal</b></br>'+
        // '<b style="color:' + me.getCanalColor("BC") + ';">Branch Canal</b></br>'+
        // '<b style="color:' + me.getCanalColor("D") + ';">Distributary</b></br>'+
        // '<b style="color:' + me.getCanalColor("M") + ';">Minor Canal</b></br>'+
        // '<b style="color:' + me.getCanalColor("SM") + ';">Sub Minor</b></br>'+
        // '<b style="color:' + me.getCanalColor("E") + ';">Escape</b></br>'+
        // '<b style="color:' + me.getCanalColor(" ") + ';">Others</b>');
    };

    me.getAttributeForm = function (e) {
        var props = e.target.feature.properties;
        me.selectHighlightGridRow('canalsDataPanel', 'imis_code', props.imis_code);
        if (me.attributeWin != null) {
            me.attributeWin.destroy();
        }
        var attributeGrid = new Ext.grid.PropertyGrid({
            layout: 'fit',
            source: {
                "Canal Name": props.channel_name,
                "Canal Type": me.getFullNameFromCanalType(props.channel_type),
                "Length": props.length_km.toFixed(4),
                "IMIS Code": props.imis_code,
                "Zone Name": props.zone_name,
                "Circle Name": props.circle_name,
                "Division Name": props.division_name,
                "Flow Type": props.flowtype_e,
                "GCA": props.gca,
                "CCA": props.cca,
                "Head X": props.head_x,
                "Head Y": props.head_y,
                "Tail X": props.tail_x,
                "Tail Y": props.tail_y,
            }
        });
        delete attributeGrid.getStore().sortInfo;
        me.attributeWin = new Ext.window.Window({
            closable: true,
            resizable: true,
            draggable: true,
            title: 'Attribute Info',
            width: 300,
            height: 355,
            minWidth: 200,
            minHeight: 50,
            plain: true,
            layout: 'fit',
            items: attributeGrid
        });
        me.attributeWin.show();
    }

    me.getFullNameFromCanalType = function (shortName) {
        var fullName = "";
        if (shortName == "M") {
            fullName = "Minor Canal";
        } else if (shortName == "MC") {
            fullName = "Main Canal";
        } else if (shortName == "BC") {
            fullName = "Branch Canal";
        } else if (shortName == "D") {
            fullName = "Distributary";
        } else if (shortName == "E") {
            fullName = "Escape";
        } else if (shortName == "SM") {
            fullName = "Sub Minor";
        } else if (shortName == " ") {
            fullName = "Others";
        } else {
            fullName = shortName;
        }
        return fullName;
    }

    me.highlightFeature = function (e) {
        var layer = e.target;
        layer.setStyle({
            weight: 5,
            color: '#ffff00',
        });
        if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
            layer.bringToFront();
        }
    }

    me.selectHighlightGridRow = function (gridId, fieldName, fieldValue) {
        var grid = Ext.getCmp(gridId);
        var targetRowIndex = grid.store.find(fieldName, fieldValue);
        // var myFilters = [{
        //     type: 'string',
        //     dataIndex: fieldName,
        //     value: fieldValue
        // }];
        // grid.filters.clearFilters();
        // grid.filters.filter;
        // grid.filters.addFilters(myFilters);
        var x = grid.getView().getScrollX();
        grid.getView().scrollTo(x, targetRowIndex * 21, true);
        grid.getSelectionModel().select(targetRowIndex);
        // var myFilters = [{
        //     type: 'string',
        //     dataIndex: fieldName,
        //     value: fieldValue
        // }];
        // grid.filters.clearFilters();
        // grid.filters.filter;
        // grid.filters.addFilters(myFilters);
    }

    me.resetHighlight = function (e) {
        canalsLayer.resetStyle(e.target);
        // me.info.update();
    }

    me.zoomToFeature = function (e) {
        // me.llMap.fitBounds(e.target.getBounds());
        // me.info.update(e.target.feature.properties);
    }

    me.onEachFeature = function (feature, layer) {
        layer.on({
            mouseover: me.highlightFeature,
            mouseout: me.resetHighlight,
            click: me.getAttributeForm
        });
    }

    me.getCanalSize = function (type) {
        return type == "MC" ? 4 :
            type == "BC" ? 2 :
                type == "D" ? 1.5 :
                    type == "M" ? 1.5 :
                        type == "SM" ? 1 :
                            type == "E" ? 0.5 :
                                type == " " ? 0.5 : 0.5;
    }

    me.getCanalColor = function (type) {
        return type == "M" ? '#0064ff' :
            type == "SM" ? '#00ffff' :
                type == "MC" ? '#000032' :
                    type == "BC" ? '#000096' :
                        type == "D" ? '#0000ff' :
                            type == "E" ? '#96ffff' :
                                type == " " ? '#000000' :
                                    '#000000';
    }

    me.getCanalStyle = function (feature) {
        return {
            color: me.getCanalColor(feature.properties.channel_type),
            weight: me.getCanalSize(feature.properties.channel_type),
            opacity: 1
        };
    }

    me.setMapExtents = function (minx, miny, maxx, maxy) {
        var southWest = L.latLng(miny, minx),
            northEast = L.latLng(maxy, maxx),
            bounds = L.latLngBounds(southWest, northEast);
        llMap.fitBounds(bounds, {padding: [10, 10]});
    }

    me.drawLineOnMap = function (record) {
        me.reMoveLayer(me.lineGeom);
        var geojsonText = record.data.geojson;
        var geojson = JSON.parse(geojsonText);
        var coordList = geojson.coordinates[0];
        var pointList = me.getLinePointsArray(coordList);
        me.lineGeom = new L.Polyline(pointList, {
            color: '#ffff00',
            weight: 8,
            opacity: 0.8,
            smoothFactor: 1
        }).addTo(llMap);
        var extent = me.lineGeom.getBounds();
        llMap.fitBounds(extent);
    }

    me.drawMarkerOnMap = function (coordList) {
        me.reMoveLayer(me.detailMarker);
        if (coordList) {
            var damIcon = L.icon({
                iconUrl: '/static/ferrp/img/irrigation/flashmarker.gif',
                iconSize: [10, 10], // size of the icon
            });
            me.detailMarker = L.marker([coordList[1], coordList[0]], {icon: damIcon}).addTo(llMap);
        } else {
            console.log('Geom not available');
        }
    }

    me.drawCanalDetailGeomOnMap = function (record, dataTaype) {
        var geoJsonText = record.data.geojson;
        var geojson = JSON.parse(geoJsonText);
        var coordList = geojson.coordinates;
        if (dataTaype == 'canal_l_section' || dataTaype == 'canal_row') {
            me.drawLineOnMap(record);
        } else {
            me.drawMarkerOnMap(coordList);
        }
    }

    me.getLinePointsArray = function (line) {
        var pointList = new Array();
        if (line) {
            for (var i = 0; i < line.length; i++) {
                var transPointArray = new Array();
                var point = L.point(line[i][0], line[i][1]);
                var transformedPoint = L.Projection.SphericalMercator.unproject(point);
                transPointArray.push(transformedPoint.lat);
                transPointArray.push(transformedPoint.lng);
                pointList.push(transPointArray);
            }
        } else {
            alert("No line selected.");
        }
        return pointList;
    }
    me.getLinePointsArrayFromGeoJson = function (line) {
        var pointList = new Array();
        if (line) {
            for (var i = 0; i < line.length; i++) {
                var transPointArray = new Array();
                var point = L.point(line[i][0], line[i][1]);
                var transformedPoint = L.Projection.SphericalMercator.unproject(point);
                transPointArray.push(transformedPoint.lng);
                transPointArray.push(transformedPoint.lat);
                pointList.push(transPointArray);
            }
        } else {
            alert("No line selected.");
        }
        return pointList;
    }

    me.reMoveLayer = function (layer) {
        if (layer) {
            llMap.removeLayer(layer);
        }
    }

    me.removeAllLayers = function () {
        if (me.selectionLayer) {
            me.selectionLayer.clearLayers();
        }
        if (me.marker) {
            llMap.removeLayer(me.marker);
        }
        if (me.detailMarker) {
            llMap.removeLayer(me.detailMarker);
        }
        if (me.xsLine) {
            llMap.removeLayer(me.xsLine);
        }
        if (me.canalDetailsLayer) {
            llMap.removeLayer(me.canalDetailsLayer);
        }

    }

    // Data panel functions
    me.getCanalsDataPanel = function (data) {
        var gridColumns = new ArzGridColumns();
        me.globalFunctions = new ArzGlobalFunctionsModel();
        var store = Ext.create('Ext.data.Store', {
            id: 'canalsDataStore',
            fields: me.globalFunctions.getFieldsList(data[0]),
            data: data,
            groupField: 'zone_name'
        });
        var gridPanel = Ext.create('Ext.grid.Panel', {
            layout: 'fit',
            id: 'canalsDataPanel',
            title: 'Irrigation Canals',
            titleAlign: 'center',
            store: store,
            stripeRows: true,
            multiSelect: true,
            columnLines: true,
            plugins: ['gridfilters'],
            autoScroll: true,
            loadMask: true,
            listeners: {
                select: function (selModel, record, index, options) {
                    // me.imisCode = record.data.imis_code;
                    me.gridSelectionModel = selModel;
                    me.imisCode = [];
                    me.canalRecord = record;
                    me.selectionLayer.clearLayers();
                    me.selectionSet = [];
                    if (selModel.selected.items.length > 1) {
                        for (key in selModel.selected.items) {
                            var row = selModel.selected.items[key];
                            me.imisCode.push(row.data.imis_code);
                            var geojson = JSON.parse(row.data.geojson);
                            var coordsList = me.getLinePointsArrayFromGeoJson(geojson.coordinates[0]);
                            me.selectionSet.push({
                                "type": "Feature",
                                "properties": row.data,
                                "geometry": {"type": "LineString", "coordinates": coordsList}
                            });
                        }
                        me.selectionLayer.addData({type: 'FeatureCollection', features: me.selectionSet});
                    } else {
                        me.imisCode.push(record.data.imis_code);
                        var geojson = JSON.parse(record.data.geojson);
                        var coordsList = me.getLinePointsArrayFromGeoJson(geojson.coordinates[0]);
                        me.selectionSet.push({
                            "type": "Feature",
                            "properties": record.data,
                            "geometry": {"type": "LineString", "coordinates": coordsList}
                        });
                        me.selectionLayer.addData({type: 'FeatureCollection', features: me.selectionSet});
                        // me.drawLineOnMap(record);
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
                        // alert(exportData.length);
                        alasql("SELECT * INTO XLSX('canals_data_table.xlsx',{headers:true}) FROM ? ", [exportData]);
                    }
                },
                {
                    icon: imgPath + '15.png',
                    tooltip: 'email data link',
                    handler: function () {
                        me.dataType = 'canal';
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
                        me.dataType = 'canal';
                        me.whereClause = 'null';
                        var filtersArray = me.globalFunctions.getGridFiltersList(gridPanel);
                        // me.globalFunctions.getSMSForm(me.dataType, me.whereClause, filtersArray);
                        $("#dataType").val(me.dataType);
                        $("#whereClause").val(me.whereClause);
                        $("#filtersArray").val(filtersArray);
                        $('#smsModal').modal('show');
                    }

                }, '-',
                {
                    icon: imgPath + '02.png',
                    tooltip: 'query canal data',
                    // iconMask: true,
                    handler: function () {
                        var reportModel = new ArzCanalQueryModel();
                        reportModel.createQueryWindow();
                    }
                }, '-',
                // {
                //     icon: imgPath + '01.png',
                //     tooltip: 'canal L section detail',
                //     iconMask: true,
                //     handler: function () {
                //         // me.setGridBackGroundColor('');
                //         if (me.imisCode) {
                //             me.dataType = 'canal_l_section';
                //             var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
                //             var url = '../lsection?code=' + me.imisCode.toString();
                //             Ext.Ajax.timeout = 900000;
                //             Ext.Ajax.request({
                //                 url: url,
                //                 method: "GET",
                //                 success: function (response) {
                //                     box.hide();
                //                     me.removeAllLayers();
                //                     var extent = me.getExtentFromSelectionModel(me.gridSelectionModel);
                //                     me.zoomToExtent(extent);
                //                     var respText = response.responseText;
                //                     var respnseText = eval('(' + JXG.decompress(respText) + ')');
                //                     if (respnseText != "false") {
                //                         var data = JSON.parse(respnseText.lSectionData);
                //                         var geoJsonData = JSON.parse(respnseText.lSectionGeoJson);
                //                         geoJsonData = geoJsonData[0].geojson;
                //                         var dataPanel = Ext.getCmp("pnlLSectionData");
                //                         dataPanel.removeAll();
                //                         if (me.canalDetailsLayer) {
                //                             me.reMoveLayer(me.canalDetailsLayer);
                //                             layerControl.removeLayer(me.canalDetailsLayer);
                //                         }
                //                         if (geoJsonData) {
                //                             me.canalDetailsLayer = me.canalsDetailMapLayer.getCanalsDetailLayer('L Section', geoJsonData);
                //                             me.canalDetailsLayer.addTo(llMap);
                //                             layerControl.addOverlay(me.canalDetailsLayer, 'L Sections');
                //                         }
                //                         if (data.length > 0) {
                //                             var detailDataPanel = me.createCanalsDetailDataPanel(data, 'L Section Detail', 'l_section');
                //                             dataPanel.add(detailDataPanel);
                //                         } else {
                //                             Ext.MessageBox.alert("Warning", "No record found.");
                //                         }
                //                     }
                //                 },
                //                 failure: function (res) {
                //                     box.hide();
                //                 }
                //             });
                //         } else {
                //             alert('Please select a row first.');
                //         }
                //     }
                // },
                // {
                //     icon: imgPath + '06.png',
                //     tooltip: 'canal gates detail',
                //     iconMask: true,
                //     handler: function () {
                //         me.dataType = 'canal_gates';
                //         if (me.imisCode) {
                //             var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
                //             var url = '../gates?code=' + me.imisCode.toString();
                //             Ext.Ajax.timeout = 900000;
                //             Ext.Ajax.request({
                //                 url: url,
                //                 method: "GET",
                //                 success: function (response) {
                //                     box.hide();
                //                     me.removeAllLayers();
                //                     var extent = me.getExtentFromSelectionModel(me.gridSelectionModel);
                //                     me.zoomToExtent(extent);
                //                     var respText = response.responseText;
                //                     var respnseText = eval('(' + JXG.decompress(respText) + ')');
                //                     if (respnseText != "false") {
                //                         var data = JSON.parse(respnseText.gatesData);
                //                         var geoJsonData = JSON.parse(respnseText.gatesGeoJson);
                //                         geoJsonData = geoJsonData[0].geojson;
                //                         var dataPanel = Ext.getCmp("pnlLSectionData");
                //                         dataPanel.removeAll();
                //                         if (me.canalDetailsLayer) {
                //                             me.reMoveLayer(me.canalDetailsLayer);
                //                             layerControl.removeLayer(me.canalDetailsLayer);
                //                         }
                //                         if (geoJsonData) {
                //                             me.canalDetailsLayer = me.canalsDetailMapLayer.getCanalsDetailLayer('Gates', geoJsonData);
                //                             me.canalDetailsLayer.addTo(llMap);
                //                             layerControl.addOverlay(me.canalDetailsLayer, 'Gates');
                //                         }
                //
                //                         if (data.length > 0) {
                //                             var detailDataPanel = me.createCanalsDetailDataPanel(data, 'Gates Detail', 'gates');
                //                             dataPanel.add(detailDataPanel);
                //                         } else {
                //                             Ext.MessageBox.alert("Warning", "No record found.");
                //                         }
                //                     }
                //                 },
                //                 failure: function (res) {
                //                     box.hide();
                //                 }
                //             });
                //         } else {
                //             alert('Please select a row first.');
                //         }
                //     }
                // },
                // {
                //     icon: imgPath + '07.png',
                //     tooltip: 'canal guages detail',
                //     iconMask: true,
                //     handler: function () {
                //         me.dataType = 'canal_guages';
                //         if (me.imisCode) {
                //             var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
                //             var url = '../guages?code=' + me.imisCode.toString();
                //             Ext.Ajax.timeout = 900000;
                //             Ext.Ajax.request({
                //                 url: url,
                //                 method: "GET",
                //                 success: function (response) {
                //                     box.hide();
                //                     me.removeAllLayers();
                //                     var extent = me.getExtentFromSelectionModel(me.gridSelectionModel);
                //                     me.zoomToExtent(extent);
                //                     var respText = response.responseText;
                //                     var respnseText = eval('(' + JXG.decompress(respText) + ')');
                //                     if (respnseText != "false") {
                //                         var data = JSON.parse(respnseText.gaugesData);
                //                         var geoJsonData = JSON.parse(respnseText.gaugesGeoJson);
                //                         geoJsonData = geoJsonData[0].geojson;
                //                         var dataPanel = Ext.getCmp("pnlLSectionData");
                //                         dataPanel.removeAll();
                //                         if (me.canalDetailsLayer) {
                //                             me.reMoveLayer(me.canalDetailsLayer);
                //                             layerControl.removeLayer(me.canalDetailsLayer);
                //                         }
                //                         if (geoJsonData) {
                //                             me.canalDetailsLayer = me.canalsDetailMapLayer.getCanalsDetailLayer('Gauges', geoJsonData);
                //                             me.canalDetailsLayer.addTo(llMap);
                //                             layerControl.addOverlay(me.canalDetailsLayer, 'Gauges');
                //                         }
                //                         if (data.length > 0) {
                //                             var detailDataPanel = me.createCanalsDetailDataPanel(data, 'Guages Detail', 'gauges');
                //                             dataPanel.add(detailDataPanel);
                //                         } else {
                //                             Ext.MessageBox.alert("Warning", "No record found.");
                //                         }
                //                     }
                //                 },
                //                 failure: function (res) {
                //                     box.hide();
                //                 }
                //             });
                //         } else {
                //             alert('Please select a row first.');
                //         }
                //     }
                // },
                // {
                //     icon: imgPath + '11.png',
                //     tooltip: 'Canal right of way detail',
                //     iconMask: true,
                //     handler: function () {
                //         me.dataType = 'canal_row';
                //         if (me.imisCode) {
                //             var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
                //             var url = '../row?code=' + me.imisCode.toString();
                //             Ext.Ajax.timeout = 900000;
                //             Ext.Ajax.request({
                //                 url: url,
                //                 method: "GET",
                //                 success: function (response) {
                //                     box.hide();
                //                     me.removeAllLayers();
                //                     var extent = me.getExtentFromSelectionModel(me.gridSelectionModel);
                //                     me.zoomToExtent(extent);
                //                     var respText = response.responseText;
                //                     var respnseText = eval('(' + JXG.decompress(respText) + ')');
                //                     if (respnseText != "false") {
                //                         var data = respnseText;
                //                         if (data.length > 0) {
                //                             var detailDataPanel = me.createCanalsDetailDataPanel(data, 'Right of way Detail', 'row');
                //                             dataPanel.add(detailDataPanel);
                //                         } else {
                //                             Ext.MessageBox.alert("Warning", "No record found.");
                //                         }
                //                     }
                //                 },
                //                 failure: function (res) {
                //                     box.hide();
                //                 }
                //             });
                //         } else {
                //             alert('Please select a row first.');
                //         }
                //     }
                // },
                // {
                //     icon: imgPath + '16.png',
                //     tooltip: 'canal structure detail',
                //     iconMask: true,
                //     handler: function () {
                //         me.dataType = 'canal_structure';
                //         if (me.imisCode) {
                //             var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
                //             var url = '../structure?code=' + me.imisCode.toString();
                //             Ext.Ajax.timeout = 900000;
                //             Ext.Ajax.request({
                //                 url: url,
                //                 method: "GET",
                //                 success: function (response) {
                //                     box.hide();
                //                     me.removeAllLayers();
                //                     var extent = me.getExtentFromSelectionModel(me.gridSelectionModel);
                //                     me.zoomToExtent(extent);
                //                     var respText = response.responseText;
                //                     var respnseText = eval('(' + JXG.decompress(respText) + ')');
                //                     if (respnseText != "false") {
                //                         var data = JSON.parse(respnseText.structureData);
                //                         var geoJsonData = JSON.parse(respnseText.structureGeoJson);
                //                         geoJsonData = geoJsonData[0].geojson;
                //                         var dataPanel = Ext.getCmp("pnlLSectionData");
                //                         dataPanel.removeAll();
                //                         if (me.canalDetailsLayer) {
                //                             me.reMoveLayer(me.canalDetailsLayer);
                //                             layerControl.removeLayer(me.canalDetailsLayer);
                //                         }
                //                         if (geoJsonData) {
                //                             me.canalDetailsLayer = me.canalsDetailMapLayer.getCanalsDetailLayer('Structure', geoJsonData);
                //                             me.canalDetailsLayer.addTo(llMap);
                //                             layerControl.addOverlay(me.canalDetailsLayer, 'Structure');
                //                         }
                //                         if (data.length > 0) {
                //                             var detailDataPanel = me.createCanalsDetailDataPanel(data, 'Structure Detail', 'structure');
                //                             dataPanel.add(detailDataPanel);
                //                         } else {
                //                             Ext.MessageBox.alert("Warning", "No record found.");
                //                         }
                //                     }
                //                 },
                //                 failure: function (res) {
                //                     box.hide();
                //                 }
                //             });
                //         } else {
                //             alert('Please select a row first.');
                //         }
                //     }
                // },
                // {
                //     icon: imgPath + '03.png',
                //     tooltip: 'canal outlets detail',
                //     iconMask: true,
                //     handler: function () {
                //         me.dataType = 'outlets';
                //         if (me.imisCode) {
                //             var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
                //             var url = '../outlets?code=' + me.imisCode.toString();
                //             Ext.Ajax.timeout = 900000;
                //             Ext.Ajax.request({
                //                 url: url,
                //                 method: "GET",
                //                 success: function (response) {
                //                     box.hide();
                //                     me.removeAllLayers();
                //                     var extent = me.getExtentFromSelectionModel(me.gridSelectionModel);
                //                     me.zoomToExtent(extent);
                //                     var respText = response.responseText;
                //                     var respnseText = eval('(' + JXG.decompress(respText) + ')');
                //                     if (respnseText != "false") {
                //                         var data = JSON.parse(respnseText.outletsData);
                //                         var geoJsonData = JSON.parse(respnseText.outletsGeoJson);
                //                         geoJsonData = geoJsonData[0].geojson;
                //                         var dataPanel = Ext.getCmp("pnlLSectionData");
                //                         dataPanel.removeAll();
                //                         if (me.canalDetailsLayer) {
                //                             me.reMoveLayer(me.canalDetailsLayer);
                //                             layerControl.removeLayer(me.canalDetailsLayer);
                //                         }
                //                         if (geoJsonData) {
                //                             me.canalDetailsLayer = me.canalsDetailMapLayer.getCanalsDetailLayer('Outlets', geoJsonData);
                //                             me.canalDetailsLayer.addTo(llMap);
                //                             layerControl.addOverlay(me.canalDetailsLayer, 'Outlets');
                //                         }
                //                         if (data.length > 0) {
                //                             var detailDataPanel = me.createCanalsDetailDataPanel(data, 'Outlets Detail', 'outlets');
                //                             dataPanel.add(detailDataPanel);
                //                         } else {
                //                             Ext.MessageBox.alert("Warning", "No record found.");
                //                         }
                //                     }
                //                 },
                //                 failure: function (res) {
                //                     box.hide();
                //                 }
                //             });
                //         } else {
                //             alert('Please select a row first.');
                //         }
                //     }
                // }, '-',
                {
                    text: 'Group by ...',
                    id: 'btnGroupBy',
                    menu: {
                        items: [{
                            text: 'L Section',
                            icon: imgPath + '01.png',
                            handler: function () {
                                me.dataType = 'canal_l_section';
                                gridPanel.store.group('is_l_section');
                                Ext.getCmp('btnGroupBy').setText('Grouped By L Section');
                            }
                        }, {
                            text: 'Gate',
                            icon: imgPath + '06.png',
                            handler: function () {
                                me.dataType = 'canal_gates';
                                gridPanel.store.group('is_gate');
                                Ext.getCmp('btnGroupBy').setText('Grouped By Gates');
                            }
                        }, {
                            text: 'Gauge',
                            icon: imgPath + '07.png',
                            handler: function () {
                                me.dataType = 'canal_guages';
                                gridPanel.store.group('is_gauge');
                                Ext.getCmp('btnGroupBy').setText('Grouped By Gauges');
                            }
                        }, {
                            text: 'ROW',
                            icon: imgPath + '11.png',
                            handler: function () {
                                me.dataType = 'canal_row';
                                gridPanel.store.group('is_row');
                                Ext.getCmp('btnGroupBy').setText('Grouped By ROW');
                            }
                        }, {
                            text: 'Structure',
                            icon: imgPath + '16.png',
                            handler: function () {
                                me.dataType = 'canal_structure';
                                gridPanel.store.group('is_structure');
                                Ext.getCmp('btnGroupBy').setText('Grouped By Structure');
                            }
                        }, {
                            text: 'Outlet',
                            icon: imgPath + '03.png',
                            handler: function () {
                                me.dataType = 'outlets';
                                gridPanel.store.group('is_outlet');
                                Ext.getCmp('btnGroupBy').setText('Grouped By Outlets');
                            }
                        }]
                    }
                },
                {
                    tooltip: 'Get group by detail of selected canal',
                    icon: imgPath + 'getdetail-color-16.png',
                    iconMask: true,
                    handler: function () {
                        if (me.imisCode) {
                            var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
                            var url = '../canal_detail_data?code=' + me.imisCode.toString() + '&type=' + me.dataType;
                            Ext.Ajax.timeout = 900000;
                            Ext.Ajax.request({
                                url: url,
                                method: "GET",
                                success: function (response) {
                                    box.hide();
                                    me.removeAllLayers();
                                    var extent = me.getExtentFromSelectionModel(me.gridSelectionModel);
                                    me.zoomToExtent(extent);
                                    var respText = response.responseText;
                                    var respnseText = eval('(' + JXG.decompress(respText) + ')');
                                    if (respnseText != "false") {
                                        var data = JSON.parse(respnseText.data);
                                        var geoJsonData = JSON.parse(respnseText.geojson);
                                        geoJsonData = geoJsonData[0].geojson;
                                        var dataPanel = Ext.getCmp("pnlLSectionData");
                                        dataPanel.removeAll();
                                        if (me.canalDetailsLayer) {
                                            me.reMoveLayer(me.canalDetailsLayer);
                                            layerControl.removeLayer(me.canalDetailsLayer);
                                        }
                                        if (me.dataType == 'canal_l_section') {
                                            if (geoJsonData) {
                                                me.canalDetailsLayer = me.canalsDetailMapLayer.getCanalsDetailLayer('L Section', geoJsonData);
                                                me.canalDetailsLayer.addTo(llMap);
                                                layerControl.addOverlay(me.canalDetailsLayer, 'L Sections');
                                            }
                                            if (data.length > 0) {
                                                var detailDataPanel = me.createCanalsDetailDataPanel(data, 'L Section Detail', 'l_section');
                                                dataPanel.add(detailDataPanel);
                                            }
                                        }
                                        if (me.dataType == 'canal_gates') {
                                            if (geoJsonData) {
                                                me.canalDetailsLayer = me.canalsDetailMapLayer.getCanalsDetailLayer('Gates', geoJsonData);
                                                me.canalDetailsLayer.addTo(llMap);
                                                layerControl.addOverlay(me.canalDetailsLayer, 'Gates');
                                            }
                                            if (data.length > 0) {
                                                var detailDataPanel = me.createCanalsDetailDataPanel(data, 'Gates Detail', 'gates');
                                                dataPanel.add(detailDataPanel);
                                            }
                                        }
                                        if (me.dataType == 'canal_guages') {
                                            if (geoJsonData) {
                                                me.canalDetailsLayer = me.canalsDetailMapLayer.getCanalsDetailLayer('Gauges', geoJsonData);
                                                me.canalDetailsLayer.addTo(llMap);
                                                layerControl.addOverlay(me.canalDetailsLayer, 'Gauges');
                                            }
                                            if (data.length > 0) {
                                                var detailDataPanel = me.createCanalsDetailDataPanel(data, 'Gauges Detail', 'gauges');
                                                dataPanel.add(detailDataPanel);
                                            }
                                        }
                                        if (me.dataType == 'canal_row') {
                                            if (data.length > 0) {
                                                var detailDataPanel = me.createCanalsDetailDataPanel(data, 'Right of way Detail', 'row');
                                                dataPanel.add(detailDataPanel);
                                            }
                                        }
                                        if (me.dataType == 'canal_structure') {
                                            if (geoJsonData) {
                                                me.canalDetailsLayer = me.canalsDetailMapLayer.getCanalsDetailLayer('Structure', geoJsonData);
                                                me.canalDetailsLayer.addTo(llMap);
                                                layerControl.addOverlay(me.canalDetailsLayer, 'Structure');
                                            }
                                            if (data.length > 0) {
                                                var detailDataPanel = me.createCanalsDetailDataPanel(data, 'Structure Detail', 'structure');
                                                dataPanel.add(detailDataPanel);
                                            }
                                        }
                                        if (me.dataType == 'outlets') {
                                            if (geoJsonData) {
                                                me.canalDetailsLayer = me.canalsDetailMapLayer.getCanalsDetailLayer('Outlets', geoJsonData);
                                                me.canalDetailsLayer.addTo(llMap);
                                                layerControl.addOverlay(me.canalDetailsLayer, 'Outlets');
                                            }
                                            if (data.length > 0) {
                                                var detailDataPanel = me.createCanalsDetailDataPanel(data, 'Outlets Detail', 'outlets');
                                                dataPanel.add(detailDataPanel);
                                            }
                                        }

                                    }
                                },
                                failure: function (res) {
                                    box.hide();
                                }
                            });
                        } else {
                            alert('Please select a row first.');
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
                    tooltip: 'DeSelect All',
                    icon: imgPath + 'deselect_all_16.png',
                    iconMask: true,
                    handler: function () {
                        me.selectionLayer.clearLayers();
                        gridPanel.getSelectionModel().deselectAll();
                        gridPanel.filters.clearFilters();
                    }
                }, '-',
            ],
            columns: gridColumns.getCanalsColumnsList(),
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
        var dataPanel = Ext.getCmp("pnlCanalsData");
        dataPanel.removeAll();
        dataPanel.add(gridPanel);
    }

    me.groupGridDataBy = function (field) {
        var store = Ext.getCmp('canalDetailDataPanel');
        store.group(field);
    }

    me.setGridBackGroundColor = function (dataType) {

        var grid = Ext.getCmp('canalsDataPanel');
        for (var i = 0; i < grid.getStore().data.length; i++) {
            var element = Ext.get(grid.getView().getRow(i));
            element.setStyle('background-color', 'yellow');
        }
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
                    color: "white",
                    weight: 2,
                    opacity: 0.7,
                    fillOpacity: 0.8,
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
        // return selectionStyles[feature.geometry.type];
    };

    me.createCanalsDetailDataPanel = function (data, type, columns) {

        var southPanel = Ext.getCmp("southCanalDetailPanel");
        southPanel.setTitle(type);
        southPanel.expand();

        var columnsList = me.getCanalsDataColumnsList(columns);
        var store = Ext.create('Ext.data.Store', {
            id: 'canalDetailDataStore',
            fields: me.globalFunctions.getFieldsList(data[0]),
            data: data,
        });

        var canalDataPanel = Ext.create('Ext.grid.Panel', {
            id: 'canalDetailDataPanel',
            name: 'canalDetailDataPanel',
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
                    cls: 'btnPT',
                    handler: function () {
                        var ptData = canalDataPanel.getStore().data;
                        var gridData = me.globalFunctions.getDataFromGridItems(ptData);
                        me.globalFunctions.createPivotTableWindow(gridData);
                    }
                }, '-',
                {
                    tooltip: 'Export to Excel',
                    icon: imgPath + 'EXCLE.png',
                    handler: function () {
                        // var gridData = canalDataPanel.getStore().config.data;
                        var data = canalDataPanel.getStore().data;
                        var exportData = me.globalFunctions.getDataFromGridItems(data);
                        alasql("SELECT * INTO XLSX('" + me.dataType + "_data_table.xlsx',{headers:true}) FROM ? ", [exportData]);
                    }
                },
                {
                    icon: imgPath + '15.png',
                    tooltip: 'email data link',
                    handler: function () {
                        me.whereClause = "imis_code = '" + me.imisCode + "'";
                        var filtersArray = me.globalFunctions.getGridFiltersList(canalDataPanel);
                        me.globalFunctions.getEmailForm(me.dataType, me.whereClause, filtersArray);
                    }
                },
                {
                    icon: imgPath + '05.png',
                    tooltip: 'sms data link',
                    handler: function () {
                        me.whereClause = "imis_code = '" + me.imisCode + "'";
                        var filtersArray = me.globalFunctions.getGridFiltersList(canalDataPanel);
                        me.globalFunctions.getSMSForm(me.dataType, me.whereClause, filtersArray);
                    }
                }
            ],
            listeners: {
                select: function (selModel, record, index, options) {
                    me.drawCanalDetailGeomOnMap(record, me.dataType)
                }
            },
            columns: columnsList,
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
        return canalDataPanel;
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

    me.getExtentFromSelectionModel = function (selectionModel) {
        var xmin = 0, ymin = 0, xmax = 0, ymax = 0;
        var selectionLength = selectionModel.selected.items.length;
        if (selectionLength > 1) {
            for (var i = 0; i < selectionLength; i++) {
                var row = selectionModel.selected.items[i];
                var extent = row.data.extent;
                var arrExtent = extent.split(',');
                var minx = parseFloat(arrExtent[0]);
                var miny = parseFloat(arrExtent[1]);
                if (i == 0) {
                    xmin = minx;
                    ymin = miny;
                }
                var maxx = parseFloat(arrExtent[2]);
                var maxy = parseFloat(arrExtent[3]);
                if (minx < xmin) {
                    xmin = minx;
                }
                if (miny < ymin) {
                    ymin = miny;
                }
                if (maxx > xmax) {
                    xmax = maxx;
                }
                if (maxy > ymax) {
                    ymax = maxy;
                }
            }
            return xmin + ',' + ymin + ',' + xmax + ',' + ymax
        } else {
            return selectionModel.selected.items[0].data.extent
        }

    }

    me.zoomToExtent = function (extent) {
        // var extent = record.data.extent;
        var arrExtent = extent.split(',');
        var minx = parseFloat(arrExtent[0]);
        var miny = parseFloat(arrExtent[1]);
        var maxx = parseFloat(arrExtent[2]);
        var maxy = parseFloat(arrExtent[3]);
        me.setMapExtents(minx, miny, maxx, maxy);
    }

    me.contextMenu = function (record) {
        var contextMenu = Ext.create('Ext.menu.Menu', {
            items: [
                {
                    text: 'Zoom to feature',
                    handler: function () {
                        me.zoomToExtent(record);
                    }
                }
            ]
        });
        return contextMenu;
    }

    me.setMapExtents = function (minx, miny, maxx, maxy) {
        var southWest = L.latLng(miny, minx),
            northEast = L.latLng(maxy, maxx),
            bounds = L.latLngBounds(southWest, northEast);
        llMap.fitBounds(bounds, {padding: [10, 10]});
    }

    me.drawXSLineOnMap = function (e) {
        var _xsStyle = {
            color: '#fc0466',
            weight: 5,
            opacity: .8,
            lineJoin: 'round',
        };
        if (me.xsLine) {
            llMap.removeLayer(me.xsLine);
        }
        me.xsPointsArray.push(e.latlng);
        me.xsLine = L.polyline(me.xsPointsArray, _xsStyle).addTo(llMap);
    }

    me.getWKT = function () {
        var wkt = "LINESTRING(";
        for (var i = 0; i < me.xsPointsArray.length; i++) {
            var point = me.xsPointsArray[i];
            if (i != me.xsPointsArray.length - 1) {

                wkt = wkt + point.lng + " " + point.lat + ",";
            } else {
                wkt = wkt + point.lng + " " + point.lat;
            }
        }
        wkt = wkt + ")";
        return wkt;
    }

    me.getHeightProfile = function (geom) {
        var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
        var url = '../linedemprofile?wkt=' + geom;
        Ext.Ajax.timeout = 900000;
        Ext.Ajax.request({
            url: url,
            method: "GET",
            success: function (response) {
                box.hide();
                var respText = response.responseText;
                var respnseText = eval('(' + JXG.decompress(respText) + ')');
                if (respnseText !== "false") {
                    var profileArray = new Array();
                    me.xsProfileData = respnseText;
                    profileArray = me.getXSProfileArray(me.xsProfileData);
                    me.getProfileHighGraph(profileArray);
                }
            },
            failure: function (res) {
                Ext.MessageBox.hide();
            }
        });
    }

    me.getXSProfileArray = function (data) {
        var dataset = new Array();
        var dataRecord = {};
        var profileArray = new Array();

        for (var i = 0; i < data.length; i++) {
            var record = new Array();
            record.push(data[i].distance);
            record.push(data[i].height);
            profileArray.push(record);
        }
        dataRecord = {
            name: "Height Profile",
            data: profileArray
        };
        dataset.push(dataRecord);
        return dataset;
    }

    me.getProfileHighGraph = function (data) {
        var southPanel = Ext.getCmp('southCanalXSProfilePanel');
        southPanel.expand();
        if (me.profileHighGraph) {
            for (var i = me.profileHighGraph.series.length - 1; i > -1; i--) {
                me.profileHighGraph.series[i].remove();
            }
            me.profileHighGraph.addSeries({data: data[0].data, name: data[0].name}, true);
            me.profileHighGraph.redraw();
        } else {
            me.createHighGraph(data);
        }
    }

    me.createHighGraph = function (data) {
        var graphDiv = Ext.getCmp('pnlXSProfile').body.dom;
        me.profileHighGraph = Highcharts.chart(graphDiv, {
            chart: {
                type: 'area',
                zoomType: 'x'
            },
            title: {
                text: 'Line Height Profile'
            },
            // subtitle: {
            //     text: document.ontouchstart === undefined ?
            //         'Click and drag in the plot area to zoom in' : 'Pinch the chart to zoom in'
            // },
            xAxis: {
                type: 'integer'
            },
            yAxis: {
                title: {
                    text: 'Height(meters)'
                }
            },
            legend: {
                enabled: true
            },
            plotOptions: {
                series: {
                    cursor: 'pointer',
                    point: {
                        events: {
                            click: function () {
                                me.drawPointOnMap(this.x, this.y);
                            }
                        }
                    }
                },
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
            series: data
        });
    }

    me.drawPointOnMap = function (distance, height) {
        var data = _.where(me.xsProfileData, {height: height, distance: distance});
        if (me.marker) {
            llMap.removeLayer(me.marker);
        }
        var point = L.point(data[0].pt_x, data[0].pt_y, 0);
        var coords4326 = L.Projection.SphericalMercator.unproject(point);
        llMap.setView([coords4326.lat, coords4326.lng], 14);
        me.marker = L.marker([coords4326.lat, coords4326.lng]).addTo(llMap);
        me.marker.bindPopup("<b>Point Info!</b><br>Height:" + height + ", Distance:" + distance + ".").openPopup();
    }

    me.getCanalsDataColumnsList = function (dataType) {
        var gridColumns = new ArzGridColumns();
        if (dataType == 'l_section') {
            return gridColumns.getLSectionColumnsList();
        }
        if (dataType == 'gates') {
            return gridColumns.getGatesColumnsList();
        }
        if (dataType == 'gauges') {
            return gridColumns.getGaugesColumnsList();
        }
        if (dataType == 'row') {
            return gridColumns.getROWColumnsList();
        }
        if (dataType == 'structure') {
            return gridColumns.getStructureColumnsList();
        }
        if (dataType == 'outlets') {
            return gridColumns.getOutletsColumnsList();
        } else {
            return null;
        }
    }
}

var ArzCanalQueryModel = function () {
    var me = this;
    me.win = null;
    me.statFunctions = new ArzGlobalFunctionsModel();

    me.createQueryWindow = function () {
        if (me.win != null) {
            me.win.destroy();
        }
        var reportForm = me.createReportForm();
        me.win = Ext.create('Ext.window.Window', {
            id: 'reportWin',
            title: 'View Report',
            layout: 'fit',
            x: 100,
            y: 90,
            width: 400,
            height: 280,
            closeAction: 'destroy',
            preventBodyReset: true,
            constrainHeader: true,
            collapsible: false,
            plain: true,
            items: reportForm
        });
        me.win.show();
    }

    me.getLevelName = function () {
        var cmbCircle = Ext.getCmp("cmbCircle").getRawValue();
        var cmbDivision = Ext.getCmp("cmbDivision").getRawValue();
        var cmbCanal = Ext.getCmp("cmbCanal").getRawValue();

        if (cmbCircle == '') {
            return 'zone_name';
        }
        if (cmbDivision == '') {
            return 'circle_name';
        }
        if (cmbCanal == '') {
            return 'division_name';
        } else {
            return 'channel_name';
        }
    }

    me.getLevelValue = function (levelName) {
        var cmbZoneValue = Ext.getCmp("cmbZone").getRawValue();
        var cmbCircleValue = Ext.getCmp("cmbCircle").getRawValue();
        var cmbDivisionValue = Ext.getCmp("cmbDivision").getRawValue();
        var cmbCanalValue = Ext.getCmp("cmbCanal").getRawValue();
        if (levelName == 'zone_name') {
            return cmbZoneValue;
        }
        if (levelName == 'circle_name') {
            return cmbCircleValue;
        }
        if (levelName == 'division_name') {
            return cmbDivisionValue;
        }
        if (levelName == 'channel_name') {
            return cmbCanalValue;
        }
    }

    me.getComboName = function () {
        var cmbCircle = Ext.getCmp("cmbCircle").getRawValue();
        var cmbDivision = Ext.getCmp("cmbDivision").getRawValue();
        var cmbCanal = Ext.getCmp("cmbCanal").getRawValue();

        if (cmbCircle == '') {
            return 'cmbZone';
        }
        if (cmbDivision == '') {
            return 'cmbCircle';
        }
        if (cmbCanal == '') {
            return 'cmbDivision';
        } else {
            return 'cmbCanal';
        }
    }

    me.getComboStore = function (storeId) {
        var featureStore = Ext.create('Ext.data.Store', {
            fields: [
                {name: 'id', type: 'string'},
                {name: 'name', type: 'string'},
                {name: 'extent', type: 'string'}
            ],
            id: storeId,
            data: []
        });
        return featureStore;
    }

    me.createReportForm = function () {
        var zoneStore = me.getComboStore('zoneStore');
        var circleStore = me.getComboStore('circleStore');
        var divisionStore = me.getComboStore('divisionStore');
        var canalStore = me.getComboStore('canalStore');
        populateZonesStore();

        var form = Ext.create('Ext.form.Panel', {
            layout: 'anchor',
            id: 'frmReport',
            defaults: {
                anchor: '100%'
            },
            bodyPadding: 20,
            items: [
                Ext.create('Ext.form.ComboBox', {
                    fieldLabel: 'Select Zone',
                    store: zoneStore,
                    id: 'cmbZone',
                    queryMode: 'local',
                    margin: '0 0 10 0',
                    emptyText: '<--Select Zone-->',
                    displayField: 'name',
                    valueField: 'id',
                    listeners: {
                        select: function (cmb, value) {
                            var id = value.data.name;
                            var whereClause = me.statFunctions.getReportWhereClause(id, "", "");
                            var data = me.statFunctions.getWhereClauseData(canalsData, whereClause);
                            var uniqueCircles = me.statFunctions.getUniqueValues(data, 'circle_name');
                            var store = me.statFunctions.getDataArray(uniqueCircles);
                            circleStore.removeAll();
                            circleStore.loadData(store);
                        }
                    }
                }),
                Ext.create('Ext.form.ComboBox', {
                    fieldLabel: 'Select Circle',
                    id: 'cmbCircle',
                    store: circleStore,
                    queryMode: 'local',
                    margin: '0 0 10 0',
                    emptyText: '<--All Circles-->',
                    displayField: 'name',
                    valueField: 'id',
                    listeners: {
                        select: function (cmb, value) {
                            var circle = value.data.name;
                            var zone = Ext.getCmp('cmbZone').getRawValue();
                            var whereClause = me.statFunctions.getReportWhereClause(zone, circle, "");
                            var data = me.statFunctions.getWhereClauseData(canalsData, whereClause);
                            var uniqueCircles = me.statFunctions.getUniqueValues(data, 'division_name');
                            var store = me.statFunctions.getDataArray(uniqueCircles);
                            divisionStore.removeAll();
                            divisionStore.loadData(store);
                        }
                    }
                }),
                Ext.create('Ext.form.ComboBox', {
                    fieldLabel: 'Select Division',
                    id: 'cmbDivision',
                    margin: '0 0 10 0',
                    emptyText: '<--All Divisions-->',
                    store: divisionStore,
                    queryMode: 'local',
                    displayField: 'name',
                    valueField: 'id',
                    listeners: {
                        select: function (cmb, value) {
                            var division = value.data.name;
                            var circle = Ext.getCmp('cmbCircle').getRawValue();
                            var zone = Ext.getCmp('cmbZone').getRawValue();
                            var whereClause = me.statFunctions.getReportWhereClause(zone, circle, division);
                            var data = me.statFunctions.getWhereClauseData(canalsData, whereClause);
                            var uniqueCircles = me.statFunctions.getUniqueValues(data, 'channel_name');
                            var store = me.statFunctions.getDataArray(uniqueCircles);
                            canalStore.removeAll();
                            canalStore.loadData(store);
                        }
                    }
                }), Ext.create('Ext.form.ComboBox',
                    {
                        fieldLabel: 'Select Canal',
                        id: 'cmbCanal',
                        margin: '0 0 10 0',
                        emptyText: '<--All Canals-->',
                        store: canalStore,
                        queryMode: 'local',
                        displayField: 'name',
                        valueField: 'id',
                        listeners: {
                            select: function (cmb, value) {
                                // var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
                                try {
                                    var id = value.data.id;
                                    // box.hide();
                                } catch (e) {
                                    // box.hide();
                                    console.error(e.stack);
                                }
                            }
                        }
                    }),
                {
                    xtype: 'button',
                    tooltip: "Get Data",
                    margin: '10, 0, 0, 0',
                    height: 30,
                    text: 'Get Data',
                    handler: function () {
                        var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
                        // me.canalsLeafLetMap = new ArzLeafletCanalMapModel();
                        try {
                            var cmbZone = Ext.getCmp("cmbZone").getRawValue();
                            if (cmbZone) {

                                // var combobox = Ext.getCmp(me.getComboName());
                                // var comboStore = combobox.store;
                                // var id = combobox.getValue();
                                // var record = comboStore.getById(id);
                                // var extent = record.data.extent;
                                // me.mapConfig.zoomToExtent(extent);

                                var levelName = me.getLevelName();
                                var levelValue = me.getLevelValue(levelName);
                                var whereClause = levelName + " = '" + levelValue + "'";

                                var myFilters = [{
                                    type: 'string',
                                    dataIndex: levelName,
                                    value: levelValue
                                }];
                                var grid = Ext.getCmp('canalsDataPanel');
                                grid.filters.clearFilters();
                                grid.filters.filter;
                                grid.filters.addFilters(myFilters);
                                var url = "../selectedcanalsgeojson?where=" + whereClause;
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
                                            var geojson = data[0].geojson;
                                            canalsLayer.clearLayers();
                                            canalsLayer.addData(data[0].geojson);
                                        }
                                    },
                                    failure: function (res) {
                                        box.hide();
                                        alert(res.responseText);
                                    }
                                });
                            } else {
                                box.hide();
                                alert("Please select a zone first.");
                            }
                        } catch (e) {
                            box.hide();
                            console.error(e.stack);
                        }
                    }
                },
                {
                    xtype: 'button',
                    tooltip: "Clear Filter",
                    margin: '5, 0, 0, 0',
                    height: 30,
                    text: 'Clear Filter',
                    handler: function () {
                        var grid = Ext.getCmp('canalsDataPanel');
                        grid.filters.clearFilters();
                        canalsLayer.clearLayers();
                        canalsLayer.addData(canalsGeoJson);
                    }
                }]
        });

        function populateZonesStore() {
            var zones = me.statFunctions.getUniqueValues(canalsData, 'zone_name');
            var store = me.statFunctions.getDataArray(zones);
            zoneStore.removeAll();
            zoneStore.loadData(store);
        }

        return form;
    }
}

var ArzCanalsDetailMapLayer = function () {
    var me = this;
    me.layerName = null;
    me.layerData = null;
    me.canalDetailsLayer = null;
    me.globalFunctions = new ArzGlobalFunctionsModel();

    me.lSectionSymbol = function (feature) {
        return {
            color: me.getCyanToBlue(feature.properties.from_rd_m),
            weight: 10,
            opacity: 1,
            lineJoin: 'round',
        }
    };
    me.rightOfWaySymbol = function () {
        return {
            color: me.getRandomColor(),
            weight: 5,
            opacity: 0.6,
            smoothFactor: 1,
            lineJoin: 'round',
        }
    };

    me.getLayerColor = function (layerName) {
        switch (layerName) {
            case 'Gauges':
                return '#ff0a58';
            case 'Gates':
                return '#ff8400';
            case 'Structure':
                return '#c8c832';
            case 'Outlets':
                return '#000064';
                return '#969600';
        }
    }

    me.getPointConstantSymbol = function (layerName) {
        return {
            radius: 12,
            fillColor: me.getLayerColor(layerName),
            color: "white",
            weight: 2,
            opacity: 1,
            fillOpacity: 0.8,
        }
    }

    me.getPointVariableSymbol = function (propertyValue) {
        return {
            radius: 12,
            fillColor: me.getCyanToBlue(propertyValue),
            color: "white",
            weight: 2,
            opacity: 1,
            fillOpacity: 0.8,
        }
    }

    me.getLineConstantSymbol = function (layerName) {
        return {
            color: me.getLayerColor(layerName),
            weight: 10,
            opacity: 1,
            lineJoin: 'round',
        }
    }

    me.getLineVariableSymbol = function (propertyValue) {
        return {
            color: me.getCyanToBlue(propertyValue),
            weight: 10,
            opacity: 1,
            lineJoin: 'round',
        }
    }

    me.resetRdValueForColor = function (value) {
        var maxValue = me.globalFunctions.geoJsonAttributeMax(me.layerData.features, 'from_rd_m');
        return (value * 100) / maxValue;
    }

    me.getUniqueIdDetails = function (props) {
        switch (me.layerName) {
            case 'L Section':
                return {name: 'from_rd_m', value: props.from_rd_m};
            case 'Gauges':
                return {name: 'rd_m', value: props.rd_m};
            case 'Gates':
                return {name: 'rd', value: props.rd};
            case 'Right of way':
                return {name: 'rd_length', value: props.rd_length};
            case 'Structure':
                return {name: 'rd_m', value: props.rd_m};
            case 'Outlets':
                return {name: 'rd', value: props.rd};
        }
    }

    me.getLayerPopup = function (e) {
        var props = e.target.feature.properties;
        var idField = me.getUniqueIdDetails(props);
        me.selectHighlightGridRow('canalDetailDataPanel', idField.name, idField.value);
    }
    me.selectHighlightGridRow = function (gridId, fieldName, fieldValue) {
        var grid = Ext.getCmp(gridId);
        var targetRowIndex = grid.store.find(fieldName, fieldValue);
        var row = grid.getView().getRow(targetRowIndex);
        Ext.get(row).highlight();
        grid.getView().focusRow(row);
        grid.getSelectionModel().select(targetRowIndex);
    }

    me.highlightFeature = function (e) {
        var layer = e.target;
        layer.setStyle({
            weight: 10,
            color: '#ffff00',
        });
        if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
            layer.bringToFront();
        }
    }

    me.resetHighlight = function (e) {
        me.canalDetailsLayer.resetStyle(e.target);
    }

    me.onEachFeature = function (feature, layer) {
        layer.on({
            mouseover: me.highlightFeature,
            mouseout: me.resetHighlight,
            click: me.getLayerPopup
        });
    }

    me.getLineLayer = function () {

        if (me.layerName == 'L Section') {
            me.canalDetailsLayer = L.geoJson(me.layerData, {
                style: me.lSectionSymbol,
                onEachFeature: me.onEachFeature
            });
        } else {
            me.canalDetailsLayer = L.geoJson(me.layerData, {
                style: me.rightOfWaySymbol,
                onEachFeature: me.onEachFeature
            });
        }
        return me.canalDetailsLayer;
    };
    me.getPointLayer = function () {
        me.canalDetailsLayer = L.geoJSON(me.layerData,
            {
                onEachFeature: me.onEachFeature,
                pointToLayer: function (feature, latlng) {
                    return L.circleMarker(latlng, me.getPointConstantSymbol(me.layerName));
                }
            })
        return me.canalDetailsLayer;
    };

    me.getCanalsDetailLayer = function (layerName, data) {
        me.layerName = layerName;
        me.layerData = data;
        if (me.layerName == 'L Section' || me.layerName == 'Right of way') {
            return me.getLineLayer();
        } else {
            return me.getPointLayer();
        }
    };

    me.getCyanToBlue = function (value) {
        var percent = me.resetRdValueForColor(value);
        b = percent < 50 ? 255 : Math.floor(255 - (percent * 2 - 100) * 255 / 100);
        g = percent > 50 ? 255 : Math.floor((percent * 2) * 255 / 100);
        return 'rgb(0,' + g + ',' + b + ')';
    };

    me.getRandomColor = function (value) {
        var letters = '0123456789ABCDEF';
        var color = '#';
        for (var i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    };

    me.getColor = function (value) {
        var resetValue = me.resetRdValueForColor(value);
        var hue = ((1 - resetValue) * 120).toString(10);
        return ["hsl(", hue, ",100%,100%)"].join("");
    };

    // me.convertJsontoGeoJson = function (data) {
    //     var geoJson = '"type": "FeatureCollection", "features": [{';
    //     var keyNames = Object.keys(data);
    //     for(var i = 0; i<data.length; i++){
    //         var feature = '"type": "Feature", ', props = '"properties": ', geom = '"geometry": ';
    //         for(var j = 0; j<keyNames.length; j++){
    //             var keyName = keyNames[j];
    //             var keyValue = data[i][keyName];
    //             if(keyName == 'geojson'){
    //                 geom = geom + keyValue;
    //             }
    //         }
    //         props = props + JSON.stringify(data[i]);
    //         feature = feature + props + geom;
    //         geoJson = geoJson + feature
    //     }
    // };

};



