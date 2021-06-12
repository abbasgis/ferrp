/**
 * Created by Dr. Ather Ashraf on 9/1/2018.
 */
var OLCesiumModel = function () {
    var me = this;
    me.initCameraOrient = {"heading": 0.0, "pitch": -Cesium.Math.PI_OVER_SIX, "roll": 0.0, "range": 6000};
    me.camera = null;
    me.scene = null;
    Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJhNDZkMzc1Yy1mZGI3LTQ1N2QtOTIwMC01NWFmY2NjYmQ5ZmYiLCJpZCI6MjkyMywiaWF0IjoxNTM1MjU4NDExfQ.NGFb_MFCyv2Zu2VYFVSDIOkmi2JuDofx6Pcz8kWPoNQ';
    me.ol3d = null;
    me.map = null;
    me.init = function (map) {
        if (me.ol3d == null) {
            me.map = map;
            me.ol3d = new olcs.OLCesium({
                map: me.map,
                // time() {
                //     return Cesium.JulianDate.now();
                // }
            });

            me.scene = me.ol3d.getCesiumScene();
            me.camera = me.ol3d.getCamera().c;
            me.setTerrainProvider();
        }
    }


    me.setTerrainProvider = function () {
        // var terrainProvider = new Cesium.CesiumTerrainProvider({
        //     url: Cesium.IonResource.fromAssetId(6063),
        // });
        var terrainProvider = Cesium.createWorldTerrain({
            requestWaterMask: true,
            requestVertexNormals: true,
        });
        me.scene.terrainProvider = terrainProvider; //Cesium.createWorldTerrain();
        me.scene.globe.enableLighting = false;
        me.scene.terrainExaggeration = 20.0
    }

    me.switch3DView = function (enable) {
        me.ol3d.setEnabled(enable);
    }

    me.setInitSliderValues = function () {
        $('#headingLevel').jqxSlider('setValue', me.initCameraOrient["heading"]);
        $('#pitchLevel').jqxSlider('setValue', Cesium.Math.toDegrees(me.initCameraOrient["pitch"]));
        $('#rollLevel').jqxSlider('setValue', me.initCameraOrient["roll"]);
    }

    me.setCamera = function (heading, pitch, roll) {
        me.camera.setView({
            orientation: {
                heading: heading, // east, default value is 0.0 (north)
                pitch: pitch,    // default value (looking down)
                roll: roll                             // default value
            }
        });
    }
    me.getCamera = function () {
        return me.camera;
    }

}

