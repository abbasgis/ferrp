/**
 * Created by ather on 10/17/2017.
 */
// import OLCesium from 'olcs/OLCesium.js';
// var feature = source.getFeatures()[1];
// var point = /** @type {ol.geom.Point} */ (feature.getGeometry());
// var size = /** @type {ol.Size} */ (map.getSize());
// me.getView().centerOn(point.getCoordinates(), size, [570, 500]);

var OLMapModel = function (extent, mapTarget, layerSwitcherTarget, viewModel, token, cameraSettingVM) {
    var me = this;
    // var mapDiv = mapDiv
    me.viewModel = viewModel;
    me.statsModel = null;
    me.fullScreenTarget = 'jqxLayout';
    me.mapTarget = mapTarget;
    me.layerSwitcherTarget = layerSwitcherTarget;
    me.defaultInteractionsColl = null;

    // me.specialLayers =[];
    me.extent = extent;
    me.bing_map_key = 'nIpvP3DE4KDIPD5rbvf8~tYqmHfqtK9FrpulnwqB6Ow~AlfsQeqqd1RiQqE5rzdQnrgwjgawr26TNXWuLLIrlyMRj2JEp_IhUATReKhb4rCt';
    me.open_weather_map_key = ['e9c0f98767ed96cefc3dd01adf8aacf2'];
    me.style = null;
    me.view = null;
    me.map = null;
    me.minZoom = 5;
    me.center = ol.extent.getCenter(extent);
    me.progressbar = new ProgressBarModel();
    me.previousExtentList = [];
    me.nextExtentList = [];
    me.overlayLayers = [];
    me.specialLayers = [];
    me.weatherLayers = null;
    me.labelLayers = [];
    me.groupLayers = [];
    me.weatherLayersGroup = new ol.layer.Group({
        title: 'Weather Layers',
        identify: false,
        openInLayerSwitcher: true,
        layers: []
    });
    me.selectedFeatureLayer = null;
    me.drawFeatureLayer = null;
    me.csrfToken = token;
    me.threeDEnable = false;
    me.olCesiumModel = null;
    me.cameraSettingVM = cameraSettingVM;
    me.geocoder = null;
    me.setViewModel = function (viewModel) {
        me.viewModel = viewModel;
    }

    me.initialize = function () {
        me.createStyle();
        me.addBaseLayer("Bing-Hybrid");
        me.addSelectedFeatureLayer();
        me.addDrawFeatureLayer();
        me.addPathFeatureLayer();
        me.view = new ol.View({
            center: me.center,
            zoom: me.minZoom,
            extent: me.extent
        });
        me.map = new ol.Map({
            target: me.mapTarget,
            // openInLayerSwitcher: true,
            controls: me.getControls(),
            interactions: ol.interaction.defaults({
                pinchRotate: true,
                dragPan: true,
                DragRotate: false,
                DragZoom: true,
                mouseWheelZoom: true
            }),
            layers: [
                me.baseLayers,
                me.specialLayers["selectedFeatureLayer"],
                me.specialLayers["drawFeatureLayer"],
                me.specialLayers["pathFeatureLayer"]
            ],
            view: me.view

        });
        // me.map.getLayers().on("propertychange", function (e) {
        //     // triggered when layer added or removed
        //     // alert(e);
        //     console.log(e)
        //
        // });
        me.setViewExtent(me.extent);
        me.defaultInteractionsColl = me.map.getInteractions();
        me.viewport = me.map.getViewport();
        me.addLayerSwitcher();
        me.addPopupOverlay();
        me.geocoder = new Geocoder('nominatim', {
            provider: 'osm',
            lang: 'en',
            placeholder: 'Search for ...',
            limit: 5,
            debug: false,
            autoComplete: true,
            keepOpen: true
        });
        me.map.addControl(me.geocoder);
        // me.geocoder.getLayer().setVisible(false);
        me.geocoder.on('addresschosen', function (evt) {
            window.setTimeout(function () {
                // me.geocoder.getLayer().getSource().clear();
                // alert(evt.coordinate+" ---,--- "+evt.address.formatted);
            }, 3000);
        });

    }

    me.addPopupOverlay = function () {
        me.popup = new Popup();
        me.map.addOverlay(me.popup);
    }

    me.getMap = function () {
        return me.map;
    }

    me.getView = function () {
        return me.view;
    }
    me.resizeMapArea = function () {
        me.map.updateSize();
    }

    me.addBaseLayer = function (base_type) {
        base_type = (!base_type ? "all" : base_type);
        if (!me.baseLayers) {
            me.baseLayers = new ol.layer.Group({
                title: 'Base Layers',
                info: false,
                openInLayerSwitcher: true,
                layers: []
            });
        }
        if (base_type == "OSM") {
            me.addOSM2BaseLayers(true);
        } else if (base_type.search("Bing") != "-1") {
            me.addBingMap2BaseLayers(base_type, true)
        } else {
            me.addOSM2BaseLayers(false);
            me.addBingMap2BaseLayers(base_type, false)
        }
    }

    me.addOSM2BaseLayers = function (visible) {
        var osmLayer = new ol.layer.Tile({
            title: "OSM",
            info: false,
            // baseLayer: true,
            source: new ol.source.OSM(),
            visible: visible
        });
        var layers = me.baseLayers.getLayers();
        layers.insertAt(layers.getLength(), osmLayer);
    }

    me.addBingMap2BaseLayers = function (bing_type, visible) {
        var imagerySet = [];
        switch (bing_type) {
            case "Bing-Aerial":
                imagerySet.push({title: bing_type, iSet: "Aerial"});
                break;
            case "Bing-Road":
                imagerySet.push({title: bing_type, iSet: "Road"});
                break;
            case "Bing-Hybrid":
                imagerySet.push({title: bing_type, iSet: 'AerialWithLabels'});
                break;
            default:
                imagerySet.push({title: "Bing-Aerial", iSet: "Aerial"});
                imagerySet.push({title: "Bing-Road", iSet: "Road"});
                imagerySet.push({title: "Bing-Hybrid", iSet: 'AerialWithLabels'});
        }
        for (var i = 0; i < imagerySet.length; i++) {
            visible = (imagerySet[i].title == "Bing-Hybrid" ? true : visible);
            var bingLayer = new ol.layer.Tile({
                title: imagerySet[i].title,
                info: false,
                visible: visible,
                source: new ol.source.BingMaps({key: me.bing_map_key, imagerySet: imagerySet[i].iSet})
            })
            var layers = me.baseLayers.getLayers();
            layers.insertAt(layers.getLength(), bingLayer);
        }
    }

    me.getVectorLayerByName = function (layer_name) {
        return me.overlayLayers[layer_name];
    };
    me.getLayerNames = function () {
        var layerNames = [];
        me.map.getLayers().forEach(function (layer) {
            var layerName = layer.get('title');
            for (var key in me.overlayLayers) {
                if (layerName == key) {
                    layerNames.push(layerName);
                    break;
                }
            }


        })

        return layerNames;
    };
    me.getLayerNamesWithStyle = function () {
        var layers = [];
        me.map.getLayers().forEach(function (layer) {
            var layerName = layer.get('title');
            for (var key in me.overlayLayers) {
                if (layerName == key) {
                    var layerStyle = me.getLayerStyle(layerName);
                    layers.push({'layer_name': layerName, 'layer_style': layerStyle});
                    break;
                }
            }


        })

        return layers;
    }
    me.getLayerNamesInGroupWithStyle = function (group_name) {
        var layers = [];
        var groupLayers = me.groupLayers[group_name];
        groupLayers.getLayers().forEach(function (layer) {
            var layerName = layer.get('title');
            for (var key in me.overlayLayers) {
                if (layerName == key) {
                    var layerStyle = me.getLayerStyle(layerName);
                    layers.push({'layer_name': layerName, 'layer_style': layerStyle});
                    break;
                }
            }


        })

        return layers;
    }
    me.addResultImageWMSLayer = function (result_table, url, layer_name, style) {
        var layers = layer_name;
        var params = {'LAYERS': layers, 'RESULT_TABLE': result_table};
        if (style && style !== '') {
            var styles = {"style": style};
            params.STYLES = JSON.stringify(styles);
        }
        me.overlayLayers[layer_name] = new ol.layer.Image({
            // extent: me.extent,
            title: layer_name,
            info: true,
            openInLayerSwitcher: true,
            source: new ol.source.ImageWMS({
                url: url,
                params: params,
                ratio: 1,
                // serverType: 'geoserver'
            })
        });
        me.map.addLayer(me.overlayLayers[layer_name]);
        return me.overlayLayers[layer_name];
    }
    me.addImageWMSLayer = function (url, layer_name, style) {
        if (!url) url = "web_services/wms/get_map/"
        var layers = layer_name;
        var params = {'LAYERS': layers};
        if (style && style !== '') {
            var styles = {"style": style};
            params.STYLES = JSON.stringify(styles);
        }
        me.overlayLayers[layer_name] = new ol.layer.Image({
            // extent: me.extent,
            title: layer_name,
            info: true,
            openInLayerSwitcher: true,
            source: new ol.source.ImageWMS({
                url: url,
                params: params,
                ratio: 1,
                // serverType: 'geoserver'
            })
        });
        me.map.addLayer(me.overlayLayers[layer_name]);
        return me.overlayLayers[layer_name];
    }

    me.addTileWMSLayer = function (url, layer_name, style, group_name) {
        if (!me.overlayLayers[layer_name]) {
            if (group_name === '') group_name = 'Unspecified'
            var layers = layer_name;
            var params = {'LAYERS': layers};
            var minResolution = 0;
            var maxResolution = 100000;
            if (style && style !== '') {
                // style = JSON.parse(style);
                var styles;
                if ('style' in style) {
                    styles = style
                } else {
                    styles = {"style": style};
                }
                params.STYLES = JSON.stringify(styles);
                // params.STYLES = style
            }
            me.overlayLayers[layer_name] = new ol.layer.Tile({
                // extent: me.extent,
                openInLayerSwitcher: true,
                title: layer_name,
                info: true,
                source: new ol.source.TileWMS({
                    url: url,
                    params: params,
                    ratio: 1,
                    // serverType: 'geoserver'
                }),
                minResolution: minResolution,
                maxResolution: maxResolution
            });
            if (!me.groupLayers[group_name]) {
                me.groupLayers[group_name] = new ol.layer.Group({
                    title: group_name,
                    identify: false,
                    openInLayerSwitcher: true,
                    layers: []
                });
                me.map.addLayer(me.groupLayers[group_name]);
            }
            var groupLayers = me.groupLayers[group_name].getLayers();
            groupLayers.insertAt(groupLayers.getLength(), me.overlayLayers[layer_name]);
        }
        // me.map.addLayer(me.overlayLayers[layer_name]);
        return me.overlayLayers[layer_name]
    }
    me.addTileWeatherMap = function (layer_name, layer_type) {
        if (me.weatherLayers === null) {
            me.weatherLayers = [];
            me.map.addLayer(me.weatherLayersGroup);
        }
        var url = 'https://tile.openweathermap.org/map/' + layer_type + '/{z}/{x}/{y}.png?appid=e9c0f98767ed96cefc3dd01adf8aacf2'
        var layer = new ol.layer.Tile({
            title: layer_name,
            info: 'weather',
            name: layer_name,
            source: new ol.source.XYZ({
                url: url,
                crossOrigion: 'anonymous'
            }),
            visible: true,
            opacity: 0.9
        });
        if (!me.weatherLayers[layer_name]) {
            me.weatherLayers[layer_name] = layer;
            var layers = me.weatherLayersGroup.getLayers();
            layers.insertAt(layers.getLength(), layer);
            // me.map.addLayer(me.weatherLayers[layer_name]);
        }
    };
    me.getWeatherData = function (layer_name) {
        if (!me.weatherLayers[layer_name]) {
            var westLng = 60;
            var northLat = 23;
            var eastLng = 77;
            var southLat = 38;
            var geojson = new ol.format.GeoJSON();
            var requestURLString = "http://api.openweathermap.org/data/2.5/box/city?bbox="
                + westLng + "," + northLat + "," //left top
                + eastLng + "," + southLat + ",10" //right bottom
                + "&cluster=yes&format=json"
                + "&APPID=" + me.open_weather_map_key[0];
            var params = {url: requestURLString, type: "GET", dataType: "json", processData: false};
            callAJAX(params, function (results) {
                if (results.list.length > 0) {
                    var features = [];
                    for (var i = 0; i < results.list.length; i++) {
                        features.push(me.convertWeatherJsonToGeoJson(results.list[i]));
                    }
                    var featuresGeoJson = {'type': 'FeatureCollection', 'features': features};
                    me.createWeatherClusterLayer(featuresGeoJson, layer_name);
                }
            });
        }
    };
    me.createWeatherClusterLayer = function (geo_json, layer_name) {
        var vectorSource = new ol.source.Vector({
            features: (new ol.format.GeoJSON()).readFeatures(geo_json, {
                dataProjection: 'EPSG:4326',
                featureProjection: 'EPSG:3857'
            }),
        });
        var clusterSource = new ol.source.Cluster({
            source: vectorSource,
            distance: 60
        });
        var clusterLayer = new ol.layer.Vector({
            source: clusterSource,
            title: layer_name,
            info: false,
            name: layer_name,
            style: me.getWeatherFeatureStyle
        });
        me.weatherLayers[layer_name] = clusterLayer;
        me.map.addLayer(me.weatherLayers[layer_name]);
        me.createWeatherPopUp();
    };
    me.showDialog = function (title, modalbody, size) {
        BootstrapDialog.show({
            title: title,
            type: BootstrapDialog.TYPE_SUCCESS,
            size: size,
            message: modalbody,
            draggable: true,
            buttons: [{
                label: 'Close',
                action: function (dialogItself) {
                    dialogItself.close()
                }
            }]
        })
    };
    me.createWeatherPopUp = function () {
        me.map.on('singleclick', function (event) {
            var modalbody = $('<div ></div>');
            var feature = me.map.forEachFeatureAtPixel(event.pixel,
                function (feature, layer) {
                    if (feature) {
                        var coord = me.map.getCoordinateFromPixel(event.pixel);
                        if (typeof feature.get('features') === 'undefined') {
                            alert(feature.get('city'));
                            modalbody.append('<img src="' + feature.get('icon') + '"> <h5>' + feature.get('city') + '</h5>');
                        } else {
                            var cfeatures = feature.get('features');
                            if (cfeatures.length > 1) {
                                // alert(cfeatures[0].get('city'));
                                modalbody.append('<h5><strong>Cities</strong></h5>');
                                for (var i = 0; i < cfeatures.length; i++) {
                                    modalbody.append('<article>' + cfeatures[i].get('city') + '</article>');
                                }
                            }
                            if (cfeatures.length == 1) {
                                modalbody.append('<center><img src="' + cfeatures[0].get('icon') + '"><h6><b>' + cfeatures[0].get('city') + '</b></h6><p>' + cfeatures[0].get('weather') + '</p><p>' + cfeatures[0].get('temperature') + ' &deg;C</p></center>');
                            }
                        }
                    }
                });
            me.showDialog("Weather Detail", modalbody, BootstrapDialog.SIZE_SMALL);
        });
    };
    me.getWeatherFeatureStyle = function (feature, resolution) {
        var styleCache = {};
        var size = feature.get('features')[0];
        var urlIcon = size.get('icon');
        var style = styleCache[urlIcon];
        if (!style) {
            style = [new ol.style.Style({
                image: new ol.style.Icon({
                    src: urlIcon
                }),
            })];
            styleCache[size] = style;
        }
        return style;
    }
    me.convertWeatherJsonToGeoJson = function (weatherItem) {
        var feature = {
            type: "Feature",
            properties: {
                city: weatherItem.name,
                weather: weatherItem.weather[0].main,
                temperature: weatherItem.main.temp,
                min: weatherItem.main.temp_min,
                max: weatherItem.main.temp_max,
                humidity: weatherItem.main.humidity,
                pressure: weatherItem.main.pressure,
                windSpeed: weatherItem.wind.speed,
                windDegrees: weatherItem.wind.deg,
                windGust: weatherItem.wind.gust,
                icon: "http://openweathermap.org/img/w/"
                + weatherItem.weather[0].icon + ".png",
                coordinates: [weatherItem.coord.Lon, weatherItem.coord.Lat]

            },
            geometry: {
                type: "Point",
                coordinates: [weatherItem.coord.Lon, weatherItem.coord.Lat]
            }
        };
        return feature;
    }
    me.addTileVectorLayer = function (url, layer_name) {
        // var url = url + '?version=1.1.0&request=GetFeature&layer_name=' + layer_name;
        var tiledSource = new ol.source.VectorTile({
            // format: new ol.format.MVT(),
            format: new ol.format.GeoJSON(),
            tileLoadFunction: function (tile) {
                var format = tile.getFormat();
                var tileCoord = tile.getTileCoord();
                var data = tileIndex.getTile(tileCoord[0], tileCoord[1], -tileCoord[2] - 1);
                var feature = data;
                // var features = format.readFeatures(
                //     JSON.stringify({
                //         type: 'FeatureCollection',
                //         features: data ? data.features : []
                //     }, replacer));
                tile.setLoader(function () {
                    tile.setFeatures(features);
                    // tile.setProjection(tilePixels);
                });
            },
            url: url
        });


        // var tiledVector = new ol.layer.Vector({
        //     source: tiledSource,
        //     style: vectorStyle
        // });

        me.overlayLayers[layer_name] = new ol.layer.VectorTile({
            // source: vectorSource
            title: layer_name,
            info: true,
            source: tiledSource,
            style: function (feature) {
                // highlightStyle.getText().setText(feature.get('name'));
                // return highlightStyle;
                return me.getStyle(feature);
            }
        })
        me.map.addLayer(me.overlayLayers[layer_name]);
        return me.overlayLayers[layer_name];
    }
    me.addVectorLayer = function (url, layer_name) {
        me.url = url;
        me.vectorSource = new ol.source.Vector({
            format: new ol.format.GeoJSON(),
            loader: function (extent, resolution, projection) {
                var size = me.map.getSize();
                me.url = me.url + '?version=1.1.0&request=GetFeature&layer_name=' + layer_name + '&' +
                    'outputFormat=application/json&srsname=EPSG:3857&width=' + size[0] + '&height=' + size[1] +
                    '&resolution=' + resolution + '&bbox=' + extent.join(',') + ',EPSG:3857';
                me.vectorSource.clear(false);
                $.getJSON(me.url, function (data) {
                    me.vectorSource.addFeatures((new ol.format.GeoJSON()).readFeatures(data));
                })
            },
            strategy: ol.loadingstrategy.bbox
        });
        me.overlayLayers[layer_name] = new ol.layer.Vector({
            title: layer_name,
            info: true,
            source: me.vectorSource,
            style: function (feature) {
                // highlightStyle.getText().setText(feature.get('name'));
                // return highlightStyle;
                return me.getStyle(feature);
            }
        });
        me.map.addLayer(me.overlayLayers[layer_name]);
        return me.overlayLayers[layer_name];
    }
    me.addFeaturesToPathLayer = function (features) {
        // for (var i = 0; i < features.length; i++) {
        var vectorSource = me.specialLayers["pathFeatureLayer"].getSource();
        // if (clearPrevious) vectorSource.clear();
        vectorSource.addFeatures(features);
        // }
    }
    me.addGeoJSON2PathLayer = function (geojson) {
        if (geojson.features != null) {
            var features = (new ol.format.GeoJSON()).readFeatures(geojson)
            if (features.length > 0) {
                me.addFeaturesToPathLayer(features)
            } else {
                showAlertDialog("No Path found", dialogTypes.info)
            }
        } else {
            showAlertDialog("No Path found", dialogTypes.info)
        }
    }
    me.clearPathLayer = function () {
        var vectorSource = me.specialLayers["pathFeatureLayer"].getSource();
        vectorSource.clear();
    }
    me.addPathFeatureLayer = function () {
        me.specialLayers["pathFeatureLayer"] = new ol.layer.Vector({
            title: "Path Layer",
            info: true,
            // openInLayerSwitcher: false,
            displayInLayerSwitcher: false,
            source: new ol.source.Vector({
                features: []
            }),
            style: function (feature) {
                return me.getPathStyle(feature)
            }
        });
        me.specialLayers["pathFeatureLayer"].setZIndex(995)
    }

    me.addDrawFeatureLayer = function () {
        me.specialLayers["drawFeatureLayer"] = new ol.layer.Vector({
            title: "Draw layer",
            info: false,
            // openInLayerSwitcher: false,
            displayInLayerSwitcher: false,
            source: new ol.source.Vector({
                features: []
            }),
            style: function (feature) {
                return me.getSelectStyle(feature)
            }
        });
        var source = me.specialLayers["drawFeatureLayer"].getSource();
        source.on('addfeature', function (e) {
            me.flash(e.feature);
        });

        me.specialLayers["drawFeatureLayer"].setZIndex(1000)
    }
    me.addSelectedFeatureLayer = function () {
        me.specialLayers["selectedFeatureLayer"] = new ol.layer.Vector({
            title: "selected features",
            info: false,
            // openInLayerSwitcher: false,
            displayInLayerSwitcher: false,
            source: new ol.source.Vector({
                features: []
            }),
            style: function (feature) {
                return me.getSelectStyle(feature)
            }
        });
        var source = me.specialLayers["selectedFeatureLayer"].getSource();
        source.on('addfeature', function (e) {
            me.flash(e.feature);
        });
        me.specialLayers["selectedFeatureLayer"].setZIndex(999)
    }

    me.clearSelection = function () {
        if (me.popup.isOpened)
            me.popup.hide();
        var vectorSource = me.specialLayers["selectedFeatureLayer"].getSource();
        vectorSource.clear();
        var drawSource = me.specialLayers["drawFeatureLayer"].getSource();
        drawSource.clear();
        me.clearPathLayer();
        me.removeAllInteraction();
        me.addBasicInteraction();
        me.geocoder.getLayer().getSource().clear();
    }

    me.convertGeom2WKT = function (geometry) {
        var format = new ol.format.WKT();
        var wkt = format.writeGeometry(geometry);
        return wkt;
    }
    me.getSelectedFeatureGeometryCombined = function () {
        // import {Point, LineString, Polygon, MultiPoint, MultiLineString, MultiPolygon} from 'ol/geom.js';
        var vectorSource = me.specialLayers["selectedFeatureLayer"].getSource();
        var features = vectorSource.getFeatures();
        var parser = new jsts.io.OL3Parser();
        parser.inject(ol.geom.Point, ol.geom.LineString, ol.geom.LinearRing, ol.geom.Polygon,
            ol.geom.MultiPoint, ol.geom.MultiLineString, ol.geom.MultiPolygon);
        var geom = null;
        for (var i = 0; i < features.length; i++) {
            var jstsGeom = parser.read(features[i].getGeometry());
            if (i == 0)
                geom = jstsGeom;
            else
                geom = geom.union(jstsGeom);

        }
        finalGeom = parser.write(geom)
        return finalGeom;

    }
    me.showSelectedFeatureGeometry = function (wkt, clearPrevious) {
        // if (!clearPrevious) clearPrevious = true;
        var format = new ol.format.WKT();
        var feature = format.readFeature(wkt, {
            dataProjection: 'EPSG:3857',
            featureProjection: 'EPSG:3857'
        });
        var vectorSource = me.specialLayers["selectedFeatureLayer"].getSource();
        if (clearPrevious) vectorSource.clear();
        vectorSource.addFeature(feature);

    }


    me.showSelectedFeatureGeojson = function (geojson, coordinate) {

        // var format = new ol.format.GeoJSON();
        // var feature = format.readFeature(geojson, {
        //     dataProjection: 'EPSG:3857',
        //     featureProjection: 'EPSG:3857'
        // });
        me.clearSelection()
        if (geojson.features != null) {
            var features = (new ol.format.GeoJSON()).readFeatures(geojson)
            if (features.length > 0) {
                var vectorSource = me.specialLayers["selectedFeatureLayer"].getSource();
                // if (clearPrevious) vectorSource.clear();
                vectorSource.addFeatures(features);
                var content = me.createPropertyTableConent(features[0].getProperties())

                me.popup.show(coordinate, content)
                // setPopupContent(features[0].getProperties())
                // me.popup.setPosition(coordinate);
            }
        } else {
            showAlertDialog("No feature found", dialogTypes.info)
        }
    }
    me.createPropertyTableConent = function (json) {
        var content = "<table class='table table-condensed'>"
        content += "<th>Name</th><th>Value</th>"
        for (var key in json) {
            if (key != "geometry") {
                content += "<tr>";
                content += "<td>" + key + "</td>";
                content += "<td>" + json[key] + "</td>";
                content += "</tr>";
            }
        }
        content += "</table>";
        return content;
    }
    me.getControls = function () {
        var controls = ol.control.defaults().extend([
            // new RotateNorthControl(),
            // new ol.control.ScaleLine({
            //     units: 'metric',
            //     target: document.getElementById('scale-line'),
            //     className: 'custom-scale-position',
            //
            // }),
            new ol.control.MousePosition({
                // coordinateFormat: ol.coordinate.createStringXY(4),
                coordinateFormat: function (coordinate) {
                    return ol.coordinate.format(coordinate, '{x}, {y}', 5);
                },
                projection: 'EPSG:3857',
                // comment the following two lines to have the mouse position
                // be placed within the map.
                className: 'custom-mouse-position',
                // target: document.getElementById('mouse-position'),
                // undefinedHTML: '&nbsp;',
                // render:function(event){
                //     position = event.frameState.focus;
                //     target = document.getElementById('mouse-position');
                //     target.innerHTML = position
                // }
            }),
            new ol.control.FullScreen({source: me.fullScreenTarget}),
            new ol.control.ZoomToExtent({extent: me.extent})
        ]);
        return controls;
    }
    me.addLayerSwitcher = function (target) {
        var switcher;
        if (!me.layerSwitcherTarget) {
            switcher = new ol.control.LayerSwitcher();
        } else {
            switcher = new ol.control.LayerSwitcher({
                target: $("." + me.layerSwitcherTarget).get(0),
                show_progress: true,
                extent: true,
                trash: true,
                oninfo: function (l) {
                    var info = l.get("info");
                    if (info) {
                        me.viewModel.layerContextMenuModel.openLayerContextMenu(l)
                    } else {
                        showAlertDialog("Info not available. . ", dialogTypes.info)

                    }
                }
            });
        }
        me.map.addControl(switcher)
    };
    me.addTempStyleToWMSLayer = function (layerName, style) {
        var layer = me.overlayLayers[layerName];
        var source = layer.getSource();
        var params = source.getParams();
        // if (params.STYLES ==""){
        var styles = {"style": style};
        params.STYLES = JSON.stringify(styles);
        // }else{
        //
        // }
        params.t = new Date().getMilliseconds();
        source.updateParams(params);
    }

    me.createLabelStyle = function (labelInfo) {
        var font = labelInfo.fontSize + 'px Calibri,sans-serif'; //+label.fontType
        var labelStyle = new ol.style.Style({
            text: new ol.style.Text({
                font: font, //'12px Calibri,sans-serif',
                overflow: true,
                fill: new ol.style.Fill({
                    color: labelInfo.labelColor
                }),
                stroke: new ol.style.Stroke({
                    color: '#fff',
                    width: 2
                })
            })
        });
        return labelStyle;
    }
    me.changeLabelStyle = function (labelInfo, layerName) {
        var labelLayer = me.labelLayers[layerName]['layer'];
        var labelStyle = me.createLabelStyle(labelInfo);
        // me.labelLayers[layerName]['labelStyle'] = labelStyle
        // function (feature) {
        //         me.labelLayers[layerName]['labelStyle'].getText().setText(feature.get('label'));
        //         return labelStyle;
        //     },

        var styleFunction = function (feature) { //, resolution
            labelStyle.getText().setText(feature.get('label'));
            return labelStyle;
        }
        labelLayer.setStyle(styleFunction);
        // var source = labelLayer.getSource().clear();
        // var url = '/web_services/wfs/get_label/geojson/?layer_name=' + layerName + "&label_field=" + labelInfo.colName;
        // $.getJSON(url, function (data) {
        //     me.labelLayers[layerName]['layer'].get('source').addFeatures((new ol.format.GeoJSON()).readFeatures(data));
        // });
    }
    me.addLabelLayer = function (labelInfo, layerName) {
        var title = layerName + "_label";
        var labelStyle = me.createLabelStyle(labelInfo)
        var labelLayer = new ol.layer.Vector({
            title: title,
            info: false,
            // openInLayerSwitcher: false,
            displayInLayerSwitcher: false,
            source: new ol.source.Vector({
                // url: url,
                format: new ol.format.GeoJSON()
            }),
            // labelStyle: labelStyle,
            style: function (feature) {
                me.labelLayers[layerName]['labelStyle'].getText().setText(feature.get('label'));
                return labelStyle;
            },
            declutter: true
        });
        me.map.addLayer(labelLayer);
        me.labelLayers[layerName] = {layer: labelLayer, labelStyle: labelStyle};
        var url = '/web_services/wfs/get_label/geojson/?layer_name=' + layerName + "&label_field=" + labelInfo.colName;
        $.getJSON(url, function (data) {
            me.labelLayers[layerName]['layer'].get('source').addFeatures((new ol.format.GeoJSON()).readFeatures(data));
        });

    }
    me.getLabelLayer = function (layerName) {
        return me.labelLayers[layerName];
    }
    me.addLabel2WMSLayer = function (layerName, colName, fontSize, fontType, labelColor) {
        var layer = me.overlayLayers[layerName];
        var source = layer.getSource();
        var params = source.getParams();
        var label = {"colName": colName, "fontSize": fontSize, "fontType": fontType, "labelColor": labelColor};
        var styles = {"label": label};
        params.STYLES = JSON.stringify(styles);
        params.t = new Date().getMilliseconds();
        source.updateParams(params);
    }

    me.removeLabelFromWMSLayer = function (layerName) {
        var layer = me.overlayLayers[layerName];
        var source = layer.getSource();
        var params = source.getParams();

        params.STYLES = "";
        params.t = new Date().getMilliseconds();
        source.updateParams(params);
    }
    me.showLegendgraphics = function (layerName) {
        var modalbody = $('<div ></div>');
        var legends = me.getLegendGraphics(layerName)
        var table = $('<table class="table table-condensed"></table>');
        var thead = $('<thead><tr><th>Value</th><th>Symbol</th></tr></thead>');
        table.append(thead);
        var tbody = $('<tbody></tbody>');
        for (var i = 0; i < legends.length; i++) {
            var graphic = legends[i];
            var row = $('<tr><td>' + graphic.literal + '</td><td>' + graphic.style + '</td></tr>');
            tbody.append(row);
        }
        table.append(tbody)
        modalbody.append(table)
        BootstrapDialog.show({
            title: "Legend",
            type: BootstrapDialog.TYPE_SUCCESS,
            size: BootstrapDialog.SIZE_SMALL,
            message: modalbody,
            draggable: true,
            buttons: [{
                label: 'Close',
                action: function (dialogItself) {
                    dialogItself.close()
                }
            }]
        })
    };
    me.getLegendGraphics = function (layerName) {
        var style = me.getLayerStyle(layerName);
        var rules = style.rules;
        var legend = [];
        if (rules) {
            for (var i = 0; i < rules.length; i++) {
                var rule = rules[i];
                var graphic = {}
                for (var key in rule) {
                    if (key == "filter") {
                        if (rule[key].literal) {
                            graphic.literal = rule[key].literal;
                        } else {
                            graphic.literal = 'default';
                        }
                    }
                    if (key == "point_symbolizer") {
                        var symbolizer = rule[key]
                        var style = {}
                        style.fillColor = symbolizer.fill;
                        style.pointSize = symbolizer.size;
                        style.stroke = symbolizer.stroke;
                        style.strokeWidth = symbolizer["stroke-width"];
                        // var svg = $('<svg width="150" height="40"></svg>');
                        var shape = '<svg width="150" height="40"><circle cx="75" cy="10" r="' + style.pointSize + '" stroke="' + style.stroke +
                            '" stroke-width="' + style.strokeWidth + '" fill="' + style.fillColor + '" /> </svg>'
                        // svg.html(shape);
                        graphic.style = shape;
                        legend.push(graphic)
                    } else if (key == "polygon_symbolizer") {
                        var symbolizer = rule[key]
                        var style = {}
                        style.strokeWidth = symbolizer["stroke-width"];
                        style.stroke = symbolizer["stroke"];
                        style.fillColor = symbolizer["fill"];
                        style.fillOpacity = symbolizer["fill_opacity"];
                        var shape = '<svg width="150" height="40"><rect width="150" height="40"style="stroke-width:' + style.strokeWidth + ';stroke:' +
                            style.stroke + ';fill:' + style.fillColor + ';fill-opacity:' + style.fillOpacity + '" /></svg>'
                        graphic.style = shape;
                        legend.push(graphic)
                    } else if (key == "line_symbolizer") {
                        var symbolizer = rule[key]
                        var style = {}
                        style.strokeWidth = symbolizer["stroke-width"];
                        style.stroke = symbolizer["stroke"];
                        var shape = '<svg width="150" height="40"><line x1="0" y1="20" x2="150" y2="20" style="stroke-width:' +
                            style.strokeWidth + ';stroke:' + style.stroke + '" /></svg>';
                        graphic.style = shape;
                        legend.push(graphic)
                    } else if (key == 'raster_symbolizer') {
                        var symbolizer = rule[key]
                        var colorMaps = symbolizer["color_map"]
                        for (var i = 0; i < colorMaps.length; i++) {
                            graphic = {}
                            var style = {}
                            var colorMap = colorMaps[i]
                            style.fillColor = colorMap["color"];
                            style.fillOpacity = colorMap["opacity"];
                            var shape = '<svg width="150" height="40"><rect width="150" height="40"style=' +
                                '"fill:' + style.fillColor + ';fill-opacity:' + style.fillOpacity + '" /></svg>'
                            graphic.style = shape;
                            graphic.literal = colorMap["label"];
                            legend.push(graphic)
                        }

                    }
                }

            }
        }
        return legend;
    }
    me.getLayerStyle = function (layerName) {
        var layer = me.overlayLayers[layerName];
        var source = layer.getSource();
        var params = source.getParams();
        layerStyle = params.STYLES;
        if (!layerStyle) {
            var url = "/web_services/get_layer_style?layer_name=" + layerName;
            var layerStyle = callSJAX({url: url});
            layerStyle = JSON.parse(layerStyle);
        }
        if (typeof layerStyle == 'string') {
            layerStyle = JSON.parse(layerStyle);
        }
        return layerStyle
    }
    me.refreshLayer = function (layerName) {
        var layer = me.overlayLayers[layerName];
        var source = layer.getSource();
        var params = source.getParams();
        params.t = new Date().getMilliseconds();
        source.updateParams(params);
    };
    me.refreshMap = function () {
        me.map.render();
        me.map.renderSync();
    };
    me.createStyle = function () {
        var image = new ol.style.Circle({
            radius: 5,
            fill: null,
            stroke: new ol.style.Stroke({color: 'red', width: 1})
        });
        me.styles = {
            'Point': new ol.style.Style({
                image: image
            }),
            'LineString': new ol.style.Style({
                stroke: new ol.style.Stroke({
                    color: 'green',
                    width: 1
                })
            }),
            'MultiLineString': new ol.style.Style({
                stroke: new ol.style.Stroke({
                    color: 'green',
                    width: 1
                })
            }),
            'MultiPoint': new ol.style.Style({
                image: image
            }),
            'MultiPolygon': new ol.style.Style({
                stroke: new ol.style.Stroke({
                    color: 'yellow',
                    width: 1
                }),
                fill: new ol.style.Fill({
                    color: 'rgba(255, 255, 0, 0.1)'
                })
            }),
            'Polygon': new ol.style.Style({
                stroke: new ol.style.Stroke({
                    color: 'blue',
                    lineDash: [4],
                    width: 3
                }),
                fill: new ol.style.Fill({
                    color: 'rgba(0, 0, 255, 0.1)'
                })
            }),
            'GeometryCollection': new ol.style.Style({
                stroke: new ol.style.Stroke({
                    color: 'magenta',
                    width: 2
                }),
                fill: new ol.style.Fill({
                    color: 'magenta'
                }),
                image: new ol.style.Circle({
                    radius: 10,
                    fill: null,
                    stroke: new ol.style.Stroke({
                        color: 'magenta'
                    })
                })
            }),
            'Circle': new ol.style.Style({
                stroke: new ol.style.Stroke({
                    color: 'red',
                    width: 2
                }),
                fill: new ol.style.Fill({
                    color: 'rgba(255,0,0,0.2)'
                })
            }),
            'Select': new ol.style.Style({
                fill: new ol.style.Fill({
                    color: 'rgba(209, 113, 20, 0.2)'
                }),
                stroke: new ol.style.Stroke({
                    color: 'd17114',
                    width: 3
                })
            })
        };
    }

    me.getPathStyle = function (feature) {
        var stroke = new ol.style.Stroke({color: 'black', width: 2});
        var fill = new ol.style.Fill({color: 'red'});
        var styles = {
            'triangle': new ol.style.Style({
                image: new ol.style.RegularShape({
                    fill: fill,
                    stroke: stroke,
                    points: 3,
                    radius: 10,
                    rotation: Math.PI / 4,
                    angle: 0
                })
            }),
            'star': new ol.style.Style({
                image: new ol.style.RegularShape({
                    fill: fill,
                    stroke: stroke,
                    points: 6,
                    radius: 10,
                    radius2: 5,
                    angle: 0
                })
            }),
            'cross': new ol.style.Style({
                image: new ol.style.RegularShape({
                    fill: fill,
                    stroke: stroke,
                    points: 4,
                    radius: 10,
                    radius2: 0,
                    angle: 0
                })
            }),

            'path': new ol.style.Style({
                stroke: new ol.style.Stroke({
                    color: fill, //'#d17114',
                    width: 5
                })
            })
        };
        var g_type = feature.getGeometry().getType();
        if (!g_type) g_type = feature.f;
        var key = "path";
        if (g_type.indexOf('Point') != -1) {
            key = "star"
        } else if (g_type.indexOf('LineString') != -1) {
            key = "path"
        }
        return styles[key];
    }
    me.getStyle = function (feature) {
        g_type = feature.getGeometry().getType();
        if (!g_type) g_type = feature.f;
        return me.styles[g_type];
    };
    me.getSelectStyle = function (feature) {
        g_type = feature.getGeometry().getType();
        if (!g_type) g_type = feature.f;
        if (g_type.indexOf('Point') != -1) {
            var selStyle = new ol.style.Style({
                image: new ol.style.Icon({
                    anchor: [0.5, 0.5],
                    opacity: 1,
                    src: '/static/ferrp/img/flashing_circle.gif'
                })
            });
        } else if (g_type.indexOf('LineString') != -1) {
            var selStyle = new ol.style.Style({
                stroke: new ol.style.Stroke({
                    color: '#d17114',
                    width: 5
                })
            });
        } else {
            var selStyle = new ol.style.Style({
                fill: new ol.style.Fill({
                    color: 'rgba(209, 113, 20, 0.2)'
                }),
                stroke: new ol.style.Stroke({
                    color: '#d17114',
                    width: 3
                })
            });
        }
        return selStyle;
    }
    me.changeStyle = function () {
        var newStyle = new ol.style.Style({
            image: new ol.style.Circle({
                radius: 5,
                fill: new ol.style.Fill({color: 'red'}),
                stroke: new ol.style.Stroke({color: 'yellow', width: 1})
            })
        });
        selectedFeature.setStyle(newStyle)
    }

    me.capturePicture = function () {
        var c = $("canvas.ol-unselectable").get(0);
        // <canvas class="ol-unselectable" style="width: 100%; height: 100%; display: block;" width="1640" height="23"></canvas>
// ?        var t = c.getContext('2d');
        // window.location.href = image;
        var aspectRatio = c.width / c.height;
        var newHeight = 120;
        var newWidth = 200; //parseInt(newHeight * aspectRatio)
        var newAspectRatio = newWidth / newHeight;
        if (aspectRatio >= 1) {
            clipWidth = newAspectRatio * c.height;
            clipHeight = c.height;
            diff = (c.width - clipWidth) / 2;
            clipX = diff
            clipY = 0
        }

        var resizeCanvas = document.createElement("canvas");
        resizeCanvas.height = clipHeight;
        resizeCanvas.width = clipWidth;

        var resizeCtx = resizeCanvas.getContext('2d');
// Put original canvas contents to the resizing canvas
        resizeCtx.drawImage(c, clipX, clipY, clipWidth, clipHeight, 0, 0, clipWidth, clipHeight);

// Resize using Hermite resampling
        var HERMITE = new Hermite_class();
//default resize
        HERMITE.resample_single(resizeCanvas, newWidth, newHeight, true);
        var image = resizeCanvas.toDataURL();
        return image
    }

//manupulating interactions.
    me.removeAllInteraction = function () {
        var interactionColl = me.map.getInteractions();
        interactionColl.forEach(function (interaction) {
            if (interaction)
                me.map.removeInteraction(interaction)
        })
    }
    me.addBasicInteraction = function () {
        me.removeAllInteraction();
        me.defaultInteractionsColl.forEach(function (interaction) {
            me.map.addInteraction(interaction)
        })
    }
    me.removeInteraction = function (interaction) {
        me.map.removeInteraction(interaction)
    }

// navigation Operations
    me.addToPerviousExtentList = function (extent) {
        if (extent) {
            me.previousExtentList.push(extent);
        } else {
            me.previousExtentList.push(me.view.calculateExtent(me.map.getSize()));
        }
    }
    me.addToNextExtentList = function (extent) {
        if (extent) {
            me.nextExtentList.push(extent)
        } else {
            me.previousExtentList.push(me.view.calculateExtent(me.map.getSize()));
        }
    }
    me.getPreviousExtent = function () {
        return me.previousExtentList.pop();
    }
    me.getCurrentExtent = function () {
        return me.getView().calculateExtent();

    }
    me.getNextExtent = function () {
        return me.nextExtentList.pop();
    }
    me.getSizeOfPreviousExtent = function () {
        return me.previousExtentList.length;
    }
    me.getSizeOfNextExtent = function () {
        return me.nextExtentList.length;
    }
    me.setFullExtent = function () {
        // me.addToPerviousExtentList();
        me.view.fit(me.extent, {});
    }
    me.zoomToSelectedFeatures = function () {
        var extent = me.specialLayers["selectedFeatureLayer"].getSource().getExtent();
        me.getView().fit(extent, me.getMap().getSize());
    }
    me.zoomToExtent = function (minX, minY, maxX, maxY) {
        var extent = [minX, minY, maxX, maxY]
        me.setViewExtent(extent)
    }
    me.setViewExtent = function (extent) {
        me.getView().fit(extent, me.getMap().getSize())
    }
    me.zoomToRectangle = function () {
        // me.removeAllInter`action();
        me.removeAllInteraction();
        var dragBox = new ol.interaction.DragBox();
        me.map.addInteraction(dragBox);

        dragBox.on('boxend', function () {
            // features that intersect the box are added to the collection of
            // selected features
            // me.addToPerviousExtentList();
            var extent = dragBox.getGeometry().getExtent();
            me.view.fit(extent, {})
        });
        return dragBox;
    }
    me.getGeometryWKT = function (geom) {
        var format = new ol.format.WKT();
        var wkt = format.writeGeometry(geom);
        return wkt;
    };
    me.convertVectorLayerToGeoJSON = function (layer) {
        var vectorSource = layer.getSource();
        var writer = new ol.format.GeoJSON();
        var geojsonStr = writer.writeFeatures(vectorSource.getFeatures());
        return geojsonStr;
    }
    ////////// callback with return as geometry
    //value could be Point, LineString,Polygon,Circle
    /// to get WKT use me.getGeometryWKT(feature.getGeometry());
    me.drawShape = function (value, callback) {
        me.removeAllInteraction();

        var source = me.specialLayers["drawFeatureLayer"].getSource();
        var drawShape = new ol.interaction.Draw({
            source: source,
            type: value
        });
        me.map.addInteraction(drawShape, callback);
        drawShape.on('drawstart', function (e) {
            // console.log("draw start...")
            source.clear();
        });
        drawShape.on('drawend', function (e) {
            // console.log("draw end...")
            // var features = source.getFeatures();
            // var geometry = e.feature.getGeometry();
            callback(e.feature);
            // me.removeAllInteraction();
            // me.addBasicInteraction();

        })
        return drawShape
    }
    me.profileExtractor = function (feature) {
        var geometry = feature.getGeometry()
        profileLength = geometry.getLength();

        if (profileLength < 1000000) {
            var format = new ol.format.WKT();
            var wkt = format.writeGeometry(geometry);
            // console.log(wkt)
            var formData = new FormData()
            formData.append('wkt', wkt)
            var params = {
                url: "/maps/profile_extractor/",
                type: "POST",
                data: formData,
                dataType: "json",
                processData: false,
                contentType: false,
                async: true,
                headers: {'X-CSRFToken': me.csrfToken},
            }
            me.viewModel.showOutputPanel(1);

            callAJAX(params, function (data) {
                // showAlertDialog("working",dialogTypes.info);


                var chartModel = new JqxChartModel(me.viewModel, 'output');
                var dataFields = [
                    {name: 'distance', type: 'int'},
                    {name: 'point', type: 'string'},
                    {name: 'value', type: 'int'}
                ];
                chartModel.createDataAdapter(dataFields, data)
                chartModel.createLineChart('Profile Extractor', 'distance', 'value', profileLength / 4)
                // me.viewModel.showChartModel(dataAdapter);
            })
        } else {
            showAlertDialog("length is greater than 1 km. It will take a lot of time for processing. " +
                "Do you want to continue", dialogTypes.warning);
        }
    }
    me.zoomIn = function () {
        // me.addToPerviousExtentList();
        me.view.setZoom(me.view.getZoom() + 1)
    }

    me.zoomOut = function () {
        // me.addToPerviousExtentList();
        me.view.setZoom(me.view.getZoom() - 1)
    }

    me.pan = function () {
        var dragPan = new ol.interaction.DragPan();
        me.map.addInteraction(dragPan);

        dragPan.on('change:active', function () {
            me.addToPerviousExtentList();
        })
        return dragPan;
    }

    me.identifier = function () {
        me.map.on('click', function (evt) {
            var coordinate = evt.coordinate;
            res = me.getView().getResolution();
            var layers = me.overlayLayers // me.map.getLayers().getArray();
            var layer = null;
            for (var key in layers){
                layer = layers[key]
                var layerInfo = layer.get("info");
                var displayInLayerSwitcher = layer.get("displayInLayerSwitcher");
                var layerName = layer.get('title');
                if (layerInfo == true && displayInLayerSwitcher == true && layerName){
                    break;
                }
            }
            // layer = layers[layers.length - 1]
            if (layer != null) {
                layerName = layer.get('title');
                url = "/web_services/wfs/get_feature/?coordinate=" + coordinate +
                    "&layer_name=" + layerName + "&resolution=" + res
                var params = {
                    url: url,
                    type: "GET",
                    // data: data,
                    dataType: "json",
                    processData: false,
                    contentType: false,
                    async: true,
                    // headers: {'X-CSRFToken': token},
                }
                callAJAX(params, function (data) {
                    // alert(data)
                    me.showSelectedFeatureGeojson(data, coordinate)
                })
            }else{
                showAlertDialog("No Layer Found...", dialogTypes.info)
            }
        });
    }

    me.zoom2PreviousExtent = function () {
        extent = me.getPreviousExtent();
        if (extent) {
            me.addToNextExtentList(extent);
            me.view.fit(extent, {});
        }
    }

    me.zoom2NextExtent = function () {
        extent = me.getNextExtent();
        if (extent) {
            me.addToPerviousExtentList(extent);
            me.view.fit(extent, {})
        }
    }

    me.mointoredViewChange = function () {
        me.view.on('')
    }
    me.wait4LayerLoad = function (layer) {
        var source = layer.getSource();
        me.noOfTiles = 0;
        source.on('tileloadstart', function (event) {
            me.noOfTiles++;
            $("#waiting-div").css('visibility', 'visible');
        });

        source.on('tileloadend', function (event) {
            me.noOfTiles--;
            if (me.noOfTiles == 0)
                $("#waiting-div").css('visibility', 'hidden');
        });

        source.on('tileloaderror', function (event) {
            me.noOfTiles--
            if (me.noOfTiles == 0)
                $("#waiting-div").css('visibility', 'hidden');
            // showAlertDialog("Error in loading tile", dialogTypes.error)
        });
    }
    me.flash = function (feature) {
        var duration = 3000;
        var map = me.getMap();
        var view = me.getView();
        var start = new Date().getTime();
        var listenerKey;


        var extent = feature.getGeometry().getExtent();
        var viewExtent = view.calculateExtent(map.getSize());
        if (!ol.extent.containsExtent(viewExtent, extent)) {
            var center = ol.extent.getCenter(extent);
            view.setCenter(center);
        }
        function getAnimateStyle(feature, radius, opacity) {
            var style = null;
            g_type = feature.getGeometry().getType();
            if (!g_type) g_type = feature.f;
            if (g_type.indexOf('Point') != -1) {
                style = new ol.style.Style({
                    image: new ol.style.Circle({
                        radius: radius,
                        snapToPixel: false,
                        stroke: new ol.style.Stroke({
                            color: 'rgba(255, 0, 0, ' + opacity + ')',
                            width: 0.25 + opacity
                        })
                    })
                });
            }
            // else if (g_type.indexOf('LineString') != -1) {
            //     var selStyle = new ol.style.Style({
            //         stroke: new ol.style.Stroke({
            //             color: 'rgba(255, 0, 0, ' + opacity + ')',
            //             width: 5
            //         })
            //     });
            // } else {
            //     var selStyle = new ol.style.Style({
            //         fill: new ol.style.Fill({
            //             color: 'rgba(0, 0, 0, 0)'
            //         }),
            //         stroke: new ol.style.Stroke({
            //             color: 'rgba(255, 0, 0, ' + opacity + ')',
            //             width: 3
            //         })
            //     });
            // }
            return style;
        }

        function animate(event) {
            var vectorContext = event.vectorContext;
            var frameState = event.frameState;
            var flashGeom = feature.getGeometry().clone();
            var elapsed = frameState.time - start;
            var elapsedRatio = elapsed / duration;
            // radius will be 5 at start and 30 at end.
            var radius = ol.easing.easeOut(elapsedRatio) * 25 + 5;
            var opacity = ol.easing.easeOut(1 - elapsedRatio);

            var style = getAnimateStyle(feature, radius, opacity);
            if (style != null) {
                vectorContext.setStyle(style);
                vectorContext.drawGeometry(flashGeom);
                if (elapsed > duration) {
                    ol.Observable.unByKey(listenerKey);
                    return;
                }
                // tell OpenLayers to continue postcompose animation
                map.render();
            }
        }

        listenerKey = map.on('postcompose', animate);
    }
    me.noOfLayers = function () {
        var layerCount = _.keys(me.overlayLayers).length;
        return layerCount;
    }
    me.createLayerNameSelect = function (selectId, isAddSpecialLayers) {
        var layerCount = me.noOfLayers();
        if (layerCount > 1 || isAddSpecialLayers) {
            var select = $('<select id="' + selectId + '" class="form-control layerNameCls" ></select>');
            select.append('<option value="-1">Select Layer</option>');
            for (var key in me.overlayLayers) {
                select.append("<option value='" + key + "'>" + me.overlayLayers[key].get("title") + "</option>")
            }
            // select.selectpicker('refresh');
            if (isAddSpecialLayers) {
                for (var key in me.specialLayers) {
                    select.append("<option value='" + key + "'>" + me.specialLayers[key].get("title") + "</option>");
                }
            }
            return select;
        } else {
            var input = "<input type='text' id='" + selectId + "' class='form-control' value='No Layer Available' disabled>";
            for (var key in me.overlayLayers) {
                input = "<input type='text' id='" + selectId + "' class='form-control' value='" + key + "' disabled>";
            }
            return input;
        }
    }

    me.set3DEnableDisable = function () {
        me.threeDEnable = !me.threeDEnable;
        if (me.olCesiumModel == null) {
            me.olCesiumModel = new OLCesiumModel();
            me.olCesiumModel.init(me.getMap());
            me.cameraSettingVM.setMap3DModel(me.olCesiumModel);
        }
        if (me.cameraSettingVM != null) {
            me.cameraSettingVM.setCamera(me.olCesiumModel.getCamera())
            me.cameraSettingVM.is3dEnabled(me.threeDEnable);

        }
        me.olCesiumModel.switch3DView(me.threeDEnable);
    }
    me.check3DEnable = function () {
        return me.threeDEnable;
    }
    me.getOLCesiumModel = function () {
        return me.olCesiumModel;
    }
    me.setMapViewRotation = function (val) {
        me.view.setRotation(val)
    }

    me.getStatsModel = function () {
        if (me.statsModel == null) {
            var statsModel = new StatsModel();
            statsModel.initializeStatsModel(me);
        }
        return statsModel;
    }
}

var setPopupContent = function (json) {
    for (var key in json) {
        var name = '<tr>' + key + '</tr>';
        var value = '<tr>' + json[key] + '</tr>';
        $('#prop-table > tbody:last-child').append(name + value);
    }
}


