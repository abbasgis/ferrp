/**
 * Created by idrees on 4/25/2018.
 */

var ArzSurveyFactsModel = function () {
    var me = this;
    me.mapPanel = null;
    me.olMap = null;
    me.mapClickCoordinates = null;
    me.popupContainer = document.getElementById('popup');
    me.popupContent = document.getElementById('popup-content');
    me.popupCloser = document.getElementById('popup-closer');
    me.popupOverlay = new ol.Overlay({
        element: me.popupContainer,
        autoPan: true,
        autoPanAnimation: {
            duration: 250
        }
    });
    me.vectorOverlay = null;
    me.vectorOverlaySource = null;
    me.districtLayer = null;
    me.tehsilLayer = null;
    me.qanongoHalkaLayer = null;
    me.patwarCircleLayer = null;
    me.mauzaLayer = null;
    me.districtPieLayer = null;
    me.tehsilPieLayer = null;
    me.qanongoHalkaPieLayer = null;
    me.patwarCirclePieLayer = null;
    me.mauzaPieLayer = null;
    me.surveyLocations = null;
    me.statsStore = null;
    me.statName = null;
    me.selectionLayer = null;

    me.createOlMap = function (geoJson) {

        var districtGeoJson = JSON.parse(geoJson.district);
        var tehsilGeoJson = JSON.parse(geoJson.tehsil);
        var qanungoiGeoJson = JSON.parse(geoJson.qanungoi);
        var patwarCircleGeoJson = JSON.parse(geoJson.parwar_circle);
        var mazaGeoJson = JSON.parse(geoJson.mauza);

        var district_type_counts = JSON.parse(geoJson.district_type_counts);
        var tehsil_type_counts = JSON.parse(geoJson.tehsil_type_counts);
        var qanungoi_type_counts = JSON.parse(geoJson.qanungoi_type_counts);
        var patwarcircle_type_counts = JSON.parse(geoJson.patwarcircle_type_counts);
        var mauza_type_counts = JSON.parse(geoJson.mauza_type_counts);

        var mapDiv = Ext.getCmp('olMap').body.dom;
        me.olMap = new ol.Map({
            layers: [
                new ol.layer.Tile({
                    // source: new ol.source.OSM()
                    source: new ol.source.OSM({
                        url: 'http://mt{0-3}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
                        attributions: [
                            new ol.Attribution({html: '© Google'}),
                            new ol.Attribution({html: '<a target="_blank" href="https://developers.google.com/maps/terms">Terms of Use.</a>'})
                        ]
                    }),
                })
            ],
            target: mapDiv,
            controls: ol.control.defaults().extend([
                new ol.control.FullScreen(),
                new ol.control.LayerSwitcher()
            ]),
            view: new ol.View({
                center: ol.proj.transform([72, 30.5], 'EPSG:4326', 'EPSG:3857'),
                zoom: 7
            })
        });
        me.vectorOverlaySource = new ol.source.Vector({wrapX: false});
        me.vectorOverlay = new ol.layer.Vector({
            source: me.vectorOverlaySource
        });
        me.olMap.addLayer(me.vectorOverlay);

        var stroke = new ol.style.Stroke({color: '#ffffff', width: 1});
        var fill = new ol.style.Fill({color: '#64ff64'});
        var pointStyle = new ol.style.Style({
            image: new ol.style.RegularShape({
                fill: fill,
                stroke: stroke,
                points: 5,
                radius: 6,
                radius2: 3,
                angle: 0
            })
        })

        var districtSource = new ol.source.Vector({
            features: (new ol.format.GeoJSON()).readFeatures(districtGeoJson[0]['geojson'])
        });
        me.districtLayer = new ol.layer.Vector({
            source: districtSource,
            style: me.getDistrictStyle(),
            minResolution: 200,
            title: 'district'
        });

        var tehsilSource = new ol.source.Vector({
            features: (new ol.format.GeoJSON()).readFeatures(tehsilGeoJson[0]['geojson'])
        });
        me.tehsilLayer = new ol.layer.Vector({
            source: tehsilSource,
            style: me.getTehsilStyle(),
            maxResolution: 200,
            minResolution: 120,
            title: 'tehsil'
            // visible:false
        });

        var qanungoiSource = new ol.source.Vector({
            features: (new ol.format.GeoJSON()).readFeatures(qanungoiGeoJson[0]['geojson'])
        });
        me.qanongoHalkaLayer = new ol.layer.Vector({
            source: qanungoiSource,
            style: me.getQanungoiStyle(),
            maxResolution: 120,
            minResolution: 70,
            title: 'qanongoi'
            // visible:false
        });

        var parwarCircleSource = new ol.source.Vector({
            features: (new ol.format.GeoJSON()).readFeatures(patwarCircleGeoJson[0]['geojson'])
        });
        me.patwarCircleLayer = new ol.layer.Vector({
            source: parwarCircleSource,
            style: me.getPatwarCircleStyle(),
            maxResolution: 70,
            minResolution: 20,
            title: 'patwar'
            // visible:false
        });

        var mauzaSource = new ol.source.Vector({
            features: (new ol.format.GeoJSON()).readFeatures(mazaGeoJson[0]['geojson'])
        });
        me.mauzaLayer = new ol.layer.Vector({
            source: mauzaSource,
            style: me.getMauzaStyle(),
            maxResolution: 20,
            title: 'mauza'
        });

        var locationSource = new ol.source.Vector({
            features: (new ol.format.GeoJSON())
        });
        me.surveyLocations = new ol.layer.Vector({
            source: locationSource,
            style: me.getLocationStyle()
        });

        var locationGeoJson = JSON.parse('{"type":"FeatureCollection","features":[{"type":"Feature","geometry":{"type":"Point", "coordinates":[0.0,0.0]},"properties":{"survey_type_name":"Bridges"}}]}');
        var selectionSource = new ol.source.Vector({
            features: (new ol.format.GeoJSON())
        });
        me.selectionLayer = new ol.layer.Vector({
            source: selectionSource,
            // style: me.getSelectStyle()
        });

        me.olMap.addLayer(me.selectionLayer);
        me.olMap.addLayer(me.surveyLocations);
        me.olMap.addLayer(me.mauzaLayer);
        me.olMap.addLayer(me.patwarCircleLayer);
        me.olMap.addLayer(me.qanongoHalkaLayer);
        me.olMap.addLayer(me.tehsilLayer);
        me.olMap.addLayer(me.districtLayer);

        me.getDistrictTypeCountsLayer(district_type_counts);
        me.getTehsilTypeCountsLayer(tehsil_type_counts);
        me.getQanungoiTypeCountsLayer(qanungoi_type_counts);
        me.getPatwarCircleTypeCountsLayer(patwarcircle_type_counts);
        me.getMauzaTypeCountsLayer(mauza_type_counts);

        var select = new ol.interaction.Select({
            style: function (f) {
                return me.getFeatureStyle(f, true);
            }
        });
        me.olMap.addInteraction(select);

        me.olMap.addOverlay(me.popupOverlay);

        // me.olMap.on('postrender', me.mapOnMoveEnd);
        me.olMap.on('singleclick', function (evt) {
            var coordinate = evt.coordinate;
            me.mapClickCoordinates = ol.proj.toLonLat(coordinate);
        });
    }

    me.removeLayerByName = function (layerName) {
        var layerToRemove;
        var all_layer_groups = me.olMap.getLayers();
        for (i = 0, n = all_layer_groups.getLength(); i < n; i++) {
            layerToRemove = all_layer_groups.item(i);
            if (layerToRemove.text == layerName) {
                me.olMap.removeLayer(layerToRemove);
            }
        }
    }

    me.setSelection = function (lat, lon) {
        if (me.vectorLayer) {
            me.removeLayerByName('Selected Features');
        }
        var point = ol.proj.transform([lon, lat], 'EPSG:4326', 'EPSG:3857');
        var selectedFeature = new ol.Feature({
            geometry: new ol.geom.Point(point)
        });
        var selectStyle = new ol.style.Style({
            stroke: new ol.style.Stroke({
                color: '#00FFFF',
                width: 8
            })
        });
        me.olMap.getView().setCenter(point);
        me.olMap.getView().setZoom(18);
        me.vectorLayer = new ol.layer.Vector({
            source: new ol.source.Vector({
                features: (new ol.format.GeoJSON()).readFeatures(
                    JSON.parse('{"type":"FeatureCollection","features":[{"type":"Feature","geometry":{"type":"Point", "coordinates":[' + lon + ',' + lat + ']},"properties":{"survey_type_name":"Bridges"}}]}'),
                    {
                        dataProjection: 'EPSG:4326',
                        featureProjection: 'EPSG:3857'
                    })
            }),
            style: selectStyle,
            name: 'Selected Features'
        });
    }

    me.removeLayerByName = function (layerName) {
        var layerToRemove;
        me.olMap.getLayers().forEach(function (layer) {
            if (layer instanceof ol.layer.Vector) {
                if (layer.text == layerName) {
                    me.olMap.removeLayer(layerName);
                }
            }
        });
    }

    me.getLocationStyle = function () {
        function getColor(feature) {
            var survey_type_name = feature.get('survey_type_name');
            var color = me.getSurveyTypeSymbology(survey_type_name);
            return color;
        }

        return function (feature) {
            var style = new ol.style.Style({
                image: new ol.style.Circle({
                    radius: 6,
                    stroke: new ol.style.Stroke({
                        color: '#fff'
                    }),
                    fill: new ol.style.Fill({
                        color: getColor(feature)
                    })
                })
            });
            return style;
        }
    }

    me.popupCloser.onclick = function () {
        me.popupOverlay.setPosition(undefined);
        me.popupCloser.blur();
        return false;
    };

    me.mapOnMoveEnd = function (evt) {
        console.log(me.olMap.getView().getZoom());
        var zoomLevel = me.olMap.getView().getZoom();
        if (zoomLevel < 10) {
            me.districtLayer.setVisible(true);
            me.districtPieLayer.setVisible(true);
            me.tehsilLayer.setVisible(false);
            me.tehsilPieLayer.setVisible(false);
            me.qanongoHalkaLayer.setVisible(false);
            me.qanongoHalkaPieLayer.setVisible(false);
            me.patwarCircleLayer.setVisible(false);
            me.patwarCirclePieLayer.setVisible(false);
            me.mauzaLayer.setVisible(false);
            me.mauzaPieLayer.setVisible(false);
        }
        if (zoomLevel < 12 && zoomLevel >= 10) {
            me.districtLayer.setVisible(false);
            me.districtPieLayer.setVisible(false);
            me.tehsilLayer.setVisible(true);
            me.tehsilPieLayer.setVisible(true);
            me.qanongoHalkaLayer.setVisible(false);
            me.qanongoHalkaPieLayer.setVisible(false);
            me.patwarCircleLayer.setVisible(false);
            me.patwarCirclePieLayer.setVisible(false);
            me.mauzaLayer.setVisible(false);
            me.mauzaPieLayer.setVisible(false);
        }
        if (zoomLevel < 14 && zoomLevel >= 12) {
            me.districtLayer.setVisible(false);
            me.districtPieLayer.setVisible(false);
            me.tehsilLayer.setVisible(false);
            me.tehsilPieLayer.setVisible(false);
            me.qanongoHalkaLayer.setVisible(true);
            me.qanongoHalkaPieLayer.setVisible(true);
            me.patwarCircleLayer.setVisible(false);
            me.patwarCirclePieLayer.setVisible(false);
            me.mauzaLayer.setVisible(false);
            me.mauzaPieLayer.setVisible(false);
        }
        if (zoomLevel < 16 && zoomLevel >= 14) {
            me.districtLayer.setVisible(false);
            me.districtPieLayer.setVisible(false);
            me.tehsilLayer.setVisible(false);
            me.tehsilPieLayer.setVisible(false);
            me.qanongoHalkaLayer.setVisible(false);
            me.qanongoHalkaPieLayer.setVisible(false);
            me.patwarCircleLayer.setVisible(true);
            me.patwarCirclePieLayer.setVisible(true);
            me.mauzaLayer.setVisible(false);
            me.mauzaPieLayer.setVisible(false);
        }
        if (zoomLevel >= 16) {
            me.districtLayer.setVisible(false);
            me.districtPieLayer.setVisible(false);
            me.tehsilLayer.setVisible(false);
            me.tehsilPieLayer.setVisible(false);
            me.qanongoHalkaLayer.setVisible(false);
            me.qanongoHalkaPieLayer.setVisible(false);
            me.patwarCircleLayer.setVisible(false);
            me.patwarCirclePieLayer.setVisible(false);
            me.mauzaLayer.setVisible(true);
            me.mauzaPieLayer.setVisible(true);
        }
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

    me.getSurveyTypeId = function (survey_type) {
        if (survey_type == 'Bridges') {
            return 0;
        }
        if (survey_type == 'COLLAPSE BUILDING') {
            return 1;
        }
        if (survey_type == 'Commercial') {
            return 2;
        }
        if (survey_type == 'DERA JAAT') {
            return 4;
        }
        if (survey_type == 'Education') {
            return 5;
        }
        if (survey_type == 'Graveyard') {
            return 6;
        }
        if (survey_type == 'Health Facility') {
            return 7;
        }
        if (survey_type == 'Industry') {
            return 8;
        }
        if (survey_type == 'Infrastructure') {
            return 8;
        }
        if (survey_type == 'Mauza General Survey') {
            return 9;
        }
        if (survey_type == 'Parks') {
            return 10;
        }
        if (survey_type == 'Public Building') {
            return 11;
        }
        if (survey_type == 'Religious Building') {
            return 12;
        }
        if (survey_type == 'Residential') {
            return 13;
        }
        if (survey_type == 'Terminal') {
            return 14;
        } else {
            return 15;
        }

        // switch (type) {
        //     case 'Bridges':
        //         return 0;
        //     case 'COLLAPSE BUILDING':
        //         return 1;
        //     case 'Commercial':
        //         return 2;
        //     case 'DERA JAAT':
        //         return 3;
        //     case 'Education':
        //         return 4;
        //     case 'Graveyard':
        //         return 5;
        //     case 'Health Facility':
        //         return 6;
        //     case type == 'Industry':
        //         return 7;
        //     case 'Infrastructure':
        //         return 8;
        //     case 'Mauza General Survey':
        //         return 9;
        //     case 'Parks':
        //         return 10;
        //     case 'Public Building':
        //         return 11;
        //     case 'Religious Building':
        //         return 12;
        //     case 'Residential':
        //         return 13;
        //     case 'Terminal':
        //         return 14;
        //     default:
        //         return 8;
        // }
    }

    me.geoJsonPointArray = function (data) {
        var count = data.length;
        var features = new Array(count);
        for (var i = 0; i < count; i++) {
            var type = me.getSurveyTypeId(data[i].properties.survey_type_name);
            var coordinates = [data[i].geometry.coordinates[0], data[i].geometry.coordinates[1]];
            features[i] = new ol.Feature(new ol.geom.Point(coordinates));
            features[i].set('id', i);
            features[i].set('type', type);
        }
        return features;
    }

    me.getColumnsList = function (data) {
        var columns = [];
        var stringType = "string";
        var numberType = 'number';
        columns.push({xtype: 'rownumberer'});
        for (var key in data) {
            if (key === "extent" || key === "geojson" || key === "id" || key === "canal_type" || key === "gid") {
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

    me.getFieldsList = function (data) {
        var arrField = new Array();
        for (var key in data) {
            var obj = {};
            if (key === "extent" || key === "geojson" || key === "canal_type") {
            } else {
                obj.id = key;
                obj.name = key;
                arrField.push(obj);
            }
        }
        return arrField;
    }

    me.getDistrictStyle = function () {
        var getText = function (feature) {
            var text = feature.get('district_name');
            return text;
        };
        var createTextStyle = function (feature) {
            return new ol.style.Text({
                textAlign: 'center',
                overflow: true,
                textBaseline: 'middle',
                font: '15px Calibri,sans-serif',
                text: getText(feature),
                fill: new ol.style.Fill({color: 'white'}),
                stroke: new ol.style.Stroke({color: '#323232', width: 4}),
            });
        };
        return function (feature) {
            var style08 = new ol.style.Style({
                stroke: new ol.style.Stroke({
                    color: '#f35006',
                    width: 2
                }),
                fill: new ol.style.Fill({
                    color: 'transparent'
                }),
                text: createTextStyle(feature)
            });
            return style08;
        };
    }

    me.getTehsilStyle = function () {
        var getText = function (feature) {
            var text = feature.get('tehsil_name');
            return text;
        };
        var createTextStyle = function (feature) {
            return new ol.style.Text({
                textAlign: 'center',
                overflow: true,
                textBaseline: 'middle',
                font: '15px Calibri,sans-serif',
                text: getText(feature),
                fill: new ol.style.Fill({color: 'white'}),
                stroke: new ol.style.Stroke({color: '#ffc800', width: 4}),
                offsetX: 0,
                offsetY: -25,
            });
        };
        return function (feature) {
            var style08 = new ol.style.Style({
                stroke: new ol.style.Stroke({
                    color: '#ffdd00',
                    width: 2
                }),
                fill: new ol.style.Fill({
                    color: 'transparent'
                }),
                text: createTextStyle(feature)
            });
            return style08;
        };
    }

    me.getQanungoiStyle = function () {
        var getText = function (feature) {
            var text = feature.get('qanungoi_halqa_name');
            return text;
        };
        var createTextStyle = function (feature) {
            return new ol.style.Text({
                textAlign: 'center',
                overflow: true,
                textBaseline: 'middle',
                font: '15px Calibri,sans-serif',
                text: getText(feature),
                fill: new ol.style.Fill({color: 'white'}),
                stroke: new ol.style.Stroke({color: '#ffc800', width: 4}),
                offsetX: 0,
                offsetY: -25,
            });
        };
        return function (feature) {
            var style08 = new ol.style.Style({
                stroke: new ol.style.Stroke({
                    color: '#029204',
                    width: 2
                }),
                fill: new ol.style.Fill({
                    color: 'transparent'
                }),
                text: createTextStyle(feature)
            });
            return style08;
        };
    }

    me.getPatwarCircleStyle = function () {
        var getText = function (feature) {
            var text = feature.get('patwar_circle_name');
            return text;
        };
        var createTextStyle = function (feature) {
            return new ol.style.Text({
                textAlign: 'center',
                overflow: true,
                textBaseline: 'middle',
                font: '15px Calibri,sans-serif',
                text: getText(feature),
                fill: new ol.style.Fill({color: 'white'}),
                stroke: new ol.style.Stroke({color: '#ffc800', width: 4}),
                offsetX: 0,
                offsetY: -25,
            });
        };
        return function (feature) {
            var style08 = new ol.style.Style({
                stroke: new ol.style.Stroke({
                    color: '#00FF00',
                    lineDash: [0.1, 5],
                    width: 2
                }),
                fill: new ol.style.Fill({
                    color: 'transparent'
                }),
                text: createTextStyle(feature)
            });
            return style08;
        };
    }

    me.getMauzaStyle = function () {
        var getText = function (feature) {
            var text = feature.get('mauza_name');
            return text;
        };
        var createTextStyle = function (feature) {
            return new ol.style.Text({
                textAlign: 'center',
                overflow: true,
                offsetX: 0,
                offsetY: 30,
                textBaseline: 'middle',
                font: '15px Calibri,sans-serif',
                text: getText(feature),
                fill: new ol.style.Fill({color: '#323232'}),
                stroke: new ol.style.Stroke({color: 'white', width: 1})
            });
        };
        return function (feature) {
            //     var style08 = new ol.style.Style({
            //         stroke: new ol.style.Stroke({
            //             color: '#064dff',
            //             lineDash: [0.1, 5],
            //             width: 2
            //         }),
            //         fill: new ol.style.Fill({
            //             color: 'transparent'
            //         }),
            //         text: createTextStyle(feature)
            //     });
            //     return style08;
            var style08 = new ol.style.Style({
                image: new ol.style.Circle({
                    fill: new ol.style.Fill({color: [255, 255, 255, 1]}),
                    stroke: new ol.style.Stroke({color: '#780000', width: 3}),
                    radius: 5
                }),
                text: createTextStyle(feature)
            });
            return style08;
        };


    }

    me.getSelectStyle = function (g_type) {
        if (g_type == 'Point') {
            var selStyle = new ol.style.Style({
                image: new ol.style.Circle({
                    fill: new ol.style.Fill({color: '#00FFFF'}),
                    stroke: new ol.style.Stroke({color: '#00FFFF', width: 5}),
                    radius: 5
                }),
            });
        } else if (g_type == 'LineString') {
            var selStyle = new ol.style.Style({
                stroke: new ol.style.Stroke({
                    color: '#02ffff',
                    width: 10
                })
            });
        } else {
            var selStyle = new ol.style.Style({
                // fill: new ol.style.Fill({
                //     color: 'transparent'
                // }),
                stroke: new ol.style.Stroke({
                    color: '#00ffff',
                    width: 10
                })
            });
        }
        return selStyle;
    }

    me.zoomToExtent = function (strExtent, isGCS) {
        var splitExtent = strExtent.split(',');
        if (splitExtent.length > 0) {
            var minx = parseFloat(splitExtent[0]);
            var miny = parseFloat(splitExtent[1]);
            var maxx = parseFloat(splitExtent[2]);
            var maxy = parseFloat(splitExtent[3]);

            var extent = null;
            if (isGCS == true) {
                extent = ol.proj.transformExtent([minx, miny, maxx, maxy], "EPSG:4326", "EPSG:3857");
            } else {
                extent = ol.proj.transformExtent([minx, miny, maxx, maxy], "EPSG:3857", "EPSG:3857");
            }
            me.olMap.getView().fit(extent, me.olMap.getSize());
        }
    }

    me.addLocationsToMauzaLayer = function (data) {
        if (me.surveyLocations.getSource()) {
            me.surveyLocations.getSource().clear();
        }
        for (var i = 0; i < data.length; i++) {
            var latitude = data[i].latitude;
            var longitude = data[i].longitude;
            var point = new ol.geom.Point(ol.proj.transform([longitude, latitude], 'EPSG:4326', 'EPSG:3857'));
            var feature = new ol.Feature({
                geometry: point,
                survey_id: data[i].survey_id,
                survey_type_name: data[i].survey_type_name,
            });
            me.surveyLocations.getSource().addFeature(feature);
        }
    }

    me.getClusterLayer = function (data) {
        var features = me.geoJsonPointArray(data);
        var source = new ol.source.Vector({
            features: features
        });
        var source = new ol.source.Vector({
            features: features
        });
        var clusterSource = new ol.source.Cluster({
            distance: parseInt(50, 10),
            source: source
        });

        var styleCache = {};
        var clusters = new ol.layer.Vector({
            source: clusterSource,
            style: function (feature) {
                var sel = feature.get('features');
                var size = sel.length;
                var type = sel[0].get('type');
                var color = me.getSurveyTypeIdSymbology(type);
                var style = styleCache[size];
                if (!style) {
                    style = new ol.style.Style({
                        image: new ol.style.Circle({
                            radius: 20,
                            stroke: new ol.style.Stroke({
                                color: '#fff'
                            }),
                            fill: new ol.style.Fill({
                                color: color
                            })
                        }),
                        text: new ol.style.Text({
                            text: size.toString(),
                            fill: new ol.style.Fill({
                                color: '#fff'
                            })
                        })
                    });
                    styleCache[size] = style;
                }
                return style;
            }
        });
        return clusters;

    }

    me.getClusterLayerAnimated = function (data) {

        function getStyle(feature, resolution) {
            var features = feature.get('features');
            var size = features.length;
            // Feature style
            if (size === 1) return featureStyle(feature);
            // ClusterStyle
            else {
                var data = [0, 0, 0, 0];
                for (var i = 0, f; f = features[i]; i++) data[f.get('type')]++;
                var style = styleCache[data.join(',')];
                if (!style) {
                    var radius = Math.min(size + 7, 20);
                    style = styleCache[data.join(',')] = new ol.style.Style({
                        image: new ol.style.Chart({
                            type: 'pie',
                            radius: radius,
                            data: data,
                            rotateWithView: true,
                            stroke: new ol.style.Stroke({
                                color: "rgba(0,0,0,0)",
                                width: 0
                            })
                        })

                    });
                }
                return [style];
            }
        }

        // Style for the features
        // var form = ['dam', 'building', 'commercial', 'campsite', 'school', 'cemetery', 'hospital', 'industrial', 'roadblock', 'village'
        //     , 'playground', 'building', 'religious-place_of_worship', 'town_hall', 'campsite'];
        var form = ['bus', 'town_hall', 'theatre', 'industrial', 'bus', 'town_hall', 'theatre', 'industrial', 'bus', 'town_hall', 'theatre', 'industrial'
            , 'bus', 'town_hall', 'theatre', 'industrial', 'bus', 'town_hall', 'theatre', 'industrial', 'bus', 'town_hall', 'theatre', 'industrial'];
        var styleCache = {};

        function featureStyle(f) {
            var sel = f.get('features')
            if (sel) {
                var type = sel[0].get('type');
                var style = styleCache[type];
                if (!style) {
                    var color = me.getSurveyTypeIdSymbology(type);
                    style = styleCache[type] = new ol.style.Style({
                        image: new ol.style.FontSymbol({
                            glyph: 'maki-' + form[type],
                            radius: 12,
                            color: color,
                            fill: new ol.style.Fill({
                                color: color
                            }),
                            stroke: new ol.style.Stroke({
                                color: '#fff',
                                width: 1
                            })
                        })
                    });
                }
                return [style];
            }
            else return [new ol.style.Style({
                stroke: new ol.style.Stroke({
                    color: "#fff",
                    width: 1
                })
            })];
        }

        // Cluster features
        var features = me.geoJsonPointArray(data);
        var source = new ol.source.Vector({
            features: features
        });
        // Cluster Source
        var clusterSource = new ol.source.Cluster({
            distance: 40,
            source: source
        });
        // Animated cluster layer
        var clusterLayer = new ol.layer.AnimatedCluster({
            name: 'Cluster',
            source: clusterSource,
            animationDuration: 500,
            // Cluster style
            style: getStyle
        });
        return clusterLayer;
        me.olMap.addLayer(clusterLayer);

        // Select interaction to spread cluster out and select features
        var selectCluster = new ol.interaction.SelectCluster({
            // Point radius: to calculate distance between the features
            pointRadius: 10,
            animate: $("#animatesel").prop('checked'),
            // Feature style when it springs apart
            featureStyle: featureStyle,
            selectCluster: false,	// disable cluster selection
        });
        me.olMap.addInteraction(selectCluster);


    }

    me.getSurveyTypeSymbology = function (survey_type) {
        if (survey_type == 'Bridges') {
            return '#969632';
        }
        if (survey_type == 'COLLAPSE BUILDING') {
            return '#780000';
        }
        if (survey_type == 'Commercial') {
            return '#ff4804';
        }
        if (survey_type == 'DERA JAAT') {
            return '#537952';
        }
        if (survey_type == 'Education') {
            return '#d7a200';
        }
        if (survey_type == 'Graveyard') {
            return '#ff5d00';
        }
        if (survey_type == 'Health Facility') {
            return '#019084';
        }
        if (survey_type == 'Industry') {
            return '#770190';
        }
        if (survey_type == 'Infrastructure') {
            return '#960';
        }
        if (survey_type == 'Mauza General Survey') {
            return '#50506d';
        }
        if (survey_type == 'Parks') {
            return '#999933';
        }
        if (survey_type == 'Public Building') {
            return '#000';
        }
        if (survey_type == 'Religious Building') {
            return '#00f';
        }
        if (survey_type == 'Residential') {
            return '#ffcc33';
        }
        if (survey_type == 'Terminal') {
            return '#FF0000';
        } else {
            return '#ffffff';
        }

    }

    me.getSurveyTypeIdSymbology = function (survey_type) {
        if (survey_type == 0) {
            return '#969632';
        }
        if (survey_type == 1) {
            return '#780000';
        }
        if (survey_type == 2) {
            return '#ff4804';
        }
        if (survey_type == 3) {
            return '#c8c8c8';
        }
        if (survey_type == 4) {
            return '#038c96';
        }
        if (survey_type == 5) {
            return '#000000';
        }
        if (survey_type == 6) {
            return '#ff0000';
        }
        if (survey_type == 7) {
            return '#6807ff';
        }
        if (survey_type == 8) {
            return '#ffffff';
        }
        if (survey_type == 9) {
            return '#059656';
        }
        if (survey_type == 10) {
            return '#00ff00';
        }
        if (survey_type == 11) {
            return '#c3ff0a';
        }
        if (survey_type == 12) {
            return '#006400';
        }
        if (survey_type == 13) {
            return '#ff0fe0';
        }
        if (survey_type == 14) {
            return '#646464';
        } else {
            return '#ffffff';
        }

    }

    me.getClusterFeatures = function (data) {
        var features = new Array(data.length);
        for (var i = 0; i < data.length; i++) {
            var record = data[i];
            var lon = record['coords'].split(',')[0];
            var lat = record['coords'].split(',')[1];
            var latLon = [lat, lon];
            features[i] = new ol.Feature(new ol.geom.Point(latLon));
        }
        return features;
    }

    me.getFeatureStyle = function (feature, sel) {
        function getLayerRadius(layerType) {
            if (layerType == 'district') {
                return 30;
            }
            if (layerType == 'tehsil') {
                return 27;
            }
            if (layerType == 'qanongoi') {
                return 24;
            }
            if (layerType == 'patwar_circle') {
                return 21;
            }
            if (layerType == 'mauza') {
                return 18;
            } else {
                return 20
            }
        }

        function getColorsArray(arrSurveyType) {
            var arrColors = [];
            for (var i = 0; i < arrSurveyType.length; i++) {
                var type = arrSurveyType[i];
                var color = me.getSurveyTypeSymbology(type);
                arrColors.push(color);
            }
            return arrColors;
        }

        var radius = getLayerRadius(feature.get('layerName'));
        var arrSurveyType = feature.get("survey_type");
        var colors = getColorsArray(arrSurveyType);
        var startPoint = arrSurveyType.length * 5;
        var data = feature.get("data");
        var style = [new ol.style.Style(
            {
                image: new ol.style.Chart(
                    {
                        type: "pie",
                        radius: radius,
                        data: data,
                        colors: colors,
                        rotateWithView: true,
                        animation: {animate: true},
                        stroke: new ol.style.Stroke(
                            {
                                color: "#fff",
                                width: 1
                            }),
                    })
            })
        ];
        if (sel) {
            var sum = feature.get("sum");

            var s = 0;
            var yOffset = 0;
            var content = '';
            content = '<p>' + feature.get('featureName') + '</p>';

            for (var i = 0; i < data.length; i++) {
                var d = data[i];
                var sType = arrSurveyType[i];
                content = content + '<b><a style="color:' + colors[i] + '; font-size: 14;">' + sType + ':' + d + '</a></b><br>';
                // var a = (2 * s + d) / sum * Math.PI - Math.PI / 2;
                // var v = Math.round(d / sum * 1000);
                // if (v > 0) {
                //     style.push(new ol.style.Style(
                //         {
                //             text: new ol.style.Text(
                //                 {
                //                     text: sType + ':' + d, /* d.toString() */
                //                     offsetX: 35, //Math.cos(a) * (50),
                //                     offsetY: (-startPoint + yOffset),// Math.sin(a) * (50),
                //                     textAlign: 'left', //(a < Math.PI / 2 ? "left" : "right"),
                //                     textBaseline: "middle",
                //                     fill: new ol.style.Fill(
                //                         {
                //                             color: colors[i]//'#1f1f1f'
                //                         }),
                //                     stroke: new ol.style.Stroke({color: '#fff', width: 1}),
                //                     font: 'bold 13px Tahoma,sans-serif',
                //                 })
                //         }));
                // }
                // s += d;
                // yOffset += 15;
            }
            me.popupContent.innerHTML = content;
            me.popupOverlay.setPosition(feature.getGeometry().getCoordinates());
        }
        return style;
    }

    me.getDistrictTypeCountsLayer = function (data) {
        var features = [];
        var dataGroupByType = _.groupBy(data, 'district_id');
        for (var row in dataGroupByType) {
            var record = dataGroupByType[row];
            var n, nb = 0, data = [], type = [];
            for (var k = 0; k < record.length; k++) {
                n = record[k]['count'];
                type.push(record[k]['survey_type_name'])
                data.push(n)
                nb = +n;
            }
            features.push(new ol.Feature(
                {
                    geometry: new ol.geom.Point(
                        ol.proj.transform(
                            [parseFloat(record[0]['latlon'].split(',')[0]), parseFloat(record[0]['latlon'].split(',')[1])],
                            'EPSG:4326',
                            'EPSG:3857'
                        )
                    ),
                    data: data,
                    sum: nb,
                    survey_type: type,
                    featureName: record[0]['district_name'],
                    layerName: 'district',
                }));
        }
        me.districtPieLayer = new ol.layer.Vector(
            {
                name: 'District Counts',
                source: new ol.source.Vector({features: features}),
                renderOrder: ol.ordering.yOrdering(),
                style: function (f) {
                    return me.getFeatureStyle(f);
                },
                minResolution: 175,
            }
        );
        me.olMap.addLayer(me.districtPieLayer);
    }
    me.getTehsilTypeCountsLayer = function (data) {
        var features = [];
        var dataGroupByType = _.groupBy(data, 'tehsil_id');
        for (var row in dataGroupByType) {
            var record = dataGroupByType[row];
            var n, nb = 0, data = [], type = [];
            for (var k = 0; k < record.length; k++) {
                n = record[k]['count'];
                type.push(record[k]['survey_type_name'])
                data.push(n)
                nb = +n;
            }
            features.push(new ol.Feature(
                {
                    geometry: new ol.geom.Point(
                        ol.proj.transform(
                            [parseFloat(record[0]['latlon'].split(',')[0]), parseFloat(record[0]['latlon'].split(',')[1])],
                            'EPSG:4326',
                            'EPSG:3857'
                        )
                    ),
                    data: data,
                    sum: nb,
                    survey_type: type,
                    featureName: record[0]['tehsil_name'],
                    layerName: 'tehsil',
                }));
        }
        me.tehsilPieLayer = new ol.layer.Vector(
            {
                name: 'Tehsil Counts',
                source: new ol.source.Vector({features: features}),
                renderOrder: ol.ordering.yOrdering(),
                style: function (f) {
                    return me.getFeatureStyle(f);
                },
                maxResolution: 200,
                minResolution: 120,
            }
        );
        me.olMap.addLayer(me.tehsilPieLayer);
    }
    me.getQanungoiTypeCountsLayer = function (data) {
        var features = [];
        var dataGroupByType = _.groupBy(data, 'qanungoi_halqa_id');
        for (var row in dataGroupByType) {
            var record = dataGroupByType[row];
            var n, nb = 0, data = [], type = [];
            for (var k = 0; k < record.length; k++) {
                n = record[k]['count'];
                type.push(record[k]['survey_type_name'])
                data.push(n)
                nb = +n;
            }
            var splittedLatLon = record[0]['latlon'].split(',');
            features.push(new ol.Feature(
                {
                    geometry: new ol.geom.Point(
                        ol.proj.transform(
                            [parseFloat(splittedLatLon[0]), parseFloat(splittedLatLon[1])],
                            'EPSG:4326',
                            'EPSG:3857'
                        )
                    ),
                    data: data,
                    sum: nb,
                    survey_type: type,
                    featureName: record[0]['qanungoi_halqa_name'],
                    layerName: 'qanongoi',
                }));
        }
        me.qanongoHalkaPieLayer = new ol.layer.Vector(
            {
                name: 'Qanongoi Counts',
                source: new ol.source.Vector({features: features}),
                renderOrder: ol.ordering.yOrdering(),
                style: function (f) {
                    return me.getFeatureStyle(f);
                },
                maxResolution: 120,
                minResolution: 70,
            }
        );
        me.olMap.addLayer(me.qanongoHalkaPieLayer);
    }
    me.getPatwarCircleTypeCountsLayer = function (data) {
        var features = [];
        var dataGroupByType = _.groupBy(data, 'patwar_circle_id');
        for (var row in dataGroupByType) {
            var record = dataGroupByType[row];
            var n, nb = 0, data = [], type = [];
            for (var k = 0; k < record.length; k++) {
                n = record[k]['count'];
                type.push(record[k]['survey_type_name'])
                data.push(n)
                nb = +n;
            }
            features.push(new ol.Feature(
                {
                    geometry: new ol.geom.Point(
                        ol.proj.transform(
                            [parseFloat(record[0]['latlon'].split(',')[0]), parseFloat(record[0]['latlon'].split(',')[1])],
                            'EPSG:4326',
                            'EPSG:3857'
                        )
                    ),
                    data: data,
                    sum: nb,
                    survey_type: type,
                    featureName: record[0]['patwar_circle_name'],
                    layerName: 'patwar_circle',
                }));
        }
        me.patwarCirclePieLayer = new ol.layer.Vector(
            {
                name: 'Patwar Circle Counts',
                source: new ol.source.Vector({features: features}),
                renderOrder: ol.ordering.yOrdering(),
                style: function (f) {
                    return me.getFeatureStyle(f);
                },
                maxResolution: 70,
                minResolution: 20,
            }
        );
        me.olMap.addLayer(me.patwarCirclePieLayer);
    }
    me.getMauzaTypeCountsLayer = function (data) {
        var features = [];
        var dataGroupByType = _.groupBy(data, 'mauza_id');
        for (var row in dataGroupByType) {
            var record = dataGroupByType[row];
            var n, nb = 0, data = [], type = [];
            for (var k = 0; k < record.length; k++) {
                n = record[k]['count'];
                type.push(record[k]['survey_type_name'])
                data.push(n)
                nb = +n;
            }
            features.push(new ol.Feature(
                {
                    geometry: new ol.geom.Point(
                        ol.proj.transform(
                            [parseFloat(record[0]['latlon'].split(',')[0]), parseFloat(record[0]['latlon'].split(',')[1])],
                            'EPSG:4326',
                            'EPSG:3857'
                        )
                    ),
                    data: data,
                    sum: nb,
                    survey_type: type,
                    featureName: record[0]['mauza_name'],
                    layerName: 'mauza',
                }));
        }
        me.mauzaPieLayer = new ol.layer.Vector(
            {
                name: 'Mauza Counts',
                source: new ol.source.Vector({features: features}),
                renderOrder: ol.ordering.yOrdering(),
                style: function (f) {
                    return me.getFeatureStyle(f);
                },
                maxResolution: 20,
            }
        );
        me.olMap.addLayer(me.mauzaPieLayer);
    }

	me.removeHighLightedLayer = function () {
        if (me.selectionLayer) {
            me.olMap.removeLayer(me.selectionLayer);
        }
    }
	
    me.highlightLayer = function (geometry) {
        var type = geometry.getType();
        if (me.selectionLayer) {
            me.olMap.removeLayer(me.selectionLayer);
        }
        var vectorSource = new ol.source.Vector();
        me.selectionLayer = new ol.layer.Vector({
            source: vectorSource
        });
        var style = me.getSelectStyle(type);

        var feature = new ol.Feature(geometry);
        feature.setStyle(style);
        vectorSource.addFeature(feature);
        if (type == 'Point'){
            me.olMap.addLayer(me.selectionLayer);
        }else{
            me.olMap.getLayers().insertAt(1, me.selectionLayer);
        }

    }

}


var ArzFactsWindow = function () {
    var me = this;
    me.factsWindow = null;
    me.tableChartData = null;
    me.chartTitle = null;
    me.statsChart = null;
    me.factsChartWindow = null;

    me.getBridgesTypePanel = function (data, type) {
        function getGridData() {
            var gridData = [];
            for (var item in data) {
                var record = {fact: JSON.stringify(data[item]), name: item};
                gridData.push(record);
            }
            return gridData;
        }

        var store = Ext.create('Ext.data.Store', {
            id: 'bridgesDataStore',
            fields: ['facts', 'name'],
            data: getGridData(),
        });

        var bridgesGrid = new Ext.grid.Panel({
            layout: 'fit',
            border: true,
            autoScroll: true,
            title: type,
            titleAlign: 'center',
            listeners: {
                select: function (selModel, record, index, options) {
                    me.tableChartData = record.data.fact;
                    me.chartTitle = record.data.name;


                },
            },
            store: store,
            columns: [
                {text: 'NAME', dataIndex: 'name', width: 120},
                {
                    text: 'Table',
                    align: 'center',
                    flex: 1,
                    renderer: function (value, meta, record) {
                        var id = Ext.id();
                        Ext.defer(function () {
                            new Ext.Button({
                                icon: imgPath + 'mhvra/table.png',
                                flex: 1,
                                handler: function (btn, e) {
                                    if (record.data.fact == null || record.data.fact == 'null') {
                                        alert('No data to display.');
                                    } else {
                                        var data = JSON.parse(record.data.fact);
                                        var panel = me.getTablePanel(data);
                                        me.getFactsWindow(panel, type, this);
                                    }

                                }
                            }).render(document.body, id);
                        }, 50);
                        return Ext.String.format('<div id="{0}"></div>', id);
                    }
                },
                {
                    text: 'Chart',
                    align: 'center',
                    flex: 1,
                    renderer: function (value, meta, record) {
                        var id = Ext.id();
                        Ext.defer(function () {
                            new Ext.Button({
                                icon: imgPath + 'mhvra/chart.png',
                                flex: 1,
                                handler: function (btn, e) {
                                    if (record.data.fact == null || record.data.fact == 'null') {
                                        alert('No data to display.');
                                    } else {
                                        var data = JSON.parse(record.data.fact);
                                        var key = me.getChartKey(data[0]);
                                        var chartData = me.getChartData(data, 'count');
                                        var categoriesList = me.getChartCategoriesList(data, key);
                                        me.getFactsChartWindow(type, this, chartData, categoriesList, record.data.name, 'Count');
                                    }
                                }
                            }).render(document.body, id);
                        }, 50);
                        return Ext.String.format('<div id="{0}"></div>', id);
                    }
                },
            ]
        });

        var factsGrid = new Ext.grid.PropertyGrid({
            layout: 'fit',
            border: true,
            title: type,
            titleAlign: 'center',
            listeners: {
                select: function (selModel, record, index, options) {
                    me.tableChartData = record.data.value;
                    me.chartTitle = record.data.name;
                },
            },
            source: {
                "Bridge Type": JSON.stringify(data.type_of_bridge),
                "Operational": JSON.stringify(data.operational),
                "Width Of Bridge": JSON.stringify(data.width_of_bridge),
                "Level of Damage": JSON.stringify(data.level_of_damage),
                "Ever Effected by Disaster": JSON.stringify(data.ever_effected_by_disaster),
                "Type of Disaster": JSON.stringify(data.type_of_disaster),
            },
            bbar: [
                {
                    icon: imgPath + 'chart.png',
                    tooltip: 'Get chart of selected record',
                    handler: function () {
                        if (me.tableChartData == null || me.tableChartData == 'null') {
                            alert('No data to display.');
                        } else {
                            var data = JSON.parse(me.tableChartData);
                            var key = me.getChartKey(data[0]);
                            var chartData = me.getChartData(data, 'count');
                            var categoriesList = me.getChartCategoriesList(data, key);
                            me.getFactsChartWindow(type, this, chartData, categoriesList, me.chartTitle, 'Count');
                        }
                    }
                },
                {
                    icon: imgPath + 'table.png',
                    tooltip: 'Get table of selected record',
                    handler: function () {
                        if (me.tableChartData == null || me.tableChartData == 'null') {
                            alert('No data to display.');
                        } else {
                            var data = JSON.parse(me.tableChartData);
                            var panel = me.getTablePanel(data);
                            me.getFactsWindow(panel, type, this);
                        }
                    }
                }
            ]
        });
        return bridgesGrid;
    };


    me.getCollapseBuildingTypePanel = function (data, type) {
        var factsGrid = new Ext.grid.PropertyGrid({
            layout: 'fit',
            border: true,
            title: type,
            titleAlign: 'center',
            source: {
                "Building Type": JSON.stringify(data.type_of_building),
                "Situated In": JSON.stringify(data.situated_in),
            },
            listeners: {
                select: function (selModel, record, index, options) {
                    me.tableChartData = record.data.value;
                    // alert(record.data.value);
                },
            },
            bbar: [
                {
                    icon: imgPath + 'chart.png',
                    tooltip: 'Get chart of selected record',

                },
                {
                    icon: imgPath + 'table.png',
                    tooltip: 'Get table of selected record',
                    handler: function () {
                        if (me.tableChartData == null || me.tableChartData == 'null') {
                            alert('No data to display.');
                        } else {
                            var data = JSON.parse(me.tableChartData);
                            var panel = me.getTablePanel(data);
                            me.getFactsWindow(panel, type, this);
                        }
                    }
                }
            ]
        });
        return factsGrid;
    };
    me.getCommercialFactsPanel = function (data, type) {
        var factsGrid = new Ext.grid.PropertyGrid({
            layout: 'fit',
            border: true,
            title: type,
            titleAlign: 'center',
            source: {
                "Building Age": JSON.stringify(data.age_of_building),
                "Effected": JSON.stringify(data.building_effected_from_disaster),
                "Emergency Exit": JSON.stringify(data.emergency_exit),
                "Evacuation Plan": JSON.stringify(data.evacuation_plan),
                "Damage Level": JSON.stringify(data.level_of_damage),
                "Plinth Level": JSON.stringify(data.plinth_level_of_building),
                "Security Guard": JSON.stringify(data.security_guard),
                "Business Type": JSON.stringify(data.type_of_business),
                "Disaster Type": JSON.stringify(data.type_of_disaster),
            },
            listeners: {
                select: function (selModel, record, index, options) {
                    me.tableChartData = record.data.value;
                    // alert(record.data.value);
                },
            },
            bbar: [
                {
                    icon: imgPath + 'chart.png',
                    tooltip: 'Get chart of selected record',
                },
                {
                    icon: imgPath + 'table.png',
                    tooltip: 'Get table of selected record',
                    handler: function () {
                        if (me.tableChartData == null || me.tableChartData == 'null') {
                            alert('No data to display.');
                        } else {
                            var data = JSON.parse(me.tableChartData);
                            var panel = me.getTablePanel(data);
                            me.getFactsWindow(panel, type, this);
                        }
                    }
                }
            ]
        });
        return factsGrid;

        // var age_of_building_data = JSON.parse(data[0].age_of_building_ft);
        // var building_effected_from_desaster_ft_data = JSON.parse(data[1].building_effected_from_desaster_ft);
        // var emergency_exit_ft_data = JSON.parse(data[2].emergency_exit_ft);
        // var evacuation_plan_ft_data = JSON.parse(data[3].evacuation_plan_ft);
        // var level_of_demage_ft_data = JSON.parse(data[4].level_of_demage_ft);
        // var plenth_level_of_building_ft_data = JSON.parse(data[5].plenth_level_of_building_ft);
        // var security_guard_ft_data = JSON.parse(data[6].security_guard_ft);
        // var type_of_bussiness_ft_data = JSON.parse(data[7].type_of_bussiness_ft);
        // var type_of_desaster_ft_data = JSON.parse(data[8].type_of_desaster_ft);
        //
        //
        //
        // var commFactsPanel = Ext.create('Ext.tab.Panel', {
        //     tabPosition: 'bottom',
        //     id: 'tabCommercialFacts',
        //     flex: 1,
        //     activeTab: 0,
        //     items: [
        //         {
        //             title: 'Age of Building',
        //             layout: 'fit',
        //             items: [
        //                 {
        //                     xtype: 'panel',
        //                     id: 'age_of_building_grid',
        //                     bodyStyle: {
        //                         backgroundColor: 'transparent'
        //                     },
        //                     flex:1,
        //                     layout: 'fit'
        //                 },{
        //                     xtype: 'panel',
        //                     id: 'age_of_building_chart',
        //                     bodyStyle: {
        //                         backgroundColor: 'transparent'
        //                     },
        //                     flex:2,
        //                     layout: 'fit'
        //                 }
        //             ]
        //         },{
        //             title: 'Building Affected',
        //             layout: 'fit',
        //             items: [
        //                 {
        //                     xtype: 'panel',
        //                     id: 'building_effected_from_desaster_ft_grid',
        //                     bodyStyle: {
        //                         backgroundColor: 'transparent'
        //                     },
        //                     flex:1,
        //                     layout: 'fit'
        //                 },{
        //                     xtype: 'panel',
        //                     id: 'building_effected_from_desaster_ft_chart',
        //                     bodyStyle: {
        //                         backgroundColor: 'transparent'
        //                     },
        //                     flex:2,
        //                     layout: 'fit'
        //                 }
        //             ]
        //         },{
        //             title: 'Emergency Exit',
        //             layout: 'fit',
        //             items: [
        //                 {
        //                     xtype: 'panel',
        //                     id: 'emergency_exit_ft_grid',
        //                     bodyStyle: {
        //                         backgroundColor: 'transparent'
        //                     },
        //                     flex:1,
        //                     layout: 'fit'
        //                 },{
        //                     xtype: 'panel',
        //                     id: 'emergency_exit_ft_chart',
        //                     bodyStyle: {
        //                         backgroundColor: 'transparent'
        //                     },
        //                     flex:2,
        //                     layout: 'fit'
        //                 }
        //             ]
        //         },{
        //             title: 'Evacuation Plan',
        //             layout: 'fit',
        //             items: [
        //                 {
        //                     xtype: 'panel',
        //                     id: 'evacuation_plan_ft_grid',
        //                     bodyStyle: {
        //                         backgroundColor: 'transparent'
        //                     },
        //                     flex:1,
        //                     layout: 'fit'
        //                 },{
        //                     xtype: 'panel',
        //                     id: 'evacuation_plan_ft_chart',
        //                     bodyStyle: {
        //                         backgroundColor: 'transparent'
        //                     },
        //                     flex:2,
        //                     layout: 'fit'
        //                 }
        //             ]
        //         },{
        //             title: 'Level of Damage',
        //             layout: 'fit',
        //             items: [
        //                 {
        //                     xtype: 'panel',
        //                     id: 'level_of_demage_ft_grid',
        //                     bodyStyle: {
        //                         backgroundColor: 'transparent'
        //                     },
        //                     flex:1,
        //                     layout: 'fit'
        //                 },{
        //                     xtype: 'panel',
        //                     id: 'level_of_demage_ft_chart',
        //                     bodyStyle: {
        //                         backgroundColor: 'transparent'
        //                     },
        //                     flex:2,
        //                     layout: 'fit'
        //                 }
        //             ]
        //         },{
        //             title: 'Plinth Level',
        //             layout: 'fit',
        //             items: [
        //                 {
        //                     xtype: 'panel',
        //                     id: 'plenth_level_of_building_ft_grid',
        //                     bodyStyle: {
        //                         backgroundColor: 'transparent'
        //                     },
        //                     flex:1,
        //                     layout: 'fit'
        //                 },{
        //                     xtype: 'panel',
        //                     id: 'plenth_level_of_building_ft_chart',
        //                     bodyStyle: {
        //                         backgroundColor: 'transparent'
        //                     },
        //                     flex:2,
        //                     layout: 'fit'
        //                 }
        //             ]
        //         },{
        //             title: 'Security Guard',
        //             layout: 'fit',
        //             items: [
        //                 {
        //                     xtype: 'panel',
        //                     id: 'security_guard_ft_grid',
        //                     bodyStyle: {
        //                         backgroundColor: 'transparent'
        //                     },
        //                     flex:1,
        //                     layout: 'fit'
        //                 },{
        //                     xtype: 'panel',
        //                     id: 'security_guard_ft_chart',
        //                     bodyStyle: {
        //                         backgroundColor: 'transparent'
        //                     },
        //                     flex:2,
        //                     layout: 'fit'
        //                 }
        //             ]
        //         },{
        //             title: 'Teyp of Business',
        //             layout: 'fit',
        //             items: [
        //                 {
        //                     xtype: 'panel',
        //                     id: 'type_of_bussiness_ft_grid',
        //                     bodyStyle: {
        //                         backgroundColor: 'transparent'
        //                     },
        //                     flex:1,
        //                     layout: 'fit'
        //                 },{
        //                     xtype: 'panel',
        //                     id: 'type_of_bussiness_ft_chart',
        //                     bodyStyle: {
        //                         backgroundColor: 'transparent'
        //                     },
        //                     flex:2,
        //                     layout: 'fit'
        //                 }
        //             ]
        //         },{
        //             title: 'Disaster Type',
        //             layout: 'fit',
        //             items: [
        //                 {
        //                     xtype: 'panel',
        //                     id: 'type_of_desaster_ft_grid',
        //                     bodyStyle: {
        //                         backgroundColor: 'transparent'
        //                     },
        //                     flex:1,
        //                     layout: 'fit'
        //                 },{
        //                     xtype: 'panel',
        //                     id: 'type_of_desaster_ft_chart',
        //                     bodyStyle: {
        //                         backgroundColor: 'transparent'
        //                     },
        //                     flex:2,
        //                     layout: 'fit'
        //                 }
        //             ]
        //         }
        //     ]
        // });
        // return commFactsPanel;

    };
    me.getDeraJaatFactsPanel = function (data, type) {
        var factsGrid = new Ext.grid.PropertyGrid({
            layout: 'fit',
            border: true,
            title: type,
            titleAlign: 'center',
            source: {
                "Building Age": JSON.stringify(data.age_of_building),
                "Plinth Level": JSON.stringify(data.plinth_level_of_building),
                "Stories": JSON.stringify(data.number_of_stories),
                "Pakka Rooms": JSON.stringify(data.number_of_pakka_rooms),
                "Kacha Rooms": JSON.stringify(data.number_of_kacha_rooms),
            },
            listeners: {
                select: function (selModel, record, index, options) {
                    me.tableChartData = record.data.value;
                    // alert(record.data.value);
                },
            },
            bbar: [
                {
                    icon: imgPath + 'chart.png',
                    tooltip: 'Get chart of selected record',
                },
                {
                    icon: imgPath + 'table.png',
                    tooltip: 'Get table of selected record',
                    handler: function () {
                        if (me.tableChartData == null || me.tableChartData == 'null') {
                            alert('No data to display.');
                        } else {
                            var data = JSON.parse(me.tableChartData);
                            var panel = me.getTablePanel(data);
                            me.getFactsWindow(panel, type, this);
                        }
                    }
                }
            ]
        });
        return factsGrid;
    };
    me.getEducationalFactsPanel = function (data, type) {
        var factsGrid = new Ext.grid.PropertyGrid({
            layout: 'fit',
            border: true,
            title: type,
            titleAlign: 'center',
            source: {
                "Ownership": JSON.stringify(data.ownership),
                "Institute Level": JSON.stringify(data.level_of_institute),
                "Teachers": JSON.stringify(data.number_of_teachers),
                "Students": JSON.stringify(data.number_of_students),
                "Class Rooms": JSON.stringify(data.number_of_class_rooms),
                "Washrooms": JSON.stringify(data.number_of_washrooms),
                "Water Supply": JSON.stringify(data.watersupply),
                "Electricity": JSON.stringify(data.electricity),
                "Boundry Wall": JSON.stringify(data.boundry_wall),
                "Construction Type": JSON.stringify(data.type_of_construction_of_building),

                "Building Age": JSON.stringify(data.age_of_building),
                "Effected": JSON.stringify(data.building_effected_from_disaster),
                "Emergency Exit": JSON.stringify(data.emergency_exit),
                "Evacuation Plan": JSON.stringify(data.evacuation_plan),
                "Damage Level": JSON.stringify(data.level_of_demage),
                "Plinth Level": JSON.stringify(data.plenth_level_of_building),
                "Security Guard": JSON.stringify(data.security_guard),
                "Disaster Type": JSON.stringify(data.type_of_desaster),
            },
            listeners: {
                select: function (selModel, record, index, options) {
                    me.tableChartData = record.data.value;
                    // alert(record.data.value);
                },
            },
            bbar: [
                {
                    icon: imgPath + 'chart.png',
                    tooltip: 'Get chart of selected record',
                },
                {
                    icon: imgPath + 'table.png',
                    tooltip: 'Get table of selected record',
                    handler: function () {
                        if (me.tableChartData == null || me.tableChartData == 'null') {
                            alert('No data to display.');
                        } else {
                            var data = JSON.parse(me.tableChartData);
                            var panel = me.getTablePanel(data);
                            me.getFactsWindow(panel, type, this);
                        }
                    }
                }
            ]
        });
        return factsGrid;
    };
    me.getGraveYardFactsPanel = function (data, type) {
        var factsGrid = new Ext.grid.PropertyGrid({
            layout: 'fit',
            border: true,
            title: type,
            titleAlign: 'center',
            source: {
                "Graveyard Type": JSON.stringify(data.type_of_graveyard),
                "Janazgah": JSON.stringify(data.janazagah),
            },
            listeners: {
                select: function (selModel, record, index, options) {
                    me.tableChartData = record.data.value;
                    // alert(record.data.value);
                },
            },
            bbar: [
                {
                    icon: imgPath + 'chart.png',
                    tooltip: 'Get chart of selected record',
                },
                {
                    icon: imgPath + 'table.png',
                    tooltip: 'Get table of selected record',
                    handler: function () {
                        if (me.tableChartData == null || me.tableChartData == 'null') {
                            alert('No data to display.');
                        } else {
                            var data = JSON.parse(me.tableChartData);
                            var panel = me.getTablePanel(data);
                            me.getFactsWindow(panel, type, this);
                        }
                    }
                }
            ]
        });
        return factsGrid;
    };
    me.getHealthFacilityFactsPanel = function (data, type) {
        var factsGrid = new Ext.grid.PropertyGrid({
            layout: 'fit',
            border: true,
            title: type,
            titleAlign: 'center',
            source: {
                "Health Facility": JSON.stringify(data.name_of_health_facility),
                "Medical Facility Type": JSON.stringify(data.medical_facility_type),
                "Ownership": JSON.stringify(data.ownership),
                "Beds": JSON.stringify(data.number_of_beds),
                "Nurses": JSON.stringify(data.number_of_nurses),
                "Dispensers": JSON.stringify(data.number_of_dispensers),
                "Leady Health Visitors": JSON.stringify(data.number_of_leady_health_visitors),
                "Medical Technicians": JSON.stringify(data.number_of_medical_technicians),
                "Snake Bite Kit": JSON.stringify(data.snake_byte_kit),
                "Epidemic Disease Medicine": JSON.stringify(data.epidemic_disease_medicine_available),
                "Construction Type": JSON.stringify(data.type_of_construction),
                "Doctors": JSON.stringify(data.number_of_doctors),
                "Veteran Doctor": JSON.stringify(data.number_of_veteran_doctor),
                "Veteran Techinicians": JSON.stringify(data.number_of_veteran_techinicians),
                "Epidemic Diseases Livestock": JSON.stringify(data.last_epidemic_diseases_livestock),
                "Health Information": JSON.stringify(data.health_information),
                "Boundry Wall": JSON.stringify(data.boundry_wall),
                "Building Age": JSON.stringify(data.age_of_building),
                "Plinth Level": JSON.stringify(data.plinth_level),
                "Security Guard": JSON.stringify(data.security_guard),
                "Emergency Exit": JSON.stringify(data.emergency_exit),
                "Evacuation Plan": JSON.stringify(data.evacuation_plan),
                "Building Effected": JSON.stringify(data.building_effected_from_disaster),
                "Disaster Type": JSON.stringify(data.type_of_disaster),
                "Damage Level": JSON.stringify(data.level_of_damage)
            },
            listeners: {
                select: function (selModel, record, index, options) {
                    me.tableChartData = record.data.value;
                    // alert(record.data.value);
                },
            },
            bbar: [
                {
                    icon: imgPath + 'chart.png',
                    tooltip: 'Get chart of selected record',
                },
                {
                    icon: imgPath + 'table.png',
                    tooltip: 'Get table of selected record',
                    handler: function () {
                        if (me.tableChartData == null || me.tableChartData == 'null') {
                            alert('No data to display.');
                        } else {
                            var data = JSON.parse(me.tableChartData);
                            var panel = me.getTablePanel(data);
                            me.getFactsWindow(panel, type, this);
                        }
                    }
                }
            ]
        });
        return factsGrid;
    };
    me.getIndustryFactsPanel = function (data, type) {
        var factsGrid = new Ext.grid.PropertyGrid({
            layout: 'fit',
            border: true,
            title: type,
            titleAlign: 'center',
            source: {
                "Industry Type": JSON.stringify(data.type_of_industry),
                "Employees": JSON.stringify(data.number_of_employee),
                "Chemical Used": JSON.stringify(data.chemical_used),
                "Industrial Waste Treatment Plant": JSON.stringify(data.industrial_waste_treatment_plant),
                "First Aid": JSON.stringify(data.first_aid_facility),
                "Fire Extinguisher": JSON.stringify(data.fire_extinguisher),
                "Toxic Chemicals": JSON.stringify(data.toxic_chemicals),
                "Fire Incident Happened": JSON.stringify(data.any_fire_incident_happen),
                "Damage Cost": JSON.stringify(data.cost_of_damage),
                "Building Age": JSON.stringify(data.age_of_building),
                "Plinth Level": JSON.stringify(data.plenth_level_of_building),
                "Security Guard": JSON.stringify(data.security_guard),
                "Emergency Exit": JSON.stringify(data.emergency_exit),
                "Evacuation Plan": JSON.stringify(data.evacuation_plan),
                "Building Effected": JSON.stringify(data.building_effected_from_desaster),
                "Disaster Type": JSON.stringify(data.type_of_desaster),
                "Damage Level": JSON.stringify(data.level_of_demage)
            },
            listeners: {
                select: function (selModel, record, index, options) {
                    me.tableChartData = record.data.value;
                    // alert(record.data.value);
                },
            },
            bbar: [
                {
                    icon: imgPath + 'chart.png',
                    tooltip: 'Get chart of selected record',
                },
                {
                    icon: imgPath + 'table.png',
                    tooltip: 'Get table of selected record',
                    handler: function () {
                        if (me.tableChartData == null || me.tableChartData == 'null') {
                            alert('No data to display.');
                        } else {
                            var data = JSON.parse(me.tableChartData);
                            var panel = me.getTablePanel(data);
                            me.getFactsWindow(panel, type, this);
                        }
                    }
                }
            ]
        });
        return factsGrid;
    };
    me.getInfrastructureFactsPanel = function (data, type) {
        var factsGrid = new Ext.grid.PropertyGrid({
            layout: 'fit',
            border: true,
            title: type,
            titleAlign: 'center',
            source: {
                "Road Width": JSON.stringify(data.road_width),
                "Road Category": JSON.stringify(data.road_category),
                "Road Type": JSON.stringify(data.road_type),
                "Maintained By": JSON.stringify(data.maintained_by),
                "Effected From Disaster": JSON.stringify(data.road_effected_from_desaster),
                "Disaster Type": JSON.stringify(data.type_of_desaster),
                "Damage Level": JSON.stringify(data.level_of_demage)
            },
            listeners: {
                select: function (selModel, record, index, options) {
                    me.tableChartData = record.data.value;
                    // alert(record.data.value);
                },
            },
            bbar: [
                {
                    icon: imgPath + 'chart.png',
                    tooltip: 'Get chart of selected record',
                },
                {
                    icon: imgPath + 'table.png',
                    tooltip: 'Get table of selected record',
                    handler: function () {
                        if (me.tableChartData == null || me.tableChartData == 'null') {
                            alert('No data to display.');
                        } else {
                            var data = JSON.parse(me.tableChartData);
                            var panel = me.getTablePanel(data);
                            me.getFactsWindow(panel, type, this);
                        }
                    }
                }
            ]
        });
        return factsGrid;
    };
    me.getMauzaGeneralSurveyFactsPanel = function (data, type) {
        var factsGrid = new Ext.grid.PropertyGrid({
            layout: 'fit',
            border: true,
            title: type,
            titleAlign: 'center',
            source: {
                "Mauza Name": JSON.stringify(data.mauza_name),
                "Disaster Year": JSON.stringify(data.year_of_disaster),
                "Surveying Settlement": JSON.stringify(data.name_of_surveying_settlement),
                "Village Population": JSON.stringify(data.village_population),
                "Number of Houses": JSON.stringify(data.no_of_houses_in_village),
            },
            // bbar:[{icon: imgPath + 'chart.png',},{icon: imgPath + 'table.png',}]
        });
        return factsGrid;
    };
    me.getParksFactsPanel = function (data, type) {
        var factsGrid = new Ext.grid.PropertyGrid({
            layout: 'fit',
            border: true,
            title: type,
            titleAlign: 'center',
            source: {
                "Boundry Wall": JSON.stringify(data.boundry_wall),
                "Security Guard": JSON.stringify(data.security_guard),
                "Building Type": JSON.stringify(data.type_of_building),
                "Swing Facility": JSON.stringify(data.swing_facility),
                "Tracks": JSON.stringify(data.tracks),
                "Refreshment Available": JSON.stringify(data.refreshment_available),
                "Toilets": JSON.stringify(data.toilets),
            },
            listeners: {
                select: function (selModel, record, index, options) {
                    me.tableChartData = record.data.value;
                    // alert(record.data.value);
                },
            },
            bbar: [
                {
                    icon: imgPath + 'chart.png',
                    tooltip: 'Get chart of selected record',
                },
                {
                    icon: imgPath + 'table.png',
                    tooltip: 'Get table of selected record',
                    handler: function () {
                        if (me.tableChartData == null || me.tableChartData == 'null') {
                            alert('No data to display.');
                        } else {
                            var data = JSON.parse(me.tableChartData);
                            var panel = me.getTablePanel(data);
                            me.getFactsWindow(panel, type, this);
                        }
                    }
                }
            ]
        });
        return factsGrid;
    };
    me.getPublicBuildingFactsPanel = function (data, type) {
        var factsGrid = new Ext.grid.PropertyGrid({
            layout: 'fit',
            border: true,
            title: type,
            titleAlign: 'center',
            source: {
                "Rooms": JSON.stringify(data.number_of_rooms),
                "Stories": JSON.stringify(data.number_of_stories),
                "Building Age": JSON.stringify(data.age_of_building),
                "Plinth Level": JSON.stringify(data.plenth_level_of_building),
                "Security Guard": JSON.stringify(data.security_guard),
                "Emergency Exit": JSON.stringify(data.emergency_exit),
                "Evacuation Plan": JSON.stringify(data.evacuation_plan),
                "Building Effected": JSON.stringify(data.building_effected_from_desaster),
                "Disaster Type": JSON.stringify(data.type_of_desaster),
                "Damage Level": JSON.stringify(data.level_of_demage),
            },
            listeners: {
                select: function (selModel, record, index, options) {
                    me.tableChartData = record.data.value;
                    // alert(record.data.value);
                },
            },
            bbar: [
                {
                    icon: imgPath + 'chart.png',
                    tooltip: 'Get chart of selected record',
                },
                {
                    icon: imgPath + 'table.png',
                    tooltip: 'Get table of selected record',
                    handler: function () {
                        if (me.tableChartData == null || me.tableChartData == 'null') {
                            alert('No data to display.');
                        } else {
                            var data = JSON.parse(me.tableChartData);
                            var panel = me.getTablePanel(data);
                            me.getFactsWindow(panel, type, this);
                        }
                    }
                }
            ]
        });
        return factsGrid;
    };
    me.getReligiousBuildingFactsPanel = function (data, type) {
        var factsGrid = new Ext.grid.PropertyGrid({
            layout: 'fit',
            border: true,
            title: type,
            titleAlign: 'center',
            source: {
                "Type Religious Building": JSON.stringify(data.type_of_religious_building),
                "Water Supply": JSON.stringify(data.water_supply),
                "Washrooms": JSON.stringify(data.number_of_washrooms),
                "Building Age": JSON.stringify(data.age_of_building),
                "Plinth Level": JSON.stringify(data.plenth_level_of_building),
                "Security Guard": JSON.stringify(data.security_guard),
                "Emergency Exit": JSON.stringify(data.emergency_exit),
                "Evacuation Plan": JSON.stringify(data.evacuation_plan),
                "Building Effected": JSON.stringify(data.building_effected_from_desaster),
                "Disaster Type": JSON.stringify(data.type_of_desaster),
                "Damage Level": JSON.stringify(data.level_of_demage),
            },
            listeners: {
                select: function (selModel, record, index, options) {
                    me.tableChartData = record.data.value;
                    // alert(record.data.value);
                },
            },
            bbar: [
                {
                    icon: imgPath + 'chart.png',
                    tooltip: 'Get chart of selected record',
                },
                {
                    icon: imgPath + 'table.png',
                    tooltip: 'Get table of selected record',
                    handler: function () {
                        if (me.tableChartData == null || me.tableChartData == 'null') {
                            alert('No data to display.');
                        } else {
                            var data = JSON.parse(me.tableChartData);
                            var panel = me.getTablePanel(data);
                            me.getFactsWindow(panel, type, this);
                        }
                    }
                }
            ]
        });
        return factsGrid;
    };
    me.getTerminalFactsPanel = function (data, type) {
        var factsGrid = new Ext.grid.PropertyGrid({
            layout: 'fit',
            border: true,
            title: type,
            titleAlign: 'center',
            source: {
                "Ownership": JSON.stringify(data.ownership),
                "Terminal Building": JSON.stringify(data.terminal_building),
                "Waiting Area": JSON.stringify(data.waiting_area),
                "Prayer Area": JSON.stringify(data.prayer_area),
                "Parking Area": JSON.stringify(data.parking_area),
                "Building Age": JSON.stringify(data.age_of_building),
                "Plinth Level": JSON.stringify(data.plenth_level_of_building),
                "Security Guard": JSON.stringify(data.security_guard),
                "Emergency Exit": JSON.stringify(data.emergency_exit),
                "Evacuation Plan": JSON.stringify(data.evacuation_plan),
                "Building Effected": JSON.stringify(data.building_effected_from_desaster),
                "Disaster Type": JSON.stringify(data.type_of_desaster),
                "Damage Level": JSON.stringify(data.level_of_demage),
            },
            listeners: {
                select: function (selModel, record, index, options) {
                    me.tableChartData = record.data.value;
                    // alert(record.data.value);
                },
            },
            bbar: [
                {
                    icon: imgPath + 'chart.png',
                    tooltip: 'Get chart of selected record',
                },
                {
                    icon: imgPath + 'table.png',
                    tooltip: 'Get table of selected record',
                    handler: function () {
                        if (me.tableChartData == null || me.tableChartData == 'null') {
                            alert('No data to display.');
                        } else {
                            var data = JSON.parse(me.tableChartData);
                            var panel = me.getTablePanel(data);
                            me.getFactsWindow(panel, type, this);
                        }
                    }
                }
            ]
        });
        return factsGrid;
    };
    me.getSurveyTypePanel = function (data, type) {
        var typePanel = null;
        if (type == 'Bridges') {
            typePanel = me.getBridgesTypePanel(data, type)
        }
        if (type == 'Collapse Building') {
            typePanel = me.getBridgesTypePanel(data, type)
        }
        if (type == 'Commercial') {
            typePanel = me.getBridgesTypePanel(data, type)
        }
        if (type == 'Dera Jaat') {
            typePanel = me.getBridgesTypePanel(data, type)
        }
        if (type == 'Educational') {
            typePanel = me.getBridgesTypePanel(data, type)
        }
        if (type == 'Grave Yard') {
            typePanel = me.getBridgesTypePanel(data, type)
        }
        if (type == 'Health Facility') {
            typePanel = me.getBridgesTypePanel(data, type)
        }
        if (type == 'Industry') {
            typePanel = me.getBridgesTypePanel(data, type)
        }
        if (type == 'Infrastructure') {
            typePanel = me.getBridgesTypePanel(data, type)
        }
        if (type == 'Mauza General Survey') {
            typePanel = me.getBridgesTypePanel(data, type)
        }
        if (type == 'Parks') {
            typePanel = me.getBridgesTypePanel(data, type)
        }
        if (type == 'Public Building') {
            typePanel = me.getBridgesTypePanel(data, type)
        }
        if (type == 'Religious Building') {
            typePanel = me.getBridgesTypePanel(data, type)
        }
        if (type == 'Terminal') {
            typePanel = me.getBridgesTypePanel(data, type)
        }
        return typePanel;
    }
    me.getFactsWindow = function (panel, type, animate) {
        if (me.factsWindow != null) {
            me.factsWindow.destroy();
        }
        me.factsWindow = Ext.create('Ext.window.Window', {
            id: 'reportWin',
            title: type + ' Facts',
            layout: 'fit',
            width: 350,
            height: 350,
            titleAlign: 'center',
            animateTarget: animate,
            closeAction: 'destroy',
            preventBodyReset: true,
            constrainHeader: true,
            collapsible: false,
            plain: true,
            items: panel
        });
        me.factsWindow.show();
    };
    me.getFactsChartWindow = function (type, animate, data, categories, xLabel, yLabel) {
        if (me.factsChartWindow != null) {
            me.factsChartWindow.destroy();
        }
        me.factsChartWindow = Ext.create('Ext.window.Window', {
            id: 'factsChartWin',
            title: type + ' Facts Chart',
            layout: 'fit',
            width: 500,
            height: 350,
            titleAlign: 'center',
            animateTarget: animate,
            closeAction: 'destroy',
            preventBodyReset: true,
            constrainHeader: true,
            collapsible: false,
            plain: true,
            items: [{
                xtype: 'panel',
                layout: 'fit',
                id: 'pnlFactsChart',
            }]
        });
        me.factsChartWindow.show();
        me.getColumnChart(data, categories, 'pnlFactsChart', xLabel, yLabel);
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
    me.getTableColumns = function (data) {
        var columns = [];
        var stringType = "string";
        var numberType = 'number';
        columns.push({xtype: 'rownumberer'});
        for (var key in data) {
            if (key === "count" || key === 'id') {
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
                }
                else {
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
        columns.push({
            dataIndex: 'count',
            text: 'count',
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
        });
        return columns;
    }
    me.getColumnsList = function (data) {
        var columns = [];
        var stringType = "string";
        var numberType = 'number';
        columns.push({xtype: 'rownumberer'});
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
                }
                else {
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
    me.getTablePanel = function (data) {
        var store = Ext.create('Ext.data.Store', {
            id: 'tableDataStore',
            fields: me.getFieldsList(data[0]),
            data: data,
        });
        var gridPanel = Ext.create('Ext.grid.Panel', {
            layout: 'fit',
            id: 'tableDataPanel',
            titleAlign: 'center',
            store: store,
            stripeRows: true,
            columnLines: true,
            plugins: ['gridfilters'],
            autoScroll: true,
            loadMask: true,
            autoDestroy: true,
            columns: me.getTableColumns(data[0]),
        });
        return gridPanel;
    }

    me.getChartKey = function (data) {
        var field = '';
        for (var key in data) {
            var obj = {};
            if (key === "count") {
            } else {
                field = key;
            }
        }
        return field;
    }
    me.getColumnChart = function (data, categories, divId, xLabel, yTitle) {
        var chartPanel = Ext.getCmp(divId);
        chartPanel.removeAll();
        var chartDiv = chartPanel.body.dom;
        me.statsChart = Highcharts.chart(chartDiv, {
            chart: {
                type: 'column'
            },
            title: {
                text: xLabel
            },
            xAxis: {
                categories: categories,
                crosshair: true
            },
            yAxis: {
                min: 0,
                title: {
                    text: yTitle
                }
            },
            legend: {
                align: 'center',
                verticalAlign: 'bottom',
            },
            tooltip: {
                headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f}</b></td></tr>',
                footerFormat: '</table>',
                shared: true,
                useHTML: true
            },
            plotOptions: {
                column: {
                    pointPadding: 0.2,
                    borderWidth: 0
                }
            },
            series: data
        });

    };
    me.getChartCategoriesList = function (data, key) {
        var dataList = [];
        for (var i = 0; i < data.length; i++) {
            var value = data[i][key];
            dataList.push(value);
        }
        return dataList;
    };
    me.getChartData = function (data, key) {
        var dataList = [];
        for (var i = 0; i < data.length; i++) {
            var year = data[i][key];
            dataList.push(year);
        }
        return [{name: me.chartTitle, data: dataList}];
    };

}