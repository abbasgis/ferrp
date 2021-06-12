/**
 * Created by idrees on 6/26/2018.
 */

var ArzAdminLevelComboes = function (factsModel, factsVM) {
    var me = this;
    me.districtStore = null;
    me.factsVM = factsVM,
    me.factsModel = factsModel;
    me.levelValue = {level: 'punjab', value: 'null'};

    me.getComboStore = function (storeId) {
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
    }

    me.getComboes = function () {
        me.districtStore = me.getComboStore('districtStore');
        var url = '../admin_level?level=district_id&value=null';
        Ext.Ajax.request({
            url: url,
            timeout: 9000000000,
            method: "GET",
            success: function (response) {
                var respText = response.responseText;
                var respnseText = eval('(' + respText + ')');
                if (respnseText != "false") {
                    var jsonData = respnseText;
                    me.districtStore.removeAll();
                    me.districtStore.loadData(jsonData);
                }
            },
            failure: function (res) {

            }
        });
        var panel = Ext.create('Ext.panel.Panel', {
            layout: 'vbox',
            bodyPadding: '10 15 10 15',
            defaults: {
                width: '100%',
            },
            items: [
                {
                    xtype: 'combo',
                    store: me.districtStore,
                    id: 'cmbDistrict',
                    // fieldLabel: 'Select District',
                    valueField: 'district_id',
                    displayField: 'district_name',
                    queryMode: 'local',
                    emptyText: '<-Select District->',
                    listeners: {
                        select: function (cmb, value) {
                            var id = value.data.district_id;
                            var extent = value.data.extent;
                            me.levelValue.level = 'district_id';
                            me.levelValue.value = id;
                            Ext.getCmp('acrdnFacts').expand();
                            me.getLevelSurveyStats();
                            if (extent) {
                                me.factsModel.zoomToExtent(extent, true);
                            }
                            var tehsilsList = new Ext.data.Store({
                                proxy: {
                                    type: 'ajax',
                                    url: '../admin_level?level=tehsil_id&value=' + id,
                                    reader: {
                                        type: 'json',
                                        idProperty: 'tehsil_id'
                                    }
                                },
                                fields: ['tehsil_id', 'tehsil_name', 'extent']
                            });
                            tehsilsList.load();
                            var cmbTehsil = Ext.getCmp('cmbTehsil');
                            cmbTehsil.reset();
                            cmbTehsil.store.removeAll();
                            cmbTehsil.bindStore(tehsilsList);

                            var cmbQanungoHalka = Ext.getCmp('cmbQanungoHalka');
                            cmbQanungoHalka.reset();
                            cmbQanungoHalka.store.removeAll();
                            var cmbPatwarCircle = Ext.getCmp('cmbPatwarCircle');
                            cmbPatwarCircle.reset();
                            cmbPatwarCircle.store.removeAll();
                            var cmbMauza = Ext.getCmp('cmbMauza');
                            cmbMauza.reset();
                            cmbMauza.store.removeAll();
                        }
                    }
                },
                {
                    xtype: 'combo',
                    valueField: 'tehsil_id',
                    // fieldLabel: 'Select Tehsil',
                    displayField: 'tehsil_name',
                    id: 'cmbTehsil',
                    emptyText: '<-Select Tehsil->',
                    listeners: {
                        select: function (cmb, value) {
                            var id = value.data.tehsil_id;
                            var extent = value.data.extent;
                            me.levelValue.level = 'tehsil_id';
                            me.levelValue.value = id;
                            Ext.getCmp('acrdnFacts').expand();
                            me.getLevelSurveyStats();
                            if (extent) {
                                me.factsModel.zoomToExtent(extent, true);
                            }
                            var qanungoHalkaList = new Ext.data.Store({
                                proxy: {
                                    type: 'ajax',
                                    url: '../admin_level?level=qanungo_halka_id&value=' + id,
                                    reader: {
                                        type: 'json',
                                        idProperty: 'qanungoi_halqa_id'
                                    }
                                },
                                fields: ['qanungoi_halqa_id', 'qanungoi_halqa_name', 'extent']
                            });
                            qanungoHalkaList.load();
                            var cmbQanungoHalka = Ext.getCmp('cmbQanungoHalka');
                            cmbQanungoHalka.reset();
                            cmbQanungoHalka.store.removeAll();
                            cmbQanungoHalka.bindStore(qanungoHalkaList);

                            var cmbPatwarCircle = Ext.getCmp('cmbPatwarCircle');
                            cmbPatwarCircle.reset();
                            cmbPatwarCircle.store.removeAll();
                            var cmbMauza = Ext.getCmp('cmbMauza');
                            cmbMauza.reset();
                            cmbMauza.store.removeAll();
                        }
                    }
                },
                {
                    xtype: 'combo',
                    valueField: 'qanungoi_halqa_id',
                    // fieldLabel: 'Select Qanungo Halka',
                    displayField: 'qanungoi_halqa_name',
                    id: 'cmbQanungoHalka',
                    emptyText: '<-Select Qanungo Halka->',
                    listeners: {
                        select: function (cmb, value) {
                            var id = value.data.qanungoi_halqa_id;
                            me.levelValue.level = 'qanungoi_halqa_id';
                            me.levelValue.value = id;
                            Ext.getCmp('acrdnFacts').expand();
                            me.getLevelSurveyStats();
                            var patwarCircleList = new Ext.data.Store({
                                proxy: {
                                    type: 'ajax',
                                    url: '../admin_level?level=patwar_circle_id&value=' + id,
                                    reader: {
                                        type: 'json',
                                        idProperty: 'patwar_circle_id'
                                    }
                                },
                                fields: ['patwar_circle_id', 'patwar_circle_name', 'extent']
                            });
                            patwarCircleList.load();
                            var cmbPatwarCircle = Ext.getCmp('cmbPatwarCircle');
                            cmbPatwarCircle.reset();
                            cmbPatwarCircle.store.removeAll();
                            cmbPatwarCircle.bindStore(patwarCircleList);

                            var cmbMauza = Ext.getCmp('cmbMauza');
                            cmbMauza.reset();
                            cmbMauza.store.removeAll();
                        }
                    }
                },
                {
                    xtype: 'combo',
                    // store: me.patwarCircleStore,
                    valueField: 'patwar_circle_id',
                    // fieldLabel: 'Select Patwar Circle',
                    displayField: 'patwar_circle_name',
                    id: 'cmbPatwarCircle',
                    emptyText: '<-Select Patwar Circle->',
                    listeners: {
                        select: function (cmb, value) {
                            var id = value.data.patwar_circle_id;
                            me.levelValue.level = 'patwar_circle_id';
                            me.levelValue.value = id;
                            Ext.getCmp('acrdnFacts').expand();
                            me.getLevelSurveyStats();
                            var mauzaList = new Ext.data.Store({
                                proxy: {
                                    type: 'ajax',
                                    url: '../admin_level?level=mauza_id&value=' + id,
                                    reader: {
                                        type: 'json',
                                        idProperty: 'mauza_id'
                                    }
                                },
                                fields: ['mauza_id', 'mauza_name', 'extent']
                            });
                            mauzaList.load();
                            var cmbMauza = Ext.getCmp('cmbMauza');
                            cmbMauza.reset();
                            cmbMauza.store.removeAll();
                            cmbMauza.bindStore(mauzaList);


                            // var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
                            // var url = '../admin_level?level=mauza&value=' + id;
                            // Ext.Ajax.request({
                            //     url: url,
                            //     timeout: 9000000000,
                            //     method: "GET",
                            //     success: function (response) {
                            //         box.hide();
                            //         var respText = response.responseText;
                            //         var respnseText = eval('(' + JXG.decompress(respText) + ')');
                            //         if (respnseText != "false") {
                            //             var jsonData = respnseText;
                            //             me.mauzaStore.removeAll();
                            //             me.mauzaStore.loadData(jsonData);
                            //         }
                            //     },
                            //     failure: function (res) {
                            //         box.hide();
                            //     }
                            // });
                        }
                    }
                },
                {
                    xtype: 'combo',
                    store: me.mauzaStore,
                    valueField: 'mauza_id',
                    displayField: 'mauza_name',
                    // fieldLabel: 'Select Mauza',
                    id: 'cmbMauza',
                    emptyText: '<-Select Mauza->',
                    listeners: {
                        select: function (cmb, value) {
                            var id = value.data.mauza_id;
                            var extent = value.data.extent;
                            me.levelValue.level = 'mauza_id';
                            me.levelValue.value = id;
                            Ext.getCmp('acrdnFacts').expand();
                            if (extent) {
                                me.factsModel.zoomToExtent(extent, true);
                            } else {
                                alert('Location not available.');
                            }
                            var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
                            var url = '../mauza_survey_location_data?mauza_id=' + id;
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
                                        var locationGeojson = JSON.parse(jsonData.survey_location);
                                        me.factsVM.setSurveyStats(surveyData);
                                        me.factsModel.addLocationsToMauzaLayer(locationGeojson);
                                        // Ext.getCmp('acrdnFacts').expand();
                                    }
                                },
                                failure: function (res) {
                                    box.hide();
                                }
                            });
                        }
                    }
                },
            ]
        });
        return panel;
    }
    me.getLevelSurveyStats = function () {
        var level = me.levelValue.level;
        var value = me.levelValue.value;
        var box = Ext.MessageBox.wait('Please wait...', 'Loading Data');
        var url = '../level_survey_stats?level='+level+'&value='+value;
        Ext.Ajax.request({
            url: url,
            timeout: 9000000000,
            method: "GET",
            success: function (response) {
                box.hide();
                var respText = response.responseText;
                var respnseText = eval('(' + JXG.decompress(respText) + ')');
                if (respnseText != "false") {
                    me.factsVM.setSurveyStats(respnseText);
                }
            },
            failure: function (res) {
                box.hide();
            }
        });
    };


}