/**
 * Created by idrees on 6/2/2018.
 */

Ext.Loader.setConfig({enabled: true});
Ext.Loader.setPath('Ext.ux', '/static/Extjs-6.2.0/packages/ux/classic/src');
Ext.require([
    'Ext.Viewport',
    'Ext.grid.Panel',
    'Ext.panel.Panel',
    'Ext.container.Container',
]);

Ext.application({
    name: 'MHVRA',
    factsModel: null,
    factsWindow: null,
    comboesModel: null,
    selectionLayer: null,
    adminHierarchy: null,
    hierarchyToolbar: null,
    levelValue: {level: 'punjab', value: 'null'},

    launch: function () {
        var me = this;
        var renderDiv = Ext.get('factsDashboard');
        var widthWin = window.innerWidth;
        var heightWin = window.innerHeight;

        me.factsModel = new ArzSurveyFactsModel();
        me.factsWindow = new ArzFactsWindow();
        // me.comboesModel = new ArzAdminLevelComboes(me.factsModel, me);
        var hierarchyClass = new ArzAdminHierarchyToolbar(me, me.factsModel);
        var panel = Ext.create('Ext.panel.Panel', {
            height: heightWin - 105,
            minHeight: 400,
            minWidth: 600,
            autoScroll: true,
            layout: 'border',
            bodyBorder: false,
            defaults: {
                collapsible: true,
                split: true,
            },
            items: [
                // {
                //     region: 'west',
                //     title: 'Query Filters',
                //     titleAlign: 'center',
                //     floatable: false,
                //     margin: '0 0 0 0',
                //     width: '18%',
                //     minWidth: 150,
                //     layout: 'fit',
                //     border: false,
                //     items: [
                //         {
                //             border: true,
                //             id: 'pnlQueryFilter',
                //             name: 'pnlQueryFilter',
                //             layout: 'fit',
                //             items: me.comboesModel.getComboes(),
                //         },
                //     ]
                //
                // },
                {
                    collapsible: false,
                    region: 'center',
                    margin: '0 0 0 0',
                    layout: 'border',
                    items: [
                        {
                            collapsible: false,
                            region: 'center',
                            layout: 'fit',
                            margin: '0 0 0 0',
                            title: 'Survey Locations Map',
                            titleAlign: 'center',
                            items: [
                                {
                                    xtype: 'panel',
                                    layout: 'fit',
                                    id: 'olMap',
                                    margin: '0 0 0 0',
                                    listeners: {
                                        resize: function (pnl, width, height, oldWidth, oldHeight, eOpts) {
                                            if (me.factsModel.olMap) {
                                                setTimeout(function () {
                                                    me.factsModel.olMap.updateSize();
                                                }, 100);
                                            }
                                        }
                                    },
                                    tbar: [
                                        hierarchyClass.getAdminToolbar(),
                                        {
                                            icon: imgPath + 'irrigation/drawline.png',
                                            tooltip: 'Draw Polygon',
                                            handler: function () {
                                                if (me.factsModel.vectorOverlay) {
                                                    var features = me.factsModel.vectorOverlay.getSource().getFeatures();
                                                    features.forEach(function (feature) {
                                                        me.factsModel.vectorOverlay.getSource().removeFeature(feature);
                                                    });
                                                }
                                                var draw = new ol.interaction.Draw({
                                                    source: me.factsModel.vectorOverlaySource,
                                                    type: 'Polygon'
                                                });
                                                me.factsModel.olMap.addInteraction(draw);
                                                draw.on('drawend', function (evt) {
                                                    me.factsModel.olMap.removeInteraction(draw);
                                                    var geom = evt.feature.getGeometry();
                                                    var format = new ol.format.WKT();
                                                    var wktRepresenation = format.writeGeometry(geom);
                                                    var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
                                                    var url = 'polygon_survey_location_data?wkt=' + wktRepresenation;
                                                    Ext.Ajax.request({
                                                        url: url,
                                                        timeout: 9000000000,
                                                        method: "GET",
                                                        success: function (response) {
                                                            box.hide();
                                                            var respText = response.responseText;
                                                            var respnseText = eval('(' + JXG.decompress(respText) + ')');
                                                            if (respnseText != "false") {
                                                                var jsonData = respnseText;
                                                                var surveyData = JSON.parse(jsonData.survey_data);
                                                                var surveyStats = me.getSelectedSurveyCounts(surveyData);
                                                                me.setSurveyStats(surveyStats);
                                                                me.getSurveyDataPanel(surveyData);
                                                                me.factsModel.addLocationsToMauzaLayer(surveyData);

                                                            }
                                                        },
                                                        failure: function (res) {
                                                            box.hide();
                                                        }
                                                    });


                                                }, this);
                                            }
                                        },
                                        {
                                            icon: imgPath + 'irrigation/11.png',
                                            tooltip: 'Upload polygon/shapefile',
                                            handler: function () {
                                                $('#uploadPolygonModal').modal('show');
                                            }
                                        },
                                        {
                                            icon: imgPath + 'irrigation/Clear.png',
                                            tooltip: 'Clear selection/overlays',
                                            handler: function () {
                                                if (me.factsModel.vectorOverlay) {
                                                    var features = me.factsModel.vectorOverlay.getSource().getFeatures();
                                                    features.forEach(function (feature) {
                                                        me.factsModel.vectorOverlay.getSource().removeFeature(feature);
                                                    });
                                                }if (me.factsModel.selectionLayer) {
                                                    var features = me.factsModel.selectionLayer.getSource().getFeatures();
                                                    features.forEach(function (feature) {
                                                        me.factsModel.selectionLayer.getSource().removeFeature(feature);
                                                    });
                                                }
                                            }
                                        },
                                    ]
                                }
                            ],
                        },
                        {
                            id: 'southSurveyDetails',
                            collapsible: true,
                            collapsed: true,
                            region: 'south',
                            title: 'Survey Data',
                            titleAlign: 'center',
                            layout: 'fit',
                            height: '35%',
                            minHeight: 75,
                            items: [
                                {
                                    xtype: 'panel',
                                    layout: 'hbox',
                                    items: [
                                        {
                                            xtype: 'panel',
                                            id: 'pnlSurveyDetails',
                                            layout: 'fit',
                                            width: '100%',
                                            height: '100%',
                                            bodyPadding: '5 5 5 5',
                                        }
                                    ]
                                },
                            ]
                        }
                    ]
                },
                {
                    title: 'Statistics',
                    titleAlign: 'center',
                    region: 'east',
                    floatable: false,
                    margin: '0 0 0 0',
                    width: '20%',
                    minWidth: 150,
                    layout: 'fit',
                    border: false,
                    items: [
                        {
                            layout: 'accordion',
                            autoScroll: true,
                            items: [
                                {
                                    title: 'Facts',
                                    layout: 'vbox',
                                    id: 'acrdnFacts',
                                    name: 'acrdnFacts',
                                    defaults: {
                                        xtype: 'button',
                                        scale: 'medium',
                                        margin: '2 5 0 5'
                                    },
                                    border: true,
                                    autoScroll: true,
                                    items: [
                                        {
                                            text: 'Bridges: 0',
                                            id: 'btnBridges',
                                            width: '100%',
                                            handler: function () {
                                                var levelValue = me.levelValue;
                                                me.factsWindow.tableChartData = null;
                                                var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
                                                var url = 'mauza_survey_type_facts?table=BridgesFt&level=' + levelValue.level + '&value=' + levelValue.value;
                                                Ext.Ajax.request({
                                                    url: url,
                                                    timeout: 9000000000,
                                                    method: "GET",
                                                    success: function (response) {
                                                        box.hide();
                                                        var respText = response.responseText;
                                                        var respnseText = eval('(' + JXG.decompress(respText) + ')');
                                                        if (respnseText != "false") {
                                                            var factsJson = JSON.parse(respnseText.survey_facts);
                                                            var surveyData = JSON.parse(respnseText.survey_data);
                                                            var surveyGeojson = JSON.parse(respnseText.survey_geojson);

                                                            var bridgesPanel = me.factsWindow.getSurveyTypePanel(factsJson[0], 'Bridges');
                                                            var factsDetailPanel = Ext.getCmp('acrdnFactsDetails');
                                                            factsDetailPanel.expand();
                                                            factsDetailPanel.removeAll();
                                                            factsDetailPanel.add(bridgesPanel);
                                                            if (levelValue.level == 'mauza_id') {
                                                                me.getSurveyDataPanel(surveyData);
                                                                me.factsModel.addLocationsToMauzaLayer(surveyData);
                                                            }
                                                        }
                                                    },
                                                    failure: function (res) {
                                                        box.hide();
                                                    }
                                                });
                                            }
                                        },
                                        {
                                            text: 'Collapse Building: 0',
                                            id: 'btnCollapseBuilding',
                                            width: '100%',
                                            handler: function () {
                                                var levelValue = me.levelValue;
                                                me.factsWindow.tableChartData = null;
                                                // if (levelValue.level == 'mauza_id') {
                                                var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
                                                var url = 'mauza_survey_type_facts?table=CollapseBuildingFt&level=' + levelValue.level + '&value=' + levelValue.value;
                                                Ext.Ajax.request({
                                                    url: url,
                                                    timeout: 9000000000,
                                                    method: "GET",
                                                    success: function (response) {
                                                        box.hide();
                                                        var respText = response.responseText;
                                                        var respnseText = eval('(' + JXG.decompress(respText) + ')');
                                                        if (respnseText != "false") {
                                                            var factsJson = JSON.parse(respnseText.survey_facts);
                                                            var surveyData = JSON.parse(respnseText.survey_data);
                                                            var collapseBuildingPanel = me.factsWindow.getSurveyTypePanel(factsJson[0], 'Collapse Building');
                                                            var factsDetailPanel = Ext.getCmp('acrdnFactsDetails');
                                                            factsDetailPanel.expand();
                                                            factsDetailPanel.removeAll();
                                                            factsDetailPanel.add(collapseBuildingPanel);
                                                            if (levelValue.level == 'mauza_id') {
                                                                me.getSurveyDataPanel(surveyData);
                                                                me.factsModel.addLocationsToMauzaLayer(surveyData);
                                                            }
                                                        }
                                                    },
                                                    failure: function (res) {
                                                        box.hide();
                                                    }
                                                });
                                                // } else {
                                                //     alert('Please select a mauza first.');
                                                // }
                                            }
                                        },
                                        {
                                            text: 'Commercial: 0',
                                            id: 'btnCommercial',
                                            name: 'btnCommercial',
                                            width: '100%',
                                            handler: function () {
                                                var levelValue = me.levelValue;
                                                me.factsWindow.tableChartData = null;
                                                // if (levelValue.level == 'mauza_id') {
                                                var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
                                                var url = 'mauza_survey_type_facts?table=CommercialFt&level=' + levelValue.level + '&value=' + levelValue.value;
                                                Ext.Ajax.request({
                                                    url: url,
                                                    timeout: 9000000000,
                                                    method: "GET",
                                                    success: function (response) {
                                                        box.hide();
                                                        var respText = response.responseText;
                                                        var respnseText = eval('(' + JXG.decompress(respText) + ')');
                                                        if (respnseText != "false") {
                                                            var factsJson = JSON.parse(respnseText.survey_facts);
                                                            var surveyData = JSON.parse(respnseText.survey_data);
                                                            var surveyGeojson = JSON.parse(respnseText.survey_geojson);
                                                            var collapseBuildingPanel = me.factsWindow.getSurveyTypePanel(factsJson[0], 'Commercial');
                                                            var factsDetailPanel = Ext.getCmp('acrdnFactsDetails');
                                                            factsDetailPanel.expand();
                                                            factsDetailPanel.removeAll();
                                                            factsDetailPanel.add(collapseBuildingPanel);
                                                            if (levelValue.level == 'mauza_id') {
                                                                me.getSurveyDataPanel(surveyData);
                                                                me.factsModel.addLocationsToMauzaLayer(surveyData);
                                                            }
                                                        }
                                                    },
                                                    failure: function (res) {
                                                        box.hide();
                                                    }
                                                });
                                                // } else {
                                                //     alert('Please select a mauza first.');
                                                // }
                                            }
                                        },
                                        {
                                            text: 'Dera Jaat: 0',
                                            id: 'btnDeraJaat',
                                            width: '100%',
                                            handler: function () {
                                                var levelValue = me.levelValue;
                                                me.factsWindow.tableChartData = null;
                                                // if (levelValue.level == 'mauza_id') {
                                                var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
                                                var url = 'mauza_survey_type_facts?table=DerajaatFt&level=' + levelValue.level + '&value=' + levelValue.value;
                                                Ext.Ajax.request({
                                                    url: url,
                                                    timeout: 9000000000,
                                                    method: "GET",
                                                    success: function (response) {
                                                        box.hide();
                                                        var respText = response.responseText;
                                                        var respnseText = eval('(' + JXG.decompress(respText) + ')');
                                                        if (respnseText != "false") {
                                                            var factsJson = JSON.parse(respnseText.survey_facts);
                                                            var surveyData = JSON.parse(respnseText.survey_data);
                                                            var surveyGeojson = JSON.parse(respnseText.survey_geojson);
                                                            var collapseBuildingPanel = me.factsWindow.getSurveyTypePanel(factsJson[0], 'Dera Jaat');
                                                            var factsDetailPanel = Ext.getCmp('acrdnFactsDetails');
                                                            factsDetailPanel.expand();
                                                            factsDetailPanel.removeAll();
                                                            factsDetailPanel.add(collapseBuildingPanel);
                                                            if (levelValue.level == 'mauza_id') {
                                                                me.getSurveyDataPanel(surveyData);
                                                                me.factsModel.addLocationsToMauzaLayer(surveyData);
                                                            }
                                                        }
                                                    },
                                                    failure: function (res) {
                                                        box.hide();
                                                    }
                                                });
                                                // } else {
                                                //     alert('Please select a mauza first.');
                                                // }
                                            }
                                        },
                                        {
                                            text: 'Education: 0',
                                            id: 'btnEducation',
                                            width: '100%',
                                            handler: function () {
                                                var levelValue = me.levelValue;
                                                me.factsWindow.tableChartData = null;
                                                // if (levelValue.level == 'mauza_id') {
                                                var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
                                                var url = 'mauza_survey_type_facts?table=EducationalFt&level=' + levelValue.level + '&value=' + levelValue.value;
                                                Ext.Ajax.request({
                                                    url: url,
                                                    timeout: 9000000000,
                                                    method: "GET",
                                                    success: function (response) {
                                                        box.hide();
                                                        var respText = response.responseText;
                                                        var respnseText = eval('(' + JXG.decompress(respText) + ')');
                                                        if (respnseText != "false") {
                                                            var factsJson = JSON.parse(respnseText.survey_facts);
                                                            var surveyData = JSON.parse(respnseText.survey_data);
                                                            var surveyGeojson = JSON.parse(respnseText.survey_geojson);
                                                            var collapseBuildingPanel = me.factsWindow.getSurveyTypePanel(factsJson[0], 'Educational');
                                                            var factsDetailPanel = Ext.getCmp('acrdnFactsDetails');
                                                            factsDetailPanel.expand();
                                                            factsDetailPanel.removeAll();
                                                            factsDetailPanel.add(collapseBuildingPanel);
                                                            if (levelValue.level == 'mauza_id') {
                                                                me.getSurveyDataPanel(surveyData);
                                                                me.factsModel.addLocationsToMauzaLayer(surveyData);
                                                            }
                                                        }
                                                    },
                                                    failure: function (res) {
                                                        box.hide();
                                                    }
                                                });
                                                // } else {
                                                //     alert('Please select a mauza first.');
                                                // }
                                            }
                                        },
                                        {
                                            text: 'Graveyard: 0',
                                            id: 'btnGraveyard',
                                            width: '100%',
                                            handler: function () {
                                                var levelValue = me.levelValue;
                                                me.factsWindow.tableChartData = null;
                                                // if (levelValue.level == 'mauza_id') {
                                                var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
                                                var url = 'mauza_survey_type_facts?table=GraveYardFt&level=' + levelValue.level + '&value=' + levelValue.value;
                                                Ext.Ajax.request({
                                                    url: url,
                                                    timeout: 9000000000,
                                                    method: "GET",
                                                    success: function (response) {
                                                        box.hide();
                                                        var respText = response.responseText;
                                                        var respnseText = eval('(' + JXG.decompress(respText) + ')');
                                                        if (respnseText != "false") {
                                                            var factsJson = JSON.parse(respnseText.survey_facts);
                                                            var surveyData = JSON.parse(respnseText.survey_data);
                                                            var surveyGeojson = JSON.parse(respnseText.survey_geojson);
                                                            var collapseBuildingPanel = me.factsWindow.getSurveyTypePanel(factsJson[0], 'Grave Yard');
                                                            var factsDetailPanel = Ext.getCmp('acrdnFactsDetails');
                                                            factsDetailPanel.expand();
                                                            factsDetailPanel.removeAll();
                                                            factsDetailPanel.add(collapseBuildingPanel);
                                                            if (levelValue.level == 'mauza_id') {
                                                                me.getSurveyDataPanel(surveyData);
                                                                me.factsModel.addLocationsToMauzaLayer(surveyData);
                                                            }
                                                        }
                                                    },
                                                    failure: function (res) {
                                                        box.hide();
                                                    }
                                                });
                                                // } else {
                                                //     alert('Please select a mauza first.');
                                                // }
                                            }
                                        },
                                        {
                                            text: 'Health Facility: 0',
                                            id: 'btnHealthFacility',
                                            width: '100%',
                                            handler: function () {
                                                var levelValue = me.levelValue;
                                                me.factsWindow.tableChartData = null;
                                                // if (levelValue.level == 'mauza_id') {
                                                var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
                                                var url = 'mauza_survey_type_facts?table=HealthFacilityFt&level=' + levelValue.level + '&value=' + levelValue.value;
                                                Ext.Ajax.request({
                                                    url: url,
                                                    timeout: 9000000000,
                                                    method: "GET",
                                                    success: function (response) {
                                                        box.hide();
                                                        var respText = response.responseText;
                                                        var respnseText = eval('(' + JXG.decompress(respText) + ')');
                                                        if (respnseText != "false") {
                                                            var factsJson = JSON.parse(respnseText.survey_facts);
                                                            var surveyData = JSON.parse(respnseText.survey_data);
                                                            var surveyGeojson = JSON.parse(respnseText.survey_geojson);
                                                            var collapseBuildingPanel = me.factsWindow.getSurveyTypePanel(factsJson[0], 'Health Facility');
                                                            var factsDetailPanel = Ext.getCmp('acrdnFactsDetails');
                                                            factsDetailPanel.expand();
                                                            factsDetailPanel.removeAll();
                                                            factsDetailPanel.add(collapseBuildingPanel);
                                                            if (levelValue.level == 'mauza_id') {
                                                                me.getSurveyDataPanel(surveyData);
                                                                me.factsModel.addLocationsToMauzaLayer(surveyData);
                                                            }
                                                        }
                                                    },
                                                    failure: function (res) {
                                                        box.hide();
                                                    }
                                                });
                                                // } else {
                                                //     alert('Please select a mauza first.');
                                                // }
                                            }
                                        },
                                        {
                                            text: 'Industry: 0',
                                            id: 'btnIndustry',
                                            width: '100%',
                                            handler: function () {
                                                var levelValue = me.levelValue;
                                                me.factsWindow.tableChartData = null;
                                                // if (levelValue.level == 'mauza_id') {
                                                var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
                                                var url = 'mauza_survey_type_facts?table=IndustryFt&level=' + levelValue.level + '&value=' + levelValue.value;
                                                Ext.Ajax.request({
                                                    url: url,
                                                    timeout: 9000000000,
                                                    method: "GET",
                                                    success: function (response) {
                                                        box.hide();
                                                        var respText = response.responseText;
                                                        var respnseText = eval('(' + JXG.decompress(respText) + ')');
                                                        if (respnseText != "false") {
                                                            var factsJson = JSON.parse(respnseText.survey_facts);
                                                            var surveyData = JSON.parse(respnseText.survey_data);
                                                            var surveyGeojson = JSON.parse(respnseText.survey_geojson);
                                                            var collapseBuildingPanel = me.factsWindow.getSurveyTypePanel(factsJson[0], 'Industry');
                                                            var factsDetailPanel = Ext.getCmp('acrdnFactsDetails');
                                                            factsDetailPanel.expand();
                                                            factsDetailPanel.removeAll();
                                                            factsDetailPanel.add(collapseBuildingPanel);
                                                            if (levelValue.level == 'mauza_id') {
                                                                me.getSurveyDataPanel(surveyData);
                                                                me.factsModel.addLocationsToMauzaLayer(surveyData);
                                                            }
                                                        }
                                                    },
                                                    failure: function (res) {
                                                        box.hide();
                                                    }
                                                });
                                                // } else {
                                                //     alert('Please select a mauza first.');
                                                // }
                                            }
                                        },
                                        {
                                            text: 'Infrastructure: 0',
                                            id: 'btnInfrastructure',
                                            width: '100%',
                                            handler: function () {
                                                var levelValue = me.levelValue;
                                                me.factsWindow.tableChartData = null;
                                                // if (levelValue.level == 'mauza_id') {
                                                var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
                                                var url = 'mauza_survey_type_facts?table=InfrastructureFt&level=' + levelValue.level + '&value=' + levelValue.value;
                                                Ext.Ajax.request({
                                                    url: url,
                                                    timeout: 9000000000,
                                                    method: "GET",
                                                    success: function (response) {
                                                        box.hide();
                                                        var respText = response.responseText;
                                                        var respnseText = eval('(' + JXG.decompress(respText) + ')');
                                                        if (respnseText != "false") {
                                                            var factsJson = JSON.parse(respnseText.survey_facts);
                                                            var surveyData = JSON.parse(respnseText.survey_data);
                                                            var surveyGeojson = JSON.parse(respnseText.survey_geojson);
                                                            var collapseBuildingPanel = me.factsWindow.getSurveyTypePanel(factsJson[0], 'Infrastructure');
                                                            var factsDetailPanel = Ext.getCmp('acrdnFactsDetails');
                                                            factsDetailPanel.expand();
                                                            factsDetailPanel.removeAll();
                                                            factsDetailPanel.add(collapseBuildingPanel);
                                                            if (levelValue.level == 'mauza_id') {
                                                                me.getSurveyDataPanel(surveyData);
                                                                me.factsModel.addLocationsToMauzaLayer(surveyData);
                                                            }
                                                        }
                                                    },
                                                    failure: function (res) {
                                                        box.hide();
                                                    }
                                                });
                                                // } else {
                                                //     alert('Please select a mauza first.');
                                                // }
                                            }
                                        },
                                        {
                                            text: 'Mauza General Survey: 0',
                                            id: 'btnMauzaGeneralSurvey',
                                            width: '100%',
                                            disabled: true,
                                            handler: function () {
                                                var levelValue = me.levelValue;
                                                me.factsWindow.tableChartData = null;
                                                // if (levelValue.level == 'mauza_id') {
                                                var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
                                                var url = 'mauza_survey_type_facts?table=MauzaGengralSurvey&level=' + levelValue.level + '&value=' + levelValue.value;
                                                Ext.Ajax.request({
                                                    url: url,
                                                    timeout: 9000000000,
                                                    method: "GET",
                                                    success: function (response) {
                                                        box.hide();
                                                        var respText = response.responseText;
                                                        var respnseText = eval('(' + JXG.decompress(respText) + ')');
                                                        if (respnseText != "false") {
                                                            var factsJson = JSON.parse(respnseText.survey_facts);
                                                            var surveyData = JSON.parse(respnseText.survey_data);
                                                            var surveyGeojson = JSON.parse(respnseText.survey_geojson);
                                                            var collapseBuildingPanel = me.factsWindow.getSurveyTypePanel(factsJson[0], 'Mauza General Survey');
                                                            var factsDetailPanel = Ext.getCmp('acrdnFactsDetails');
                                                            factsDetailPanel.expand();
                                                            factsDetailPanel.removeAll();
                                                            factsDetailPanel.add(collapseBuildingPanel);
                                                            if (levelValue.level == 'mauza_id') {
                                                                me.getSurveyDataPanel(surveyData);
                                                                me.factsModel.addLocationsToMauzaLayer(surveyData);
                                                            }
                                                        }
                                                    },
                                                    failure: function (res) {
                                                        box.hide();
                                                    }
                                                });
                                                // } else {
                                                //     alert('Please select a mauza first.');
                                                // }
                                            }
                                        },
                                        {
                                            text: 'Parks: 0',
                                            id: 'btnParks',
                                            width: '100%',
                                            handler: function () {
                                                var levelValue = me.levelValue;
                                                me.factsWindow.tableChartData = null;
                                                // if (levelValue.level == 'mauza_id') {
                                                var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
                                                var url = 'mauza_survey_type_facts?table=ParksFt&level=' + levelValue.level + '&value=' + levelValue.value;
                                                Ext.Ajax.request({
                                                    url: url,
                                                    timeout: 9000000000,
                                                    method: "GET",
                                                    success: function (response) {
                                                        box.hide();
                                                        var respText = response.responseText;
                                                        var respnseText = eval('(' + JXG.decompress(respText) + ')');
                                                        if (respnseText != "false") {
                                                            var factsJson = JSON.parse(respnseText.survey_facts);
                                                            var surveyData = JSON.parse(respnseText.survey_data);
                                                            var surveyGeojson = JSON.parse(respnseText.survey_geojson);
                                                            var collapseBuildingPanel = me.factsWindow.getSurveyTypePanel(factsJson[0], 'Parks');
                                                            var factsDetailPanel = Ext.getCmp('acrdnFactsDetails');
                                                            factsDetailPanel.expand();
                                                            factsDetailPanel.removeAll();
                                                            factsDetailPanel.add(collapseBuildingPanel);
                                                            if (levelValue.level == 'mauza_id') {
                                                                me.getSurveyDataPanel(surveyData);
                                                                me.factsModel.addLocationsToMauzaLayer(surveyData);
                                                            }
                                                        }
                                                    },
                                                    failure: function (res) {
                                                        box.hide();
                                                    }
                                                });
                                                // } else {
                                                //     alert('Please select a mauza first.');
                                                // }
                                            }
                                        },
                                        {
                                            text: 'Public Building: 0',
                                            id: 'btnPublicBuilding',
                                            width: '100%',
                                            handler: function () {
                                                var levelValue = me.levelValue;
                                                me.factsWindow.tableChartData = null;
                                                // if (levelValue.level == 'mauza_id') {
                                                var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
                                                var url = 'mauza_survey_type_facts?table=PublicBuildingFt&level=' + levelValue.level + '&value=' + levelValue.value;
                                                Ext.Ajax.request({
                                                    url: url,
                                                    timeout: 9000000000,
                                                    method: "GET",
                                                    success: function (response) {
                                                        box.hide();
                                                        var respText = response.responseText;
                                                        var respnseText = eval('(' + JXG.decompress(respText) + ')');
                                                        if (respnseText != "false") {
                                                            var factsJson = JSON.parse(respnseText.survey_facts);
                                                            var surveyData = JSON.parse(respnseText.survey_data);
                                                            var surveyGeojson = JSON.parse(respnseText.survey_geojson);
                                                            var collapseBuildingPanel = me.factsWindow.getSurveyTypePanel(factsJson[0], 'Public Building');
                                                            var factsDetailPanel = Ext.getCmp('acrdnFactsDetails');
                                                            factsDetailPanel.expand();
                                                            factsDetailPanel.removeAll();
                                                            factsDetailPanel.add(collapseBuildingPanel);
                                                            if (levelValue.level == 'mauza_id') {
                                                                me.getSurveyDataPanel(surveyData);
                                                                me.factsModel.addLocationsToMauzaLayer(surveyData);
                                                            }
                                                        }
                                                    },
                                                    failure: function (res) {
                                                        box.hide();
                                                    }
                                                });
                                                // } else {
                                                //     alert('Please select a mauza first.');
                                                // }
                                            }
                                        },
                                        {
                                            text: 'Religious Building: 0',
                                            id: 'btnReligiousBuilding',
                                            width: '100%',
                                            handler: function () {
                                                var levelValue = me.levelValue;
                                                me.factsWindow.tableChartData = null;
                                                // if (levelValue.level == 'mauza_id') {
                                                var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
                                                var url = 'mauza_survey_type_facts?table=ReligiousBuildingFt&level=' + levelValue.level + '&value=' + levelValue.value;
                                                Ext.Ajax.request({
                                                    url: url,
                                                    timeout: 9000000000,
                                                    method: "GET",
                                                    success: function (response) {
                                                        box.hide();
                                                        var respText = response.responseText;
                                                        var respnseText = eval('(' + JXG.decompress(respText) + ')');
                                                        if (respnseText != "false") {
                                                            var factsJson = JSON.parse(respnseText.survey_facts);
                                                            var surveyData = JSON.parse(respnseText.survey_data);
                                                            var surveyGeojson = JSON.parse(respnseText.survey_geojson);
                                                            var collapseBuildingPanel = me.factsWindow.getSurveyTypePanel(factsJson[0], 'Religious Building');
                                                            var factsDetailPanel = Ext.getCmp('acrdnFactsDetails');
                                                            factsDetailPanel.expand();
                                                            factsDetailPanel.removeAll();
                                                            factsDetailPanel.add(collapseBuildingPanel);
                                                            if (levelValue.level == 'mauza_id') {
                                                                me.getSurveyDataPanel(surveyData);
                                                                me.factsModel.addLocationsToMauzaLayer(surveyData);
                                                            }
                                                        }
                                                    },
                                                    failure: function (res) {
                                                        box.hide();
                                                    }
                                                });
                                                // } else {
                                                //     alert('Please select a mauza first.');
                                                // }
                                            }
                                        },
                                        {
                                            text: 'Residential: 0',
                                            id: 'btnResidential',
                                            disabled: true,
                                            width: '100%',
                                        },
                                        {
                                            text: 'Terminal: 0',
                                            id: 'btnTerminal',
                                            width: '100%',
                                            handler: function () {
                                                var levelValue = me.levelValue;
                                                me.factsWindow.tableChartData = null;
                                                // if (levelValue.level == 'mauza_id') {
                                                var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
                                                var url = 'mauza_survey_type_facts?table=TerminalFt&level=' + levelValue.level + '&value=' + levelValue.value;
                                                Ext.Ajax.request({
                                                    url: url,
                                                    timeout: 9000000000,
                                                    method: "GET",
                                                    success: function (response) {
                                                        box.hide();
                                                        var respText = response.responseText;
                                                        var respnseText = eval('(' + JXG.decompress(respText) + ')');
                                                        if (respnseText != "false") {
                                                            var factsJson = JSON.parse(respnseText.survey_facts);
                                                            var surveyData = JSON.parse(respnseText.survey_data);
                                                            var surveyGeojson = JSON.parse(respnseText.survey_geojson);
                                                            var collapseBuildingPanel = me.factsWindow.getSurveyTypePanel(factsJson[0], 'Terminal');
                                                            var factsDetailPanel = Ext.getCmp('acrdnFactsDetails');
                                                            factsDetailPanel.expand();
                                                            factsDetailPanel.removeAll();
                                                            factsDetailPanel.add(collapseBuildingPanel);
                                                            if (levelValue.level == 'mauza_id') {
                                                                me.getSurveyDataPanel(surveyData);
                                                                me.factsModel.addLocationsToMauzaLayer(surveyData);
                                                            }
                                                        }
                                                    },
                                                    failure: function (res) {
                                                        box.hide();
                                                    }
                                                });
                                                // } else {
                                                //     alert('Please select a mauza first.');
                                                // }
                                            }
                                        },
                                    ]
                                },
                                {
                                    title: 'Facts Details',
                                    border: true,
                                    id: 'acrdnFactsDetails',
                                    name: 'acrdnFactsDetails',
                                    autoScroll: true,
                                    layout: 'fit',
                                    bodyPadding: 2,
                                }
                            ]
                        }
                    ]
                }
            ],
            renderTo: renderDiv,
            align: 'stretch'
        });


        var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
        var url = 'admin_geojson?level=punjab&value=null';
        Ext.Ajax.request({
            url: url,
            timeout: 9000000000,
            method: "GET",
            success: function (response) {
                box.hide();
                var respText = response.responseText;
                var respnseText = eval('(' + JXG.decompress(respText) + ')');
                if (respnseText != "false") {
                    var geoJsonData = respnseText;
                    var surveyData = JSON.parse(geoJsonData.survey_stats);
                    // var sureyTypeLocations = JSON.parse(geoJsonData.survey_type_locations);
                    me.factsModel.createOlMap(geoJsonData);
                    me.setSurveyStats(surveyData);
                }
            },
            failure: function (res) {
                box.hide();
            }
        });
        Ext.EventManager.onWindowResize(function () {
            var widthWin = window.innerWidth - 15;
            var heightWin = window.innerHeight;
            panel.setHeight(heightWin - 105);
            panel.setWidth(widthWin - 20);
        });
    },
    getJsonFromGeoJson: function (data, level) {
        var jsonArray = []
        var geojsonData = data[0].geojson.features;
        for (var i = 0; i < geojsonData.length; i++) {
            var record = {district_id: null, district_name: null, extent: null}
            record.district_id = geojsonData[i].properties[level + '_id'];
            record.district_name = geojsonData[i].properties[level + '_name'];
            record.extent = geojsonData[i].properties['extent'];
            jsonArray.push(record);
        }
        return jsonArray;
    },
    getComboStore: function (storeId) {
        function getId(id) {
            if (id == 'districtStore') {
                return 'district_id'
            }
            if (id == 'tehsilStore') {
                return 'tehsil_id'
            }
            if (id == 'qanungoHalkaStore') {
                return 'qanungoi_halqa_id'
            }
            if (id == 'patwarCircleStore') {
                return 'patwar_circle_id'
            }
            if (id == 'mauzaStore') {
                return 'mauza_id'
            } else {
                return null;
            }
        }

        function getName(id) {
            if (id == 'districtStore') {
                return 'district_name'
            }
            if (id == 'tehsilStore') {
                return 'tehsil_name'
            }
            if (id == 'qanungoHalkaStore') {
                return 'qanungoi_halqa_name'
            }
            if (id == 'patwarCircleStore') {
                return 'patwar_circle_name'
            }
            if (id == 'mauzaStore') {
                return 'mauza_name'
            } else {
                return null;
            }
        }

        var featureStore = Ext.create('Ext.data.Store', {
            fields: [
                {name: getId(storeId), type: 'number'},
                {name: getName(storeId), type: 'string'},
                {name: 'extent', type: 'string'}
            ],
            id: getId(storeId),
            data: []
        });
        return featureStore;
    },
    getToolbarItems: function () {
        var me = this;
        me.districtStore = me.getComboStore('districtStore');
        me.tehsilStore = me.getComboStore('tehsilStore');
        me.qanungoHalqaStore = me.getComboStore('qanungoHalkaStore');
        me.patwarCircleStore = me.getComboStore('patwarCircleStore');
        me.mauzaStore = me.getComboStore('mauzaStore');

        var toolbarItems = [
            {
                xtype: 'combo',
                store: me.districtStore,
                id: 'cmbDistrict',
                fieldLabel: 'Select District',
                valueField: 'district_id',
                displayField: 'district_name',
                queryMode: 'local',
                emptyText: '<-Select District->',
                listeners: {
                    select: function (cmb, value) {
                        var id = value.data.district_id;
                        var extent = value.data.extent;
                        me.factsModel.zoomToExtent(extent, true);
                        var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
                        var url = 'admin_level?level=tehsil&value=' + id;
                        Ext.Ajax.request({
                            url: url,
                            timeout: 9000000000,
                            method: "GET",
                            success: function (response) {
                                box.hide();
                                var respText = response.responseText;
                                var respnseText = eval('(' + JXG.decompress(respText) + ')');
                                if (respnseText != "false") {
                                    var jsonData = respnseText;
                                    me.tehsilStore.removeAll();
                                    me.tehsilStore.loadData(jsonData);
                                }
                            },
                            failure: function (res) {
                                box.hide();
                            }
                        });
                    }
                }
            },
            {
                xtype: 'combo',
                store: me.tehsilStore,
                valueField: 'tehsil_id',
                fieldLabel: 'Select Tehsil',
                displayField: 'tehsil_name',
                id: 'cmbTehsil',
                emptyText: '<-Select Tehsil->',
                listeners: {
                    select: function (cmb, value) {
                        var id = value.data.tehsil_id;
                        var extent = value.data.extent;
                        me.factsModel.zoomToExtent(extent, true)
                        var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
                        var url = 'admin_level?level=mauza&value=' + id;
                        Ext.Ajax.request({
                            url: url,
                            timeout: 9000000000,
                            method: "GET",
                            success: function (response) {
                                box.hide();
                                var respText = response.responseText;
                                var respnseText = eval('(' + JXG.decompress(respText) + ')');
                                if (respnseText != "false") {
                                    var jsonData = respnseText;
                                    me.mauzaStore.removeAll();
                                    me.mauzaStore.loadData(jsonData);
                                }
                            },
                            failure: function (res) {
                                box.hide();
                            }
                        });
                    }
                }
            },
            {
                xtype: 'combo',
                store: me.qanungoHalqaStore,
                valueField: 'qanungoi_halqa_id',
                fieldLabel: 'Select Qanungo Halka',
                displayField: 'qanungoi_halqa_name',
                id: 'cmbQanungoHalka',
                emptyText: '<-Select Qanungo Halka->',
                listeners: {
                    select: function (cmb, value) {

                    }
                }
            },
            {
                xtype: 'combo',
                store: me.patwarCircleStore,
                valueField: 'patwar_circle_id',
                fieldLabel: 'Select Patwar Circle',
                displayField: 'patwar_circle_name',
                id: 'cmbPatwarCircle',
                emptyText: '<-Select Patwar Circle->',
                listeners: {
                    select: function (cmb, value) {

                    }
                }
            },
            {
                xtype: 'combo',
                store: me.mauzaStore,
                valueField: 'mauza_id',
                displayField: 'mauza_name',
                fieldLabel: 'Select Mauza',
                id: 'cmbMauza',
                emptyText: '<-Select Mauza->',
                listeners: {
                    select: function (cmb, value) {
                        var mauza_id = value.data.mauza_id;
                        var extent = value.data.extent;
                        if (extent) {
                            me.factsModel.zoomToExtent(extent, true);
                            var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
                            var url = 'mauza_survey_location_data?mauza_id=' + mauza_id;
                            Ext.Ajax.request({
                                url: url,
                                timeout: 9000000000,
                                method: "GET",
                                success: function (response) {
                                    box.hide();
                                    var respText = response.responseText;
                                    var respnseText = eval('(' + JXG.decompress(respText) + ')');
                                    if (respnseText != "false") {
                                        var jsonData = respnseText;
                                        var surveyData = jsonData.survey_data;
                                        var locationGeojson = JSON.parse(jsonData.survey_location);
                                        me.factsModel.addLocationsToMauzaLayer(locationGeojson);
                                        // if (surveyData.length > 0) {
                                        // me.getSurveyDataPanel(surveyData);
                                        // } else {
                                        //     alert('No record found.');
                                        // }

                                    }
                                },
                                failure: function (res) {
                                    box.hide();
                                }
                            });
                        } else {
                            alert('Location not available.');
                        }


                    }
                }
            },
        ];
        var panel = Ext.create('Ext.panel.Panel', {
            layout: 'vbox',
            bodyPadding: '10 15 10 15',
            defaults: {
                width: '100%',
            },
            items: toolbarItems
        });
        return panel;
    },

    setSurveyStats: function (data) {
        Ext.getCmp('btnBridges').setText('Bridges: ' + data['bridges']);
        Ext.getCmp('btnCollapseBuilding').setText('Collapse Building: ' + data['collapse_building']);
        Ext.getCmp('btnCommercial').setText('Commercial: ' + data['commercial']);
        Ext.getCmp('btnDeraJaat').setText('Dera Jaat: ' + data['dera_jaat']);
        Ext.getCmp('btnEducation').setText('Education: ' + data['education']);
        Ext.getCmp('btnGraveyard').setText('Graveyard: ' + data['graveyard']);
        Ext.getCmp('btnHealthFacility').setText('Health Facility: ' + data['health_facility']);
        Ext.getCmp('btnIndustry').setText('Industry: ' + data['industry']);
        Ext.getCmp('btnInfrastructure').setText('Infrastructure: ' + data['infrastructure']);
        Ext.getCmp('btnMauzaGeneralSurvey').setText('Mauza General Survey: ' + data['mauza_general_survey']);
        Ext.getCmp('btnParks').setText('Parks: ' + data['parks']);
        Ext.getCmp('btnPublicBuilding').setText('Public Building: ' + data['public_building']);
        Ext.getCmp('btnReligiousBuilding').setText('Religious Building: ' + data['religious_building']);
        Ext.getCmp('btnResidential').setText('Residential: ' + data['residential']);
        Ext.getCmp('btnTerminal').setText('Terminal: ' + data['terminal']);
    },

    getFactsTypeURL: function (type) {
        var url = '';
        if (type == 'Commercial') {
            url = 'commercial_facts';
        }
        return url;
    },
    getTypeFactsData: function (type) {
        var me = this;
        var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
        var typeUrl = me.getFactsTypeURL(type)
        var url = 'commercial_facts?level=' + me.levelValue.level + '&value=' + me.levelValue.value;
        Ext.Ajax.request({
            url: url,
            timeout: 9000000000,
            method: "GET",
            success: function (response) {
                box.hide();
                var respText = response.responseText;
                var respnseText = eval('(' + JXG.decompress(respText) + ')');
                if (respnseText != "false") {
                    me.factsWindow.getFactsWindow(respnseText, type);
                }
            },
            failure: function (res) {
                box.hide();
            }
        });
    },
    statsChart: null,
    getColumnChart: function (data, categories, divId, xLabel, yTitle) {
        var me = this;
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
                layout: 'vertical',
                align: 'right',
                verticalAlign: 'middle'
            },
            // plotOptions: {
            //     line: {
            //         dataLabels: {
            //             enabled: true
            //         },
            //         enableMouseTracking: true
            //     }
            // },
            tooltip: {
                headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f} mm</b></td></tr>',
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

    },
    getChartCategoriesList: function (data, key) {
        var dataList = [];
        for (var i = 0; i < data.length; i++) {
            var value = data[i][key];
            dataList.push(value);
        }
        return dataList;
    },
    getChartData: function (data, key) {
        var dataList = [];
        for (var i = 0; i < data.length; i++) {
            var year = data[i][key];
            dataList.push(year);
        }
        return [{name: 'Survey Types', data: dataList}];
    },
    getCombinedSurveyTableColumns: function () {
        var getStringFilterObj = function () {
            return filter = {
                type: 'string',
                itemDefaults: {emptyText: 'Search for...'},
                caseSensitive: true,
                exactMatch: true,
                anyMatch: false,
            };
        }
        var columnsList = [
            {xtype: 'rownumberer', width: 50},
            {
                dataIndex: 'respondent_name', text: 'Respondent Name', width: 120, filter: getStringFilterObj()
            }, {
                dataIndex: 'respondent_cell_no', text: 'Respondent Cell No', width: 120, filter: getStringFilterObj()
            }, {
                dataIndex: 'respondant_cnic', text: 'Respondent CNIC', width: 120, filter: getStringFilterObj()
            }, {
                dataIndex: 'survey_type_name', text: 'Survey Type', width: 120, filter: getStringFilterObj()
            }, {
                dataIndex: 'surveyor_name', text: 'Surveyor Name', width: 120, filter: getStringFilterObj()
            }, {
                dataIndex: 'district_name', text: 'District', width: 120, filter: getStringFilterObj()
            }, {
                dataIndex: 'tehsil_name', text: 'Tehsil', width: 120, filter: getStringFilterObj()
            }, {
                dataIndex: 'qanungoi_halqa_name', text: 'Qanoongoi', width: 120, filter: getStringFilterObj()
            }, {
                dataIndex: 'patwar_circle_name', text: 'Patwar Circle', width: 120, filter: getStringFilterObj()
            }, {
                dataIndex: 'mauza_name', text: 'Mauza', width: 120, filter: getStringFilterObj()
            }
        ];
        return columnsList;
    },
    selectedSurveyRecord: null,

    getSurveyDataPanel: function (data) {
        var me = this;
        var fieldsList = me.factsWindow.getFieldsList(data[0]);
        var columnsList = me.getCombinedSurveyTableColumns();
        var store = Ext.create('Ext.data.Store', {
            id: 'surveyDataStore',
            fields: fieldsList,
            data: data,
        });
        var gridPanel = Ext.create('Ext.grid.Panel', {
            layout: 'fit',
            id: 'surveyDataPanel',
            titleAlign: 'center',
            store: store,
            stripeRows: true,
            columnLines: true,
            loadMask: true,
            selModel: {
                pruneRemoved: false
            },
            viewConfig: {
                trackOver: false
            },
            plugins: ['gridfilters', 'bufferedrenderer'],
            autoScroll: true,
            listeners: {
                select: function (selModel, record, index, options) {
                    me.selectedSurveyRecord = record;
                    me.setSelection(record);
                }
            },
            tbar: [
                {
                    text: 'Zoom to selection',
                    handler: function () {
                        if (me.selectedSurveyRecord) {
                            var point = new ol.proj.transform([me.selectedSurveyRecord.data.longitude, me.selectedSurveyRecord.data.latitude], 'EPSG:4326', 'EPSG:3857');
                            me.factsModel.olMap.getView().setCenter(point);
                            me.factsModel.olMap.getView().setZoom(18);
                        } else {
                            alert('No selection found.');
                        }
                    }
                },
                {
                    icon: imgPath + 'irrigation/Clear.png',
                    tooltip: 'Clear selection/overlays',
                    handler: function () {
                        if (me.selectionLayer) {
                            var features = me.selectionLayer.getSource().getFeatures();
                            features.forEach(function (feature) {
                                me.selectionLayer.getSource().removeFeature(feature);
                            });
                        }
                    }
                },
                {
                    icon: imgPath + 'mhvra/table.png',
                    tooltip: 'View dimension model',
                    handler: function () {
                        me.createFlexMonsterPivotTable(data);
                    }
                }
            ],
            autoDestroy: true,
            columns: columnsList,
        });
        var dataPanel = Ext.getCmp("southSurveyDetails");
        dataPanel.expand();
        dataPanel.removeAll();
        dataPanel.add(gridPanel);
    },

    setSelection: function (record) {
        var me = this;
        if (me.selectionLayer) {
            me.factsModel.olMap.removeLayer(me.selectionLayer);
        }
        var vectorSource = new ol.source.Vector();
        me.selectionLayer = new ol.layer.Vector({
            source: vectorSource
        });
        var imagePath = imgPath + 'flashing_circle.gif';
        var iconStyle = new ol.style.Style({
            image: new ol.style.Circle({
                fill: new ol.style.Fill({color: '#00FFFF'}),
                stroke: new ol.style.Stroke({color: '#00FFFF', width: 5}),
                radius: 5
            }),
        });
        var point = new ol.proj.transform([record.data.longitude, record.data.latitude], 'EPSG:4326', 'EPSG:3857');
        var feature = new ol.Feature(
            new ol.geom.Point(point)
        );
        feature.setStyle(iconStyle);
        vectorSource.addFeature(feature);
        me.factsModel.olMap.addLayer(me.selectionLayer);
    },

    win:null,
    createFlexMonsterPivotTable: function (data) {
        var me = this;
        if (me.win != null) {
            me.win.destroy();
        }
        me.win = Ext.create('Ext.window.Window', {
            id: 'dimensionModelWin',
            title: 'Survey Dimension Model',
            layout: 'fit',
            x: 250,
            y: 100,
            width: '60%',
            height: '50%',
            frame:true,
            closeAction: 'destroy',
            preventBodyReset: true,
            resizable:false,
            constrainHeader: true,
            collapsible: false,
            plain: true,
            items: [
                Ext.create('Ext.form.Panel', {
                    defaults: {
                        anchor: '100%'
                    },
                    autoScroll:true,
                    id:'frmSurveyPivotTable',
                    layout:'fit',
                    name:'frmSurveyPivotTable'
                })
            ]
        });
        me.win.show();
        var div = Ext.getCmp('frmSurveyPivotTable').body.dom;
        var flexmonster = new Flexmonster({
            container: div,
            componentFolder: "https://cdn.flexmonster.com/",
            toolbar: true,
            height: '100%',
            width: '100%',
            report: {
                dataSource: {
                    data: data
                },
                "slice": {
                    "rows": [
                        {
                            "uniqueName": "survey_type",
                        }
                    ],
                    "columns": [
                        {
                            "uniqueName": "[Measures]"
                        }
                    ],
                    "measures": [
                        {
                            "uniqueName": "respondant_name",
                            "aggregation": "count"
                        }
                    ]
                },
            },
            licenseKey: 'Z7HI-XG503S-5O4M4H-6F456Z-0A3E3Z-1X663C-5O4R35-4R'
        })
    },


    getHierarchyButtons: function (items) {
        var tbar = JSON.parse(items);
        var adminHierarchy = Ext.create('Ext.Action', {
            text: "Admin Unit",
            id: 'btnAdmin',
            handler: function () {
            },
            tooltip: "Select Administrative Unit",
            menu: tbar
        });
        var olMapPanel = Ext.getCmp('olMap');
        olMapPanel.tbar = adminHierarchy; //.add(adminHierarchy);
    },

    getSelectedSurveyCounts: function (data) {
        var bridges = 0, collapse_building = 0, commercial = 0, dera_jaat = 0, education = 0, graveyard = 0,
            health_facility = 0,
            industry = 0, infrastructure = 0, mauza_general_survey = 0, parks = 0, public_building = 0,
            religious_building = 0,
            residential = 0, terminal = 0;
        for (var i = 0; i < data.length; i++) {
            var type_name = data[i]['survey_type_name'];
            if (type_name == 'Bridges') {
                bridges++;
            }
            if (type_name == 'COLLAPSE BUILDING') {
                collapse_building++;
            }
            if (type_name == 'Commercial') {
                commercial++;
            }
            if (type_name == 'DERA JAAT') {
                dera_jaat++;
            }
            if (type_name == 'Education') {
                education++;
            }
            if (type_name == 'Graveyard') {
                graveyard++;
            }
            if (type_name == 'Health Facility') {
                health_facility++;
            }
            if (type_name == 'Industry') {
                industry++;
            }
            if (type_name == 'Infrastructure') {
                infrastructure++;
            }
            if (type_name == 'Mauza General Survey') {
                mauza_general_survey++;
            }
            if (type_name == 'Parks') {
                parks++;
            }
            if (type_name == 'Public Building') {
                public_building++;
            }
            if (type_name == 'Religious Building') {
                religious_building++;
            }
            if (type_name == 'Residential') {
                residential++;
            }
            if (type_name == 'Terminal') {
                terminal++;
            }
        }
        return {
            bridges: bridges,
            collapse_building: collapse_building,
            commercial: commercial,
            dera_jaat: dera_jaat,
            education: education,
            graveyard: graveyard,
            health_facility: health_facility,
            industry: industry,
            infrastructure: infrastructure,
            mauza_general_survey: mauza_general_survey,
            parks: parks,
            public_building: public_building,
            religious_building: religious_building,
            residential: residential,
            terminal: terminal
        }
    }

});