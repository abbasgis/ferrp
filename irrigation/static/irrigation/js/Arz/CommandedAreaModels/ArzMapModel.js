/**
 * Created by idrees on 11/3/2017.
 */

var ArzMapModel = function () {
    var me = this;
    me.statsModel = new ArzGlobalFunctionsModel();
    me.dataModel = new ArzDataModel();
    me.chartModel = new ArzChartModel();
    me.overviewInfoModel = new ArzOverviewModel();
    me.titleText = ['Zones', 'Circles', 'Divisions', 'CCAs'];
    me.level = ['Zone', 'Circle', 'Division', 'CCA'];
    me.levelNames = {'Zone':'', 'Circle':'', 'Division':'', 'CCA':''};
    me.levelCodes = {'Zone':'zone_name', 'Circle':'circle_name', 'Division':'division_name', 'CCA':'cca'};
    me.levelIndex = 0;
    me.resultJSON = null;
    me.wtStats = null;
    me.minCCA = 0;
    me.maxCCA = 0;
    me.zoneStats = null;
    me.circleStats = null;
    me.divisionStats = null;
    me.zoneCanalStats = null;
    me.circleCanalStats = null;
    me.divisionCanalStats = null;
    me.getMap = function () {
        var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
        var url = 'irrigationstats?level=zone_name&value=null';
        Ext.Ajax.timeout = 900000;
        Ext.Ajax.request({
            url: url,
            method: "GET",
            success: function (response) {
                box.hide();
                var respText = response.responseText;
                var respnseText = eval('(' + JXG.decompress(respText) + ')');
                if (respnseText != "false") {
                    var jsonData = respnseText;
                    var geojson = JSON.parse(jsonData.geojson);
                    me.minCCA = me.statsModel.geoJsonAttributeMin(geojson[0].geojson.features, 'cca_geom_ma');
                    me.maxCCA = me.statsModel.geoJsonAttributeMax(geojson[0].geojson.features, 'cca_geom_ma');
                    me.zoneStats = JSON.parse(jsonData.stats);
                    me.zoneCanalStats = JSON.parse(jsonData.canals);

                    me.overviewInfoModel.createPopup(me.zoneCanalStats);
                    me.overviewInfoModel.getGrossCommandedAreaArray(me.zoneStats);
                    me.overviewInfoModel.getCultivableCommandedAreaArray(me.zoneStats);

                    me.dataModel.getDataPanel(me.zoneStats, "zone_name");
                    me.chartModel.createBarChart(me.zoneStats, "All Zones");
                    me.drawExtHighMaps(geojson[0].geojson, me.minCCA, me.maxCCA);
                    // me.chartModel.createCanalsChart(me.zoneStats, "All Zones");
                    // me.setLevelNameLabel();
                }
            },
            failure: function (res) {
                box.hide();
            }
        });

    }

    me.createHMap = function (geoJsonData) {
        var mapDiv = Ext.getCmp("HMapCA").body.dom;
        var data = Highcharts.geojson(geoJsonData);
        $.each(data, function (i) {
            this.drilldown = this.properties['name'];
            this.value = this.properties['cca_geom_ma']; // Non-random bogus data
        });
        me.minCCA = me.statsModel.geoJsonAttributeMin(data, 'cca_geom_ma');
        me.maxCCA = me.statsModel.geoJsonAttributeMax(data, 'cca_geom_ma');
        Highcharts.mapChart(mapDiv, {
            chart: {
                events: {
                    drilldown: function (e) {
                        if (!e.seriesOptions) {
                            var chart = this;
                            var level = 'circle_name', value = e.point.drilldown;
                            var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
                            var url = 'irrigationstats?level='+level+'&value=' + value;
                            Ext.Ajax.timeout = 900000;
                            Ext.Ajax.request({
                                url: url,
                                method: "GET",
                                success: function (response) {
                                    box.hide();
                                    var respText = response.responseText;
                                    var respnseText = eval('(' + JXG.decompress(respText) + ')');
                                    if (respnseText != "false") {
                                        var jsonData = respnseText;
                                        var mapKey = JSON.parse(jsonData.geojson);
                                        me.circleStats = jsonData.stats;
                                        me.dataModel.getDataPanel(me.circleStats, "circle", value);
                                        me.circleCanalStats = jsonData.canals;
                                        me.overviewInfoModel.createPopup(me.circleCanalStats);
                                        me.overviewInfoModel.getGrossCommandedAreaArray(me.circleStats);
                                        me.chartModel.createBarChart(me.circleStats, e.point.drilldown + " Circles");
                                        var drillDownGeoJsonData = Highcharts.geojson(mapKey);
                                        $.each(drillDownGeoJsonData, function (i) {
                                            this.value = this.properties['cca'];
                                        });
                                        me.minCCA = me.statsModel.geoJsonAttributeMin(drillDownGeoJsonData, "cca");
                                        me.maxCCA = me.statsModel.geoJsonAttributeMax(drillDownGeoJsonData, "cca");
                                        chart.addSeriesAsDrilldown(e.point, {
                                            name: e.point.name,
                                            data: drillDownGeoJsonData,
                                            dataLabels: {
                                                enabled: true,
                                                format: '{point.name}'
                                            },
                                            events: {
                                                click: function (e) {
                                                    var circleName = e.point.name;
                                                    var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
                                                    var url = 'irrigationstats?level=division_name&value=' + circleName;
                                                    Ext.Ajax.timeout = 900000;
                                                    Ext.Ajax.request({
                                                        url: url,
                                                        method: "GET",
                                                        success: function (response) {
                                                            box.hide();
                                                            var respText = response.responseText;
                                                            var respnseText = eval('(' + JXG.decompress(respText) + ')');
                                                            if (respnseText != "false") {
                                                                var statsData = respnseText;
                                                                me.divisionStats = statsData.stats;
                                                                me.divisionCanalStats = statsData.canals;
                                                                me.dataModel.getDataPanel(me.divisionStats, "division");
                                                                me.chartModel.createBarChart(me.divisionStats, circleName + " Divisions");
                                                                me.overviewInfoModel.createPopup(me.divisionCanalStats);
                                                                me.overviewInfoModel.getGrossCommandedAreaArray(me.divisionStats);
                                                            }
                                                        }
                                                    });
                                                }
                                            }
                                        });
                                    }
                                },
                                failure: function (res) {
                                    // Ext.MessageBox.hide();
                                }
                            });
                        }
                        this.setTitle(null, { text: e.point.name });
                    },
                    drillup: function () {
                        this.setTitle(null, { text: 'Irrigation Zones' });
                        me.dataModel.getDataPanel(me.zoneStats, "zone", "null");
                        me.chartModel.createBarChart(me.zoneStats, "Irrigation Zones");
                        me.overviewInfoModel.createPopup(me.zoneCanalStats);
                        me.overviewInfoModel.getGrossCommandedAreaArray(me.zoneStats);
                    }
                }
            },
            credits: {
                enabled: false
            },
            title: {
                text: 'Irrigation'
            },
            legend: {
                layout: 'horizotal',
                align: 'center',
                verticalAlign: 'bottom'
            },
            colorAxis: {
                min: me.minCCA,
                max: me.maxCCA,
                minColor: '#fefdf6',
                maxColor: '#003300'
            },
            mapNavigation: {
                enabled: true,
                buttonOptions: {
                    verticalAlign: 'top'
                }
            },
            plotOptions: {
                map: {
                    borderColor: "#2F4F4F",
                    borderWidth: 1.0,
                    states: {
                        hover: {
                            color: '#EEDD66'
                        }
                    }
                },
                series: {
                    cursor: 'pointer',
                    point: {
                        events: {
                            click: function () {
                                // alert("Hello");
                            }
                            // mouseMove:function () {
                            //
                            // }
                        }
                    }
                }
            },

            series: [{
                data: data,
                name: 'Irrigation Zone',
                dataLabels: {
                    enabled: true,
                    color: '#FFFFFF',
                    format: '{point.name}'
                },
                tooltip: {
                    pointFormat: '{point.name}: {point.properties.cca} ft'
                }
            }],

            drilldown: {
                activeDataLabelStyle: {
                    color: '#FFFFFF',
                    textDecoration: 'none',
                    textShadow: '0 0 3px #000000'
                },
                drillUpButton: {
                    relativeTo: 'spacingBox',
                    position: {
                        x: 0,
                        y: 60
                    }
                }
            }
        });
    }

    me.highMapChart = function(config){
        var highMap = new Highcharts.Map({
            credits: false,
            type:"map",
            chart: {
                renderTo: Ext.getCmp("HMapCA").body.dom,
                borderWidth: 0,
                events: {
                    drilldown: function (e) {
                        if(config.drilldownCallback){
                            config.drilldownCallback(e);
                        }
                    },
                    drillup: function (e) {
                        this.setTitle(null, {text: 'Entity'});
                        if(config.drillupCallback){
                            config.drilldownCallback(e);
                        }
                    }
                }
            },
            title: {
                text: ''
            },
            subtitle: {
                floating: true,
                align: 'right',
                y: 0,
                style: {
                    fontSize: '12px'
                }
            },
            legend: {
                enabled: true,
                layout: "vertical",
                align:'right'
            },
            colorAxis: {
                min: me.minCCA,
                max: me.maxCCA,
                minColor: '#ffffff',
                maxColor: '#1d5604'
            },
            mapNavigation: {
                enabled: true,
                buttonOptions: {
                    verticalAlign: 'top'
                }
            },
            plotOptions: {
                map: {
                    borderColor: "#009600",
                    borderWidth: 1,
                    states: {
                        hover: {
                            color: '#EEDD66'
                        }
                    }
                },
                series: {
                    cursor: 'pointer',
                    point: {
                        events: {
                            click: function () {
                                if(me.level[me.levelIndex] == 'Canal'){

                                }
                            }
                        }
                    }
                }
            },
            series: [{
                data: config.data,
                name: 'Irrigation',
                dataLabels: {
                    enabled: true,
                    format: '{point.properties.name}'
                }
            }],
            drilldown: {
                activeDataLabelStyle: {
                    color: '#FFFFFF',
                    textDecoration: 'none',
                    textShadow: '0 0 3px #000000'
                },
                drillUpButton: {
                    relativeTo: 'spacingBox',
                    position: {
                        x: 0,
                        y: 60
                    }
                }
            }
        });
    }

    me.drawExtHighMaps = function (geoJSON, minVal, maxVal) {
        var data = Highcharts.geojson(geoJSON);
        Ext.each(data, function (i) {
            this.drilldown = this.properties['name'];
            this.value = this.properties['cca_geom_ma'];
        });
        me.highMapChart({
            data: data,
            minVal: minVal,
            maxVal: maxVal,
            drilldownCallback: function (e) {
                me.highMapDrilldownActivity(e);
            },
            drillupCallback: null
        });
    };

    me.highMapDrilldownActivity = function (e) {
        if (me.levelIndex < 3) {
            if (me.levelIndex < me.level.length) {
                if (!e.seriesOptions) {
                    var chart = this;
                    me.levelIndex++;
                    var levelName = e.point.drilldown;
                    var levelCode = me.levelCodes[me.level[me.levelIndex]];
                    me.levelCodes[me.level[me.levelIndex]] = levelCode;
                    me.levelNames[me.level[me.levelIndex]] = levelName;
                    me.requestLevelData(levelCode, levelName);
                    me.setButtonStatus('btnBackHighMaps');
                }
            }
        }
        // else {
        //     me.levelIndex--;
        // }
    };

    me.mapPanelHeaderToolbar = function () {
        var headerToolbar = [{
            xtype: 'toolbar',
            dock: 'top',
            items: [
            {xtype: 'tbspacer', flex: 1},
            {
                xtype: 'label',
                id:'irrigationMapTitle',
                cls:'lblTitle',
                text: 'All Zones'
            },
            '->',
            {
                text: 'Back',
                icon: imgPath + 'arrow_left.png',
                id: 'btnBackHighMaps',
                disabled: true,
                handler: function () {
                    if (me.levelIndex <= 3) {
                        var levelCode;
                        var levelName;
                        var nextLevelKey = me.level[me.levelIndex - 1];
                        if (nextLevelKey === 'Zone') {
                            levelCode = me.levelCodes[nextLevelKey];
                            levelName = me.levelNames[nextLevelKey];
                        }
                        else {
                            levelCode = me.levelCodes[nextLevelKey];
                            levelName = me.levelNames[nextLevelKey];
                        }
                        if (levelCode) {
                            me.levelIndex--;
                            me.requestLevelData(levelCode, levelName);
                        }
                        me.setButtonStatus('btnBackHighMaps');
                        me.setButtonStatus('btnForwardHighMaps');
                    }
                }
            },
            '-',
            {
                text: 'Forward',
                icon: imgPath +  'arrow_right.png',
                id: 'btnForwardHighMaps',
                disabled: true,
                handler: function () {
                    if (me.levelIndex <= 3) {
                        var levelCode;
                        var levelName;
                        var nextLevelKey = me.level[me.levelIndex + 1];
                        if (nextLevelKey === 'Zone') {
                            levelCode = me.levelCodes[nextLevelKey];
                            levelName = me.levelNames[nextLevelKey];
                        }
                        else {
                            levelCode = me.levelCodes[nextLevelKey];
                            levelName = me.levelNames[nextLevelKey];
                        }
                        if (levelCode) {
                            me.levelIndex++;
                            me.requestLevelData(levelCode, levelName);
                        }
                    }
                    me.setButtonStatus('btnBackHighMaps');
                }
            }]
        }];
        return headerToolbar;
    };

    me.getStatusBarItems = function () {
        var items = [
            Ext.create('Ext.toolbar.Toolbar', {
                id: 'statusbar',
                items: [
                    '-',
                    {
                        id: 'lblAllZones',
                        disabled:true,
                        xtype:'button',
                        text: 'All Zones',
                        handler:function(){
                            me.levelIndex = 0;
                            // me.requestLevelData('0','Punjab');
                        }

                    },
                    '-',
                    {
                        id: 'lblZone',
                        disabled:true,
                        text: '',
                        handler:function(){
                            me.levelIndex = 0;
                            // me.requestLevelData('0','Punjab');
                        }

                    },
                    '-',
                    {
                        id: 'lblCircle',
                        disabled:true,
                        text: '',
                        handler:function(){
                            me.levelIndex = 1;
                            // me.requestLevelData(me.levelCodes['Division'] ,me.levelNames['Division']);
                        }
                    },
                    '-',
                    {
                        id: 'lblDivision',
                        disabled:true,
                        text: '',
                        handler:function(){
                            me.levelIndex = 2;
                            // me.requestLevelData(me.levelCodes['District'] ,me.levelNames['District']);
                        }
                    }
                ]
            })
        ];
        return items;
    }

    me.requestLevelData = function (levelcode, levelName) {
        var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
        var url = 'irrigationstats?level='+levelcode+'&value=' + levelName;
        Ext.Ajax.timeout = 900000;
        Ext.Ajax.request({
            url: url,
            method: "GET",
            success: function (response) {
                box.hide();
                me.drawHighMapsWithGrid(response);
            }
        });
    };

    me.drawHighMapsWithGrid = function (result) {
        // Ext.MessageBox.hide();
        var mapTitle = Ext.getCmp('irrigationMapTitle');
        var respText = result.responseText;
        var respnseText = eval('(' + JXG.decompress(respText) + ')');
        if (respnseText != "false") {
            var jsonData = respnseText;
            var geojson = JSON.parse(jsonData.geojson);
            var canalsJson = JSON.parse(jsonData.canals);
            var statsJson = JSON.parse(jsonData.stats);
            var labelText = "";
            if(me.titleText[me.levelIndex] == "Zones"){
                labelText = "All Zones";
            }else {
                labelText = me.titleText[me.levelIndex] + ' of ' + me.levelNames[me.level[me.levelIndex]] + ' ' + me.level[me.levelIndex - 1];
            }
            // var chartLabel = me.level[me.levelIndex] + ' ' + me.levelCodes[me.level[me.levelIndex]];
            mapTitle.setText(labelText);
            if(me.level[me.levelIndex] == 'CCA'){
                me.dataModel.getDataPanel(statsJson, me.level[me.levelIndex], me.levelNames[me.level[me.levelIndex]]);
                me.chartModel.createBarChart(statsJson, labelText);
                me.overviewInfoModel.createPopup([]);
                me.overviewInfoModel.getGrossCommandedAreaArray([]);
                me.overviewInfoModel.getCultivableCommandedAreaArray([]);
                me.drawExtHighMaps(geojson[0].geojson, me.minCCA, me.maxCCA);
                // me.setLevelNameLabel();
                // me.levelIndex--;
            }else {
                me.overviewInfoModel.createPopup(canalsJson);
                me.overviewInfoModel.getGrossCommandedAreaArray(statsJson);
                me.overviewInfoModel.getCultivableCommandedAreaArray(statsJson);
                if(me.level == 1){
                    var level = "zone_name";
                    me.dataModel.getDataPanel(statsJson, level, "null");
                }else {
                    me.dataModel.getDataPanel(statsJson, me.levelCodes[me.level[me.levelIndex]], me.levelNames[me.level[me.levelIndex]]);
                }
                me.chartModel.createBarChart(statsJson, labelText);
                // me.chartModel.createCanalsChart(statsJson, labelText);
                me.minCCA = me.statsModel.geoJsonAttributeMin(geojson[0].geojson.features, 'cca_geom_ma');
                me.maxCCA = me.statsModel.geoJsonAttributeMax(geojson[0].geojson.features, 'cca_geom_ma');
                me.drawExtHighMaps(geojson[0].geojson, me.minCCA, me.maxCCA);
                // me.setLevelNameLabel();
            }
        }
    };

    me.setButtonStatus = function (btnID) {
        var btn = Ext.getCmp(btnID);
        if (btnID === 'btnBackHighMaps') {
            if (me.levelIndex > 0) {
                btn.setDisabled(false);
            }
            else if (me.levelIndex <= 0) {
                btn.setDisabled(true);
            }
        }
        else {
            var objSize = me.getObjectSize(me.levelNames);
            if (objSize > 0) {
                btn.setDisabled(false);
            }
            else if (objSize <= 0) {
                btn.setDisabled(true);
            }
        }
        // btn.doComponentLayout();
    };

    me.setLevelNameLabel = function() {
        // var me = this;
        var lblAllZone = Ext.getCmp('lblAllZone');
        var lblZone = Ext.getCmp('lblZone');
        var lblCircle = Ext.getCmp('lblCircle');
        var lblDivision = Ext.getCmp('lblDivision');
        if (me.levelIndex == 0) {
            lblAllZone.setText('All Zones');
            lblZone.setText('');
            lblCircle.setText('');
            lblDivision.setText('');
            lblAllZone.setDisabled(false);
            lblZone.setDisabled(true);
            lblCircle.setDisabled(true);
            lblDivision.setDisabled(true);
        }
        else if (me.levelIndex == 1) {
            lblAllZone.setText('All Zones');
            lblZone.setText('Zone:' + me.levelNames["Zone"]);
            lblCircle.setText('');
            lblDivision.setText('');
            lblAllZone.setDisabled(false);
            lblZone.setDisabled(true);
            lblCircle.setDisabled(true);
            lblDivision.setDisabled(true);
        }
        else if (me.levelIndex == 2) {
            lblAllZone.setText('All Zones');
            lblZone.setText('Zone:' + me.levelNames["Zone"]);
            lblCircle.setText('Circle:' + me.levelNames["Circle"]);
            lblDivision.setText('');
            lblAllZone.setDisabled(false);
            lblZone.setDisabled(false);
            lblCircle.setDisabled(false);
            lblDivision.setDisabled(true);
        }
        else if (me.levelIndex == 3) {
            lblAllZone.setText('All Zones');
            lblZone.setText('Zone:' + me.levelNames["Zone"]);
            lblCircle.setText('Circle:' + me.levelNames["Circle"]);
            lblDivision.setText('Division:' + me.levelNames["Division"]);
            lblAllZone.setDisabled(false);
            lblZone.setDisabled(false);
            lblCircle.setDisabled(false);
            lblDivision.setDisabled(false);
        }
    };

    me.getObjectSize = function (obj) {
        var size = 0, key;
        for (key in obj) {
            if (obj.hasOwnProperty(key)) size++;
        }
        return size;
    };

}
