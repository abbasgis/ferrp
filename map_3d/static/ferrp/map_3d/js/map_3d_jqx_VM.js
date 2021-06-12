/**
 * Created by Dr. Ather Ashraf on 8/21/2018.
 */
var Map3DJQXModel = function (mapInfo) {
    var me = this;
    me.mapInfo = mapInfo
    me.jqxLayoutTarget = $('#jqxLayout');
    me.layoutDist = {"westgroup": "18%", "centergroup": "82%", "eastgroup": "18%"};
    me.cesiumDivId = 'cesiumContainer';
    me.cModel = new CesiumModel(me.mapInfo.extent, me.cesiumDivId);
    me.layout = [{
        type: 'layoutGroup',
        orientation: 'horizontal',
        items: [{
            type: 'layoutGroup',
            orientation: 'vertical',
            width: me.layoutDist.centergroup,
            items: [{
                type: 'documentGroup',
                height: '100%',
                items: [{
                    type: 'documentPanel',
                    title: 'Map View',
                    contentContainer: 'MapPanel'
                }]
            }]
        }, {
            type: 'tabbedGroup',
            alignment: 'right',
            width: me.layoutDist.eastgroup,
            // minWidth: 200,
            items: [{
                type: 'layoutPanel',
                title: 'Catalogue',
                contentContainer: 'CataloguePanel',
                initContent: function () {
                    var addLayerModel = new AddLayerModel(me.cModel, mapInfo)
                    addLayerModel.initialize();
                }
            }, {
                type: 'layoutPanel',
                title: 'Camera Setting',
                contentContainer: 'CameraSettingPanel',
                initContent: function () {
                    me.cModel.cameraSetting();
                }
            }]
        }]
    }];

    me.setLayout = function () {
        me.jqxLayoutTarget.jqxLayout({
            theme: theme,
            width: '100%',
            height: me.getViewportLayoutHeight(),
            layout: me.layout
        });

        me.toolbarModel = new JQXToolbarModel_3d(me)
        var navbar = me.toolbarModel.navbar;
        var navbarSeq = [navbar.initialExtent, navbar.camera]
        me.toolbarModel.init(navbarSeq);

        me.cModel.init();
        // me.toolbarModel.setCesiumModel(me.cModel)

    }
    me.getCesiumModel = function () {
        return me.cModel;
    }
    me.setViewportLayoutHeight = function () {
        var rem_height = me.getViewportLayoutHeight();
        rem_height = (rem_height > 500 ? rem_height : 500);
        // me.viewPort.height(rem_height);
        me.jqxLayoutTarget.jqxLayout({height: rem_height});
        var cDivIdHeight = $('#' + me.cesiumDivId).height();
        $('#' + me.cesiumDivId).height(cDivIdHeight - 35);
    }

    me.getViewportLayoutHeight = function () {
        var width = $(document).width();
        var height = $(document).height();
        var navbar_height = $("#base_nav").height();
        var header_height = $("#header").height();
        var footer_heght = $("#footer").height();
        var rem_height = height - (navbar_height + header_height + footer_heght);
        // var minHeight = 450
        // rem_height = (rem_height > minHeight ? rem_height : minHeight);
        return rem_height;
    }
    me.getCameraSettingPanel = function () {
        var layout = me.jqxLayoutTarget.jqxLayout('layout');
        var cameraSettingPanel = layout[0].items[1].items[1];
        return cameraSettingPanel;
    }
    // me.getOutputPanelSize = function () {
    //     var outputPanel = me.getOutputPanel();
    //     // alert(outputPanel.title)
    //     var width = $(outputPanel.widget[0]).width();
    //     var height = $(outputPanel.widget[0]).height();
    //     return {width: width, height: height};
    // }
    me.openCameraSettingPanel = function () {
        alert("opening...");
        var cameraSettingPanel = me.getCameraSettingPanel();

        cameraSettingPanel.parent.parent.widget.jqxRibbon('selectAt', 1)
        // cameraSettingPanel.parent.widget.jqxTabs('select',1)
    }

}

var CesiumModel = function (extent, cesiumDivId) {
    var me = this;
    me.viewer = null;
    me.initLookAt = Cesium.Cartesian3.fromDegrees(extent[0] + (extent[2] - extent[0]) / 2, extent[1] + (extent[3] - extent[1]) / 2);
    me.initCameraPos = Cesium.Cartesian3.fromDegrees(extent[0] - (extent[2] - extent[0]) / 2, extent[1] - (extent[3] - extent[1]) / 2, 15000);
    // me.initCameraPos = Cesium.Cartesian3(1548623.0221527813, 5105610.674814318, 3505148.185008414)
    me.initExtent = Cesium.Rectangle.fromDegrees(extent[0], extent[1], extent[2], extent[3]);
    me.cesiumDivId = cesiumDivId;
    me.initCameraOrient = {"heading": 0.0, "pitch": -Cesium.Math.PI_OVER_THREE, "roll": 0.0, "range": 6000}; //-Cesium.Math.PI_OVER_FOUR
    me.init = function () {
        Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJhNDZkMzc1Yy1mZGI3LTQ1N2QtOTIwMC01NWFmY2NjYmQ5ZmYiLCJpZCI6MjkyMywiaWF0IjoxNTM1MjU4NDExfQ.NGFb_MFCyv2Zu2VYFVSDIOkmi2JuDofx6Pcz8kWPoNQ';

        me.viewer = new Cesium.Viewer(me.cesiumDivId);
        // var terrainProvider = Cesium.createWorldTerrain({
        //     requestWaterMask : true
        // });

        var terrainProvider = new Cesium.CesiumTerrainProvider({
            url: Cesium.IonResource.fromAssetId(6063),
            // requestVertexNormals: true
        });


        me.viewer.camera.setView({
            destination: me.initCameraPos,
            orientation: {
                heading: me.initCameraOrient["heading"],
                pitch: me.initCameraOrient["pitch"],
                roll: me.initCameraOrient["roll"]
            }
        });
        me.viewer.terrainProvider = terrainProvider;
        // me.viewer.scene.globe.enableLighting = true;

        // me.viewer.camera.lookAt(me.initCenter, new Cesium.HeadingPitchRange(me.initCameraOrient["heading"],
        //     me.initCameraOrient["pitch"], me.initCameraOrient["range"]));

    }
    me.setInitExtent = function () {
        me.viewer.camera.setView({
            destination: me.initExtent,
            orientation: {
                heading: me.initCameraOrient["heading"],
                pitch: me.initCameraOrient["pitch"],
                roll: me.initCameraOrient["roll"]
            }

        });
        // me.viewer.camera.lookAt(me.initCenter, new Cesium.HeadingPitchRange(me.initCameraOrient["heading"],
        //     me.initCameraOrient["pitch"], me.initCameraOrient["range"]));
        me.setInitSliderValues();
    }
    me.cameraSetting = function () {
        $('#headingLevel').jqxSlider({
            showTickLabels: true,
            tooltip: true,
            mode: "default",
            height: 60,
            width: '100%',
            min: 0,
            max: 360,
            // ticksFrequency: 30,
            value: me.initCameraOrient["heading"],
            // step: 10,
            tickLabelFormatFunction: function (value) {
                if (value == 0) return value;
                if (value == 360) return value;
                return "";
            }
        });
        $('#pitchLevel').jqxSlider({
            showTickLabels: true,
            tooltip: true,
            mode: "default",
            height: 60,
            width: '100%',
            min: -90,
            max: 0,
            // ticksFrequency: 25.5,
            value: Cesium.Math.toDegrees(me.initCameraOrient["pitch"]),
            // step: 5,
            tickLabelFormatFunction: function (value) {
                if (value == -90) return value;
                if (value == 0) return value;
                return "";
            }
        });
        $('#rollLevel').jqxSlider({
            showTickLabels: true,
            tooltip: true,
            mode: "default",
            height: 60,
            width: '100%',
            min: -90,
            max: 90,
            // ticksFrequency: 10,
            value: me.initCameraOrient["roll"],
            // step: 5,
            tickLabelFormatFunction: function (value) {
                if (value == -90) return value;
                if (value == 90) return value;
                return "";
            }
        });
        // me.setInitSliderValues();
        $('#headingLevel').on('change', function (event) {
            me.setCamera();
        });
        $('#pitchLevel').on('change', function (event) {
            me.setCamera();
        });
        $('#rollLevel').on('change', function (event) {
            me.setCamera();
        });
    }
    me.setInitSliderValues = function () {
        $('#headingLevel').jqxSlider('setValue', me.initCameraOrient["heading"]);
        $('#pitchLevel').jqxSlider('setValue', Cesium.Math.toDegrees(me.initCameraOrient["pitch"]));
        $('#rollLevel').jqxSlider('setValue', me.initCameraOrient["roll"]);
    }
    me.setCamera = function () {
        me.getCameraView();
        var heading = Cesium.Math.toRadians(parseFloat($('#headingLevel').jqxSlider('value')));
        var pitch = Cesium.Math.toRadians(parseFloat($('#pitchLevel').jqxSlider('value')));
        var roll = Cesium.Math.toRadians(parseFloat($('#rollLevel').jqxSlider('value')));
        // alert("heading:" + heading + ", pitch:" + pitch + ", roll:" + roll);
        var camera = me.viewer.camera;
        camera.setView({
            orientation: {
                heading: heading, // east, default value is 0.0 (north)
                pitch: pitch,    // default value (looking down)
                roll: roll                             // default value
            }
        });
    }
    me.getCameraView = function () {
        var camera = me.viewer.camera;
        // var view = camera.getView();
        console.log(camera.position);
    }

    me.addTileWMSLayer = function (url_wms_map, layerName, title) {
        // var shadedRelief2 = new Cesium.WebMapTileServiceImageryProvider({
        //     url: 'http://basemap.nationalmap.gov/arcgis/rest/services/USGSShadedReliefOnly/MapServer/WMTS/tile/1.0.0/USGSShadedReliefOnly/{Style}/{TileMatrixSet}/{TileMatrix}/{TileRow}/{TileCol}.jpg',
        //     layer: 'USGSShadedReliefOnly',
        //     style: 'default',
        //     format: 'image/jpeg',
        //     tileMatrixSetID: 'default028mm',
        //     maximumLevel: 19,
        //     credit: new Cesium.Credit('U. S. Geological Survey')
        // });
        Cesium.WebMapServiceImageryProvider.DefaultParameters = {
            service: 'WMS',
            version: '1.1.1',
            request: 'GetMap',
            styles: '',
            format: 'image/png'
        };
        var tileWMS = new Cesium.WebMapServiceImageryProvider({
            url: url_wms_map,
            layers: layerName,
            // style:'default',
            proxy: new Cesium.DefaultProxy('/proxy/')
        });
        me.viewer.imageryLayers.addImageryProvider(tileWMS);
    }

}