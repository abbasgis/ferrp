/**
 * Created by idrees on 4/25/2018.
 */

var ArzSurveyStatsModel = function () {
    var me = this;
    me.mapPanel = null;
    me.olMap = null;
    me.vectorOverlay = null;
    me.vectorOverlaySource = null;
    me.statsStore = null;
    me.statName = null;
    me.createOlMap = function (residentialGeoJson) {
        // me.mapPanel = Ext.create('Ext.panel.Panel',{
        //     id:'olMapPanel',
        //     name:'olMapPanel',
        //     tbar:[
        //         {
        //             tooltip:   'Filter by administrative boundary',
        //             icon: imgPath + '04.png',
        //
        //         },
        //         {
        //             icon: imgPath + 'drawline.png',
        //             tooltip:'Draw Polygon',
        //
        //         },
        //         {
        //             icon: imgPath + '11.png',
        //             tooltip:'Upload polygon/shapefile',
        //         }
        //     ],
        // });
        // var mapPanel = Ext.getCmp("olMap");
        // mapPanel.removeAll();
        // mapPanel.add(me.mapPanel);

        var mapDiv = Ext.getCmp('olMap').body.dom;
        me.olMap = new ol.Map({
            layers: [
                new ol.layer.Tile({
                    source: new ol.source.OSM()
                })
            ],
            target: mapDiv,
            controls: ol.control.defaults().extend([
                new ol.control.FullScreen()
            ]),
            view: new ol.View({
                center: ol.proj.transform([73.66, 32.29725], 'EPSG:4326', 'EPSG:3857'),
                zoom: 13
            })
        });
        me.vectorOverlaySource = new ol.source.Vector({wrapX: false});
        me.vectorOverlay = new ol.layer.Vector({
            source: me.vectorOverlaySource
        });
        me.olMap.addLayer(me.vectorOverlay);

        var stroke = new ol.style.Stroke({color: 'black', width: 2});
        var fill = new ol.style.Fill({color: 'red'});
        var pointStyle = new ol.style.Style({
            image: new ol.style.RegularShape({
                fill: fill,
                stroke: stroke,
                points: 5,
                radius: 10,
                radius2: 4,
                angle: 0
            })
        })

        var vectorSource = new ol.source.Vector({
            features: (new ol.format.GeoJSON()).readFeatures(residentialGeoJson[0]['geojson'])
        });
        var vectorLayer = new ol.layer.Vector({
            source: vectorSource,
            style: pointStyle
        });
        me.olMap.addLayer(vectorLayer);

        // var features = me.getPointArray(residentialGeoJson);
        // var source = new ol.source.Vector({
        //     features: features
        // });
        // var clusterSource = new ol.source.Cluster({
        //     distance: parseInt(25, 10),
        //     source: source
        // });
        //
        // var styleCache = {};
        // var clusters = new ol.layer.Vector({
        //     source: clusterSource,
        //     style: function (feature) {
        //         var size = feature.get('features').length;
        //         var style = styleCache[size];
        //         if (!style) {
        //             style = new ol.style.Style({
        //                 image: new ol.style.Circle({
        //                     radius: 10,
        //                     stroke: new ol.style.Stroke({
        //                         color: '#fff'
        //                     }),
        //                     fill: new ol.style.Fill({
        //                         color: '#ffc800'
        //                     })
        //                 }),
        //                 text: new ol.style.Text({
        //                     text: size.toString(),
        //                     fill: new ol.style.Fill({
        //                         color: '#fff'
        //                     })
        //                 })
        //             });
        //             styleCache[size] = style;
        //         }
        //         return style;
        //     }
        // });
        // me.olMap.addLayer(clusters);
        //
        // var element = document.getElementById('popup');
        // var popup = new ol.Overlay({
        //     element: element,
        //     positioning: 'bottom-center',
        //     stopEvent: false
        // });
        // me.olMap.addOverlay(popup);
        // me.olMap.on('click', function (evt) {
        //     var feature = me.olMap.forEachFeatureAtPixel(evt.pixel,
        //         function (feature, layer) {
        //             return feature;
        //         });
        //     if (feature) {
        //         var geometry = feature.getGeometry();
        //         var coord = geometry.getCoordinates();
        //         popup.setPosition(coord);
        //         coord = ol.proj.transform(coord, 'EPSG:3857', 'EPSG:4326');
        //         var content = '<h3> Respondant Name:' + feature.get('respondent_name') + '</h3>';
        //         content += '<h5> Respondant Gender:' + feature.get('respondent_gender') + '</h5>';
        //         content += '<h5> Respondant Religion:' + feature.get('religion') + '</h5>';
        //         $(element).popover({
        //             'placement': 'top',
        //             'html': true,
        //             'content': (content)
        //         });
        //         $(element).popover('show');
        //     } else {
        //         $(element).popover('destroy');
        //     }
        // });
    }
    me.createStatsGrid = function () {

        me.statsStore = Ext.create('Ext.data.Store', {
            id: 'statsStore',
            data: [
                {name: 'Surveys', value: 0},
                {name: 'Residential', value: 0},
                {name: 'Public Building', value: 0},
                {name: 'Education', value: 0},
                {name: 'Health Facility', value: 0},
                {name: 'Commercial', value: 0},
                {name: 'Religious Building', value: 0},
                {name: 'Infrastructure', value: 0},
                {name: 'Terminal', value: 0},
                {name: 'Mauza General Survey', value: 0},
                {name: 'Graveyard', value: 0},
                {name: 'Parks', value: 0},
                {name: 'Bridges', value: 0},
                {name: 'Industry', value: 0},
                {name: 'COLLAPSE BUILDING', value: 0},
                {name: 'DERA JAAT', value: 0},
                {name: 'Districts', value: 0},
                {name: 'Tehsils', value: 0},
                {name: 'Union Councils', value: 0},
                {name: 'Patwar Circles', value: 0},
                {name: 'Qanoongoi', value: 0},
                {name: 'Mauzas', value: 0},
            ],
            fields: ['name', 'value'],
        });

        var statsPanel = Ext.create('Ext.grid.Panel', {
            id: 'statsDataPanel',
            name: 'statsDataPanel',
            store: me.statsStore,
            stripeRows: true,
            columnLines: true,
            plugins: 'gridfilters',
            autoScroll: true,
            tbar: [
                {
                    tooltip: 'View Details',
                    icon: imgPath + 'icon_information.png',

                }
            ],
            listeners: {
                select: function (selModel, record, index, options) {
                    me.statName = record.data.name;
                }
            },
            columns: [
                {xtype: 'rownumberer', width: 40, text: 'No.'},
                {text: "Name", dataIndex: 'name', flex: 1, sortable: true},
                {text: "Value", dataIndex: 'value', flex: 1, sortable: true},
            ],
        });
        var mainPanel = Ext.getCmp("pnlStatsData");
        mainPanel.removeAll();
        mainPanel.add(statsPanel);
    }

    me.getPointArray = function (jsonArray) {
        var count = jsonArray.length;
        var features = new Array(count);
        for (var i = 0; i < count; i++) {
            var coordinates = [jsonArray[i]['lon'], jsonArray[i]['lat']];
            features[i] = new ol.Feature(new ol.geom.Point(coordinates));
        }
        return features;
    }

}

var ArzAdminQueryModel = function () {
    var me = this;
    me.win = null;

    me.createQueryWindow = function () {
        if (me.win != null) {
            me.win.destroy();
        }
        var reportForm = me.createReportForm();
        me.win = Ext.create('Ext.window.Window', {
            id: 'reportWin',
            title: 'Administrative Query',
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
        var districtStore = me.getComboStore('districtStore');
        var tehsilStore = me.getComboStore('tehsilStore');
        var ucStore = me.getComboStore('ucStore');
        var mauzaStore = me.getComboStore('mauzaStore');

        var form = Ext.create('Ext.form.Panel', {
            layout: 'anchor',
            id: 'frmAdminQuery',
            defaults: {
                anchor: '100%'
            },
            bodyPadding: 20,
            items: [
                Ext.create('Ext.form.ComboBox', {
                    fieldLabel: 'Select District',
                    store: districtStore,
                    id: 'cmbDistrict',
                    queryMode: 'local',
                    margin: '0 0 10 0',
                    emptyText: '<--Select District-->',
                    displayField: 'name',
                    valueField: 'id',
                    listeners: {
                        select: function (cmb, value) {
                            // var id = value.data.name;
                        }
                    }
                }),
                Ext.create('Ext.form.ComboBox', {
                    fieldLabel: 'Select Tehsil',
                    id: 'cmbTehsil',
                    store: tehsilStore,
                    queryMode: 'local',
                    margin: '0 0 10 0',
                    emptyText: '<--All Tehsils-->',
                    displayField: 'name',
                    valueField: 'id',
                    listeners: {
                        select: function (cmb, value) {

                        }
                    }
                }),
                Ext.create('Ext.form.ComboBox', {
                    fieldLabel: 'Select UC',
                    id: 'cmbUC',
                    margin: '0 0 10 0',
                    emptyText: '<--All UCs-->',
                    store: ucStore,
                    queryMode: 'local',
                    displayField: 'name',
                    valueField: 'id',
                    listeners: {
                        select: function (cmb, value) {

                        }
                    }
                }), Ext.create('Ext.form.ComboBox',
                    {
                        fieldLabel: 'Select Mauza',
                        id: 'cmbMauza',
                        margin: '0 0 10 0',
                        emptyText: '<--All Mauzas-->',
                        store: mauzaStore,
                        queryMode: 'local',
                        displayField: 'name',
                        valueField: 'id',
                        listeners: {
                            select: function (cmb, value) {

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

                    }
                },
                {
                    xtype: 'button',
                    tooltip: "Clear Filter",
                    margin: '5, 0, 0, 0',
                    height: 30,
                    text: 'Clear Filter',
                    handler: function () {

                    }
                }]
        });
        return form;
    }
}

