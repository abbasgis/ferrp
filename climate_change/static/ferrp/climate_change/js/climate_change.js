/**
 * Created by Shakir on 10/18/2018.
 */
var ClimateChangeModel = function (mapInfo) {
    var me = this;
    me.olMapModel = null;
    me.flexmonster = null;
    me.data = [{
        "id": 407120,
        "year": "2017",
        "jan": "12.9881000000",
        "feb": "14.7247000000",
        "mar": "16.0959000000",
        "apr": "20.7626000000",
        "may": "28.6039000000",
        "jun": "32.3539000000",
        "jul": "31.2014000000",
        "aug": "27.6163000000",
        "sep": "24.4787000000",
        "oct": "20.3765000000",
        "nov": "15.4977000000",
        "dec": "10.5405000000",
        "division": 'Lahore',
        "district": 'Lahore',
        "tehsil": 'Lahore'
    }];
    //me.flexKey = 'Z7CJ-XF9J50-5J4J6X-2H136N-2L036W-1A0O01-6S5S6R-0W0T20-3C' // for localhost
    me.flexKey = 'Z7HI-XG503S-5O4M4H-6F456Z-0A3E3Z-1X663C-5O4R35-4R'  //for DCH
    me.heatmapURL = '/climate/get_temperature_geojson/';
    me.monthList = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'];
    me.btnCSSClasses = ['btn-success', 'btn-default', 'btn-primary', 'btn-success', 'btn-warning', 'btn-danger',
        'btn-default', 'btn-primary', 'btn-success', 'btn-warning', 'btn-danger', 'btn-success', 'btn-warning',];
    me.selectedYear = 2018;
    me.selectedLayer = 'temperature';
    me.frmHeatMap = $('#frmHeatMap');
    me.frmAnimation = $('#frmHeatMapAnimation');
    me.rangeBar = $("#range");
    me.rangeBarValUI = $('#range_value');
    me.btnStartAnimation = $("#btn_start-animation");
    me.isAnimating = false;
    me.animationDelay = 2000;
    me.initialize = function () {
        me.olMapModel = new OLMapModel(mapInfo.extent, "map", "layerSwitcher", null, mapInfo.csrfToken, null);
        me.olMapModel.initialize();
        me.createMapToolbar(mapInfo);
        // me.addLayersToMap(mapInfo);
        me.createFlexMonsterPivotTable(me.data);
        me.getTemperatureDataFromDB();
        me.createHeatMapFromGeoJson(me.heatmapURL);
    };
    me.createMapToolbar = function (mapInfo) {
        me.toolbarModel = new JQXToolbarModel("10%", mapInfo, me);
        var navbar = me.toolbarModel.navbar;
        var navbarSeq = [navbar.addLayer, navbar.fullExtent, navbar.pan, navbar.zoom2Rect, navbar.zoomIn, navbar.zoomOut, navbar.zoom2Prev, navbar.zoom2Next,
            navbar.spacebar, navbar.zoom2Selection, navbar.clearSelection, navbar.identifier, navbar.spacebar, navbar.heatmap
        ];
        me.toolbarModel.initialize(me, navbarSeq);
    };
    me.addLayersToMap = function (mapInfo) {
        for (var j = 0; j < mapInfo.groupLayers.length; j++) {
            var layers = mapInfo.groupLayers[j].layers;
            var group_name = mapInfo.groupLayers[j].group_name;
            for (var i = 0; i < layers.length; i++) {
                me.olMapModel.addTileWMSLayer(mapInfo.url_wms_map, layers[i].layer_name, layers[i].layer_style, group_name);
            }
        }
        me.toolbarModel.monitorViewChange();
    };
    me.getTemperatureDataFromDB = function () {
        var url = '/climate/get_temp_rcp_data/';
        var params = {
            url: url,
            type: "GET",
            // data: data,
            // dataType: "json",
            processData: false,
            contentType: false,
            async: true
            // headers: {'X-CSRFToken': token},
        }
        // var data = callSJAX(params);
        callAJAX(params, function (response) {
            var data = eval('(' + JXG.decompress(response) + ')');
            me.flexMonsterUpdateData(data);
        })
    }
    me.createFlexMonsterPivotTable = function (data) {
        me.flexmonster = new Flexmonster({
            container: 'pivotTable',
            componentFolder: "https://cdn.flexmonster.com/",
            toolbar: true,
            height: '100%',
            report: {
                dataSource: {
                    data: data
                },
                "slice": {
                    "rows": [
                        {
                            "uniqueName": "year",
                        }

                    ],
                    "columns": [
                        {
                            // "uniqueName": "[year]"
                        }
                    ],
                    "measures": [
                        {
                            "uniqueName": "jan",
                            "aggregation": "average"
                        }
                        ,
                        {
                            "uniqueName": "mar",
                            "aggregation": "average"
                        },
                        {
                            "uniqueName": "jun",
                            "aggregation": "average"
                        },
                        {
                            "uniqueName": "sep",
                            "aggregation": "average"
                        },
                        {
                            "uniqueName": "dec",
                            "aggregation": "average"
                        }
                    ]
                },
            },
            licenseKey: me.flexKey,//'Z7HI-XG503S-5O4M4H-6F456Z-0A3E3Z-1X663C-5O4R35-4R'
            // beforetoolbarcreated: me.customizeToolbar
        })
    };
    me.flexMonsterUpdateData = function (jsonData) {
        me.flexmonster.updateData({data: jsonData});
    };
    me.customizeToolbar = function (toolbar) {
        // get all tabs
        var tabs = toolbar.getTabs();
        toolbar.getTabs = function () {
            // add new tab
            tabs.unshift({
                id: "fm-tab-newtab",
                title: "New Tab",
                menu: [{
                    id: "fm-menue1",
                    title: "New Menue",
                    handler: function () {
                        alert('New Menue')
                    },
                    icon: this.icons.open
                }],
                handler: newtabHandler,
                icon: this.icons.open
            });
            return tabs;
        }

        var newtabHandler = function () {
            alert("New Tab");
        }
    };
    me.getGeoJsonFromDBForHeatMap = function () {
        var url = '/climate/get_temperature_geojson/';
        var params = {
            url: url,
            type: "GET",
            // data: data,
            dataType: "json",
            processData: false,
            contentType: false,
            async: true
            // headers: {'X-CSRFToken': token},
        };
        // var data = callSJAX(params);
        callAJAX(params, function (response) {
            me.createHeatMapFromGeoJson(response);
        })
    };
    me.createHeatMapFromGeoJson = function (url) {
        var vectorSource = me.getGeoJsonSourceFromURL(url);
        var radius = me.getRadiusValue();
        me.vector = new ol.layer.Heatmap({
            title: 'Heat Map',
            source: vectorSource,
            blur: parseInt(radius * 3),
            radius: radius
        });
        me.olMapModel.map.addLayer(me.vector);
        me.olMapModel.view.on('change:resolution', function (event) {
            var radius = me.getRadiusValue();
            me.vector.setRadius(radius);
            me.vector.setBlur(parseInt(radius * 3));
        });


    }
    me.getGeoJsonSourceFromURL = function (url) {
        var vectorSource = new ol.source.Vector({
            url: url,
            format: new ol.format.GeoJSON(),
            loader: function (extent, resolution, projection) {
                var xhr = new XMLHttpRequest();
                xhr.open('GET', url, true);
                xhr.onload = function () {
                    if (xhr.status === 200) {
                        vectorSource.addFeatures(vectorSource.getFormat().readFeatures(xhr.responseText, {
                            dataProjection: 'EPSG:3857',
                            featureProjection: 'EPSG:3857'
                        }));
                        me.setLegendOnMap();
                    }
                };
                xhr.send();
            },
        });
        return vectorSource;
    }
    me.getRadiusValue = function () {
        var resolution = me.olMapModel.view.getResolution();
        var gridSize = 26000;
        return parseInt(gridSize / resolution);
    };
    me.createHeatMapDialogue = function () {
        var modalbody = $('<div ></div>');
        me.frmHeatMap.css('display', 'block');
        modalbody.append(me.frmHeatMap);
        BootstrapDialog.show({
            title: "Heat Map",
            type: BootstrapDialog.TYPE_SUCCESS,
            size: BootstrapDialog.SIZE_SMALL,
            message: modalbody,
            draggable: true,
            buttons: [{
                label: 'Heat Map',
                title: 'Heat Map of Selected Values',
                cssClass: 'btn-success',
                action: function (dialogItself) {
                    me.selectedYear = parseInt($('#id_year').val());
                    me.selectedLayer = $('#id_layer').val();
                    var month = parseInt($('#id_month').val());
                    var url = '/climate/get_temperature_geojson/?layer=' + me.selectedLayer + '&year=' + me.selectedYear + '&month=' + me.monthList[month - 1];
                    var source = me.getGeoJsonSourceFromURL(url);
                    me.vector.setSource(source);
                    me.olMapModel.map.render();
                    dialogItself.close()
                }
            },
                {
                    label: 'Animation',
                    title: 'Animation of Selected Year',
                    cssClass: 'btn-warning',
                    action: function (dialogItself) {
                        me.selectedYear = parseInt($('#id_year').val());
                        me.selectedLayer = $('#id_layer').val();
                        var div_animation = document.getElementById("div_animation");
                        if (div_animation.style.display === "none") {
                            div_animation.style.display = "block";
                        }
                        dialogItself.close()
                    }
                },
                {
                    label: 'Close',
                    cssClass: 'btn-danger',
                    action: function (dialogItself) {
                        dialogItself.close()
                    }
                }
            ]
        });

    };
    me.createHeatMapAnimationDialogue = function () {
        var modalbody = $('<div ></div>');
        me.frmAnimation.css('display', 'block');
        modalbody.append(me.frmHeatMap);
        BootstrapDialog.show({
            title: "Heat Map",
            type: BootstrapDialog.TYPE_SUCCESS,
            size: BootstrapDialog.SIZE_SMALL,
            message: modalbody,
            draggable: true,
            buttons: [{
                label: 'Heat Map',
                title: 'Heat Map of Selected Values',
                cssClass: 'btn-success',
                action: function (dialogItself) {
                    me.selectedYear = parseInt($('#id_year').val());
                    me.selectedLayer = $('#id_layer').val();
                    var month = parseInt($('#id_month').val());
                    var url = '/climate/get_temperature_geojson/?layer=' + me.selectedLayer + '&year=' + me.selectedYear + '&month=' + me.monthList[month - 1];
                    var source = me.getGeoJsonSourceFromURL(url);
                    me.vector.setSource(source);
                    me.olMapModel.map.render();
                    dialogItself.close()
                }
            },
                {
                    label: 'Animation',
                    title: 'Animation of Selected Year',
                    cssClass: 'btn-warning',
                    action: function (dialogItself) {
                        me.selectedYear = parseInt($('#id_year').val());
                        me.selectedLayer = $('#id_layer').val();
                        var div_animation = document.getElementById("div_animation");
                        if (div_animation.style.display === "none") {
                            div_animation.style.display = "block";
                        }
                        dialogItself.close()
                    }
                },
                {
                    label: 'Close',
                    cssClass: 'btn-danger',
                    action: function (dialogItself) {
                        dialogItself.close()
                    }
                }
            ]
        });

    };
    $("#btnCloseAnimation").click(function () {
        var div_animation = document.getElementById("div_animation");
        if (div_animation.style.display === "block") {
            div_animation.style.display = "none";
        }
    });
    me.rangeBar.change(function (e) {
        var val = parseInt(e.target.value);
        me.rangeBarValUI.text(me.monthList[val - 1].toUpperCase() + ', ' + me.selectedYear);
        var url = me.heatmapURL + '?layer=' + me.selectedLayer + '&year=' + me.selectedYear + '&month=' + me.monthList[val - 1];
        var source = me.getGeoJsonSourceFromURL(url);
        me.vector.setSource(source);
        me.olMapModel.map.render();
    });
    me.btnStartAnimation.click(function (e) {
        if (me.isAnimating) {
            me.stopAnimation(false);
        } else {
            me.isAnimating = true;
            me.btnStartAnimation.text('Stop');
            me.startAnimation(0, me.monthList.length, me.animationDelay, me.monthList);
        }
    });
    me.startAnimation = function (start, end, delay, month) {
        for (var i = start; i < end; i++) {
            if (me.isAnimating) {
                setTimeout(function () {
                    var url = '/climate/get_temperature_geojson/?layer=' + me.selectedLayer + '&year=' + me.selectedYear + '&month=' + month[i];
                    var source = me.getGeoJsonSourceFromURL(url);
                    me.vector.setSource(source);
                    me.olMapModel.map.render();
                    me.rangeBarValUI.text(month[i].toUpperCase() + ', ' + me.selectedYear);
                    me.rangeBarValUI.removeClass(me.btnCSSClasses[i]);
                    me.rangeBarValUI.addClass(me.btnCSSClasses[i + 1]);
                    me.rangeBar.val(i);
                    me.startAnimation(i + 1, end, delay, month);
                }, delay);
                break;
            } else {
                break;
            }
        }
    };
    me.stopAnimation = function (ended) {
        me.isAnimating = false;
        me.btnStartAnimation.text('Start');
    };
    me.setLegendOnMap = function () {
        var temperature_legend = document.getElementById("temperature_legend");
        var precipitation_legend = document.getElementById("precipitation_legend");
        if (me.selectedLayer === 'temperature') {
            temperature_legend.style.display = "block";
            precipitation_legend.style.display = "none";
        } else {
            temperature_legend.style.display = "none";
            precipitation_legend.style.display = "block";
        }

    }
};

